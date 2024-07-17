from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
fits_file = '../manga-7495-6102-LINCUBE.fits.gz'
#ruta del archivo .fits
hdul = fits.open(fits_file) #abre el archivo .fits
flux = hdul["FLUX"].data #lee los datos de flujo
print(flux.shape) #dimensiones del cubo de datos
#(espectral x espacial x espacial)
#el nmero de espectros es (6732, 54, 54)

flg=plt.figure()
ax = flg.add_subplot(111)
ax.plot(flux[:,27,27])
ax.set_ymargin(0.1)
#ax.set_xlim(self.datacube.getData("WAVE")[0])
ax.xaxis.set_major_formatter(ticker.FuncFormatter(
        lambda x, pos: '{}{}'.format('', str(int(x)+self.datacube.getData("WAVE")[0]))))
ax.set_xlabel("Longitud de onda Å")
ax.set_ylabel("Flujo [10-17 erg/cm2/s/Å]")
ax.set_title("Galaxia: manga-7495-6102 \nSpaxel: 27,27") 

#extrayendo un corte del cubo en la longitud de onda 900 a través de toda la imagen y aplicando log10 - devuelve una imagen  
fig=plt.figure()
bx=fig.add_subplot(111) 
cx = bx.imshow(np.log10(flux[900,:,:]))

plt.show() #muestra los gráficos
