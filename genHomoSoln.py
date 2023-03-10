#!/bin/bash
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
# the Mittag-Leffler function package https://github.com/khinsen/mittag-leffler
from mittag_leffler import ml
# import the stochastic integral package
#import sdeint  #  https://pypi.org/project/sdeint/
import scipy.integrate as integrate
import scipy.io as sio
import sys
import healpy as hp
from colormap import cmbcmap
import math
#################################################
# usage :python3 genHomoSoln kt Lmax 
#        python3 genHomoSoln 1 600    : generate homogeneous soln at tau   
#
tau = 1e-5 
kappa1= 2.3
kappa2= 2.5
Lmax = 1500   # Truncated the exact series at large Degree L_tilde up to 1500

map_type = 'Homo_soln'
kt = int(sys.argv[1]) #  number from command line
Lmax = int(sys.argv[2]) # Lmax  from command line

#tt = 0.0
tt = kt*tau

def AA(L): # Angular power spectrum of the random noise W
      if (L>0):
         value = L**(-kappa2)
      else:
         value = 1.0
      return value
def CC(L): # Angular power spectrum of the random field
      if (L>0):
         value2 = L**(-kappa1)
      else:
         value2 = 1.0
      return value2
#
al = 0.5
total = 0.0
Nside = 2048
sig0 = 200 
# read in the coefficients of the initial random field
ld_dir = './'
# The initial random field was generated by ....
ld_alm = ld_dir + 'Rand4FracPDE_Frac_Nside2048_instance1' + '.mat'
mat_alm = sio.loadmat(ld_alm)
RF_LMAX = 2500
alm = np.reshape(mat_alm['alm'],[hp.Alm.getsize(RF_LMAX)])
Vlm = np.zeros( alm.shape, dtype=complex)
#np.random.seed(2022)
for Lm in range(0,Lmax+1):
   Vm = np.zeros((Lm+1))
   lam = Lm*(Lm+1)

   # get the coefficients from the random field
   Z_lm = np.zeros(Lm+1,dtype=complex)
   MLvalZ = ml(-lam*tt**al, al) 
   for m in range(0,Lm+1):
        idxlm  = hp.Alm.getidx(RF_LMAX,Lm,m)
        Z_lm[m]= alm[idxlm]
   
   bZ = MLvalZ.item()*Z_lm
   #print(Lm, bZ.shape, I0.shape, I1.shape, I2.shape)
   Vm = bZ
   for m in range(0,Lm+1):
        idxlm  = hp.Alm.getidx(RF_LMAX,Lm,m)
        Vlm[idxlm] = Vm[m]

randfield = hp.alm2map(alms=Vlm,nside=Nside)   
sv_fig = map_type + '_Lmax' + str(Lmax) + '_t_'+str(kt)+'tau_tau_1e-5.png'
plt.figure(1)
cm = cmbcmap()
#ti =r'Initial condition $u_L(0)$ ' + ', $L= %d$' %Lmax
#ti =r'Homogeneous solution $u_L(t)$ at $t=10\tau$, with ${\tau}=10^{-5}$ ' + ', $L= %d$' %Lmax
#ti =r'Homogeneous solution $u_H(t)$ at $t=%d\tau$, with ${\tau}=10^{-5}$ ' %kt + ', $L= %d$' %Lmax
ti = ''
#hp.mollview(randfield, title = ti, cmap=cm, min=-1, max=1, xsize=1200, nest=False)
hp.mollview(randfield, title=ti,cmap=cm, min=-5, max=5, xsize=1200, nest=False)
plt.title(ti)
plt.savefig(sv_fig,format='png',dpi=600)


