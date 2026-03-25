# Deze python file zal de resultaten van het Faraday effect experiment verwerken en visualiseren.

# ==========================================================
# Imports
# ==========================================================

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import scipy.integrate as integrate
from pathlib import Path
import matplotlib.pyplot as plt

# ==========================================================
# Excel sheet vinden en inlezen
# ==========================================================

base_dir = Path(__file__).resolve().parent
excel_path = base_dir.parent.parent / "Data" / "Data-sheet.xlsx"

# Excel sheet 4 (vanaf 0 geteld: 3) bevat de resultaten.
verwerking_2 = pd.read_excel(excel_path, 3)

metingen = pd.read_excel(excel_path, 1)

# ==========================================================
# Resultaten experiment Faraday effect
# ==========================================================

verdet_cst_col = np.array(verwerking_2['Verdet (rad/(T * mm))'])
verdet_cst_col_rel = verdet_cst_col[:25]
af_verdet_col = np.array(verwerking_2['AF_Verdet'])
af_verdet_col_rel = af_verdet_col[:25]

mag_veld_col = np.array(verwerking_2['B_spoel (mT)'])
mag_veld_col_rel = mag_veld_col[:25]

af_mag_veld_col = np.array(verwerking_2['AF_B (mt)'])
af_mag_veld_col_rel = af_mag_veld_col[:25]

lengte_kwarts = 200  # mm
af_lengte_kwarts = 1  # mm

frequentie = np.array(metingen['Frequentie (Hz)'])  

# ==========================================================
# Figuren plotten
# ==========================================================

# Verdet constante in functie van magnetisch veld
plt.plot(mag_veld_col_rel, verdet_cst_col_rel, 'o', label='Verdet constante')
plt.errorbar(mag_veld_col_rel, verdet_cst_col_rel, xerr=af_mag_veld_col_rel, yerr=af_verdet_col_rel, fmt='o', ecolor='red', capsize=5, label='Foutbalken')
plt.xlabel(r'Magnetisch veld $(mT)$')
plt.ylabel(r'Verdet constante $(rad/(T * mm))$')
plt.title('Verdet constante in functie van het magnetisch veld')
plt.grid()
plt.legend(fontsize=6, loc='upper right')
plt.savefig(base_dir.parent.parent / "Data" / "Figuren" / "verdet_constante_vs_magnetisch_veld.png", dpi=300, bbox_inches='tight')
plt.close()


# Verdet constante in functie van de frequentie
plt.plot(frequentie, verdet_cst_col_rel, 'o', label='Verdet constante')
plt.errorbar(frequentie, verdet_cst_col_rel, xerr=None, yerr=af_verdet_col_rel, fmt='o', ecolor='red', capsize=5, label='Foutbalken')
plt.xlabel(r'Frequentie $(Hz)$')
plt.ylabel(r'Verdet constante $(rad/(T * mm))$')
plt.title('Verdet constante in functie van de frequentie')
plt.grid()
plt.legend(fontsize=6, loc='upper right')
plt.savefig(base_dir.parent.parent / "Data" / "Figuren" / "verdet_constante_vs_frequentie.png", dpi=300, bbox_inches='tight')
plt.close()