import dearpygui.dearpygui as dpg
import numpy as np
from scipy.optimize import curve_fit
import math
from scipy.integrate import quad


def gaussiana(x, a, x0, sigma):
    return a * np.exp(-((x - x0) ** 2) / (2 * sigma**2))


def ajuste(wv, sp, max_val, index_max_val):
    popt, pconv = curve_fit(gaussiana, wv, sp, p0=[max_val, index_max_val, 1])
    return popt


class ExtractLineEmision:
    def __init__(self, cube) -> None:

        self.datacube = cube

        self.updateImage()

        with dpg.window(
            label="Extract Line Emision " + self.datacube.plate_ifu,
            tag=self.datacube.plate_ifu + "LineEmision",
            no_collapse=True,
            min_size=[600, 800],
            pos=[0, 0],
            on_close=self.close,
        ):
            with dpg.plot(width=-1, label="", tag="espectrum_v2", crosshairs=True):
                dpg.bind_colormap(dpg.last_item(), dpg.mvPlotColormap_Spectral)
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="Wavelength Å", tag="x_axis_v2")
                dpg.add_plot_axis(
                    dpg.mvYAxis,
                    label=self.datacube.getHeaderInfo("FLUX", "BUNIT"),
                    tag="y_axis_v2",
                )
                dpg.add_heat_series(
                    x=self.img,
                    cols=self.datacube.shape[1],
                    rows=self.datacube.shape[2],
                    tag="lineEmisionImage",
                    parent="y_axis_v2",
                    format="",
                )
            dpg.add_button(label="Back", callback=self.close)
            dpg.bind_item_theme(dpg.last_item(), "exit_btn_theme")

            dpg.configure_item(
                "lineEmisionImage",
                x=self.img,
                scale_max=max(self.img),
                scale_min=min(self.img),
            )

    def updateImage(self):
        flux = self.datacube.getFluxData()
        wave = self.datacube.getWaveData()
        redshift = self.datacube.redshift

        img_h = flux.shape[1]
        img_w = flux.shape[2]

        wave = wave / (1 + redshift)
        self.img = []

        for i in range(img_h):
            for j in range(img_w):
                espectro = flux[:, i, j]
                # espectro = np.nan_to_num(espectro)
                # Verificar si el espectro está lleno de ceros
                if np.all(espectro == 0) or np.isinf(espectro).any():
                    self.img.append(0)
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

                    self.img.append(max_val)
                    print(f"{i,j} : listo - avr : {continuo_avr}")
                except:
                    self.img.append(0)
                    print(f"{i,j} : listo")

    def close(self):
        dpg.delete_item(self.datacube.plate_ifu + "LineEmision")
