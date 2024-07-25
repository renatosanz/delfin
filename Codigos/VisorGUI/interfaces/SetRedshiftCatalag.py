import dearpygui.dearpygui as dpg
from interfaces.Popup import Popup
import os


class SetRedshiftCatalog:
    def __init__(self, admDataCubes) -> None:
        self.admDataCubes = admDataCubes
        with dpg.file_dialog(
            directory_selector=False,
            callback=self.getCallBack,
            width=500,
            height=400,
            label="Redshift Catalog",
            id="redshift_Catalog_win",
            modal=True,
            cancel_callback=lambda: dpg.delete_item("redshift_Catalog_win"),
        ):
            dpg.add_file_extension(".gz", color=(237, 81, 193, 255), custom_text="[gz]")
            dpg.add_file_extension(
                ".fits", color=(237, 81, 193, 255), custom_text="[.fits]"
            )

    def getCallBack(self, sender, app_data, user_data):
        self.admDataCubes.set_redshift_catalog(app_data["file_path_name"])
        Popup(
            f"Redshift Catalog Loaded!\n{os.path.basename(self.admDataCubes.redshift_catalog)}"
        )
        dpg.delete_item("redshift_Catalog_win")
        if self.admDataCubes.redshift_catalog == None:
            dpg.configure_item("open_new_btn", show=False)
            dpg.configure_item("open_recent_btn", show=False)
        else:
            dpg.configure_item("open_new_btn", show=True)
            dpg.configure_item("open_recent_btn", show=True)
            dpg.set_value(
                "redshift_catalog_label",
                 f"Redshift catalog: {os.path.basename(self.admDataCubes.redshift_catalog)}",
            )
