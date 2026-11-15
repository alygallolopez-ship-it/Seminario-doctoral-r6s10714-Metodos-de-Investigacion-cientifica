"""Simulacion 6 (ChroniCare-AI, protocolo v0.5.1): pipeline COMPLETO de PE3 sobre pacientes simulados.
Todo es simulado: no se usa ningun dato real. Los parametros salen de los cuadernos 4 y 5 (VitalDB).
BSI en unidades de SD (mayor = mejor). Pipeline por evento:
  nadir robusto (media de las 2 menores en la ventana de nadir) -> R_i = fin - nadir ->
  recuperacion esperada con cross-fitting POR PACIENTE (sin BSI basal) -> AC_i = R_i - E^[R|S,X] ->
  prueba principal: pendiente de minimos cuadrados beta_mean de AC sobre BSI basal (+covariables), una cola.
Se corre igual con F_i = R_i / D_i (fraccion de la caida recuperada), para la regla de cambio (6.4.7).
"""
import warnings
import numpy as np
from statsmodels.regression.quantile_regression import QuantReg

warnings.filterwarnings('ignore')

# ---- parametros fijos del generador (iguales a los cuadernos 4 y 5 salvo lo indicado) ----
W = 7.0          # ventana de recuperacion (dias)
T0 = 2.0         # dia del nadir verdadero
TAU = 2.0        # escala de tiempo de la recuperacion
WN = 4.0         # ventana de nadir: dias 0 a WN
WE = 2.0         # ventana de cierre: ultimos WE dias
UMBRAL = 0.5     # caida minima observada (SD del BSI) para incluir el evento
KMAX = 14        # maximo de mediciones post-evento por evento
K_FOLDS = 5      # cross-fitting por paciente


def generar(rng, n, noise, c, world="null", effect=0.0, techo=None, dens=4.0):
    """Genera n pacientes (1 a 3 eventos cada uno, comparten su estado basal latente).
    world: 'null' (sin asociacion), 'linear' (la fraccion recuperable sube `effect` por SD de BSI) o 'ceiling'
    (techo: peor estado basal -> menor fraccion recuperable maxima; `techo` = 0.5 moderado, 1.0 fuerte).
    c = acoplamiento (cuanto mas profunda la caida cuando el BSI basal es alto)."""
    age = rng.normal(size=n)
    theta = -0.3 * age + np.sqrt(1 - 0.09) * rng.normal(size=n)       # estado basal verdadero (SD=1)
    ne = 1 + np.minimum(rng.poisson(0.4, n), 2)                         # eventos por paciente
    pid = np.repeat(np.arange(n), ne); E = len(pid)
    th, agez = theta[pid], age[pid]
    S = rng.uniform(0, 1, E)                                            # gravedad clinica (independiente del BSI)
    D = (0.8 + 0.4 * S) * np.clip(1 + c * th, 0.3, None) * np.exp(0.1 * rng.normal(size=E))
    u = rng.beta(4, 2, E) * (1 - 0.25 * S)                              # la recuperacion esperada depende de S
    if world == "linear":
        r = np.clip(u + effect * th, 0.02, 1.0)
    elif world == "ceiling":
        r = np.minimum(u, np.clip(0.95 + techo * th, 0.05, 1.0))
    else:
        r = np.clip(u, 0.02, 1.0)
    # mediciones post-evento (tiempos parametricos, mas densas en los mas graves)
    npost = np.minimum(3 + rng.poisson(dens * S), KMAX)
    t = np.sort(np.where(np.arange(KMAX)[None, :] < npost[:, None], rng.uniform(0.1, W, (E, KMAX)), np.inf), axis=1)
    valid = np.isfinite(t); tt = np.where(valid, t, 0.0)
    k = 1 - np.exp(-(W - T0) / TAU)
    rec = r[:, None] * (1 - np.exp(-(tt - T0) / TAU)) / k
    q = np.where(tt <= T0, tt / T0, 1 - rec)
    x = th[:, None] - D[:, None] * q
    obs = x + noise * rng.normal(size=x.shape)
    npre = 1 + rng.poisson(1.0, E)
    base = th + noise * rng.normal(size=E) / np.sqrt(npre)             # media de las mediciones previas
    # nadir robusto: media de las dos menores dentro de [0, WN]
    inwin = valid & (t <= WN)
    srt = np.sort(np.where(inwin, obs, np.inf), axis=1)[:, :2]
    n_nad = inwin.sum(1)
    nadir = srt.mean(1)
    # valor final: media de las (hasta) dos ultimas mediciones dentro de [W-WE, W]
    inclo = valid & (t >= W - WE)
    n_clo = inclo.sum(1)
    idx = np.argsort(-np.where(inclo, t, -np.inf), axis=1)[:, :2]
    v2 = np.take_along_axis(obs, idx, 1)
    ok2 = np.take_along_axis(inclo, idx, 1)
    fin = np.where(ok2.sum(1) > 0, (v2 * ok2).sum(1) / np.maximum(ok2.sum(1), 1), np.nan)
    Dobs = base - nadir
    inc = (n_nad >= 2) & (n_clo >= 1)                                   # inclusion clinica: solo disponibilidad de mediciones
    R = fin - nadir
    return dict(pid=pid[inc], base=base[inc], S=S[inc], agez=agez[inc], dens=n_nad[inc].astype(float),
                R=R[inc], D=Dobs[inc])


def _cross_fit(Y, Z, pid):
    """AC = Y - E^[Y|Z] con cross-fitting por paciente (todos los eventos de un paciente caen en el mismo pliegue)."""
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
    Z = np.column_stack([one, d["S"], d["agez"], d["dens"]])           # E^[.|S,X]: SIN BSI basal
    X = np.column_stack([one, d["base"], d["S"], d["agez"], d["dens"]])  # modelo primario: CON BSI basal
    ac = _cross_fit(y, Z, pid)
    b, se = _ols_cluster(X, ac, pid)
    out = [float(b[1]), float(se)]
    if quantile:
        b90 = QuantReg(ac, X).fit(q=0.90, max_iter=1000, p_tol=1e-4).params[1]
        b50 = QuantReg(ac, X).fit(q=0.50, max_iter=1000, p_tol=1e-4).params[1]
        out.append(float(b90 - b50))
    return out


def analizar(d, quantile=False):
    """Pipeline completo sobre un conjunto simulado. Tres analisis:
    R  = recuperacion absoluta, TODOS los eventos con mediciones suficientes (inclusion clinica; es el primario del protocolo);
    Rb = igual pero solo eventos con caida observada > UMBRAL (criterio basado en el BSI, como en los cuadernos 4 y 5; sensibilidad);
    F  = fraccion de la caida recuperada R/D, solo eventos con D > UMBRAL (candidato de la regla de cambio 6.4.7)."""
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
    """Genera suficientes candidatos para obtener EXACTAMENTE n_el pacientes elegibles (los primeros n_el,
    que son una muestra aleatoria porque los pacientes se generan en orden aleatorio)."""
    n_cand = int(n_el / 0.55) + 100
    while True:
        d = generar(rng, n_cand, noise, c, world, effect, techo)
        up = np.unique(d["pid"])
        if len(up) >= n_el:
            keep = d["pid"] <= up[n_el - 1]
            return {k: v[keep] for k, v in d.items()}
        n_cand *= 2


def repetir(seed_seq, reps, n_el, noise, c, world="null", effect=0.0, techo=None, quantile=False):
    """Repite reps veces (semilla propia, reproducible). n_el = pacientes ELEGIBLES (despues de la regla de inclusion).
    Devuelve un dict de arrays (una entrada por repeticion)."""
    rng = np.random.default_rng(seed_seq)
    res = [analizar(generar_elegibles(rng, n_el, noise, c, world, effect, techo), quantile) for _ in range(reps)]
    return {k: np.array([r[k] for r in res]) for k in res[0]}
