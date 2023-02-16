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
#################################################
# usage :python3 genSoln instance Lmax 
#        python3 genSoln 1 1000 
#
tau = 1e-5 
kappa1= 2.3
kappa2= 2.5
Lmax = 1500   # Truncated the exact series at large Degree L_tilde up to 1500

map_type = 'Inhom_soln'
inst_num = int(sys.argv[1]) # instance number from command line
Lmax = int(sys.argv[2]) # Lmax  from command line

tt = 10*tau
#tt = 0.0
#tt = tau

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
sig0 = 1e2 
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
   Vm = np.zeros((Lm+1),dtype=complex)
   lam = Lm*(Lm+1)

   def sigma(L):
      return integrate.quad(lambda u: (ml(-lam*(u)**al, al))**2, 0,tt-tau,epsabs=1e-10)
   if (tt>tau):
      scale = np.sqrt(sigma(Lm)[0]) 
      I0 = np.random.normal(0, scale)
      I1 = np.random.normal(0, scale, size=Lm)
      I2 = np.random.normal(0, scale, size=Lm)
   else:
      I0 = 0.
      I1 = np.zeros(Lm)
      I2 = np.zeros(Lm)
 
   Vm[0] = sig0*np.sqrt(AA(Lm))*I0  # V_{Lm,0}
   Vm[1:] = sig0*np.sqrt(AA(Lm)/2)*(I1 - complex(0,1)*I2)
   # get the coefficients from the random field
   Z_lm = np.zeros(Lm+1,dtype=complex)
   MLvalZ = ml(-lam*tt**al, al) 
   for m in range(0,Lm+1):
        idxlm  = hp.Alm.getidx(RF_LMAX,Lm,m)
        Z_lm[m]= alm[idxlm]
   
   bZ = MLvalZ.item()*Z_lm
   #print(Lm, bZ.shape, I0.shape, I1.shape, I2.shape)
   #Vm = bZ + Vm
   #Vm = bZ
   for m in range(0,Lm+1):
        idxlm  = hp.Alm.getidx(RF_LMAX,Lm,m)
        Vlm[idxlm] = Vm[m]

randfield = hp.alm2map(alms=Vlm,nside=Nside)   
print('min/max val=',min(randfield), max(randfield))
sv_fig = map_type + '_Lmax' + str(Lmax) + '_t_1e_5_instance' + str(inst_num) + '.png'
plt.figure(1)
cm = cmbcmap()
#ti =r'Initial condition $u_L(0)$ ' + ', $L= %d$' %Lmax
ti =r'Inhomogeneous solution $u_L(t)$ at $t=10\tau$, with ${\tau}=10^{-5}$ ' + ', $L= %d$' %Lmax
#ti =r'Homogeneous solution $u_H(t)$ at $t=10{\tau}$, with ${\tau}=10^{-5}$ ' + ', $L= %d$' %Lmax
hp.mollview(randfield, title = ti, cmap=cm, min=-2.5, max=2.5, xsize=1200, nest=False)
plt.title(ti)
plt.savefig(sv_fig,format='png',dpi=600)


