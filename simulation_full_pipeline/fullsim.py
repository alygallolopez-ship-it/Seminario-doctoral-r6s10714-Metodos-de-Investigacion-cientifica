"""Simulation 6 (ChroniCare-AI, protocol v0.5.1): FULL PE3 pipeline on simulated patients.
Everything is simulated: no real data are used. The parameters come from notebooks 4 and 5 (VitalDB).
BSI in SD units (higher = better). Pipeline per event:
  robust nadir (mean of the 2 lowest values in the nadir window) -> R_i = end - nadir ->
  expected recovery with PATIENT-level cross-fitting (without baseline BSI) -> AC_i = R_i - E^[R|S,X] ->
  primary test: least-squares slope beta_mean of AC on baseline BSI (+ covariates), one-sided.
It is run in the same way with F_i = R_i / D_i (fraction of the drop recovered), for the switching rule of v0.5.1 (6.4.7; in v0.6 F is a preregistered secondary outcome).
"""
import warnings
import numpy as np
from statsmodels.regression.quantile_regression import QuantReg

warnings.filterwarnings('ignore')

# ---- fixed generator parameters (same as notebooks 4 and 5 except where noted) ----
W = 7.0          # recovery window (days)
T0 = 2.0         # day of the true nadir
TAU = 2.0        # time scale of the recovery
WN = 4.0         # nadir window: days 0 to WN
WE = 2.0         # closing window: last WE days
UMBRAL = 0.5     # minimum observed drop (SD of the BSI) to include the event
KMAX = 14        # maximum post-event measurements per event
K_FOLDS = 5      # patient-level cross-fitting


def generar(rng, n, noise, c, world="null", effect=0.0, techo=None, dens=4.0):
    """Generates n patients (1 to 3 events each, sharing their latent baseline state).
    world: 'null' (no association), 'linear' (the recoverable fraction rises by `effect` per SD of BSI) or 'ceiling'
    (ceiling: worse baseline state -> lower maximum recoverable fraction; `techo` = 0.5 moderate, 1.0 strong).
    c = coupling (how much deeper the drop is when the baseline BSI is high)."""
    age = rng.normal(size=n)
    theta = -0.3 * age + np.sqrt(1 - 0.09) * rng.normal(size=n)       # true baseline state (SD=1)
    ne = 1 + np.minimum(rng.poisson(0.4, n), 2)                         # events per patient
    pid = np.repeat(np.arange(n), ne); E = len(pid)
    th, agez = theta[pid], age[pid]
    S = rng.uniform(0, 1, E)                                            # clinical severity (independent of the BSI)
    D = (0.8 + 0.4 * S) * np.clip(1 + c * th, 0.3, None) * np.exp(0.1 * rng.normal(size=E))
    u = rng.beta(4, 2, E) * (1 - 0.25 * S)                              # the expected recovery depends on S
    if world == "linear":
        r = np.clip(u + effect * th, 0.02, 1.0)
    elif world == "ceiling":
        r = np.minimum(u, np.clip(0.95 + techo * th, 0.05, 1.0))
    else:
        r = np.clip(u, 0.02, 1.0)
    # post-event measurements (parametric times, denser in the most severe events)
    npost = np.minimum(3 + rng.poisson(dens * S), KMAX)
    t = np.sort(np.where(np.arange(KMAX)[None, :] < npost[:, None], rng.uniform(0.1, W, (E, KMAX)), np.inf), axis=1)
    valid = np.isfinite(t); tt = np.where(valid, t, 0.0)
    k = 1 - np.exp(-(W - T0) / TAU)
    rec = r[:, None] * (1 - np.exp(-(tt - T0) / TAU)) / k
    q = np.where(tt <= T0, tt / T0, 1 - rec)
    x = th[:, None] - D[:, None] * q
    obs = x + noise * rng.normal(size=x.shape)
    npre = 1 + rng.poisson(1.0, E)
    base = th + noise * rng.normal(size=E) / np.sqrt(npre)             # mean of the prior measurements
    # robust nadir: mean of the two lowest values within [0, WN]
    inwin = valid & (t <= WN)
    srt = np.sort(np.where(inwin, obs, np.inf), axis=1)[:, :2]
    n_nad = inwin.sum(1)
    nadir = srt.mean(1)
    # final value: mean of the (up to) two last measurements within [W-WE, W]
    inclo = valid & (t >= W - WE)
    n_clo = inclo.sum(1)
    idx = np.argsort(-np.where(inclo, t, -np.inf), axis=1)[:, :2]
    v2 = np.take_along_axis(obs, idx, 1)
    ok2 = np.take_along_axis(inclo, idx, 1)
    fin = np.where(ok2.sum(1) > 0, (v2 * ok2).sum(1) / np.maximum(ok2.sum(1), 1), np.nan)
    Dobs = base - nadir
    inc = (n_nad >= 2) & (n_clo >= 1)                                   # clinical inclusion: measurement availability only
    R = fin - nadir
    return dict(pid=pid[inc], base=base[inc], S=S[inc], agez=agez[inc], dens=n_nad[inc].astype(float),
                R=R[inc], D=Dobs[inc])


def _cross_fit(Y, Z, pid):
    """AC = Y - E^[Y|Z] with patient-level cross-fitting (all events of a patient fall in the same fold)."""
    fold = pid % K_FOLDS
    pred = np.empty_like(Y)
    for f in range(K_FOLDS):
        te = fold == f; tr = ~te
        b = np.linalg.lstsq(Z[tr], Y[tr], rcond=None)[0]
        pred[te] = Z[te] @ b
    return Y - pred


def _ols_cluster(X, y, pid):
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    bread = np.linalg.inv(X.T @ X)
    starts = np.r_[0, np.flatnonzero(np.diff(pid)) + 1]
    sc = np.add.reduceat(X * e[:, None], starts, axis=0)
    G = len(starts)
    V = bread @ (sc.T @ sc) @ bread * G / max(G - 1, 1)
    return b, np.sqrt(V[1, 1])


def _un_analisis(d, y, quantile=False):
    pid = d["pid"]; one = np.ones(len(pid))
    Z = np.column_stack([one, d["S"], d["agez"], d["dens"]])           # E^[.|S,X]: WITHOUT baseline BSI
    X = np.column_stack([one, d["base"], d["S"], d["agez"], d["dens"]])  # primary model: WITH baseline BSI
    ac = _cross_fit(y, Z, pid)
    b, se = _ols_cluster(X, ac, pid)
    out = [float(b[1]), float(se)]
    if quantile:
        b90 = QuantReg(ac, X).fit(q=0.90, max_iter=1000, p_tol=1e-4).params[1]
        b50 = QuantReg(ac, X).fit(q=0.50, max_iter=1000, p_tol=1e-4).params[1]
        out.append(float(b90 - b50))
    return out


def analizar(d, quantile=False):
    """Full pipeline on a simulated data set. Three analyses:
    R  = absolute recovery, ALL events with enough measurements (clinical inclusion; the protocol's primary);
    Rb = same, but only events with observed drop > UMBRAL (BSI-based criterion, as in notebooks 4 and 5; sensitivity);
    F  = fraction of the drop recovered R/D, only events with D > UMBRAL (candidate for the switching rule of v0.5.1, 6.4.7)."""
    out = {"n_pac": int(len(np.unique(d["pid"]))), "n_ev": int(len(d["pid"])), "Dbar": float(d["D"].mean())}
    r = _un_analisis(d, d["R"], quantile)
    out["b_R"], out["se_R"] = r[0], r[1]
    if quantile:
        out["dbeta_R"] = r[2]
    k = d["D"] > UMBRAL
    dk = {key: v[k] for key, v in d.items()}
    out["n_pac_b"] = int(len(np.unique(dk["pid"]))); out["Dbar_b"] = float(dk["D"].mean())
    rb = _un_analisis(dk, dk["R"], False); out["b_Rb"], out["se_Rb"] = rb
    f = _un_analisis(dk, np.clip(dk["R"] / dk["D"], -0.5, 1.5), False); out["b_F"], out["se_F"] = f
    return out


def generar_elegibles(rng, n_el, noise, c, world="null", effect=0.0, techo=None):
    """Generates enough candidates to obtain EXACTLY n_el eligible patients (the first n_el,
    which are a random sample because the patients are generated in random order)."""
    n_cand = int(n_el / 0.55) + 100
    while True:
        d = generar(rng, n_cand, noise, c, world, effect, techo)
        up = np.unique(d["pid"])
        if len(up) >= n_el:
            keep = d["pid"] <= up[n_el - 1]
            return {k: v[keep] for k, v in d.items()}
        n_cand *= 2


def repetir(seed_seq, reps, n_el, noise, c, world="null", effect=0.0, techo=None, quantile=False):
    """Repeats reps times (own seed, reproducible). n_el = ELIGIBLE patients (after the inclusion rule).
    Returns a dict of arrays (one entry per repetition)."""
    rng = np.random.default_rng(seed_seq)
    res = [analizar(generar_elegibles(rng, n_el, noise, c, world, effect, techo), quantile) for _ in range(reps)]
    return {k: np.array([r[k] for r in res]) for k in res[0]}
