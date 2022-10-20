import os
import sys
import numpy as np

def write_circular_CRIMSON_VTK(filename: str, centerline_points, radii):
    """
    This function writes a vtk file given centerline points and radii that can be imported into CRIMSON.
    Typically the input is 10-30 evenly sampled points along centerline and not all the centerline points/radii.

    One VTK file must be written PER BRANCH to be compatible with CRIMSON's lofting an blending workflow.
    Import by right clicking the vessel tree in CRIMSON and selecting "import vessel"

    filename: name of vtk file where this vessel will be encoded
    centerline_points: Nx3 numpy array containing (x,y,z) coordinates of centerline points in [mm]
    radii: Nx1 or (N,) numpy array/list containing radius in [mm] at each centerline point
    """
    numPoints = centerline_points.shape[0]
    numContours = len(radii)

    if numPoints != numContours:
        sys.exit("Number of points doesn't match number of contours")
    if os.path.exists(filename):
        os.remove(filename) #ensures file is over-written instead of appended
    with open(filename, "w+") as text_file:
        #overwrite using text_file.write('new content')
        print("# vtk DataFile Version 3.0", file=text_file)
        print("CRIMSON vessel path output from python", file=text_file)
        print("ASCII\nDATASET POLYDATA", file=text_file)

        total_points = numPoints + 2*len(radii)
        print("POINTS {} float".format(total_points), file=text_file)
        for point in centerline_points:
            string_point = ' '.join(map(str, point))
            print("{}".format(string_point), file=text_file)
        for radius in radii:
            radius_point1 = [radius, 0, 0]
            radius_point2 = [0, radius, 0]
            string_radius_point1 = ' '.join(map(str, radius_point1))
            string_radius_point2 = ' '.join(map(str, radius_point2))
            print("{}\n{}".format(string_radius_point1, string_radius_point2), file=text_file)

        #cell info header
        print("LINES {} {}".format(numPoints+1,total_points+(numPoints+1)),file=text_file)
        print("{} {}".format(numPoints, ' '.join(map(str, np.arange(0, numPoints)))),file=text_file)

        nextID = numPoints
        for i in range(numPoints):
            firstID = nextID
            nextID = nextID + 2 #2 radius points per centerline point
            print("{} {}".format(2, ' '.join(map(str,np.arange(firstID, nextID)))), file=text_file)

def write_elliptical_CRIMSON_VTK(filename, centerline_points, ellipse_radii):
    """
    NOTE: in-plane rotation/specifying orientation of ellipses is not well supported by CRIMSON. Alex was working on this but never figured it out.

    This function writes a vtk file given centerline points and elliptical radii pairs that can be imported into CRIMSON.
    Typically the input is 10-30 evenly sampled points along centerline and not all the centerline points/radii.

    One VTK file must be written PER BRANCH to be compatible with CRIMSON's lofting an blending workflow.
    Import by right clicking the vessel tree in CRIMSON and selecting "import vessel"

    filename: name of vtk file where this vessel will be encoded
    centerline_points: Nx3 numpy array containing (x,y,z) coordinates of centerline points in [mm]
    radii: Nx2 numpy array or list containing major and minor radii in [mm] at each centerline point

    """

    numPoints = centerline_points.shape[0]
    numContours = len(ellipse_radii)
    if numPoints != numContours:
        sys.exit("Number of points doesn't match number of contours")

    if os.path.exists(filename):
        os.remove(filename)  # ensures file is over-written instead of appended
    with open(filename, "w+") as text_file:
        # overwrite using text_file.write('new content')
        print("# vtk DataFile Version 3.0", file=text_file)
        print("CRIMSON vessel path output from python", file=text_file)
        print("ASCII\nDATASET POLYDATA", file=text_file)

        total_points = numPoints + 2 * len(ellipse_radii)
        print("POINTS {} float".format(total_points), file=text_file)
        for point in centerline_points:
            string_point = ' '.join(map(str, point))
            print("{}".format(string_point), file=text_file)
        for radius_pair in ellipse_radii:
            radius_point1 = radius_pair[0]
            radius_point2 = radius_pair[1]
            string_radius_point1 = ' '.join(map(str, radius_point1))
            string_radius_point2 = ' '.join(map(str, radius_point2))
            print("{}\n{}".format(string_radius_point1, string_radius_point2), file=text_file)

        # cell info header
        print("LINES {} {}".format(numPoints + 1, total_points + (numPoints + 1)), file=text_file)
        # i=1 in matlab code: centerline points
        print("{} {}".format(numPoints, ' '.join(map(str, np.arange(0, numPoints)))), file=text_file)

        # i=2:length(polyLines) in matlab
        nextID = numPoints
        for i in range(numPoints):
            firstID = nextID
            nextID = nextID + 2  # 2 radius points per centerline point
            print("{} {}".format(2, ' '.join(map(str, np.arange(firstID, nextID)))), file=text_file)