import dearpygui.dearpygui as dpg
import matplotlib.pyplot as plt
from Logic.ExportPlot import save_item
from math import log

class ExtractPhoto():
  def __init__(self,cube):
    self.datacube = cube
    self.flux_data = self.datacube.getFluxData() 
    
    self.min_wavelength = self.datacube.getData("WAVE")[0]
    
    heat_data = []
    for i in self.flux_data[0,:,:].tolist():
      heat_data = heat_data+i

  
    with dpg.window(label=self.datacube.plate_ifu+" Photo",
                  tag="photo"+self.datacube.plate_ifu,
                  min_size=[500,600],
                  pos=(300,300),
                  no_resize=True,
                  on_close=self.close):
      dpg.add_text("Enter the wave length to analyze: ")
      dpg.add_input_int(tag="wavelength_inp",
                        default_value=self.min_wavelength,label="Wavelength",
                        max_clamped=True,
                        min_clamped=True,
                        step=1,
                        step_fast=100,
                        min_value=self.min_wavelength,
                        callback=self.reGenHeatMap,
                        max_value=self.datacube.shape[0]-1+self.min_wavelength)
      with dpg.group():
        dpg.add_radio_button(("none","log10", "log2"),tag="options_extract", callback=self.reGenHeatMap, horizontal=True)   
      with dpg.group(horizontal=True):
        dpg.add_colormap_scale(tag="colormap_scale",
                               height=400,
                               max_scale=max(heat_data),
                               min_scale=min(heat_data))
        dpg.bind_colormap(dpg.last_item(),
                          dpg.mvPlotColormap_Spectral)
        
        with dpg.plot(label="HeatPlot",
                      width=400,
                      height=400,tag="heat_plot"):
          dpg.bind_colormap(dpg.last_item(),
                            dpg.mvPlotColormap_Spectral)
          dpg.add_plot_axis(dpg.mvXAxis, 
                            label="x")
          with dpg.plot_axis(dpg.mvYAxis, 
                            label="y"):
            dpg.add_heat_series(label="Image", 
                                tag="heat_data",
                                x=heat_data, 
                                cols=self.datacube.shape[1], 
                                rows=self.datacube.shape[2],
                                format='',
                                scale_max=max(heat_data),
                                scale_min=min(heat_data))

  def close(self):
    dpg.delete_item("photo"+self.datacube.plate_ifu)
    dpg.delete_item("texture_tag"+self.datacube.plate_ifu)
    
  def reGenHeatMap(self):  
    heat_data = []
    for i in self.flux_data[int(dpg.get_value("wavelength_inp")-self.min_wavelength),:,:].tolist():
      heat_data = heat_data+self.applyFunction(i)
    dpg.configure_item("heat_data",x=heat_data,scale_max=max(heat_data),scale_min=min(heat_data))
    dpg.configure_item("colormap_scale",max_scale=max(heat_data),min_scale=min(heat_data))
    #fig=plt.figure()
    #bx=fig.add_subplot(111) 
    #cx = bx.imshow(self.datacube.getFluxData()[dpg.get_value("wavelength_inp")-self.datacube.getData("WAVE")[0],:,:])
    #plt.savefig("img.png",bbox_inches="tight")
    #width, height, channels, data = dpg.load_image("img.png")
    #dpg.configure_item("texture_tag"+self.datacube.plate_ifu,width=width, height=height, default_value=data)
    
  def applyFunction(self,array):
    if dpg.get_value("options_extract")=="log10":
      l = [log(x ,10) if x>0 else 0 for x in array]
    elif dpg.get_value("options_extract")=="log2":
      l = [log(x ,2) if x>0 else 0 for x in array]
    else:
      l = array
    return l
      
      