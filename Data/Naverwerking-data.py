import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import scipy.integrate as integrate

# =================================================================
# Deze python file heeft als doel om het magnetisch veld door onze
# staaf fused kwarts te bepalen die (200 +- 1)mm lang is.
# =================================================================


sheet = pd.read_excel("Data/Kalibratie_magnetisch_veld.xlsx", 0)

d = np.array(sheet['d(cm)'])
B = np.stack((sheet['Bx (µT)'], sheet['By (µT)'], sheet['Bz (µT)']), 1) * 10**-6
B_magnitude = (np.einsum('ij, ij -> i', B, B))**(1/2)

# =================================================================
# Interpolatie van het veld
# =================================================================

mask = B[:, 1] > 10**-3
# We selecteren de metingen met een y-component groter dan 1 mT

eenheidsvector = np.sum(B[mask, :], 0)
eenheidsvector = eenheidsvector / (eenheidsvector @ eenheidsvector)**(1/2)

B_langs_as = B @ eenheidsvector

interpolatie = interp1d(d, B_langs_as, kind='cubic')
d_interpolatie = np.linspace(d[0], d[-1], 1000)
B_interpolatie = interpolatie(d_interpolatie)

# De staaf werd in het midden van de 2 spoelen geplaatst,
# wat op een afstand van 13.69cm lag in de interpolatie van het veld.
# We willen dus het veld in het interval [3.69, 23.69]cm hebben,
# en dat veld dan integreren over de lengte van de fused kwarts staaf.
# Hiervoor zullen we een mask gebruiken.

mask_staaf = (3.69 < d_interpolatie) & (d_interpolatie < 23.69)
B_staaf = B_interpolatie[mask_staaf]
d_staaf = d_interpolatie[mask_staaf]

# Gemiddeld magnetisch veld door de staaf


def integrand(x):
    return interpolatie(x)

#integratie van het veld over de lengte van de staaf
Integraal = integrate.quad(integrand, 3.69, 23.69)
print("Het veld dat door de staaf gaat is ongeveer", Integraal[0], "T*cm")
print(Integraal[1], "is de fout op deze waarde")
print(Integraal)
