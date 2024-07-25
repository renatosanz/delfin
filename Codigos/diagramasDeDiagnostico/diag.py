"""
Este programa usa la informacion de las lineas de 
emision extraidas previamente para obtener un 
diagrama de diagnostico que nos asegure que la 
galaxia que estamos analizando tiene formacion 
estelar mediante una integracion de los siguientes datos: 
(x,y) = (log10([NII]/Ha), log10([OIII]/Hb))
"""

from math import log10
from astropy.io.fits import open
import numpy as np
import matplotlib.pyplot as plt


def integrar(flujo):
    suma = 0
    for i in flujo:
        if np.all(flujo == np.nan):
            continue
        for k in i:
            if not np.isnan(k):
                suma += k
    return suma


def integracionPar(flujo1, flujo2):
    f = flujo1.shape
    suma1 = 0
    suma2 = 0
    for i in range(f[0]):
        if np.all(flujo1[i] == np.nan) or np.all(flujo2[i] == np.nan):
            continue
        for k in range(f[1]):
            if not np.isnan(flujo1[i][k]) and not np.isnan(flujo2[i][k]):
                suma1 += flujo1[i][k]
                suma2 += flujo2[i][k]
    return suma1, suma2


"""8988-6104
hdul_NII = open(
    "../extractorLineasEmision/fits/fits8988-6104_lines/fits8988-6104_[NII]_6548_.fits"
)
hdul_Ha = open(
    "../extractorLineasEmision/fits/fits8988-6104_lines/fits8988-6104_Ha_6564_.fits"
)

hdul_Hb = open(
    "../extractorLineasEmision/fits/fits8988-6104_lines/fits8988-6104_Hb_4861_.fits"
)
hdul_OIII = open(
    "../extractorLineasEmision/fits/fits8988-6104_lines/fits8988-6104_[OIII]_5007_.fits"
)
"""

plateifu = "7960-3704"
#plateifu = "8988-6104"
#plateifu = "7495-6102"

hdul_NII = open(
    f"../extractorLineasEmision/fits/fits{plateifu}_lines/fits{plateifu}_[NII]_6548_.fits"
)
hdul_Ha = open(
    f"../extractorLineasEmision/fits/fits{plateifu}_lines/fits{plateifu}_Ha_6564_.fits"
)

hdul_Hb = open(
    f"../extractorLineasEmision/fits/fits{plateifu}_lines/fits{plateifu}_Hb_4861_.fits"
)
hdul_OIII = open(
    f"../extractorLineasEmision/fits/fits{plateifu}_lines/fits{plateifu}_[OIII]_5007_.fits"
)

flujoNII = hdul_NII[0].data
flujoHa = hdul_Ha[0].data
flujoHb = hdul_Hb[0].data
flujoOIII = hdul_OIII[0].data

"""
integradoNII = integrar(flujoNII)
integradoHb = integrar(flujoHb)
integradoHa = integrar(flujoHa)
integradoOIII = integrar(flujoOIII)
"""

integradoNII, integradoHa = integracionPar(flujoNII, flujoHa)
integradoOIII, integradoHb = integracionPar(flujoOIII, flujoHb)

print("Ha flujo integrado:", integradoHa)
print("Hb flujo integrado:", integradoHb)
print("0III flujo integrado:", integradoOIII)
print("NII flujo integrado:", integradoNII)

NIIdivHa = integradoNII / integradoHa
print("(NII/Ha):", NIIdivHa)

OIIIdivHb = integradoOIII / integradoHb
print("(OIII/Hb):", OIIIdivHb)


Log10NIIdivHa = log10(integradoNII / integradoHa)
print("log10(NII/Ha):", Log10NIIdivHa)

Log10OIIIdivHb = log10(integradoOIII / integradoHb)
print("log10(OIII/Hb):", Log10OIIIdivHb)

flg = plt.figure()
ax = flg.add_subplot(111)
ax.set_title(f"Diagrama de Diagnostico (log10([NII]/Ha), log10([OIII]/Hb))\n{plateifu}")
ax.set_xlabel("log10(NII/Ha)")
ax.set_ylabel("log10(OIII/Hb)")

ax.set_xlim(-2, 1)  # Establece los límites del eje x
ax.set_ylim(-2, 1.5)  # Establece los límites del eje y

X = np.linspace(-2, 0.049, 100)
Y = 0.61 / (X - 0.05) + 1.3
ax.plot(X, Y, c="k", linestyle="--", label="Y = 0.61/[X-0.05]+1.3")

X1 = np.linspace(-2, 0.46, 1900)
Y1 = 0.61 / (X1 - 0.47) + 1.19
ax.plot(X1, Y1, label="Y1 = 0.61/[X1-0.47]+1.19")

ax.plot(
    Log10NIIdivHa,
    Log10OIIIdivHb,
    "ro",
)
plt.grid()
plt.legend()
plt.show()
