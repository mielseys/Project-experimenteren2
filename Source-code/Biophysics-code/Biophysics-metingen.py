# Deze Python file zorgt voor een grafische weergave van de meetdata. 

# ==========================================================
# Imports
# ==========================================================

import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# ==========================================================
# Excel sheet vinden en inlezen
# ==========================================================

base_dir = Path(__file__).resolve().parent
excel_path = base_dir.parent.parent / "Data" / "Data-sheet.xlsx"


metingen = pd.read_excel(excel_path, sheet_name="Metingen")


expected_metingen_cols = {
    'Frequentie (Hz)',
}
missing_metingen_cols = expected_metingen_cols.difference(metingen.columns)
if missing_metingen_cols:
    raise ValueError(
        f"Excel-sheet 'Metingen' mist de volgende kolommen: {sorted(missing_metingen_cols)}"
    )

N_POINTS = 25

metingnr_col = np.array(metingen['Metingnr'])
frequentie_col = np.array(metingen['Frequentie (Hz)']) 
stroom_col = np.array(metingen['Stroom (mA)'])
v_max_col = np.array(metingen['V_MAX (V)'])
v_min_col = np.array(metingen['V_MIN (V)'])

v = (v_max_col - v_min_col) / 2

plt.plot(stroom_col, v, 'o', label='Meetdata')
#plt.errorbar(stroom_col, v, xerr=np.ones(25)*0.1, yerr=np.ones(25)*0.002, fmt='o', ecolor='red', capsize=5, label='Meetdata met foutbalken')
plt.xlabel(r'Stroom (mA)')
plt.ylabel(r'Spanningsverschil $\Delta V = V_\text{MAX} - V_\text{MIN}$ (V)')
plt.grid()
plt.savefig(base_dir.parent.parent / "Data" / "Figuren" / "spanningsverschil_vs_stroom.png", dpi=300, bbox_inches='tight')
plt.close()