import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d

sheet = pd.read_excel("Data/Data-sheet.xlsx", 0)

d = np.array(sheet['d(cm)'])
B = np.stack((sheet['Bx (µT)'], sheet['By (µT)'], sheet['Bz (µT)']), 1) * 10**-6
B_magnitude = (np.einsum('ij, ij -> i', B, B))**(1/2)
# We gaan er vanuit dat het veld in het midden van de spoelen perfect in de juiste richting is gericht
# Om het veld dan langs deze as te integreren moeten we de component van het veld langs deze as te bepalen
# We bepalen dus een eenheidsvector door de gemiddelde richting te bepalen van de middelste metingen
# en dan het puntproduct te nemen met onze data
mask = B_magnitude > 10**-3
# We selecteren de metingen met een veldsterkte (magnitude) groter dan 1 mT,
# zodat we de gemiddelde veldrichting bepalen in het gebied waar het veld sterk en goed gedefinieerd is.
eenheidsvector = np.sum(B[mask, :], 0)
eenheidsvector = eenheidsvector / (eenheidsvector @ eenheidsvector)**(1/2)

B_langs_as = B @ eenheidsvector


# =================================================================
# Is dat hier BIOPHYSICS
# =================================================================

B_data = B_langs_as * 10**3 # B_data in militesla

plt.plot(d- 13.69, B_data,'o')
plt.xlabel("d (cm)")
plt.ylabel("B langs as (mT)")
plt.grid()
plt.savefig("Data/Figuren/kalibratie_magnetisch_veld.png", dpi=300, bbox_inches='tight')
plt.close()

# =================================================================
# Interpolatie van het veld
# =================================================================

interpolatie = interp1d(d, B_langs_as, kind='cubic')
d_interpolatie = np.linspace(d[0], d[-1], 1000)
B_interpolatie = interpolatie(d_interpolatie)

# Het minimum van het veld in het midden tussen de 10 en 17 cm,
# het minimum dat daar wordt bekomen is het gevolg van dat onze 2 spoelen tegen elkaar gelijmd zijn,
# en dat het veld daar iets minder sterk is.

# Aan de hand van dat minimum kunnen we bepalen op welke afstand het midden van de spoelen ligt,
# en op welke afstanden van de spoel de rest van het magnetisch veld is.

# =======================================================================
# minimum van de interpolatie bepalen in het gebied tussen 10 en 17 cm
# =======================================================================

mask = (10 < d_interpolatie) & (d_interpolatie < 17)
d_midden = d_interpolatie[mask][np.argmin(B_interpolatie[mask])]
print(f"Het midden van de spoelen ligt op {d_midden:.2f} cm") # Dit gaf een waarde van 13.69 cm


# =======================================================================
# Resultaat plotten
# =======================================================================


plt.plot(d, B_langs_as*10**3, 'o', label='Data')
plt.plot(d_interpolatie, B_interpolatie*10**3, '-', label='Interpolatie')
plt.xlabel("d (cm)")
plt.ylabel("B langs as (mT)")
plt.grid()
plt.axvline(x=d_midden, color='r', linestyle='--', label='Midden van de spoelen')
plt.legend(fontsize=6, loc='upper right')
plt.savefig("Data/Figuren/interpolatie_magnetisch_veld.png", dpi=300, bbox_inches='tight')
plt.close()

# =======================================================================
# B_magnitude vergelijken met B_langs_as scatterplotten   
# =======================================================================

plt.scatter(d, B_langs_as*10**3, s=5,  label=r'$B_{langs\_as}$')
plt.scatter(d, B_magnitude*10**3, s=5, label=r'$B_{Magnitude}$')
plt.xlabel("d (cm)")
plt.ylabel("B langs as (mT)")
plt.grid()
plt.legend(fontsize=6, loc='upper right')
plt.savefig("Data/Figuren/b_magnitude_vs_b_langs_as.png", dpi=300, bbox_inches='tight')
plt.close()

# =======================================================================
# Data magnetisch veld plotten in functie van de afstand d, met foutbalken
# =======================================================================

plt.plot(d, B_langs_as*10**3, 'o', label='Data')
plt.xlabel("d (cm)")
plt.ylabel("B langs as (mT)")
plt.title("Data van het magnetisch veld")
plt.legend(fontsize=6, loc='upper right')
plt.savefig("Data/Figuren/data_magnetisch_veld.png", dpi=300, bbox_inches='tight')
plt.close()