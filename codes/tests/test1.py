import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.optimize import curve_fit
from scipy.integrate import quad


def gaussiana(x, a, x0, sigma):
    return a * np.exp(-((x - x0) ** 2) / (2 * sigma**2))


def ajuste(wv, sp, max_val, index_max_val):
    try:
        popt, pconv = curve_fit(gaussiana, wv, sp, p0=[int(max_val), index_max_val, 30])
        return popt
    except RuntimeError as e:
        print(f"Error en el ajuste: {e}")
        return None


# Cargar los datos del archivo FITS (cubo de datos)
nombre = "../../../datacubes/manga-7495-6102-LINCUBE.fits.gz"
hdu = fits.open(nombre)
flujos = hdu["FLUX"].data
wave = hdu["WAVE"].data
espectro = flujos[:, 20, 20]
espectro = np.nan_to_num(espectro)

# Cargar los datos del archivo FITS (catalogo de redshift)
hdul_catalog = fits.open("../../../datacubes/redshift_catalog/dapall-v3_1_1-3.1.0.fits")
data_catalog = hdul_catalog[1].data
ix = np.where(data_catalog["PLATEIFU"] == hdu["FLUX"].header["PLATEIFU"])
redshift = data_catalog["nsa_z"][ix][0]

wave = wave / (1 + redshift)

max_element_index = np.argmax(espectro)
max_val = np.max(espectro)

margin = 20
continuo_margin = int(margin * 0.5)

wv_ini = int(wave[max_element_index - margin])
wv_fin = int(wave[max_element_index + margin])

continuo_ini = int(wave[max_element_index - continuo_margin])
continuo_fin = int(wave[max_element_index + continuo_margin])

print(f"{wv_ini}---{continuo_ini}--A--{continuo_fin}---{wv_fin}")

t = np.where((wave > wv_ini) & (wave < wv_fin))
wv = wave[t]
sp = espectro[t]
continuo_avr = (
    np.mean(espectro[wv_ini:continuo_ini]) + np.mean(espectro[continuo_fin:wv_fin])
) / 2

res = ajuste(wv, sp, max_val, wave[max_element_index])
if res is not None:
    print(res, continuo_avr)

    gaus = gaussiana(wv, res[0], res[1], res[2])
    print(f"gaussiana = {gaus}")

    # Calcular la integral de la gaussiana ajustada
    integral, _ = quad(gaussiana, wv[10], wv[30], args=(res[0], res[1], res[2]))

    flg = plt.figure()
    ax = flg.add_subplot(111)
    ax.set_xlabel("Longitud de onda ")
    ax.set_ylabel(hdu["FLUX"].header["BUNIT"])
    ax.plot(wv, sp, color="#26854c",label = "Espectro")
    ax.plot(wv, gaus + continuo_avr, color="#ec273f",label = "Campana Gauss")
    ax.set_title(f"integral: {integral} : (20,20)")
    ax.vlines(
        wave[max_element_index],
        ymin=0,
        colors="#de5d3a",
        linestyles="dashdot",
        ymax=max_val,
        label="l",
    )
    ax.vlines(continuo_ini, ymin=0, colors="#26854c", ymax=max_val, label="l-p")
    ax.vlines(continuo_fin, ymin=0, colors="#26854c", ymax=max_val, label="l+p")
    plt.fill_between(wv, gaus + continuo_avr, color="#26854c83")
    plt.grid()
    plt.legend()
    plt.show()
else:
    print("No se pudo ajustar la curva.")
