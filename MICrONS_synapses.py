# MICrONS_synapses.py

# A script to load synapse location data from MICrONS dataset
# As a pandas dataframe (requires Pandas is installed), 
# and loads the synapse locations as a point cloud - 
# (as a edge-less, face-less mesh). 
# Point cloud can be visualized with a particle system emitting 
# from the vertices. 

import os
import pandas as pd
import numpy as np

import bpy
import bmesh


# A few manually selected example cells:
cell_id = 648518346349538527
#cell_id = 648518346349539840

obj_scale = 10000

# Auto-detected synapse dataset (all_ prefix)
all_synapses_path = 'Z://Open_data_sets/MICrONS/layer23_v185/pni_synapses_v185.csv'
all_syn_df = pd.read_csv(all_synapses_path)
all_syn_df

# Proofread synapse dataset (pr_ prefix)
pr_synapses_path = 'Z://Open_data_sets/MICrONS/layer23_v185/soma_subgraph_synapses_spines_v185.csv'
pr_syn_df = pd.read_csv(pr_synapses_path)
pr_syn_df


def get_synapses(this_cell_id):
    
    '''
    For a given cell_id, find all of the pre a post-synapses
    '''
    # proofread pre
    df1 = pr_syn_df[pr_syn_df['pre_root_id'] == this_cell_id]
    arr1 = df1[['ctr_pt_x_nm','ctr_pt_y_nm','ctr_pt_z_nm']].values

    # prefread post
    df2 = pr_syn_df[pr_syn_df['post_root_id'] == this_cell_id]
    arr2 = df2[['ctr_pt_x_nm','ctr_pt_y_nm','ctr_pt_z_nm']].values
    # auto pre
    df3 = all_syn_df[all_syn_df['pre_root_id'] == this_cell_id]  
    arr3 = df3[['ctr_pt_x_nm','ctr_pt_y_nm','ctr_pt_z_nm']].values
    
    # auto-post
    df4 = all_syn_df[all_syn_df['post_root_id'] == this_cell_id]  
    arr4 = df4[['ctr_pt_x_nm','ctr_pt_y_nm','ctr_pt_z_nm']].values
    
    return (arr1, arr2, arr3, arr4)



def draw_verts(data,label = 'Verts',incr=1):

    '''
    Load point clouds into a non-mesh cloud of vertices.

    '''

    mesh = bpy.data.meshes.new("Mesh")  # add a new mesh
    obj = bpy.data.objects.new(label, mesh)  # add a new object using the mesh

    bpy.context.collection.objects.link(obj)   # Since 2.8, this is the way to do this
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    mesh = bpy.context.object.data
    bm = bmesh.new()

    for i in range(0,len(data[:,0]),incr):

        x = (data[i][0]) / obj_scale
        y = (data[i][1]) / obj_scale
        z = (data[i][2]) / obj_scale

        bm.verts.new([x, y, z])  # add a new vert

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()  # always do this when finished


# Draw the synapses for the selected cell. 
(pr_pre_arr, pr_post_arr, all_pre_arr, all_post_arr) = get_synapses(cell_id)

draw_verts(pr_pre_arr, 'pr_pre_arr_'+str(cell_id)) # Proofread presynapses
draw_verts(pr_post_arr, 'pr_post_arr_'+str(cell_id)) # Proofread postsynapses
draw_verts(all_pre_arr, 'all_pre_arr_'+str(cell_id)) # Auto-detected presynapses
draw_verts(all_post_arr, 'all_post_arr_'+str(cell_id))# Auto-detected postsynapses



# Draw all of the 3.2 million synapses. 
# Comment this out of your PC memory / GPU can't handle it. 
all_syn_arr = all_syn_df[['ctr_pt_x_nm','ctr_pt_y_nm','ctr_pt_z_nm']].values
draw_verts(all_syn_arr,'all_syn_arr')





#'''
#Don't include this in the published scripts, all ready standalone.
#'''

#import h5py


#def h5_to_mesh(file):

#    
#    obj_name = file[0:-3] # Name the object the same as the file, minus ext

#    # Load verts, edges, faces from the h5 file. 
#    f = h5py.File(os.path.join(path, file))
#    verts = np.asarray(f['vertices']) / obj_scale
#    edges = f['link_edges']
#    faces = f['faces']

#    # Create a new mesh. 
#    mesh = bpy.data.meshes.new(obj_name)  # add the new mesh
#    obj = bpy.data.objects.new(mesh.name, mesh)
#    col = bpy.data.collections[collection_name]
#    col.objects.link(obj)
#    bpy.context.view_layer.objects.active = obj
#    
#    mesh.from_pydata(verts, edges, faces) # Build the mesh from Python data.


## Build the mesh, too. 

#collection_name = "Collection"
#path = 'Z://Open_data_sets/MICrONS/layer23_v185/layer23_v185/'
#h5_to_mesh(str(cell_id) + '.h5')

