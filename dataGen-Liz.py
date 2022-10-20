import os
import numpy as np
import matplotlib.pyplot as plt
from CRIMSON_io import *
import json
from scipy.interpolate import splev, splrep
# original gmsh-api from gmsh package
import gmsh_api.gmsh as gmsh


def write_STEP_using_GMSH(savePath,pts):
    h = 0.1
    numPts = len(pts)

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

currentDir = os.getcwd()
savePath = os.path.join(currentDir,'test')


radiusRange = [70]
lengthRange = [5,6,7,8,9,10,11,12,13,14,15]

for radius in radiusRange:
    for length in lengthRange:
        dataset_name = f'r{radius:02d}_l{length:02d}'

        num_pts = 300
        ves_len = 120 # in mm
        ves_diam = 3.5 # in mm

        # multiply by 2 because using Z0 = 1/2(stenosis length)
        sten_len = int(length*2*(num_pts/ves_len))
        sten_sev = radius/100

        ################################ Run spline generator ################################
        myArgs = f'--num_centerline_points {num_pts} --set_length {ves_len/1e3:0.3f} --constant_radius --set_diameter {ves_diam/1e3:0.5f} --num_stenoses 1 --stenosis_type "cosine" --stenosis_position 75 --stenosis_severity {sten_sev:0.2f} --stenosis_length {sten_len} --save_visualization'
        print(myArgs)
        # os.system(f'python3 tube_generator.py --save_path "C:\\Users\\eliza\\Documents\\Github\\vessel_tree_generator\\test" --dataset_name {dataset_name} --num_trees 1 --vessel_type cylinder {myArgs}')
        os.system(f'python3 tube_generator.py --save_path {savePath} --dataset_name {dataset_name} --num_trees 1 --vessel_type cylinder {myArgs}')
        
        # Copy files from array/info directory to parent and delete directories
        os.replace(os.path.join(savePath,dataset_name,"arrays","{}_{:04d}.npy".format(dataset_name, 0)),os.path.join(savePath,dataset_name,dataset_name+".npy"))
        # os.remove(os.path.join(savePath,dataset_name,"arrays","{}_{:04d}.npy".format(dataset_name, 0)))
        os.rmdir(os.path.join(savePath, dataset_name, "arrays"))
        os.replace(os.path.join(savePath, dataset_name, "info", "{}_{:04d}.info.json".format(dataset_name, 0)),os.path.join(savePath, dataset_name, dataset_name+".info.json"))
        # os.remove(os.path.join(savePath, dataset_name, "info", "{}_{:04d}.info.json".format(dataset_name, 0)))
        os.rmdir(os.path.join(savePath, dataset_name, "info"))

        ################################ Load spline and save ################################
        newNpy = np.load(os.path.join(savePath, dataset_name, f'{dataset_name}.npy'))
        parametric = newNpy[0]*1e3

        # Fit spline using vtk points
        true_x = parametric[:,0]
        true_r = parametric[:,3]
        numDataPts = len(true_r)

        # Try writing to a GMSH file
        # print(np.stack((parametric[:,0],parametric[:,1],parametric[:,3])))
        myPts = np.zeros((len(parametric),3))
        myPts[:,0] = parametric[:,0]
        myPts[:,1] = parametric[:,1]
        myPts[:,2] = parametric[:,3]
        
        write_STEP_using_GMSH(os.path.join(savePath, dataset_name,f'{dataset_name}.step'), myPts)

        # splExact = splrep(true_x,true_r)
        smoothingCoef = 1e-6
        splExact = splrep(true_x,true_r,s=smoothingCoef)
        knotPositions = np.unique(splExact[0])
        knotRadii = splev(np.unique(splExact[0]), splExact)

        pts = np.zeros((len(knotPositions),3))
        pts[:,0] = knotPositions

        # add noise to pts so Crimson doesn't have a heart attack
        pts = pts + np.random.normal(0, 1e-4, pts.shape)
        write_circular_CRIMSON_VTK(os.path.join(savePath, dataset_name,f'{dataset_name}.vtk'), pts, knotRadii)

        # Update the info file to include the spline fit smoothing
        infoPath = os.path.join(savePath,dataset_name,f'{dataset_name}.info.json')
        with open(infoPath, 'r') as openfile:
            summaryData = json.load(openfile)

        summaryData.update({"spline_smoothing":smoothingCoef})
        json_object = json.dumps(summaryData, indent=4)

        with open(infoPath, "w") as outfile:
            outfile.write(json_object)


        # ################################ Compare old and new ################################
        # oldNpy = np.load(os.path.join('D:\\Simulations\\3-LADModels', dataset_name, f'{dataset_name}.npy'))*1e3
      
        # fig = plt.figure(dpi=600)
        # plt.plot(oldNpy[:,0],oldNpy[:,3],'k',linewidth=2,label="Old")
        # plt.plot(parametric[:,0],parametric[:,3],'r--',label="New")
        # plt.legend()
        # plt.ylabel('Radius [mm]')
        # plt.xlabel('Position [mm]')
        # plt.title(f'Geometry: {dataset_name}, Error: {np.max(np.abs(parametric[:,3]-oldNpy[:,3])):0.3e}')
        # # plt.show()
        # plt.savefig(os.path.join(savePath, f'{dataset_name}-comparison'))
        # plt.close()