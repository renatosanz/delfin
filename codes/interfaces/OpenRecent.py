import dearpygui.dearpygui as dpg
from interfaces.Modes import Modes
import os

class OpenRecent():
  def __init__(self,cntrl):
    self.cntrl = cntrl
    with dpg.window(label="Open Recent File",
                    modal=True,
                    min_size=[600,400],
                    pos=(300,300),no_resize=True,
                    tag="recents_files_win",no_title_bar=True):
      dpg.add_text("Recent Files")

      with dpg.table(scrollY=True,height=300):
        dpg.add_table_column(label="IFU ID")
        dpg.add_table_column(label="DATE")
        dpg.add_table_column(label="Options")
        
        for cube in self.cntrl.cubes:
          with dpg.table_row():
            with dpg.table_cell():
              dpg.add_text(cube.plate_ifu)
            with dpg.table_cell():
              dpg.add_text(cube.date_obs)
            with dpg.table_cell():
              dpg.add_spacer(height=1)
              dpg.add_button(label="Open",callback=self.getCallBack,user_data=cube)
              
      dpg.add_button(label="Back",callback=lambda:dpg.delete_item("recents_files_win"))
      dpg.bind_item_theme(dpg.last_item(),"exit_btn_theme")

  def getCallBack(self,sender, app_data, user_data):
    if not dpg.does_item_exist("modes"+user_data.plate_ifu):
      try:
        self.modesWindow = Modes(user_data)
      except:
        dpg.delete_item(dpg.last_item())
      dpg.delete_item("recents_files_win")