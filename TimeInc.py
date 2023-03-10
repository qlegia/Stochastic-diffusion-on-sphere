#!/bin/bash

import numpy as np
# the Mittag-Leffler function package https://github.com/khinsen/mittag-leffler
from mittag_leffler import ml
# import the stochastic integral package
#import sdeint  #  https://pypi.org/project/sdeint/
import scipy.integrate as integrate
import scipy.io as sio
import sys
import healpy as hp
#################################################
# usage :python3 TimeInc instance Lmax h
#        python3 TimeInc 1 1000 1e-5
#
tau = 1e-3 
kappa1= 2.3
kappa2= 2.5
Lmax = 1500   # Truncated the exact series at large Degree L_tilde up to 1500

instance = np.int(sys.argv[1]) # instance number from command line
Lmax = np.int(sys.argv[2]) # Lmax  from command line
h = np.float(sys.argv[3]) # h  from command line
print(Lmax,h)
tt = tau+h

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

# read in the coefficients of the initial random field
ld_dir = './'
# The initial random field was generated by ....
ld_alm = ld_dir + 'Rand4FracPDE_Frac_Nside2048_instance1' + '.mat'
mat_alm = sio.loadmat(ld_alm)
RF_LMAX = 2500
alm = np.reshape(mat_alm['alm'],[hp.Alm.getsize(RF_LMAX)])

#np.random.seed(2022)
for Lm in range(0,Lmax+1):
   Vm = np.zeros((Lm+1))
   lam = Lm*(Lm+1)

   def sigma(L):
      return integrate.quad(lambda u: (ml(-lam*(u)**al, al))**2, 0,tt-tau,epsabs=1e-10)
   if (tt>tau):
      I0 = np.random.normal(0, sigma(Lm)[0])
      I1 = np.random.normal(0, sigma(Lm)[0], size=Lm)
      I2 = np.random.normal(0, sigma(Lm)[0], size=Lm)
   else:
      I0 = 0.
      I1 = np.zeros(Lm)
      I2 = np.zeros(Lm)
 
   Vm[0] = np.sqrt(AA(Lm))*I0  # V_{Lm,0}
   Vm[1:] =  np.sqrt(2*AA(Lm))*(I1 + I2)
   # get the coefficients from the random field
   #Z_lm = np.zeros(Lm+1,dtype=complex)
   #MLvalZ = ml(-lam*tt**al, al) 
   #for m in range(0,Lm+1):
   #     idxlm  = hp.Alm.getidx(RF_LMAX,Lm,m)
   #     Z_lm[m]= alm[idxlm]
   #
   #Z_lm[0] = 0.5*Z_lm[0] # adjust the case m=0 before multiplying by 2 
   #bZ = CC(Lm)*MLvalZ.item()*2*np.real(Z_lm)
   #print(Lm, bZ.shape, I0.shape, I1.shape, I2.shape)
   #result2 = (bZ + Vm)-(bZ)
   result2 = Vm
   total = total + sum( (np.abs(result2))**2 )

L2_Errors = total
print(Lmax,L2_Errors)
sv = 'IncL2errors_Lmax'+str(Lmax)+'_Ltrun'+str(h)+'_instance' + str(instance) + '.mat'
sio.savemat(sv, mdict={'L2_errs':L2_Errors,'Lmax':Lmax,'instance':instance,'tt':tt,'al':al,'tau':tau}) 


