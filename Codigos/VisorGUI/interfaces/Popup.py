import dearpygui.dearpygui as dpg

class Popup:
    def __init__(self, text):
        with dpg.window(
            label="Popup",
            tag="popup_id",
            no_title_bar=True,
            no_resize=True,pos=[500,500]
        ):
            dpg.add_separator()
            dpg.add_text(text)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="OK",
                    width=75,
                    callback=lambda: dpg.delete_item("popup_id"),
                )
