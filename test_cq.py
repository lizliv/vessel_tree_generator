import os
import numpy as np
import cadquery as cq
from cadquery import exporters

savePath = os.getcwd()

pts = np.array([[ 0., 0., 1.75 ], [ 4.01337793, 0., 1.75 ], [ 8.02675585 , 0. , 1.75 ], [ 12.04013378 , 0. , 1.75 ], [ 16.05351171 ,   0. , 1.75 ], [ 20.06688963 , 0. , 1.75 ], [ 24.08026756 , 0. , 1.31132249], [ 28.09364548 , 0. , 0.62301328], [ 32.10702341 ,  0. , 0.67000487], [ 36.12040134 , 0. , 1.38505489], [ 40.13377926 ,  0. , 1.75 ], [ 44.14715719 , 0. , 1.75 ], [ 48.16053512 ,  0. , 1.75 ], [ 52.17391304 , 0. , 1.75 ], [ 56.18729097 ,  0. , 1.75 ], [ 60.2006689  , 0. , 1.75 ], [ 64.21404682 ,  0. , 1.75 ], [ 68.22742475 , 0. , 1.75 ], [ 72.24080268 ,  0. , 1.75 ], [ 76.2541806  , 0. , 1.75 ], [ 80.26755853 ,  0. , 1.75 ], [ 84.28093645 , 0. , 1.75 ], [ 88.29431438 ,  0. , 1.75 ], [ 92.30769231 , 0. , 1.75 ], [ 96.32107023 ,  0. , 1.75 ], [100.33444816 , 0. , 1.75 ], [104.34782609 ,  0. , 1.75 ], [108.36120401 , 0. , 1.75 ], [112.37458194 ,  0. , 1.75 ], [116.38795987 , 0. , 1.75 ]])


## Revolve Method
pts2D = np.delete(pts,1,1)
sPnts = list(map(tuple, pts2D))
r = cq.Workplane("XY")
r = r.lineTo(pts[0,0], pts[0,2]).spline(sPnts, includeCurrent=False).lineTo(pts[-1,0], 0).close()
revolve_result = r.revolve(360,(0,0,0),(1,0,0))

exporters.export(revolve_result, os.path.join(savePath,'test-cq_revolve.step'))



## Loft Method
l = cq.Workplane("YZ")

for idx,pt in enumerate(pts):
    if idx == 0:
        l.circle(pt[2])
    else:
        l.workplane(offset=pt[0]).circle(pt[2])

loft_result = l.loft(combine=True)

exporters.export(loft_result, os.path.join(savePath,'test-cq_loft.step'))



## Sweep Method 
ptsReorder = pts[:, [1, 1, 0]]
splinePts = list(map(tuple, ptsReorder))
spline_path= cq.Workplane("YZ").spline(splinePts)

s = cq.Workplane("YZ")
for idx,pt in enumerate(pts):
    if idx == 0:
        s.circle(pt[2])
    else:
        s.workplane(offset=pt[0]).circle(pt[2])

sweep_result = (s
    .consolidateWires()
    .sweep(spline_path,multisection=True)
    )
    
exporters.export(sweep_result, os.path.join(savePath,'test-cq_sweep.step'))


## Multi-Sweep Method 
tanZ =  cq.Vector(0, 0, 1)
ptVector = []
for idx,pt in enumerate(pts):
    ptVector.append(cq.Vector(0,0,pt[0]))

msPath = cq.Edge.makeSpline(
    ptVector,
    tangents=(tanZ, tanZ),
)

faceArray = []
for idx,pt in enumerate(pts):
    f = cq.Face.makeFromWires(
        cq.Wire.makeCircle(pt[2], center=(0,0,pt[0]), normal=msPath.tangentAt(0))
        )
    faceArray.append(f)

multisweep_result = cq.Solid.sweep_multi(faceArray, path=msPath)

exporters.export(sweep_result, os.path.join(savePath,'test-cq_multisweep.step'))