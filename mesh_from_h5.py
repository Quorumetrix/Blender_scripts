import os
import numpy as np
import bpy

# Non-standard Python modules that may need to be installed. 
# import time
import h5py



N_NEURONS = 10

add_modifiers = False
apply_modifiers = False
smoothing_iterations = 5
decimate_ratio = 0.1
obj_scale = 10000
smooth_factor = 0.5

collection_name = "Collection"

save_progress = True
save_path = 'Z://Blender/MiCRONS.blend'

# First download and extract the h5 file
# From: https://www.microns-explorer.org/phase1
#https://zenodo.org/record/3710459/files/layer23_v185.tar.gz?download=1

path = 'Z://Open_data_sets/MICrONS/layer23_v185/layer23_v185/'
files = os.listdir(path)


def h5_to_mesh(file):

    
    obj_name = file[0:-3] # Name the object the same as the file, minus ext

    # Load verts, edges, faces from the h5 file. 
    f = h5py.File(os.path.join(path, file))
    verts = np.asarray(f['vertices']) / obj_scale
    edges = f['link_edges']
    faces = f['faces']

    # Create a new mesh. 
    mesh = bpy.data.meshes.new(obj_name)  # add the new mesh
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections[collection_name]
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    
    mesh.from_pydata(verts, edges, faces) # Build the mesh from Python data.

    # Add modifiers
    if add_modifiers:
        
        smoothing_modifier = obj.modifiers.new(name='smooth', type='SMOOTH')
        smoothing_modifier.factor = smooth_factor
        smoothing_modifier.iterations = smoothing_iterations

        decimate_modifier = obj.modifiers.new(name='decimate', type='DECIMATE')
        decimate_modifier.ratio = decimate_ratio

        if apply_modifiers:
            
            bpy.context.view_layer.objects.active = obj # 2.8
            while obj.modifiers:

                bpy.ops.object.modifier_apply(modifier=obj.modifiers[0].name)
            

# Optionally, select specific neurons to build. 
#files = ['648518346349521083.h5', '648518346349533267.h5']

# Alternatively, select the first N files to build
files = files[0:N_NEURONS] # Comment this line out to build all of them. 
print('Subset of files to build: ', files)


for i,file in enumerate(files):
    print('---',i,'------')
    # start = time.time()
    h5_to_mesh(file)
    # end = time.time()
    # print(file, 'time elapsed: ',end - start)

    if save_progress:
        bpy.ops.wm.save_mainfile(filepath=save_path)
