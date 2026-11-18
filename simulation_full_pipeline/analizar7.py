import sys, pickle, numpy as np, pandas as pd
D = sys.argv[1]; OUTD = sys.argv[2]  # D = carpeta con R.pkl y RC.pkl (salida de run_sim7.py)
R_ = pickle.load(open(D + "/R.pkl", "rb")); RC = pickle.load(open(D + "/RC.pkl", "rb"))
N_EL = [500, 738, 1000, 2000, 3000, 5000]; NOISES = [0.15, 0.30, 0.60]; CS = [0.0, 0.12, 0.24, 0.36]
EFFECTS = [0.05, 0.10]; OUT = ["R", "F", "Rb"]; N_CEIL = [738, 2000, 5000]; NZC = [0.15, 0.30]; CSC = [0.0, 0.36]
PCT = {"a05": 95, "a025": 97.5}
def crit(i, oc, p):
    m = None
    for j in range(3):
        for k in range(4):
            v = np.percentile(R_[(i, j, k, 0)]["b_" + oc], p)
            if m is None or v > m[0]: m = (v, j, k)
    return m
rows = []
for i, n in enumerate(N_EL):
    for oc in OUT:
        r = dict(n=n, resultado=oc)
        for tag, p in PCT.items():
            v, j, k = crit(i, oc, p); r["vc_" + tag] = v; r["celda_" + tag] = f"ruido {NOISES[j]}, c {CS[k]}"
        rows.append(r)
vc = pd.DataFrame(rows); vc.to_csv(OUTD + "/sim7_valores_criticos.csv", index=False)
print("VALORES CRITICOS"); print(vc.round(4).to_string(index=False))
# tamaño y poder (alfa 0.025), suficiencia
tam, pot = [], []
for i, n in enumerate(N_EL):
    cv = {oc: crit(i, oc, 97.5)[0] for oc in OUT}
    for j, nz in enumerate(NOISES):
        for k, c in enumerate(CS):
            ver = R_[(i, j, k, 1)]; nul = R_[(i, j, k, 0)]
            for oc in OUT:
                s = float(np.mean(ver["b_" + oc] > cv[oc]))
                tam.append(dict(n=n, ruido=nz, c=c, resultado=oc, tamano=s, error_MC=np.sqrt(max(s * (1 - s), 1e-9) / 1000)))
                Dbar = {"R": nul["Dbar"].mean(), "Rb": nul["Dbar_b"].mean(), "F": 1.0}[oc]
                dref = 0.10 * Dbar; sa = 1.96 * nul["se_" + oc].mean()
                for e, eff in enumerate(EFFECTS):
                    b = R_[(i, j, k, 2 + e)]["b_" + oc]; pw = float(np.mean(b > cv[oc]))
                    pot.append(dict(n=n, ruido=nz, c=c, resultado=oc, efecto=eff, poder=pw, semiancho=sa, delta_ref=dref,
                                    suficiente=(pw >= 0.8) and (sa <= dref)))
tam = pd.DataFrame(tam); pot = pd.DataFrame(pot)
tam.to_csv(OUTD + "/sim7_tamano.csv", index=False); pot.to_csv(OUTD + "/sim7_poder_suficiencia.csv", index=False)
print("\nTAMAÑO (alfa 0.025): maximo y media sobre la malla")
print(tam.groupby(["resultado", "n"]).tamano.agg(["max", "mean"]).round(3).unstack(0).to_string())
print("\nSUFICIENCIA (efecto 0.10): celdas suficientes de 12, por N")
sf = pot[pot.efecto == 0.10].groupby(["resultado", "n"]).suficiente.sum().unstack(0); print(sf.to_string())
print("\nPODER efecto 0.10 N=738 por celda (R / F)")
for oc in ("R", "F"):
    g = pot[(pot.n == 738) & (pot.efecto == 0.10) & (pot.resultado == oc)].pivot(index="c", columns="ruido", values="poder"); print(oc); print(g.round(3).to_string())
print("\nPODER efecto 0.05 N=738 (R / F)")
for oc in ("R", "F"):
    g = pot[(pot.n == 738) & (pot.efecto == 0.05) & (pot.resultado == oc)].pivot(index="c", columns="ruido", values="poder"); print(oc); print(g.round(3).to_string())
print("\nSUFICIENCIA por celda N=738 efecto 0.10 (R)")
print(pot[(pot.n == 738) & (pot.efecto == 0.10) & (pot.resultado == "R")].pivot(index="c", columns="ruido", values="suficiente").to_string())
# sensibilidad 7 y regla de decision compuesta (N=738)
sr = []
for i, n in enumerate(N_EL):
    cvR = crit(i, "R", 97.5)[0]
    for j, nz in enumerate(NOISES):
        for k, c in enumerate(CS):
            nul = R_[(i, j, k, 0)]; ver = R_[(i, j, k, 1)]
            rule_s = float(np.mean((ver["b_R"] > cvR) & (ver["b_F"] > 0) & (ver["b7"] > 0)))
            row = dict(n=n, ruido=nz, c=c, b7_nula_media=nul["b7"].mean(), b7_nula_sd=nul["b7"].std(),
                       P_b7_positivo_nulo=float(np.mean(nul["b7"] > 0)), P_bF_positivo_nulo=float(np.mean(nul["b_F"] > 0)), tamano_regla=rule_s)
            for e, eff in enumerate(EFFECTS):
                alt = R_[(i, j, k, 2 + e)]
                row[f"poder_regla_{eff}"] = float(np.mean((alt["b_R"] > cvR) & (alt["b_F"] > 0) & (alt["b7"] > 0)))
                row[f"poder_R_{eff}"] = float(np.mean(alt["b_R"] > cvR))
                row[f"P_b7_pos_{eff}"] = float(np.mean(alt["b7"] > 0)); row[f"P_bF_pos_{eff}"] = float(np.mean(alt["b_F"] > 0))
            sr.append(row)
sr = pd.DataFrame(sr); sr.to_csv(OUTD + "/sim7_sensibilidad7_regla.csv", index=False)
print("\nSENSIBILIDAD 7 y REGLA COMPUESTA (a: b_R>vc; b: F>0; c: b7>0), N=738")
print(sr[sr.n == 738].round(3).to_string(index=False))
print("tamano maximo de la regla (todas las celdas y N):", round(sr.tamano_regla.max(), 4))
# D_min
dm = []
i = N_EL.index(738)
for thr in ("0.1", "0.25", "0.5", "1.0"):
    key = "b_F" if thr == "0.5" else "b_F_" + thr
    cv = max(np.nanpercentile(R_[(i, j, k, 0)][key], 97.5) for j in range(3) for k in range(4))
    for j, nz in enumerate(NOISES):
        for k, c in enumerate(CS):
            ver = R_[(i, j, k, 1)][key]; alt = R_[(i, j, k, 3)][key]; nul = R_[(i, j, k, 0)]
            evk = "n_ev_F_" + thr; rk = "frac_F_recortada" if thr == "0.5" else "frac_recort_" + thr
            dm.append(dict(D_min=float(thr), ruido=nz, c=c, vc=cv, tamano=float(np.nanmean(ver > cv)), poder_0_10=float(np.nanmean(alt > cv)),
                           eventos_retenidos=float(np.nanmean(nul[evk])), frac_F_recortada=float(np.nanmean(nul[rk])), sd_b_nula=float(np.nanstd(nul[key]))))
dm = pd.DataFrame(dm); dm.to_csv(OUTD + "/sim7_Dmin_F.csv", index=False)
print("\nUMBRAL D_min para F (N=738): resumen por umbral")
print(dm.groupby("D_min").agg(vc=("vc", "first"), tamano_max=("tamano", "max"), poder_min=("poder_0_10", "min"), poder_mediano=("poder_0_10", "median"),
                              eventos=("eventos_retenidos", "mean"), recortada=("frac_F_recortada", "mean"), sd_nula=("sd_b_nula", "mean")).round(3).to_string())
print("poder F por umbral y ruido (mediana sobre c):"); print(dm.groupby(["D_min", "ruido"]).poder_0_10.median().unstack().round(3).to_string())
# techo
ce = []
for i, n in enumerate(N_CEIL):
    cd = {oc: max(np.percentile(RC[(100 + i, j, k, 4)]["dbeta_" + oc], 97.5) for j in range(2) for k in range(2)) for oc in ("R", "F")}
    cd95 = {oc: max(np.percentile(RC[(100 + i, j, k, 4)]["dbeta_" + oc], 95) for j in range(2) for k in range(2)) for oc in ("R", "F")}
    for j, nz in enumerate(NZC):
        for k, c in enumerate(CSC):
            nulc = RC[(100 + i, j, k, 4)]
            for e, tc in enumerate([0.5, 1.0]):
                r = RC[(100 + i, j, k, 5 + e)]
                for oc in ("R", "F"):
                    ce.append(dict(n=n, ruido=nz, c=c, techo=tc, resultado=oc, vc_dbeta_a025=cd[oc], vc_dbeta_a05=cd95[oc],
                                   poder_a025=float(np.mean(r["dbeta_" + oc] > cd[oc])), poder_a05=float(np.mean(r["dbeta_" + oc] > cd95[oc])),
                                   tamano_celda_a025=float(np.mean(nulc["dbeta_" + oc] > cd[oc]))))
ce = pd.DataFrame(ce); ce.to_csv(OUTD + "/sim7_techo_dbeta.csv", index=False)
print("\nCONTRASTE DEL TECHO: poder maximo por N, resultado y fuerza del techo (alfa 0.025 / 0.05)")
print(ce.groupby(["resultado", "techo", "n"]).agg(vc=("vc_dbeta_a025", "first"), poder_max_025=("poder_a025", "max"), poder_max_05=("poder_a05", "max")).round(3).to_string())
print("tamano max por celda (techo, N):", ce.groupby("resultado").tamano_celda_a025.max().round(3).to_dict())
