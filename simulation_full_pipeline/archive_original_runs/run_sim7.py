"""Simulacion 7: repite la malla de la Simulacion 6 (mismas semillas y generador) guardando TODAS las repeticiones,
con las adiciones del protocolo v0.6 (sensibilidad 7, umbrales D_min, contraste del techo para F). Todo simulado."""
import sys, time, pickle, numpy as np
from joblib import Parallel, delayed
import fullsim2 as FS
SEED = 20261113
N_EL = [500, 738, 1000, 2000, 3000, 5000]; NOISES = [0.15, 0.30, 0.60]; CS = [0.0, 0.12, 0.24, 0.36]
REPS_CAL, REPS_VER, REPS_POW, REPS_CEIL = 2000, 1000, 1000, 300
EFFECTS = [0.05, 0.10]; TECHOS = [0.5, 1.0]
N_CEIL, NOISES_CEIL, CS_CEIL = [738, 2000, 5000], [0.15, 0.30], [0.0, 0.36]
def tarea(key, reps, n, noise, c, world, effect, techo, quantile):
    ss = np.random.SeedSequence(SEED, spawn_key=key)
    return key, FS.repetir(ss, reps, n, noise, c, world, effect, techo, quantile)
tasks = []
for i, n in enumerate(N_EL):
    for j, nz in enumerate(NOISES):
        for k, c in enumerate(CS):
            tasks.append(((i, j, k, 0), REPS_CAL, n, nz, c, "null", 0.0, None, False))
            tasks.append(((i, j, k, 1), REPS_VER, n, nz, c, "null", 0.0, None, False))
            for e, eff in enumerate(EFFECTS):
                tasks.append(((i, j, k, 2 + e), REPS_POW, n, nz, c, "linear", eff, None, False))
ctasks = []
for i, n in enumerate(N_CEIL):
    for j, nz in enumerate(NOISES_CEIL):
        for k, c in enumerate(CS_CEIL):
            ctasks.append(((100 + i, j, k, 4), REPS_CEIL, n, nz, c, "null", 0.0, None, True))
            for e, tc in enumerate(TECHOS):
                ctasks.append(((100 + i, j, k, 5 + e), REPS_CEIL, n, nz, c, "ceiling", 0.0, tc, True))
t0 = time.time()
RC = dict(Parallel(n_jobs=2)(delayed(tarea)(*t) for t in ctasks))
pickle.dump(RC, open(sys.argv[1] + "/RC.pkl", "wb")); print("techo listo", round((time.time() - t0) / 60, 1), "min", flush=True)
R_ = dict(Parallel(n_jobs=2, verbose=1)(delayed(tarea)(*t) for t in tasks))
pickle.dump(R_, open(sys.argv[1] + "/R.pkl", "wb")); print("malla lista", round((time.time() - t0) / 60, 1), "min", flush=True)
