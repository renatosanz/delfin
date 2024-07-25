import dearpygui.dearpygui as dpg
from interfaces.Modes import Modes


class DirPickr:
    def __init__(self, admDataCubes) -> None:
        self.admDataCubes = admDataCubes
        dpg.add_file_dialog(
            callback=self.getCallBack,
            width=500,
            height=400,
            label="DirPicker",
            id="dir_picker",
            modal=True,
            cancel_callback=lambda: dpg.delete_item("dir_picker"),
        )

    def getCallBack(self, sender, app_data, user_data):
        newCube = self.admDataCubes.createDataCube(app_data["file_path_name"])
        if not dpg.does_item_exist("modes" + newCube.plate_ifu):
            try:
                self.modesWindow = Modes(newCube)
            except:
                dpg.delete_item(dpg.last_item())
            dpg.delete_item("dir_picker")
