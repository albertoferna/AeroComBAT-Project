# =============================================================================
# HEPHAESTUS VALIDATION 8 - BEAM DISPLACEMENTS AND ROTATIONS SIMPLE AL BOX BEAM
# =============================================================================

# IMPORTS:
import numpy as np
from Structures import MaterialLib
from AircraftParts import Wing

# Define the width of the cross-section
x1 = -0.8990566037735849
x2 = 0.8990566037735849
c = 1.
ctip = c
croot = c
L = 20.
Y_rib = np.linspace(0.,L,2)
b_s = np.linalg.norm((Y_rib[0],Y_rib[-1]))

matLib = MaterialLib()
matLib.addMat(1,'AL','iso',[71.7e9,.33,2810],.005)
matLib.addMat(2,'Weak_mat','iso',[100,.33,10],.005)

n_ply = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
m_i = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

noe_dens = 2
wing1 = Wing(b_s,croot,ctip,x1,x2,Y_rib,n_ply,m_i,matLib,name='box',noe_per_unit_length=noe_dens)
sbeam1 = wing1.wingSects[0].SuperBeams[0]

# Apply the constraint for the model
wing1.addConstraint(0,'fix')

# CASE 1:
# Apply the case load
tipLoad = np.array([-10000.,100000.,-300000.,35000.,60000.,10000.])
F = {40:tipLoad}
wing1.applyLoads(F=F)
# Run the analysis
wing1.staticAnalysis()
wing1.plotDeformedWing(figName='V8 Case 1',numXSects=10,contLim=[0.,5.0e8],\
    warpScale=100,displScale=10,contour='MaxPrin')
# Write the beam displacements and rotations to a file
sbeam1.writeDisplacements(fileName = 'V8_Case_1.csv')

# CASE 2:
# Apply the case load
def f(x):
    vx = -0.1*(-1.0e3*x[2]**2+6e7*x[2]+1.0e6)
    vy = (-1.0e3*x[2]**2+6e7*x[2]+1.0e6)
    pz = 0
    tz = .2*c*(-1.0e3*x[2]**2+6e7*x[2]+1.0e6)
    return np.array([vx,vy,pz,tz])/1.0e4
wing1.applyLoads(f=f,allElems=True)
# Run the analysis
wing1.staticAnalysis(resetPointLoads=True)
wing1.plotDeformedWing(figName='V8 Case 2',numXSects=10,contLim=[0.,5.0e8],\
    warpScale=100,displScale=10,contour='MaxPrin')
# Write the beam displacements and rotations to a file
sbeam1.writeDisplacements(fileName = 'V8_Case_2.csv')

# CASE 3:
# Apply the case load
def f(x):
    vx = 1e3
    vy = 1e3
    pz = -1e3
    tz = 1e3
    return np.array([vx,vy,pz,tz])
wing1.applyLoads(f=f,allElems=True)
# Run the analysis
wing1.staticAnalysis(resetPointLoads=True)
wing1.plotDeformedWing(figName='V8 Case 3',numXSects=10,contLim=[0.,5.0e8],\
    warpScale=100,displScale=10,contour='MaxPrin')
# Write the beam displacements and rotations to a file
sbeam1.writeDisplacements(fileName = 'V8_Case_3.csv')