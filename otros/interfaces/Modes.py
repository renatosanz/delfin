import dearpygui.dearpygui as dpg
from interfaces.PlotLineWindow import PlotLineWindow
from interfaces.MoreInfo import MoreInfo
from interfaces.ExtractPhoto import ExtractPhoto
from interfaces.ExtractLineEmision import ExtractLineEmision

class Modes():
  def __init__(self,cube) -> None:
    self.datacube = cube
    self.plate_ifu = self.datacube.plate_ifu
    telescop = self.datacube.telescop
    author = self.datacube.author
    date_obs = self.datacube.date_obs
    
    with dpg.window(label="Modes "+self.plate_ifu,
                    id="modes"+self.plate_ifu,
                    min_size=[500,300],
                    pos=(0,500),
                    no_resize=True,
                    on_close=lambda:dpg.delete_item("modes"+self.plate_ifu)):
      dpg.add_text("GENERAL INFORMATION")
      dpg.bind_item_font(dpg.last_item(),"bold_font25")
      dpg.add_text("PLANE IFU: "+self.plate_ifu+"\n"
                  +"TELESCOP: "+telescop+"\n"
                  +"AUTHOR: "+author+"\n"
                  +"DATE-OBS: " +date_obs,
                  tag="title_modes_lbl")
      
      dpg.add_button(label="More Information",callback=self.showMoreInfo)
      dpg.add_button(label="Generate spectrum",callback=self.genSpectrum)
      dpg.add_button(label="Extract image",callback=self.showExtractPhoto)
      dpg.add_button(label="View Emision Lines",callback=self.showExtractLineEmision)
      
  def genSpectrum(self):
    if not dpg.does_item_exist(self.datacube.plate_ifu+"spectrum_win"):
      self.plotWin = PlotLineWindow(self.datacube)
    
  def showMoreInfo(self):
    if not dpg.does_item_exist("info"+self.datacube.plate_ifu):
      self.moreinfo = MoreInfo(self.datacube)
      
  def showExtractPhoto(self):
    if not dpg.does_item_exist("photo"+self.datacube.plate_ifu):
      self.extractPhoto = ExtractPhoto(self.datacube)
      
  def showExtractLineEmision(self):
    if not dpg.does_item_exist(self.datacube.plate_ifu+"LineEmision"):
      self.extractLineEmision = ExtractLineEmision(self.datacube)