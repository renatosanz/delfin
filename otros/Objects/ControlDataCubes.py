from Objects.DataCube import DataCube
import os,pickle

class ControlDataCubes():
  def __init__(self) -> None:
    self.cubes = []
    self.backupFile = 'data.pickle'
    
  def createDataCube(self,path_file):
    for i in self.cubes:
      if i.filename == path_file:
        return i
    new_cube = DataCube(path_file)
    self.cubes.append(new_cube)
    return new_cube
    
  def restoreInfo(self):
    if os.path.isfile(self.backupFile):
      with open(self.backupFile, 'rb') as file:
        self.cubes = pickle.load(file)

  def storeInfo(self):
    with open(self.backupFile, 'wb') as file:
      pickle.dump(self.cubes, file)
      
  def getDatCubeByPlateIFU(self,plateIFU):
    for i in self.cubes:
      if i.plate_ifu == plateIFU:
        return i
    return None