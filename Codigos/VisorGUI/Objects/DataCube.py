from astropy.io import fits
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

class DataCube:
  def __init__(self, filename,reshift_filepath):
    print("creating : "+filename)
    self.filename = filename 
    self.reshift_catalog = reshift_filepath
    self.shape =self.getFluxData().shape
    self.plate_ifu = str(self.getHeaderInfo("FLUX","PLATEIFU"))
    self.telescop = str(self.getHeaderInfo("FLUX","TELESCOP"))
    self.author = str(self.getHeaderInfo("FLUX","AUTHOR"))
    self.date_obs = str(self.getHeaderInfo("FLUX","DATE-OBS"))
    self.redshift = self.getRedshift()
    
        
  def getFluxData(self):
    hdul = fits.open(self.filename)
    flux_data = hdul["FLUX"].data
    hdul.close()
    return flux_data
    
  def getWaveData(self):
    hdul = fits.open(self.filename)
    wave_data = hdul["Wave"].data
    hdul.close()
    return wave_data
  
  def getData(self,extname):
    hdul = fits.open(self.filename)
    try:
      value = hdul[extname].data
      hdul.close()
      return value
    except:
      hdul.close()
      return None
    
  def getHeaderInfo(self,extname,key):
    hdul = fits.open(self.filename)
    try:
      value = hdul[extname].header[key]
      hdul.close()  
      return value
    except:
      hdul.close()
      return None
    
  def getHeader(self):
    hdul = fits.open(self.filename)
    h = hdul["FLUX"].header
    return h
    
  def getRedshift(self):
    hdul_catalog = fits.open(self.reshift_catalog) #path al catalogo de redshift
    data_catalog = hdul_catalog[1].data
    ix = np.where(data_catalog["PLATEIFU"]==self.plate_ifu)
    return data_catalog["nsa_z"][ix][0]
