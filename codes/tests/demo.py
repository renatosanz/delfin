import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.optimize import curve_fit
from scipy.integrate import quad
import math


def gaussiana(x, a, x0, sigma):
    return a * np.exp(-((x - x0) ** 2) / (2 * sigma**2))


def ajuste(wv, sp, max_val, index_max_val, sigma):
    popt, pconv = curve_fit(gaussiana, wv, sp, p0=[max_val, index_max_val, sigma])
    return popt


def integralGauss(x):
    total = 0
    for n in x:
        total += math.pow(math.e, math.pow(-n, 2))
    return total


def getClosestValue(array, k):
    return min(array, key=lambda x: abs(x - k))


# Cargar los datos del archivo FITS
nombre = "../../../datacubes/manga-7495-6102-LINCUBE.fits.gz"
hdu = fits.open(nombre)
flujos = hdu["FLUX"].data
wave = hdu["WAVE"].data

img_h = flujos.shape[1]
img_w = flujos.shape[2]

hdul_catalog = fits.open("../../../datacubes/redshift_catalog/dapall-v3_1_1-3.1.0.fits")
data_catalog = hdul_catalog[1].data
ix = np.where(data_catalog["PLATEIFU"] == hdu["FLUX"].header["PLATEIFU"])
redshift = data_catalog["nsa_z"][ix][0]
wave = wave / (1 + redshift)
wave = wave.astype(int)

lineas = [
    {"nombre": "Ha", "x": 6564},
]

lineas1 = [
    {"nombre": "[OIII]", "x": 5007},
    {"nombre": "Ha", "x": 6564},
    {"nombre": "[NII]", "x": 6584},
    {"nombre": "[NII]", "x": 6548},
    {"nombre": "Hb", "x": 4861},
    {"nombre": "[OIII]", "x": 4959},
    {"nombre": "[OII]", "x": 3727},
    # {"nombre": "[SII]", "x": 6717},
    # {"nombre": "[SII]", "x": 6731},
]

for k in lineas:
    img = np.zeros((img_h, img_w))
    longOnda = k["x"]
    nom = k["nombre"]
    print(longOnda)
    for i in range(img_h):
        for j in range(img_w):
            espectro = flujos[:, i, j]
            if np.all(espectro == 0) or np.isinf(espectro).any():
                img[i, j] = None
                continue

            try:
                max_element_index = np.where(wave == longOnda)[0][0]
                max_val = espectro[max_element_index]

                wv_ini = wave[max_element_index - 30]
                wv_fin = wave[max_element_index + 30]

                continuo_ini = wave[max_element_index - 10]
                continuo_fin = wave[max_element_index + 10]

                t = np.where((wave > wv_ini) & (wave < wv_fin))
                wv = wave[t]
                sp = espectro[t]
                max_val = max(sp)
                continuo_avr = (
                    np.mean(espectro[wv_ini:continuo_ini])
                    + np.mean(espectro[continuo_fin:wv_fin])
                ) / 2

                medium_height = (max_val - continuo_avr) / 2 + continuo_avr
                leftSide = sp[:30]
                rightSide = sp[30:]
                print(leftSide,rightSide)
                leftPoint = getClosestValue(leftSide, medium_height)
                rightPoint = getClosestValue(rightSide, medium_height)
                print(leftPoint,rightPoint)
                leftPoint_wave = wv[np.where(sp==leftPoint)[0]]
                rightPoint_wave = wv[np.where(sp==rightPoint)[0]]
                print(leftPoint_wave,rightPoint_wave)

                fwahm = abs(rightPoint_wave[0] - leftPoint_wave[0])

                res = ajuste(wv, sp, max_val, wave[max_element_index], fwahm)
                integral, _ = quad(
                    gaussiana, wv[0], wv[-1], args=(res[0], res[1], res[2])
                )
                img[i, j] = integral - continuo_avr * (wv[-1] - wv[0])
                print(f"{i,j} : {img[i,j]} - listo - fwahm : {fwahm}")

                # Generar la gráfica si i y j son 27
                if i == 20 and j == 27:
                    gaus = gaussiana(wv, res[0], res[1], res[2])

                    flg = plt.figure()
                    ax = flg.add_subplot(111)
                    ax.set_xlabel("Longitud de onda")
                    ax.set_ylabel(hdu["FLUX"].header["BUNIT"])
                    ax.plot(wv, sp, color="#26854c", label="Espectro")
                    ax.plot(
                        wv, gaus + continuo_avr, color="#ec273f", label="Campana Gauss"
                    )
                    ax.set_title(f"integral: {integral} : (27,27)")
                    ax.text(0, 0, f"fwahm : {fwahm}")
                    ax.axhline(y=continuo_avr, color="#ffffff", linestyle="-")
                    ax.axhline(y=medium_height, color="#f6d", linestyle="-")
                    ax.vlines(
                        wave[max_element_index],
                        ymin=0,
                        colors="#de5d3a",
                        linestyles="dashdot",
                        ymax=max_val,
                        label="l",
                    )
                    ax.vlines(
                        continuo_ini,
                        ymin=0,
                        colors="#26854c",
                        ymax=max_val,
                        label="l-p",
                    )
                    ax.vlines(
                        continuo_fin,
                        ymin=0,
                        colors="#26854c",
                        ymax=max_val,
                        label="l+p",
                    )
                    plt.fill_between(wv, gaus + continuo_avr, color="#26854c83")
                    plt.grid()
                    plt.legend()
                    plt.show()

            except:
                img[i, j] = None

    fig = plt.figure()
    bx = fig.add_subplot(111)
    cx = bx.imshow(img)
    plt.colorbar(cx, label="Integral de la Gaussiana")
    plt.title("Mapa " + str(longOnda) + str(nom))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("./imgs/img" + str(longOnda) + str(nom) + ".png")
