import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import quad
from astropy.io import fits
import dearpygui.dearpygui as dpg
import os
import math


# Función gaussiana para el ajuste
def gaussiana(x, a, x0, sigma):
    return a * np.exp(-((x - x0) ** 2) / (2 * sigma**2))


# Función para ajustar la gaussiana a los datos
def ajuste(wv, sp, max_val, index_max_val, sigma):
    popt, pconv = curve_fit(gaussiana, wv, sp, p0=[max_val, index_max_val, sigma])
    return popt


# Función para calcular la integral de la gaussiana
def integralGauss(x):
    total = 0
    for n in x:
        total += math.pow(math.e, math.pow(-n, 2))
    return total


# Función para encontrar el valor más cercano en un array
def getClosestValue(array, k):
    return min(array, key=lambda x: abs(x - k))


def gaussiana(x, a, x0, sigma):
    return a * np.exp(-((x - x0) ** 2) / (2 * sigma**2))


def ajuste(wv, sp, max_val, index_max_val):
    popt, pconv = curve_fit(gaussiana, wv, sp, p0=[max_val, index_max_val, 0.05])
    return popt


class ExtractLineEmision:
    def __init__(self, cube) -> None:

        self.datacube = cube

        self.lines = [
            {"tag": "O[III] 5007", "line": "O[III]", "x": 5007},
            {"tag": "Ha 6564", "line": "Ha", "x": 6564},
            {"tag": "N[II] 6584", "line": "N[II]", "x": 6584},
            {"tag": "N[II] 6548", "line": "N[II]", "x": 6548},
            {"tag": "Hb 4861", "line": "Hb", "x": 4861},
            {"tag": "O[III] 4959", "line": "O[III]", "x": 4959},
            {"tag": "O[II] 3727", "line": "O[II]", "x": 3727},
            {"tag": "S[II] 6717", "line": "S[II]", "x": 6717},
            {"tag": "S[II] 6731", "line": "S[II]", "x": 6731},
        ]

        with dpg.window(
            label="Extract Line Emision " + self.datacube.plate_ifu,
            tag=self.datacube.plate_ifu + "LineEmision",
            no_collapse=True,
            min_size=[500, 500],
            pos=[0, 0],
            on_close=self.close,
        ):
            with dpg.group():
                dpg.add_radio_button(
                    ([x["tag"] for x in self.lines]),
                    tag="options_extract",
                )
                dpg.add_text(" ", tag="info_extraction_lbl")
                dpg.add_button(label="Extract", callback=self.generateFits)
                dpg.add_button(label="Back", callback=self.close)
                dpg.bind_item_theme(dpg.last_item(), "exit_btn_theme")

    def generateFits(self, sender, app_data, user_data):
        linedata = None
        for line in self.lines:
            if line["tag"] == dpg.get_value("options_extract"):
                linedata = line
                print(line)
                break

        flux = self.datacube.getFluxData()
        wave = self.datacube.getWaveData()
        redshift = self.datacube.redshift

        # Dimensiones de la imagen
        img_h = flux.shape[1]
        img_w = flux.shape[2]

        # Ajustar las longitudes de onda por el redshift
        wave = wave / (1 + redshift)
        wave = wave.astype(int)

        # Márgenes para el ajuste
        margen = 8
        submargen = 4

        img = np.zeros((img_h, img_w))
        longOnda = linedata["x"]
        nom = linedata["line"]
        print(longOnda)
        for i in range(img_h):
            for j in range(img_w):
                espectro = flux[:, i, j]
                if np.all(espectro == 0) or np.isinf(espectro).any():
                    img[i, j] = None
                    continue

                try:
                    max_element_index = np.where(wave == longOnda)[0][0]
                    max_val = espectro[max_element_index]

                    wv_ini = wave[max_element_index - margen]
                    wv_fin = wave[max_element_index + margen]

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
                    dpg.set_value(
                        "info_extraction_lbl", f"extracting {i,j} : {img[i,j]}"
                    )
                except:
                    img[i, j] = None

        # Guardar los datos en un archivo FITS
        hdu = fits.PrimaryHDU(data=img)
        hdul = fits.HDUList([hdu])
        if not os.path.exists(
            "./results/fits/" + f"fits{self.datacube.plate_ifu}_lines"
        ):
            os.makedirs("./results/fits/" + f"fits{self.datacube.plate_ifu}_lines")
        hdul.writeto(
            "./results/fits/"
            + f"fits{self.datacube.plate_ifu}_lines"
            + "/fits"
            + str(self.datacube.plate_ifu)
            + "_"
            + str(nom)
            + "_"
            + str(longOnda)
            + "_"
            + ".fits",
            overwrite=True,
        )
        dpg.set_value(
            "info_extraction_lbl",
            ".fits file on: "
            + "./results/fits/"
            + f"fits{self.datacube.plate_ifu}_lines",
        )

    def close(self):
        dpg.delete_item(self.datacube.plate_ifu + "LineEmision")
