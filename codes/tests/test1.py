import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.optimize import curve_fit
from scipy.integrate import quad


def gaussiana(x, a, x0, sigma):
    return a * np.exp(-((x - x0) ** 2) / (2 * sigma**2))


def ajuste(wv, sp, max_val, index_max_val):
    try:
        popt, pconv = curve_fit(gaussiana, wv, sp, p0=[int(max_val), index_max_val, 10])
        return popt
    except RuntimeError as e:
        print(f"Error en el ajuste: {e}")
        return None


# Cargar los datos del archivo FITS
nombre = "../manga-7495-6102-LINCUBE.fits.gz"
hdu = fits.open(nombre)
flujos = hdu["FLUX"].data
wave = hdu["WAVE"].data
espectro = flujos[:, 27, 27]
espectro = np.nan_to_num(espectro)

hdul_catalog = fits.open("../redshift_catalog/dapall-v3_1_1-3.1.0.fits")
data_catalog = hdul_catalog[1].data
ix = np.where(data_catalog["PLATEIFU"] == hdu["FLUX"].header["PLATEIFU"])
redshift = data_catalog["nsa_z"][ix][0]

wave = wave / (1 + redshift)

max_element_index = np.argmax(espectro)
max_val = np.max(espectro)

wv_ini = int(wave[max_element_index - 30])
wv_fin = int(wave[max_element_index + 30])

continuo_ini = int(wave[max_element_index - 15])
continuo_fin = int(wave[max_element_index + 15])

print(f"{wv_ini}---{continuo_ini}--A--{continuo_fin}---{wv_fin}")

t = np.where((wave > wv_ini) & (wave < wv_fin))
wv = wave[t]
sp = espectro[t]
continuo_avr = np.mean(espectro[wv_ini:continuo_ini] + espectro[continuo_fin:wv_fin])

res = ajuste(wv, sp, max_val, wave[max_element_index])
if res is not None:
    print(res, continuo_avr)

    gaus = gaussiana(wv, res[0], res[1], res[2])
    print(f"gaussiana = {gaus}")

    # Calcular la integral de la gaussiana ajustada
    integral, _ = quad(gaussiana, wv[0], wv[-1], args=(res[0], res[1], res[2]))

    flg = plt.figure()
    ax = flg.add_subplot(111)
    ax.plot(wv, sp)
    ax.plot(wv, gaus + continuo_avr)
    ax.set_title(f"integral: {integral}")
    plt.show()
else:
    print("No se pudo ajustar la curva.")
