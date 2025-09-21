Finding the source of NaN values in GetPowerFlux arrays

## Python code which causes errore

```
def RCWA_spectrum(lbda,material,layer,pattern,u,v,phi,theta,polar,N_ord):
    
    import numpy as np
    import S4 as S4
    from Functions.get_anisotropic_permittivities import get_anisotropic_permittivities
    from Functions.get_permittivities import get_permittivities
    from Functions.get_sp_Amplitude_Phase import get_sp_Amplitude_Phase
                
    permittivity_xx,permittivity_yy,permittivity_zz=get_anisotropic_permittivities(lbda,material)   # Set the materials permitivitties                                   
    # permittivity=get_permittivities(lbda,material)   # Set the materials permitivitties                                   
    # permittivity_xx=permittivity
    # permittivity_yy=permittivity
    # permittivity_zz=permittivity
    
    A_p,A_s,phase_p,phase_s=get_sp_Amplitude_Phase(polar,phi) #  Set the polarization   

    A=np.zeros((lbda.size,1),dtype=float)
    R=np.zeros((lbda.size,1),dtype=float)
    T=np.zeros((lbda.size,1),dtype=float)
    
    for lb in range(0,lbda.size):
    
        S = S4.New(Lattice = ((u[0],u[1]), (v[0],v[1])), NumBasis = N_ord)
              
        # set the materials
        for m in range(0,len(material)): 
            # S.AddMaterial(Name ='Mat'+str(m+1), Epsilon = permittivity[lb,m])
            S.SetMaterial(Name ='Mat'+str(m+1), Epsilon = (
                                                          (permittivity_xx[lb,m], 0, 0),
                                                          (0, permittivity_yy[lb,m], 0),
                                                          (0, 0, permittivity_zz[lb,m])
                                                                                   ))
             
        # set the layers  
        for ly in range(0,len(layer)):
            S.AddLayer(Name ='Layer'+str(ly+1), Thickness = layer[ly][0], Material = 'Mat'+str(layer[ly][1])) 
            
        # set the pattern    
        if len(pattern)>0: # There is some pattern
            for p in range(0,len(pattern)):
                if pattern[p][2]==1: # grating
                      S.SetRegionRectangle(Layer='Layer'+str(pattern[p][0]),Material='Mat'+str(pattern[p][1]), Center=(pattern[p][3][0],pattern[p][3][1]), Angle=0, Halfwidths=(pattern[p][4][0]/2,pattern[p][4][0]/2))
                elif pattern[p][2]==2: # circular
                      S.SetRegionCircle(Layer='Layer'+str(pattern[p][0]),Material='Mat'+str(pattern[p][1]), Center=(pattern[p][3][0],pattern[p][3][1]), Halfwidths=pattern[p][4][0]/2)
                elif pattern[p][2]==3: # rectangular
                      S.SetRegionRectangle(Layer='Layer'+str(pattern[p][0]),Material='Mat'+str(pattern[p][1]), Center=(pattern[p][3][0],pattern[p][3][1]), Angle=pattern[p][5], Halfwidths=(pattern[p][4][0]/2,pattern[p][4][0]/2))
                elif pattern[p][2]==4: # ellipse
                      S.SetRegionEllipse(Layer='Layer'+str(pattern[p][0]),Material='Mat'+str(pattern[p][1]), Center=(pattern[p][3][0],pattern[p][3][1]), Angle=pattern[p][5], Halfwidths=(pattern[p][4][0]/2,pattern[p][4][0]/2))
                else:
                    print("PATTERN DEFINITION: invalid pattern form")
            
        freq=1/lbda[lb] 
          
        S.SetExcitationPlanewave(IncidenceAngles=(theta[lb],phi), sAmplitude=A_s*(np.exp(phase_s*1j)), pAmplitude=A_p*(np.exp(phase_p*1j)), Order=0) 
        
        S.SetFrequency(freq) 
        
        (forward,backward)=S.GetPowerFlux(Layer='Layer'+str(1),zOffset=-1)
        (transmitted,useless)=S.GetPowerFlux(Layer='Layer'+str(len(layer)),zOffset=1) 
    
        R[lb]=np.abs(-backward/forward)
        T[lb]=np.abs(transmitted/forward)
        A[lb]=1-R[lb]-T[lb]
        
    R=R.conj().transpose()
    T=T.conj().transpose()
    A=A.conj().transpose()
        
    return lbda,R,T,A
```

## Problem source

```
S.SetMaterial(Name ='Mat'+str(m+1), Epsilon = ( \
        (permittivity_xx[lb,m], 0, 0),\
        (0, permittivity_yy[lb,m], 0),\
        (0, 0, permittivity_zz[lb,m])\
    ))
```
Calling SetMaterial with a 3x3 permittivity tensor produces bad output.
Using a numpy complex 128 scalar does not.

## Python to C++ function calls 

### New
S4_New ->
S4Sim_New ->
{
Simulation_Init
,s
Simulation_MakeReciprocalLattice
,
Simulation_SetNumG
}


### SetMaterial
S4Sim_SetMaterial ->
Simulation_GetMaterialByName ->
{ if null,
Simulation_AddMaterial
,
MaterialInit OR MaterialInitTensor (epsdata.type)
}
Assign epsdata.eps to M->eps.s;
Assign epsdata.eps to M->eps.abcde;

### AddLayer
S4Sim_AddLayer ->
Simulation_AddLayer ->
Simulation_DestroySolution {free memory} ->
{malloc layer}
LayerInit

### SetRegionRectangle
S4Sim_SetRegionRectangle ->
{
Simulation_GetMaterialByName
,
Simulation_AddLayerPatternRectangle ->
{Simulation_DestroySolution, SimulationInvalidateFieldCache}
}

### SetExcitationPlanewave
S4Sim_ExcitationPlanewave ->
Simulation_MakeExcitationPlanewave ->
Simulation_DestroySolution ->
{takes scalar value or e of abcde -> root ->{}-> assigns to S->k[0&1]}


### SetFrequency
S4Sim_SetFrequency ->
Simulation_DestroySolution
{sets S.omega}

### GetPowerFlux
S4Sim_GetPowerFlux ->
Simulation_GetLayerByName ->
Simulation_GetPoyntingFLux ->
{
Simulation_GetLayerSolution -> 
{
Simulation_ComputeLayerSolution -> 
Simulation_ComputeLayerBands -> 
SolveLayerEigensystem ->

}
,
TranslateAmplitudes(RCWA.cpp)
,
GetZPoyntingFlux(RCWA.cpp) ->
{
MultKPMatrix(RCWA.cpp) -> MultiMM, MultiMV
,
RNP::TBLAS::CopyMatrix, MultiMM, ConjugateDot,
}
}

