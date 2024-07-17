import dearpygui.dearpygui as dpg
from interfaces.Modes import Modes

class FilePickr():
  def __init__(self,admDataCubes) -> None:
    self.admDataCubes = admDataCubes 
    with dpg.file_dialog(directory_selector=False,
                         callback=self.getCallBack,
                         width=500,
                         height=400,
                         label="FilePicker",
                         id="file_picker",
                         modal=True,
                         cancel_callback=lambda:dpg.delete_item("file_picker")):
      dpg.add_file_extension(".gz", 
                             color=(237, 81, 193, 255), 
                             custom_text="[GZ]")
    
  def getCallBack(self,sender, app_data, user_data):
    newCube = self.admDataCubes.createDataCube(app_data["file_path_name"])
    if not dpg.does_item_exist("modes"+newCube.plate_ifu):
      try:
        self.modesWindow = Modes(newCube)
      except:
        dpg.delete_item(dpg.last_item())
      dpg.delete_item("file_picker")