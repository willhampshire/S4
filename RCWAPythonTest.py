"""
Single-point test case for debugging solver value issues

This script should numerically produce
lbda=0.92 R=0.1494408578053402 T=0.6968687749374614 A=0.15369036725719842

"""

import numpy as np
import math
import S4 as S4

def RCWA_spectrum(lbda,phi,theta,polar,pattern):
    
    scalar_permittivity = (3.8 + 0.01j)**2
    silicon_permittivity = (1.46 + 0j)**2
    
    A_p,A_s,phase_p,phase_s=get_sp_Amplitude_Phase(polar,phi) #  Set the polarization

    p = 0.5
    S = S4.New(Lattice=((p,0),(0,0)),NumBasis=20)
    
  
    # S.AddMaterial(Name = "test", Epsilon = scalar_permittivity)
    
    S.SetMaterial(Name = "test", Epsilon = (
            (scalar_permittivity, 0, 0),
            (0, scalar_permittivity, 0),
            (0, 0, scalar_permittivity),
        ))
    S.SetMaterial(Name="silicon", Epsilon = ((1.46 + 0j)**2))
    S.SetMaterial(Name='air', Epsilon=((1+0j)**2))

    S.AddLayer(Name="Air", Thickness=0, Material="air")
    S.AddLayer(Name = "TestLayer", Thickness = 0.03, Material = "test")
    S.AddLayer(Name = "SiO2", Thickness = 2., Material = "silicon")

    # set the pattern
    if len(pattern)>0: # There is some pattern
        for p in range(0,len(pattern)):
            
            if pattern[p][2]==1: # grating
                    S.SetRegionRectangle(Layer="TestLayer", Material="test", Center=(pattern[p][3][0],pattern[p][3][1]), Angle=0, Halfwidths=(pattern[p][4][0]/2,pattern[p][4][0]/2))
            else:
                print("PATTERN DEFINITION: invalid pattern form")
        
    freq=1/lbda
    
    S.SetExcitationPlanewave(IncidenceAngles=(theta,phi), sAmplitude=A_s*(np.exp(phase_s*1j)), pAmplitude=A_p*(np.exp(phase_p*1j)), Order=0) 
    
    S.SetFrequency(freq)
    
    (forward,backward)=S.GetPowerFlux(Layer="TestLayer",zOffset=-1)
    (transmitted,useless)=S.GetPowerFlux(Layer="SiO2",zOffset=1)
    
    print(f"{forward=}\n{backward=}\n{transmitted=}")

    import time
    time.sleep(1)
    R=np.abs(-backward/forward)
    T=np.abs(transmitted/forward)
    A=1-R-T
        
    return lbda,R,T,A


def get_sp_Amplitude_Phase(polar,phi):
            
    # Excitation polarization x
    A_s_H=math.sin(phi*math.pi/180)
    A_p_H=math.cos(phi*math.pi/180)
    phase_s_H=180
    phase_p_H=0
    # Excitation polarization y
    A_s_V=math.cos(phi*math.pi/180)
    A_p_V=math.sin(phi*math.pi/180)
    phase_s_V=0
    phase_p_V=0
    # Excitation polarization 45°
    A_s_D=math.sin(math.pi/4 - phi*math.pi/180)
    A_p_D=math.sin(math.pi/4 + phi*math.pi/180)
    phase_s_D=0
    phase_p_D=0
    # Excitation polarization -45°
    A_s_A=math.sin(math.pi/4 + phi*math.pi/180)
    A_p_A=math.sin(math.pi/4 - phi*math.pi/180)
    phase_s_A=180
    phase_p_A=0
    # Excitation polarization L
    A_s_L=1/math.sqrt(2)
    A_p_L=1/math.sqrt(2)
    phase_s_L=90+phi
    phase_p_L=phi
    # Excitation polarization R			
    A_s_R=1/math.sqrt(2)
    A_p_R=1/math.sqrt(2)
    phase_s_R=270-phi
    phase_p_R=-phi
           
    if (polar>0):  # Single polarization
        if (polar==1): # polar x
            A_s=A_s_H
            A_p=A_p_H
            phase_s=phase_s_H
            phase_p=phase_p_H
        elif (polar==2): # polar y		
            A_s=A_s_V
            A_p=A_p_V
            phase_s=phase_s_V
            phase_p=phase_p_V
        elif (polar==3): # polar L
            A_s=A_s_L
            A_p=A_p_L
            phase_s=phase_s_L
            phase_p=phase_p_L
        elif (polar==4): # polar R
            A_s=A_s_R
            A_p=A_p_R
            phase_s=phase_s_R
            phase_p=phase_p_R
        elif (polar==5): # polar s
            A_s=1
            A_p=0
            phase_s=0
            phase_p=0
        elif (polar==6): # polar p
            A_s=0
            A_p=1
            phase_s=0
            phase_p=0
        elif (polar==7): # polar 45°
            A_s=A_s_D
            A_p=A_p_D
            phase_s=phase_s_D
            phase_p=phase_p_D
        elif (polar==8): # polar -45°
            A_s=A_s_A
            A_p=A_p_A
            phase_s=phase_s_A
            phase_p=phase_p_A
        else:
            print("invalid polarization")
        phase_s=phase_s*(np.pi/180)
        phase_p=phase_p*(np.pi/180)    
 
    return A_p,A_s,phase_p,phase_s


def argument_angle(kx,ky,k_inplan):
#UNTITLED2 Summary of this function goes here
# phi: value of the angle in degrees, comprise in the range [0;360[ degrees
# cos_phi: cosinus of the angle 
# sin_phi: sinus of the angle 

    if k_inplan==0:     
        phi=0    
    else:
        cos_phi=kx/k_inplan
        sin_phi=ky/k_inplan
        
        if abs(cos_phi**2+sin_phi**2-1)>10**-3:
            phi=555 
            print('error')
        else: 
            if sin_phi >= 0 :    
                phi=np.arccos(cos_phi)
                phi=np.degrees(phi)
            else:
                phi=np.arccos(cos_phi)
                phi=360-np.degrees(phi)
           
    return phi



kx, ky = (0., 0.)
wavelength = 0.92 #um?

# periods = [0.25]
# thicknesses = [0.03]
# filling = [0.7]
# gamma 0.36
# gives:
pattern = [[2, 1, 1, [0.037500000000000006, 0], [0.07500000000000001, 0], 0], 
           [2, 1, 1, [0.37749999999999995, 0], [0.07500000000000001, 0], 0]] 


k_inplan = math.sqrt(kx ** 2 + ky ** 2)
## Conic angle (in degrees)
phi = argument_angle(kx, ky, k_inplan)
## Incident angles (in degrees)
theta = np.arcsin(k_inplan / 2 / 3.14159 * wavelength)
theta = np.degrees(theta)

print(phi, theta)

lbda,R,T,A = RCWA_spectrum(lbda=wavelength, phi=phi, theta=theta, polar=2, pattern=pattern)

print(f"{lbda=} {R=} {T=} {A=}")