import os
import numpy as np
# import OCC
from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Pnt

savePath = os.getcwd()
savePath = os.path.join(savePath,'test-occ.step')

pts = np.array([[ 0., 0., 1.75 ], [ 4.01337793, 0., 1.75 ], [ 8.02675585 , 0. , 1.75 ], [ 12.04013378 , 0. , 1.75 ], [ 16.05351171 ,   0. , 1.75 ], [ 20.06688963 , 0. , 1.75 ], [ 24.08026756 , 0. , 1.31132249], [ 28.09364548 , 0. , 0.62301328], [ 32.10702341 ,  0. , 0.67000487], [ 36.12040134 , 0. , 1.38505489], [ 40.13377926 ,  0. , 1.75 ], [ 44.14715719 , 0. , 1.75 ], [ 48.16053512 ,  0. , 1.75 ], [ 52.17391304 , 0. , 1.75 ], [ 56.18729097 ,  0. , 1.75 ], [ 60.2006689  , 0. , 1.75 ], [ 64.21404682 ,  0. , 1.75 ], [ 68.22742475 , 0. , 1.75 ], [ 72.24080268 ,  0. , 1.75 ], [ 76.2541806  , 0. , 1.75 ], [ 80.26755853 ,  0. , 1.75 ], [ 84.28093645 , 0. , 1.75 ], [ 88.29431438 ,  0. , 1.75 ], [ 92.30769231 , 0. , 1.75 ], [ 96.32107023 ,  0. , 1.75 ], [100.33444816 , 0. , 1.75 ], [104.34782609 ,  0. , 1.75 ], [108.36120401 , 0. , 1.75 ], [112.37458194 ,  0. , 1.75 ], [116.38795987 , 0. , 1.75 ]])
 
numPts = len(pts)

print(f'Using {numPts} of the points')
print(f'Will save to: {savePath}')

pointArray = []
for idx,pt in enumerate(pts):
    if idx == 0:
        print('First Point:', pt[0], pt[1], pt[2])
        firstPt = gp_Pnt(pt[0],pt[1], pt[2])
        pointArray.append(firstPt)
    elif idx == numPts-1:
        print('Last Point:', pt[0], pt[1], pt[2])
        lastPt = gp_Pnt(pt[0],pt[1], pt[2])
        pointArray.append(lastPt)
    else:
        p = gp_Pnt(pt[0],pt[1], pt[2])
        pointArray.append(p)


#############################################################
################### MAKEPIPE DEMO ###########################
######### https://github.com/tpaviot/pythonocc-demos/blob/master/examples/core_topology_pipe.py
#############################################################

# from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
# from OCC.Core.TColgp import TColgp_Array1OfPnt
# from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
# from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe

# # the bspline path, must be a wire
# array2 = TColgp_Array1OfPnt(1, 3)
# array2.SetValue(1, gp_Pnt(0, 0, 0))
# array2.SetValue(2, gp_Pnt(0, 1, 2))
# array2.SetValue(3, gp_Pnt(0, 2, 3))
# bspline2 = GeomAPI_PointsToBSpline(array2).Curve()
# path_edge = BRepBuilderAPI_MakeEdge(bspline2).Edge()
# path_wire = BRepBuilderAPI_MakeWire(path_edge).Wire()

# # the bspline profile. Profile mist be a wire
# array = TColgp_Array1OfPnt(1, 5)
# array.SetValue(1, gp_Pnt(0, 0, 0))
# array.SetValue(2, gp_Pnt(1, 2, 0))
# array.SetValue(3, gp_Pnt(2, 3, 0))
# array.SetValue(4, gp_Pnt(4, 3, 0))
# array.SetValue(5, gp_Pnt(5, 5, 0))
# bspline = GeomAPI_PointsToBSpline(array).Curve()
# profile_edge = BRepBuilderAPI_MakeEdge(bspline).Edge()

# # pipe
# pipe = BRepOffsetAPI_MakePipe(path_wire, profile_edge).Shape()

# display, start_display, add_menu, add_function_to_menu = init_display()
 
# display.DisplayShape(profile_edge, update=False)
# display.DisplayShape(path_wire, update=False)
# display.DisplayShape(pipe, update=True)

# start_display()



########################################################
#################### SAVE THE STEP FILE ################
########################################################

from OCC.Core.STEPControl import (
    STEPControl_Reader,
    STEPControl_Writer,
    STEPControl_AsIs,
)
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.IFSelect import IFSelect_RetDone

application_protocol="AP203"
# creates and initialise the step exporter
step_writer = STEPControl_Writer()
Interface_Static_SetCVal("write.step.schema", application_protocol)

# transfer shapes and write file
step_writer.Transfer(revolved_shape_, STEPControl_AsIs)
status = step_writer.Write(savePath)

if not status == IFSelect_RetDone:
    raise IOError("Error while writing shape to STEP file.")
if not os.path.isfile(savePath):
    raise IOError(f"{savePath} not saved to filesystem.")

