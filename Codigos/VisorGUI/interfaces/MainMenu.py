import dearpygui.dearpygui as dpg
import os

from interfaces.Modes import Modes
from interfaces.FilePickr import FilePickr
from interfaces.OpenRecent import OpenRecent
from interfaces.SetRedshiftCatalag import SetRedshiftCatalog
from Objects.ControlDataCubes import ControlDataCubes


class MainMenu:
    def __init__(self) -> None:

        dpg.create_context()
        dpg.create_viewport(title="InterVisor", resizable=False)

        self.gruvbox_theme = {
            "dark0_hard": (29, 32, 33, 255),
            "dark0": (40, 40, 40, 255),
            "dark0_soft": (50, 48, 47, 255),
            "dark1": (60, 56, 54, 255),
            "dark2": (80, 73, 69, 255),
            "dark3": (102, 92, 84, 255),
            "dark4": (124, 111, 100, 255),
            "dark4_256": (124, 111, 100, 255),
            "gray_245": (146, 131, 116, 255),
            "gray_244": (146, 131, 116, 255),
            "light0_hard": (249, 245, 215, 255),
            "light0": (253, 244, 193, 255),
            "light0_soft": (242, 229, 188, 255),
            "light1": (235, 219, 178, 255),
            "light2": (213, 196, 161, 255),
            "light3": (189, 174, 147, 255),
            "light4": (168, 153, 132, 255),
            "light4_256": (168, 153, 132, 255),
            "bright_red": (251, 73, 52, 255),
            "bright_green": (184, 187, 38, 255),
            "bright_yellow": (250, 189, 47, 255),
            "bright_blue": (131, 165, 152, 255),
            "bright_purple": (211, 134, 155, 255),
            "bright_aqua": (142, 192, 124, 255),
            "bright_orange": (254, 128, 25, 255),
            "neutral_red": (204, 36, 29, 255),
            "neutral_green": (152, 151, 26, 255),
            "neutral_yellow": (215, 153, 33, 255),
            "neutral_blue": (69, 133, 136, 255),
            "neutral_purple": (177, 98, 134, 255),
            "neutral_aqua": (104, 157, 106, 255),
            "neutral_orange": (214, 93, 14, 255),
            "faded_red": (157, 0, 6, 255),
            "faded_green": (121, 116, 14, 255),
            "faded_yellow": (181, 118, 20, 255),
            "faded_blue": (7, 102, 120, 255),
            "faded_purple": (143, 63, 113, 255),
            "faded_aqua": (66, 123, 88, 255),
            "faded_orange": (175, 58, 3, 255),
            "background": (29, 32, 33, 255),  # Background color
            "text": (235, 219, 178, 255),  # Foreground text color
            "primary": (80, 120, 100, 255),  # Primary color
            "secondary": (214, 93, 14, 255),  # Secondary color
            "hover": (102, 92, 84, 255),  # Hover color
            "active": (175, 58, 3, 255),  # Active color
        }
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_WindowBg, self.gruvbox_theme["dark0_hard"]
                )
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.gruvbox_theme["text"])
                dpg.add_theme_color(
                    dpg.mvThemeCol_Button, self.gruvbox_theme["primary"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonHovered, self.gruvbox_theme["hover"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonActive, self.gruvbox_theme["active"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBg, self.gruvbox_theme["dark0_hard"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBgHovered, self.gruvbox_theme["hover"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBgActive, self.gruvbox_theme["active"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_TitleBg, self.gruvbox_theme["primary"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_TitleBgActive, self.gruvbox_theme["faded_aqua"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_CheckMark, self.gruvbox_theme["secondary"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_SliderGrab, self.gruvbox_theme["secondary"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_SliderGrabActive, self.gruvbox_theme["active"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ResizeGrip, self.gruvbox_theme["primary"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ResizeGripHovered, self.gruvbox_theme["hover"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ResizeGripActive, self.gruvbox_theme["active"]
                )
                dpg.add_theme_color(dpg.mvThemeCol_Tab, self.gruvbox_theme["primary"])
                dpg.add_theme_color(
                    dpg.mvThemeCol_TabHovered, self.gruvbox_theme["hover"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_TabActive, self.gruvbox_theme["active"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_Header, self.gruvbox_theme["primary"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderHovered, self.gruvbox_theme["hover"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderActive, self.gruvbox_theme["active"]
                )
            with dpg.theme_component(dpg.mvInputText):
                dpg.add_theme_color(
                    dpg.mvThemeCol_TextDisabled, self.gruvbox_theme["light0_soft"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBg, self.gruvbox_theme["faded_green"]
                )
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, 5)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, 5)

            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(
                    dpg.mvThemeCol_Button, self.gruvbox_theme["primary"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonHovered, self.gruvbox_theme["hover"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonActive, self.gruvbox_theme["active"]
                )
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.gruvbox_theme["text"])
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 5.0
                )  # Corner rounding value
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 10, 10)

        with dpg.theme(tag="sign_in_theme"):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(
                    dpg.mvThemeCol_Button, self.gruvbox_theme["neutral_green"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonHovered, self.gruvbox_theme["faded_green"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonActive, self.gruvbox_theme["dark0_soft"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_Text, self.gruvbox_theme["light0_hard"]
                )

        with dpg.theme(tag="exit_btn_theme") as self.exit_btn_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(
                    dpg.mvThemeCol_Text, self.gruvbox_theme["light0_hard"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_Button, self.gruvbox_theme["neutral_orange"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonHovered, self.gruvbox_theme["faded_orange"]
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonActive, self.gruvbox_theme["dark0_soft"]
                )

        dpg.bind_theme(global_theme)

        dpg.add_colormap_registry(label="Colormap Registry", tag="colormap_registry")

        with dpg.font_registry():
            self.extrabold_font40 = dpg.add_font(
                file="./Inter-4.0/extras/ttf/InterDisplay-ExtraBold.ttf",
                size=40,
                tag="extrabold_font40",
            )
            self.bold_font30 = dpg.add_font(
                file="./Inter-4.0/extras/ttf/Inter-Bold.ttf", size=30, tag="bold_font30"
            )
            self.bold_font25 = dpg.add_font(
                file="./Inter-4.0/extras/ttf/Inter-Bold.ttf", size=25, tag="bold_font25"
            )
            self.bold_font20 = dpg.add_font(
                file="./Inter-4.0/extras/ttf/Inter-Bold.ttf", size=20, tag="bold_font20"
            )
            self.bold_font15 = dpg.add_font(
                file="./Inter-4.0/extras/ttf/Inter-Bold.ttf", size=15, tag="bold_font15"
            )
            self.regular_font17 = dpg.add_font(
                file="./Inter-4.0/extras/ttf/Inter-Regular.ttf",
                size=17,
                tag="regular_font17",
            )
            self.regular_font20 = dpg.add_font(
                file="./Inter-4.0/extras/ttf/Inter-Regular.ttf",
                size=20,
                tag="regular_font20 ",
            )
            self.semibold_font20 = dpg.add_font(
                file="./Inter-4.0/extras/ttf/Inter-SemiBold.ttf",
                size=20,
                tag="semibold_font20 ",
            )
            dpg.add_font(
                file="./Inter-4.0/extras/ttf/Inter-Medium.ttf",
                size=17,
                tag="medium_font17",
            )
            dpg.bind_font("medium_font17")

        self.cntrlDataCubes = ControlDataCubes()

        self.cntrlDataCubes.restoreInfo()

        with dpg.window(
            label="Main Menu",
            no_resize=True,
            id="main_menu",
            min_size=[800, 1000],
            on_close=lambda: self.exit(),
        ):
            dpg.add_spacer(height=200)
            with dpg.group(horizontal=True):
                with dpg.group():
                    dpg.add_spacer(width=200)
                with dpg.group():
                    dpg.add_text("InterVisor")
                    dpg.bind_item_font(dpg.last_item(), "extrabold_font40")
                    dpg.add_button(
                        label="Open a new file",
                        tag="open_new_btn",
                        callback=lambda: FilePickr(self.cntrlDataCubes),
                    )
                    dpg.add_button(
                        label="Recent files",
                        tag="open_recent_btn",
                        callback=lambda: OpenRecent(self.cntrlDataCubes),
                    )
                    dpg.add_button(
                        label="Select Redshift Catalog",
                        tag="select_redshift_btn",
                        callback=lambda: SetRedshiftCatalog(self.cntrlDataCubes),
                    )
                    dpg.add_button(
                        label="Exit", tag="exit_btn", callback=lambda: self.exit()
                    )
                    dpg.bind_item_theme("exit_btn", "exit_btn_theme")
                    dpg.add_text("",tag="redshift_catalog_label")

                    if self.cntrlDataCubes.redshift_catalog == None:
                        dpg.configure_item("open_new_btn", show=False)
                        dpg.configure_item("open_recent_btn", show=False)
                    else:
                        dpg.configure_item("open_new_btn", show=True)
                        dpg.configure_item("open_recent_btn", show=True)
                        dpg.set_value("redshift_catalog_label",
                            f"Redshift catalog: {os.path.basename(self.cntrlDataCubes.redshift_catalog)}"
                        )

        dpg.set_primary_window("main_menu", True)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.toggle_viewport_fullscreen()
        dpg.maximize_viewport()
        dpg.start_dearpygui()

        dpg.destroy_context()

    def exit(self):
        self.cntrlDataCubes.storeInfo()
        dpg.stop_dearpygui()
