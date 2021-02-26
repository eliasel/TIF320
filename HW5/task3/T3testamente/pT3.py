
import numpy as np
import matplotlib.pyplot as plt


for i in range(9):
  data = np.genfromtxt('vib_spec_'+str(i+1)+'.txt', dtype = complex, delimiter =',', skip_header = 1)

  fig = plt.figure(figsize = (8,5))
  ax = fig.add_subplot(1, 1, 1)
  ax.plot(data[:,0],data[:,1])
  #ax.grid(True)
  ax.set_xlabel("Frequency [cm^-1]")
  ax.set_ylabel("Energy [eV]")
  #print(data)
  fig.savefig('spec_'+str(i+1)+'.png')
