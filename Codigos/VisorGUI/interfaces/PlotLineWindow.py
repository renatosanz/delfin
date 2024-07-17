import dearpygui.dearpygui as dpg
import numpy as np
import math

class PlotLineWindow():
  def __init__(self,cube) -> None:  

    self.datacube = cube
    
    self.spaxel_j = 0
    self.spaxel_i = 0
    
    self.wavedata = self.datacube.getData("WAVE")
    
    self.wavelength_min = int(self.wavedata[0])
    self.wavelength_max = int(self.wavedata[-1])
    
    with dpg.window(label="Spectrum "+self.datacube.plate_ifu,
                    tag=self.datacube.plate_ifu+"spectrum_win",
                    no_collapse=True,
                    min_size=[600,800],
                    pos=[0,0],on_close=self.close):
      dpg.add_text("Enter the spaxel coordenates:")
      with dpg.group():      
        dpg.add_input_int(label="i",
                          tag="spaxel_i",
                          width=200,
                          max_clamped=True,
                          min_clamped=True,
                          max_value=1,
                          min_value=0,
                          callback=lambda:self.updateCubeSpectrum())
        dpg.add_input_int(label="j",
                          tag="spaxel_j",
                          width=200,
                          max_clamped=True,
                          min_clamped=True,
                          max_value=1,
                          min_value=0,
                          callback=lambda:self.updateCubeSpectrum())
        dpg.add_input_int(label="min wavelength",
                          tag="min_wavelength_inp",
                          width=200,
                          max_clamped=True,
                          min_clamped=True,
                          max_value=self.wavelength_max,
                          min_value=self.wavelength_min,
                          default_value=self.wavelength_min)
        dpg.add_input_int(label="max wavelength",
                          tag="max_wavelength_inp",
                          width=200,
                          max_clamped=True,
                          min_clamped=True,
                          max_value=self.wavelength_max,
                          min_value=self.wavelength_min,
                          default_value=self.wavelength_max)
      def query(sender, app_data, user_data):
        dpg.set_axis_limits("xaxis_tag2", app_data[0], app_data[1])
        dpg.set_axis_limits("yaxis_tag2", app_data[2], app_data[3])
        
      with dpg.group(horizontal=True):    
        dpg.add_button(label="Update Spectrum",callback=lambda:self.updateCubeSpectrum())
        dpg.add_button(label="fit y axis", callback=lambda: dpg.fit_axis_data("y_axis"))
        dpg.add_button(label="fit x axis", callback=lambda: dpg.fit_axis_data("x_axis")) 
        dpg.add_button(label="Back",callback=self.close) 
        dpg.bind_item_theme(dpg.last_item(),"exit_btn_theme")
        
      with dpg.plot(width=-1,label="",tag="espectrum",crosshairs=True,query=True,callback=query):
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis, label="Wavelength Å", tag="x_axis")
        dpg.add_plot_axis(dpg.mvYAxis, label=self.datacube.getHeaderInfo("FLUX","BUNIT"), tag="y_axis")
        dpg.add_line_series([],[],label="Flux Observed",parent="y_axis", tag="series_tag")
        dpg.add_line_series([],[],label="Rest Frame",parent="y_axis", tag="series_tag_redshift")
    # plot 2
      with dpg.plot(no_title=True, height=250,crosshairs=True, no_menus=True, width=-1):
        dpg.add_plot_axis(dpg.mvXAxis, label="Wavelength Å", tag="xaxis_tag2")
        dpg.add_plot_axis(dpg.mvYAxis, label=self.datacube.getHeaderInfo("FLUX","BUNIT"), tag="yaxis_tag2")
        dpg.add_line_series([], [],tag="series_tag_query", parent="yaxis_tag2")
        dpg.add_line_series([], [],tag="series_tag_query_redshift", parent="yaxis_tag2")
        
      
    dpg.set_value("spaxel_i",math.floor(self.datacube.shape[1]/2))
    dpg.set_value("spaxel_j",math.floor(self.datacube.shape[2]/2))
    
    dpg.configure_item("spaxel_i",max_value = self.datacube.shape[1]-1)
    dpg.configure_item("spaxel_j",max_value = self.datacube.shape[2]-1)
    
    self.flux_data = self.datacube.getFluxData()
    self.updateCubeSpectrum()
    
    dpg.fit_axis_data("y_axis")
    dpg.fit_axis_data("x_axis")
    
    dpg.fit_axis_data("xaxis_tag2")
    dpg.fit_axis_data("yaxis_tag2")
    

  def updateCubeSpectrum(self):    
    self.spaxel_i = dpg.get_value("spaxel_i")
    self.spaxel_j = dpg.get_value("spaxel_j")
    
    index_inf = dpg.get_value("min_wavelength_inp")-self.wavelength_min
    index_max = dpg.get_value("max_wavelength_inp")-self.wavelength_min
    
    if self.wavelength_min<=self.wavelength_max:
      spectrum_data = list(self.flux_data[index_inf:index_max,self.spaxel_i,self.spaxel_j])
      wavelength_data = list(self.wavedata)
      wavelength_data_redshift = list(self.wavedata/(1+self.datacube.redshift))
      dpg.set_value('series_tag',[wavelength_data,spectrum_data])
      dpg.set_value('series_tag_redshift',[wavelength_data_redshift,spectrum_data])
      dpg.set_value('series_tag_query',[wavelength_data,spectrum_data])
      dpg.set_value('series_tag_query_redshift',[wavelength_data_redshift,spectrum_data])
      
  def close(self):
    dpg.configure_item("espectrum",callback = None)
    dpg.delete_item(self.datacube.plate_ifu+"spectrum_win")