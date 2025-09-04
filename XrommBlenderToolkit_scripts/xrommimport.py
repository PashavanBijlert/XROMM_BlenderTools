########################################
#import rigid body transformation matrix and apply to selected object
#Written by Peter Falkingham, July 2023
#Credit for original Maya Mel scripts on which this is based goes to: Dave Baier.
########################################



import bpy
import csv
import numpy as np
from mathutils import Matrix, Vector



def importRBT(importCSV, skipFirstColumn):
    #hardcode datatype for now
    ### Inputs:
    # importCSV (absolute path to the target csv file, string)
    # skipFirstColumn (boolean, whether or not to skip the first column of the CSV when importing)
    #############################
    #Rigid Body Transformation
    #############################

    # List to store the transformation data
    transformations = []

    # Open the CSV file
    with open(importCSV, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)

        
        # Loop through each row in the CSV file
        for row in reader:
            
            if skipFirstColumn: # If we skip the first column, extract element 1-16
                matrix_elements = [float(x) for x in row[1:17]]
            else: #else, we extract element 0-15 as normal. 
                matrix_elements = [float(x) for x in row[:16]]
            
            print("Me: ", matrix_elements)
            # Create a 4x4 matrix from the elements
            matrix = Matrix((
                (matrix_elements[0], matrix_elements[1], matrix_elements[2], matrix_elements[3]),
                (matrix_elements[4], matrix_elements[5], matrix_elements[6], matrix_elements[7]),
                (matrix_elements[8], matrix_elements[9], matrix_elements[10], matrix_elements[11]),
                (matrix_elements[12], matrix_elements[13], matrix_elements[14], matrix_elements[15])
            ))
            print ("matrix:", matrix)
            # Append the matrix to the transformations list
            transformations.append(matrix)

    # Get the selected object
    selected = bpy.context.selected_objects[0]

    # Set the current frame to 1
    bpy.context.scene.frame_set(1)



    # Loop through each transformation and create a keyframe for each frame
    for i, matrix in enumerate(transformations):
                    
                
        # Transpose the matrix using numpy
        matrix_data_transposed = np.transpose(matrix)

        # Create a matrix from the transposed data
        matrix = Matrix(matrix_data_transposed)

        # Set the object's world matrix
        selected.matrix_world = matrix
        
        
        print(selected.matrix_world)

        # Create a keyframe for the object's world matrix
        frame_number = 1 + i
        if not np.isnan(matrix).any():  #if the matrix contains NaNs, don't keyframe it
            selected.keyframe_insert(data_path='location', frame=frame_number)
            selected.keyframe_insert(data_path='rotation_euler', frame=frame_number)
            selected.keyframe_insert(data_path='scale', frame=frame_number)