import os
import numpy as np
# import gmsh_api.gmsh as gmsh
import gmsh


savePath = os.getcwd()
savePath = os.path.join(savePath,'test.step')

pts = np.array([[ 0., 0., 1.75 ], [ 4.01337793, 0., 1.75 ], [ 8.02675585 , 0. , 1.75 ], [ 12.04013378 , 0. , 1.75 ], [ 16.05351171 ,   0. , 1.75 ], [ 20.06688963 , 0. , 1.75 ], [ 24.08026756 , 0. , 1.31132249], [ 28.09364548 , 0. , 0.62301328], [ 32.10702341 ,  0. , 0.67000487], [ 36.12040134 , 0. , 1.38505489], [ 40.13377926 ,  0. , 1.75 ], [ 44.14715719 , 0. , 1.75 ], [ 48.16053512 ,  0. , 1.75 ], [ 52.17391304 , 0. , 1.75 ], [ 56.18729097 ,  0. , 1.75 ], [ 60.2006689  , 0. , 1.75 ], [ 64.21404682 ,  0. , 1.75 ], [ 68.22742475 , 0. , 1.75 ], [ 72.24080268 ,  0. , 1.75 ], [ 76.2541806  , 0. , 1.75 ], [ 80.26755853 ,  0. , 1.75 ], [ 84.28093645 , 0. , 1.75 ], [ 88.29431438 ,  0. , 1.75 ], [ 92.30769231 , 0. , 1.75 ], [ 96.32107023 ,  0. , 1.75 ], [100.33444816 , 0. , 1.75 ], [104.34782609 ,  0. , 1.75 ], [108.36120401 , 0. , 1.75 ], [112.37458194 ,  0. , 1.75 ], [116.38795987 , 0. , 1.75 ]])

h = 1
numPts = len(pts)

print(f'Using {numPts} of the points')
print(f'Will save to: {savePath}')

gmsh.initialize()

pointArray = []
for idx,pt in enumerate(pts):
    if idx == 0:
        print('First Point:', pt[0], pt[1], pt[2])
        firstPt = gmsh.model.occ.addPoint(pt[0],pt[1],pt[2], h)
        pointArray = np.append(pointArray,firstPt)
    elif idx == numPts-1:
        lastPt = gmsh.model.occ.addPoint(pt[0],pt[1],pt[2], h)
        pointArray = np.append(pointArray,lastPt)
    else:
        p = gmsh.model.occ.addPoint(pt[0],pt[1],pt[2], h)
        pointArray = np.append(pointArray,p)

line1 = gmsh.model.occ.addSpline(pointArray)

firstCoord = pts[0,:]
lastCoord  = pts[-1,:]
endPt = gmsh.model.occ.addPoint(lastCoord[0],0,0, h)
startPt = gmsh.model.occ.addPoint(0,0,0, h)
line2 = gmsh.model.occ.addLine(lastPt,endPt)
line3 = gmsh.model.occ.addLine(startPt,firstPt)

rev = gmsh.model.occ.revolve(gmsh.model.occ.getEntities(1), 0,0,0, 1,0,0, 2*np.pi )

b = [s[1] for s in gmsh.model.occ.getEntities(2)]
surfLoop = gmsh.model.occ.addSurfaceLoop(b)
vol = gmsh.model.occ.addVolume([surfLoop])

gmsh.model.occ.synchronize()
  
gmsh.write(savePath)
gmsh.finalize()
