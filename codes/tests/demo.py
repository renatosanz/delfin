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
        total += math.pow(math.e,math.pow(-n,2))
    return total
    

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

lineas = [
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

for i in lineas:
    img = np.zeros((img_h, img_w))
    longOnda = i["x"]
    nom = i["nombre"]
    print(longOnda)
    for i in range(img_h):
        for j in range(img_w):
            espectro = flujos[:, i, j]
            # espectro = np.nan_to_num(espectro)
            # Verificar si el espectro está lleno de ceros
            if np.all(espectro == 0) or np.isinf(espectro).any():
                img[i, j] = 0
                continue

            try:
                max_element_index = int(longOnda - wave[0])
                max_val = espectro[max_element_index]

                wv_ini = int(wave[max_element_index - 30])
                wv_fin = int(wave[max_element_index + 30])

                continuo_ini = int(wave[max_element_index - 15])
                continuo_fin = int(wave[max_element_index + 15])

                t = np.where((wave > wv_ini) & (wave < wv_fin))
                wv = wave[t]
                sp = espectro[t]
                continuo_avr = (
                    np.mean(espectro[wv_ini:continuo_ini])
                    + np.mean(espectro[continuo_fin:wv_fin])
                ) / 2
                media = (max_val - continuo_avr) / 2
                ds = wv[np.where((sp > media - 1) & (sp < media + 1))]
                
                print(media, ds)
                
                FWAHM = ds[-1] - ds[0]

                res = ajuste(wv, sp, max_val, wave[max_element_index], FWAHM)
                if res is not None:
                    gaus = gaussiana(wv, res[0], res[1], res[2])
                    # Calcular la integral de la gaussiana ajustada
                    integral, _ = quad(
                        gaussiana, wv[0], wv[-1], args=(res[0], res[1], res[2])
                    )

                img[i, j] = integral - continuo_avr * (wv[-1] - wv[0])
                print(f"{i,j} : {img[i,j]} - listo - avr : {continuo_avr}")
            except:
                img[i, j] = 0
                print(f"{i,j} : {img[i,j]} - listo")
    
    print(longOnda)
    # Mostrar un gráfico tipo mapa de calor de los datos generados
    fig = plt.figure()
    bx = fig.add_subplot(111)
    cx = bx.imshow(np.log10(img))
    plt.colorbar(cx, label="Integral de la Gaussiana")
    plt.title("Mapa log10 "+str(longOnda)+str(nom))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("./imgs/img"+str(longOnda)+str(nom)+"log10.png")
    
    fig = plt.figure()
    bx = fig.add_subplot(111)
    cx = bx.imshow(img)
    plt.colorbar(cx, label="Integral de la Gaussiana")
    plt.title("Mapa "+str(longOnda)+str(nom))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("./imgs/img"+str(longOnda)+str(nom)+".png")
