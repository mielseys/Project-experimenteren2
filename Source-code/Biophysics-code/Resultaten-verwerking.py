# Deze python file zal de resultaten van het Faraday effect experiment verwerken en visualiseren.

# ==========================================================
# Imports
# ==========================================================

import numpy as np
import scipy as sp
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# ==========================================================
# Excel sheet vinden en inlezen
# ==========================================================

base_dir = Path(__file__).resolve().parent
excel_path = base_dir.parent.parent / "Data" / "Data-sheet.xlsx"

# Excel sheet "Verwerking 2" bevat de resultaten.
verwerking_2 = pd.read_excel(excel_path, sheet_name="Verwerking_2")

expected_verwerking_cols = {
    'Verdet (rad/(T * mm))',
    'AF_Verdet',
    'B_spoel (mT)',
    'AF_B (mt)',
}
missing_verwerking_cols = expected_verwerking_cols.difference(verwerking_2.columns)
if missing_verwerking_cols:
    raise ValueError(
        f"Excel-sheet 'Verwerking 2' mist de volgende kolommen: {sorted(missing_verwerking_cols)}"
    )

metingen = pd.read_excel(excel_path, sheet_name="Metingen")


expected_metingen_cols = {
    'Frequentie (Hz)',
}
missing_metingen_cols = expected_metingen_cols.difference(metingen.columns)
if missing_metingen_cols:
    raise ValueError(
        f"Excel-sheet 'Metingen' mist de volgende kolommen: {sorted(missing_metingen_cols)}"
    )


# Aantal meetpunten dat uit de dataset wordt gebruikt (b.v. 25 magnetische veld-metingen)
N_POINTS = 25  # Alleen maar de relevante data.

# ==========================================================
# Resultaten experiment Faraday effect
# ==========================================================

verdet_cst_col = np.array(verwerking_2['Verdet (rad/(T * mm))'])[:N_POINTS]
af_verdet_col = np.array(verwerking_2['AF_Verdet'])[:N_POINTS]

mag_veld_col = np.array(verwerking_2['B_spoel (mT)'])[:N_POINTS]
af_mag_veld_col = np.array(verwerking_2['AF_B (mt)'])[:N_POINTS]

lengte_kwarts = 200  # mm
af_lengte_kwarts = 1  # mm

hoek_beta = np.array(verwerking_2['dtheta'])[:N_POINTS]
af_hoek_beta = np.array(verwerking_2['AF (dtheta)'])[:N_POINTS]

frequentie = np.array(metingen['Frequentie (Hz)'])[:N_POINTS]

# ==========================================================
# Figuren plotten
# ==========================================================

# Verdet constante in functie van magnetisch veld
plt.plot(mag_veld_col, verdet_cst_col, 'o', label='Verdet constante')
plt.errorbar(mag_veld_col, verdet_cst_col, xerr=af_mag_veld_col, yerr=af_verdet_col, fmt='o', ecolor='red', capsize=5, label='Foutbalken')
plt.xlabel(r'Magnetisch veld $(mT)$')
plt.ylabel(r'Verdet constante $(rad/(T * mm))$')
plt.grid()
plt.legend(fontsize=6, loc='upper right')
plt.savefig(base_dir.parent.parent / "Data" / "Figuren" / "verdet_constante_vs_magnetisch_veld.png", dpi=300, bbox_inches='tight')
plt.close()


# Verdet constante in functie van de frequentie
plt.plot(frequentie, verdet_cst_col, 'o', label='Verdet constante')
plt.errorbar(frequentie, verdet_cst_col, xerr=None, yerr=af_verdet_col, fmt='o', ecolor='red', capsize=5, label='Foutbalken')
plt.xlabel(r'Frequentie $(Hz)$')
plt.ylabel(r'Verdet constante $(rad/(T * mm))$')
plt.grid()
plt.legend(fontsize=6, loc='upper right')
plt.savefig(base_dir.parent.parent / "Data" / "Figuren" / "verdet_constante_vs_frequentie.png", dpi=300, bbox_inches='tight')
plt.close()

# Hoek beta in functie van het magnetisch veld
plt.plot(mag_veld_col, hoek_beta, 'o', label=r'Hoek $\beta$')
plt.errorbar(mag_veld_col, hoek_beta, xerr=af_mag_veld_col, yerr=af_hoek_beta, fmt='o', ecolor='red', capsize=5, label='Foutbalken')
plt.xlabel(r'Magnetisch veld $(mT)$')
plt.ylabel(r'Hoek $\beta$ $(rad)$')
plt.grid()
plt.legend(fontsize=6, loc='upper right')
plt.savefig(base_dir.parent.parent / "Data" / "Figuren" / "hoek_beta_vs_magnetisch_veld.png", dpi=300, bbox_inches='tight')
plt.close()

# =======================================================
# Lineaire regressie van hoek beta in functie van het magnetisch veld
# =======================================================

gewichten_beta = 3 / af_hoek_beta

B_over_as = mag_veld_col * lengte_kwarts / 10**6
AF_B_over_as = B_over_as * (af_mag_veld_col / mag_veld_col + af_lengte_kwarts / lengte_kwarts)

Delta = np.sum(gewichten_beta) * (gewichten_beta @ (B_over_as)**2) - (B_over_as @ gewichten_beta)**2

a0 = ((gewichten_beta @ (B_over_as)**2) * (gewichten_beta @ hoek_beta) - (gewichten_beta @ B_over_as) * (np.sum(gewichten_beta * hoek_beta * B_over_as))) / Delta
a1 = (np.sum(gewichten_beta) * np.sum(gewichten_beta * hoek_beta * B_over_as) - (gewichten_beta @ B_over_as) * (gewichten_beta @ hoek_beta)) / Delta

sigma_y = ((gewichten_beta @ (hoek_beta - a0 - a1 * B_over_as)**2) / 23)**(1/2)
sf_a0 = sigma_y * ((gewichten_beta @ (B_over_as)**2) / Delta)**(1/2)
sf_a1 = sigma_y * ((np.sum(gewichten_beta)) / Delta)**(1/2)

print(f"a0: {a0}")
print(f"a1: {a1}")
print(f"sf_a0: {sf_a0}")
print(f"AF(a0): {3*sf_a0}")
print(f"sf_a1: {sf_a1}")
print(f"AF(a1): {3*sf_a1}")

B_punten = np.linspace(np.min(B_over_as), np.max(B_over_as), 300)
theta_punten = a0 + a1 * B_punten

plt.plot(mag_veld_col, hoek_beta, 'o', label=r'Hoek $\beta$')
plt.errorbar(mag_veld_col, hoek_beta, xerr=af_mag_veld_col, yerr=af_hoek_beta, fmt='o', ecolor='red', capsize=5, label=r'Hoek $\beta$')
plt.plot(B_punten, theta_punten, label="fit")
plt.xlabel(r'Magnetisch veld $(mT)$')
plt.errorbar(B_over_as, hoek_beta, xerr=AF_B_over_as, yerr=af_hoek_beta, fmt='o', ecolor='red', capsize=5, label=r'Hoek $\beta$')
plt.plot(B_punten, theta_punten, label=rf"Beste fit: $\beta = ({a1:.1f}\pm {np.ceil(30 * sf_a1) / 10})\frac{{\text{{rad}}}}{{\text{{Tm}}}}Bl + ({a0:.4f} \pm {np.ceil(3 * 10**4 * sf_a0) * 10**-4:.4f})\text{{rad}}$")
plt.xlabel(r'Magnetisch veld langs de as $(Tm)$')
plt.ylabel(r'Hoek $\beta$ $(rad)$')
plt.grid()
plt.legend(fontsize=6, loc='upper right')
plt.savefig(base_dir.parent.parent / "Data" / "Figuren" / "hoek_beta_vs_magnetisch_veld_met_intercept.png", dpi=300, bbox_inches='tight')
plt.close()

# =======================================================
# Lineaire regressie met gewichtsfactoren zonder intercept
# =======================================================

f = lambda x, a: a * x

# Gebruik curve_fit omdat deze een error estimation geeft
fit = sp.optimize.curve_fit(f, mag_veld_col * lengte_kwarts / 10**6, hoek_beta, sigma = af_hoek_beta/3)
print(fit)

f = lambda x, a: a * x

# Gebruik curve_fit omdat deze een error estimation geeft
fit = sp.optimize.curve_fit(f, mag_veld_col * lengte_kwarts / 10**6, hoek_beta, sigma = af_hoek_beta/3)
print(fit)

xpunten = (np.min(B_over_as), np.max(B_over_as))
ypunten = fit[0] * xpunten

plt.errorbar(mag_veld_col * lengte_kwarts / 10**6, hoek_beta, xerr=AF_B_over_as, yerr=af_hoek_beta, fmt='o', ecolor='red', capsize=5, label=r'Hoek $\beta$')
plt.plot(xpunten, ypunten, label=rf"Beste fit: $\beta = ({fit[0][0]:.1f}\pm {np.ceil(30 * fit[1][0, 0], ) / 10})\frac{{\text{{rad}}}}{{\text{{Tm}}}}Bl$")
plt.xlabel(r'Magnetisch veld langs de as $(Tm)$')
plt.ylabel(r'Hoek $\beta$ $(rad)$')
plt.grid()
plt.legend(fontsize=6, loc='upper right')
plt.savefig(base_dir.parent.parent / "Data" / "Figuren" / "hoek_beta_vs_magnetisch_veld_zonder_intercept.png", dpi=300, bbox_inches='tight')
plt.close()
