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


def dividirDatos(f1, f2, f3, f4):
    l = len(f1)
    print(len(f1), len(f2), len(f3), len(f4))
    f1divf2 = []
    f3divf4 = []
    for i in range(l):
        if f1[i] != 0 and f2[i] != 0 and f3[i] != 0 and f4[i] != 0:
            try:
                f1divf2.append(log10(f1[i] / f2[i]))
                f3divf4.append(log10(f3[i] / f4[i]))
            except Exception as e:
                raise e
    return f1divf2, f3divf4


def integracionPar(f1, f2, f3, f4):
    f = f1.shape
    datos_f1 = []
    datos_f2 = []
    datos_f3 = []
    datos_f4 = []
    for i in range(f[0]):
        if np.all(f1[i] == np.nan) or np.all(f2[i] == np.nan):
            continue
        for k in range(f[1]):
            if (
                not np.isnan(f1[i][k])
                and not np.isnan(f2[i][k])
                and not np.isnan(f3[i][k])
                and not np.isnan(f4[i][k])
            ):
                datos_f1.append(f1[i][k])
                datos_f2.append(f2[i][k])
                datos_f3.append(f3[i][k])
                datos_f4.append(f4[i][k])
    f1divf2 = []
    f3divf4 = []

    print(len(datos_f1), len(datos_f2), len(datos_f3), len(datos_f4))
    for i in range(len(datos_f1)):
        if (
            datos_f1[i] != 0
            and datos_f2[i] != 0
            and datos_f3[i] != 0
            and datos_f4[i] != 0
        ):
            try:
                div1_2aux = log10(datos_f1[i] / datos_f2[i])
                div3_4aux = log10(datos_f3[i] / datos_f4[i])
                f1divf2.append(div1_2aux)
                f3divf4.append(div3_4aux)
            except Exception as e:
                pass

    return f1divf2, f3divf4


#plateifu = "8988-6104"
plateifu = "7960-3704"
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

print(hdul_Ha[0].data.shape)

flujoNII = hdul_NII[0].data
flujoHa = hdul_Ha[0].data
flujoHb = hdul_Hb[0].data
flujoOIII = hdul_OIII[0].data

Log10NIIdivHa, Log10OIIIdivHb = integracionPar(flujoNII, flujoHa, flujoOIII, flujoHb)

flg = plt.figure()
ax = flg.add_subplot(111)
ax.set_title(
    f"Diagrama de Diagnostico (log10([NII]/Ha), log10([OIII]/Hb))\nNube de puntos : {plateifu}"
)
ax.set_xlabel("log10(NII/Ha)")
ax.set_ylabel("log10(OIII/Hb)")


X = np.linspace(-2, 0.049, 100)
Y = 0.61 / (X - 0.05) + 1.3
ax.plot(X, Y, c="k", linestyle="--", label="Y = 0.61/[X-0.05]+1.3")

X1 = np.linspace(-2, 0.46, 1900)
Y1 = 0.61 / (X1 - 0.47) + 1.19
ax.plot(X1, Y1, label="Y1 = 0.61/[X1-0.47]+1.19")

ax.set_xlim(-2, 1)  # Establece los límites del eje x
ax.set_ylim(-2, 1.5)  # Establece los límites del eje y

ax.plot(Log10NIIdivHa, Log10OIIIdivHb, "ro", markersize=1)
plt.grid()
plt.legend()
plt.show()
