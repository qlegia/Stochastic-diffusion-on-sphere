The directory contains Python files used to generate computer simulations in the paper 

"On approximation for time-fractional stochastic diffusion equations on the unit sphere"

by Tareq Alodat, Quoc Thong Le Gia (qlegia@unsw.edu.au) and Ian H. Sloan (UNSW, Sydney, Australia)

Feb-2023

The Python files are:

ErrorsLtr_wRF_v2.py
  compute the expected errors of the truncated solutions of a realisation of the truncated solution
  using formulae (8.1) and (8.2) in the paper.
  E.g.
     python3 ErrorsLtr_wRF_v2 1 1000 100 
  computes the square L2 errors of U_{100} with Lmax=1000 for the instance 1 of the numerical solution.
  The associated PBS scripts are
     frL200.pbs  frL300.pbs  frL400.pbs  frL500.pbs  frL600.pbs  frL700.pbs  frL800.pbs
  which generate square L2 errors for different values of truncated degree L=200; 300; 400; 500; 600; 700; 800
  Each pbs script generates 100 sample of square L2 errors on parallel CPUs.
 
genHomoSoln.py
  generate the homogeneous truncated solution at time k*tau with given tau.
  e.g. python genHomoSoln.py 10 600
  computes a homogeneous truncated solution U_{600} at time t = 10*tau
 
genInhomoSoln.py
  generate inhomogeneous truncated random solution. 
   
genSoln.py
  generate full solution which is a sum of homogeneous and inhomogenous solution
  e.g. python genSoln.py 1 600     generates U_L with L=600 at tau
       python genSoln.py 10 600    generates U_L with L=600 at 10tau

genU0.py
  generate the initial condition

genSoln_v2.py
  generate the full solution which is a sum of homogeneous and inhomogenous solution.
  Here the inhomogeneous solution is generated as the same time as the full solution.

TimeInc.py
  Simulations of temporal increments U_L(x,t+h) - U_L(x,t) 
  The associated PBS scripts are
  frh1e_4.pbs  frh1e_5.pbs  frh2e_5.pbs  frh3e_5.pbs  frh4e_5.pbs  frh5e_5.pbs  frh6e_5.pbs  
  frh7e_5.pbs  frh8e_5.pbs  frh9e_5.pbs
  
  which computes the square temporal increments ||U_L(x,t+h)-U_L(x,t)||^2 for h=1e-5, 2e-5, ...,10e-5.
