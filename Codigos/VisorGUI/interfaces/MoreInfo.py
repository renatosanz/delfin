import dearpygui.dearpygui as dpg

class MoreInfo():
    def __init__(self,cube):
      self.datacube = cube
      with dpg.window(label=self.datacube.plate_ifu+" Info",
                    tag="info"+self.datacube.plate_ifu,
                    min_size=[500,300],
                    pos=(0,500),
                    no_resize=True,
                    on_close=lambda:dpg.delete_item("info"+self.datacube.plate_ifu)):
        h = self.datacube.getHeader()
        for key in h:
          dpg.add_text(key+" : "+str(h[key]))
        dpg.add_text("Shape: "+str(self.datacube.shape))