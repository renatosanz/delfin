import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.optimize import curve_fit
from scipy.integrate import quad
import math, os


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
plateifu = hdu["FLUX"].header["plateifu"]
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
    {"nombre": "[NII]", "x": 6584},
]

lineas1 = [
    {"nombre": "[OIII]", "x": 5007},
    {"nombre": "Ha", "x": 6564},
    {"nombre": "[NII]", "x": 6584},
    {"nombre": "[NII]", "x": 6548},
    {"nombre": "Hb", "x": 4861},
    {"nombre": "[OIII]", "x": 4959},
    {"nombre": "[OII]", "x": 3727},
    {"nombre": "[SII]", "x": 6717},
    {"nombre": "[SII]", "x": 6731},
]

margen = 8
submargen = 4

for k in lineas1:
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

                wv_ini = wave[max_element_index - margen]
                wv_fin = wave[max_element_index + margen]

                continuo_ini = wave[max_element_index - submargen]
                continuo_fin = wave[max_element_index + submargen]

                t = np.where((wave > wv_ini) & (wave < wv_fin))
                wv = wave[t]
                sp = espectro[t]
                max_val = max(sp)
                continuo_avr = (
                    np.mean(sp[: margen - submargen])
                    + np.mean(sp[margen + submargen :])
                ) / 2

                medium_height = (max_val - continuo_avr) / 2 + continuo_avr
                leftSide = sp[:margen]
                rightSide = sp[margen:]
                # print(leftSide, rightSide)
                leftPoint = getClosestValue(leftSide, medium_height)
                rightPoint = getClosestValue(rightSide, medium_height)
                print(leftPoint, rightPoint)
                leftPoint_wave = wv[np.where(sp == leftPoint)[0]]
                rightPoint_wave = wv[np.where(sp == rightPoint)[0]]
                print(leftPoint_wave, rightPoint_wave)

                fwahm = abs(rightPoint_wave[0] - leftPoint_wave[0])

                res = ajuste(wv, sp, max_val, wave[max_element_index], fwahm)
                integral, _ = quad(
                    gaussiana, wv[0], wv[-1], args=(res[0], res[1], res[2])
                )
                img[i, j] = integral - continuo_avr * int(margen / 3)
                print(f"{i,j} : {img[i,j]} - listo - fwahm : {fwahm}")
            except:
                img[i, j] = None

    fig = plt.figure()
    bx = fig.add_subplot(111)
    cx = bx.imshow(img)
    plt.colorbar(cx, label="Integral de la Gaussiana")
    plt.title("Mapa " + str(longOnda) + str(nom))
    plt.xlabel("X")
    plt.ylabel("Y")
    if not os.path.exists("./imgs/" + f"imgs{plateifu}_lines"):
        os.makedirs("./imgs/" + f"imgs{plateifu}_lines")
    plt.savefig(
        "./imgs/"
        + f"imgs{plateifu}_lines"
        + "/img"
        + str(plateifu)
        + "_"
        + str(nom)
        + "_"
        + str(longOnda)
        + "_"
        + ".png"
    )
    hdu = fits.PrimaryHDU(data=img)
    hdul = fits.HDUList([hdu])
    if not os.path.exists("./fits/" + f"fits{plateifu}_lines"):
        os.makedirs("./fits/" + f"fits{plateifu}_lines")
    hdul.writeto(
        "./fits/"
        + f"fits{plateifu}_lines"
        + "/fits"
        + str(plateifu)
        + "_"
        + str(nom)
        + "_"
        + str(longOnda)
        + "_"
        + ".fits",
        overwrite=True,
    )
