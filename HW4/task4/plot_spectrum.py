# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt

x = np.genfromtxt("be_spectrum_x.dat")
y = np.genfromtxt("be_spectrum_y.dat")
z = np.genfromtxt("be_spectrum_z.dat")

avg = (x[:,1]+y[:,2]+z[:,3])/3

plt.plot(x[:,0],avg)


fig = plt.figure(figsize = (8,5))
ax = fig.add_subplot(1, 1, 1)
ax.plot(x[:,0],avg, label ='photoabsorption spectrum')   
ax.set_xlim([0, 6.5])
#ax.grid(True)
ax.set_xlabel("Energy [eV]")
ax.set_ylabel("Absorption")

