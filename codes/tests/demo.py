import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.optimize import curve_fit
from scipy.integrate import quad


def gaussiana(x, a, x0, sigma):
    return a * np.exp(-((x - x0) ** 2) / (2 * sigma**2))


def ajuste(wv, sp, max_val, index_max_val):
    popt, pconv = curve_fit(gaussiana, wv, sp, p0=[max_val, index_max_val, 0.5])
    return popt


# Cargar los datos del archivo FITS
nombre = "../manga-7495-6102-LINCUBE.fits.gz"
hdu = fits.open(nombre)
flujos = hdu["FLUX"].data
wave = hdu["WAVE"].data

img_h = flujos.shape[1]
img_w = flujos.shape[2]

hdul_catalog = fits.open("../redshift_catalog/dapall-v3_1_1-3.1.0.fits")
data_catalog = hdul_catalog[1].data
ix = np.where(data_catalog["PLATEIFU"] == hdu["FLUX"].header["PLATEIFU"])
redshift = data_catalog["nsa_z"][ix][0]

wave = wave / (1 + redshift)

img = np.zeros((img_h, img_w))

for i in range(img_h):
    for j in range(img_w):
        espectro = flujos[:, i, j]
        # espectro = np.nan_to_num(espectro)
        # Verificar si el espectro está lleno de ceros
        if np.all(espectro == 0) or np.isinf(espectro).any():
            img[i, j] = 0
            continue

        try:
            max_element_index = np.argmax(espectro)
            max_val = np.max(espectro)

            wv_ini = int(wave[max_element_index - 30])
            wv_fin = int(wave[max_element_index + 30])

            continuo_ini = int(wave[max_element_index - 15])
            continuo_fin = int(wave[max_element_index + 15])

            t = np.where((wave > wv_ini) & (wave < wv_fin))
            wv = wave[t]
            sp = espectro[t]
            continuo_avr = np.mean(
                espectro[wv_ini:continuo_ini] + espectro[continuo_fin:wv_fin]
            )

            res = ajuste(wv, sp, max_val, wave[max_element_index])
            if res is not None:

                gaus = gaussiana(wv, res[0], res[1], res[2])

                # Calcular la integral de la gaussiana ajustada
                integral, _ = quad(
                    gaussiana, wv[0], wv[-1], args=(res[0], res[1], res[2])
                )

            img[i, j] = integral
            print(f"{i,j} : {img[i,j]} - listo - avr : {continuo_avr}")
        except:
            img[i, j] = 0
            print(f"{i,j} : {img[i,j]} - listo")

# Mostrar un gráfico tipo mapa de calor de los datos generados
fig = plt.figure()
bx = fig.add_subplot(111)
cx = bx.imshow(np.log10(img))
plt.colorbar(cx, label="Integral de la Gaussiana")
plt.title("Mapa de calor de las integrales gaussianas")
plt.xlabel("X")
plt.ylabel("Y")

fig = plt.figure()
bx = fig.add_subplot(111)
cx = bx.imshow(img)
plt.colorbar(cx, label="Integral de la Gaussiana")
plt.title("Mapa de calor de las integrales gaussianas")
plt.xlabel("X")
plt.ylabel("Y")

plt.show()
