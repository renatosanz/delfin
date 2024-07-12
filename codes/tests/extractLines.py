import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.optimize import curve_fit
from scipy.integrate import quad


def gaussiana(x, a, x0, sigma):
    return a * np.exp(-((x - x0) ** 2) / (2 * sigma**2))


def ajuste(wv, sp, max_val, index_max_val, sigma):
    popt, pconv = curve_fit(gaussiana, wv, sp, p0=[max_val, index_max_val, sigma])
    return popt


# Cargar los datos del archivo FITS (cubo de datos)
nombre = "../../../datacubes/manga-7495-6102-LINCUBE.fits.gz"
hdu = fits.open(nombre)
flux = hdu["FLUX"].data
current_flux = flux[:, 27, 10]
current_flux = np.nan_to_num(current_flux)

wave_data = hdu["WAVE"].data

# Cargar los datos del archivo FITS (catalogo de redshift)
hdul_catalog = fits.open("../../../datacubes/redshift_catalog/dapall-v3_1_1-3.1.0.fits")
data_catalog = hdul_catalog[1].data
ix = np.where(data_catalog["PLATEIFU"] == hdu["FLUX"].header["PLATEIFU"])
redshift = data_catalog["nsa_z"][ix][0]

wave = wave_data / (1 + redshift)
wave = wave.astype(int)
longOnda = 5007
index = np.where(wave == longOnda)[0][0]
print(index)
# index_redshift = int(index * (1 + redshift))
lambda0 = current_flux[index]
print(lambda0)

margin = 20
continuo_margin = 10

wv_ini = int(wave[index - margin])
wv_fin = int(wave[index + margin])

continuo_ini = int(wave[index - continuo_margin])
continuo_fin = int(wave[index + continuo_margin])

print(f"{wv_ini}---{continuo_ini}--A--{continuo_fin}---{wv_fin}")

t = np.where((wave > wv_ini) & (wave < wv_fin))
wv = wave[t]
sp = current_flux[t]
continuo_avr = (np.mean(sp[:continuo_margin]) + np.mean(sp[continuo_margin * 2 :])) / 2

medium_height = (lambda0 - continuo_avr) / 2 + continuo_avr
medium_indexs = np.where((sp > (medium_height - 5)) & (sp < (medium_height + 5)))
medium_points = wv[medium_indexs]
print(medium_points)

fwahm = abs(medium_points[-1] - medium_points[0])
print(fwahm)

res = ajuste(wv, sp, lambda0, wave[index], fwahm)
if res is not None:
    # print(res, continuo_avr)

    gaus = gaussiana(wv, res[0], res[1], res[2])
    # print(f"gaussiana = {gaus}")

    # Calcular la integral de la gaussiana ajustada
    integral, _ = quad(gaussiana, wv[10], wv[30], args=(res[0], res[1], res[2]))

    flg = plt.figure()
    ax = flg.add_subplot(111)
    ax.set_xlabel("Longitud de onda ")
    ax.set_ylabel(hdu["FLUX"].header["BUNIT"])
    ax.plot(wv, sp, color="#26854c", label="Espectro")
    ax.plot(wv, gaus + continuo_avr, color="#ec273f", label="Campana Gauss")
    ax.set_title(f"integral: {integral} : (20,20)")
    ax.axhline(y=continuo_avr, color="#ffffff", linestyle="-")
    ax.axhline(y=medium_height, color="#f6d", linestyle="-")
    ax.vlines(
        wave[index],
        ymin=0,
        colors="#de5d3a",
        linestyles="dashdot",
        ymax=lambda0,
        label="l",
    )
    ax.vlines(continuo_ini, ymin=0, colors="#26854c", ymax=lambda0, label="l-p")
    ax.vlines(continuo_fin, ymin=0, colors="#26854c", ymax=lambda0, label="l+p")
    plt.fill_between(wv, gaus + continuo_avr, color="#26854c83")
    plt.grid()
    plt.legend()
    plt.show()
else:
    print("No se pudo ajustar la curva.")
