# microns_calcium_trace_animation.py

'''
Assumes you already have the MICrONS layer 2/3 meshes constructed, and they are named
the same as the individual files, i.e. 
    648518346349477331
    648518346349487432
    As would be generated using the mesh_from_h5.py script
Only a subset of 112 of the dense reconstruction have calcium imaging data, so this_spike
script will only animate that subset.  
'''

import numpy as np
import pandas as pd

import bpy
import os 
from tqdm import tqdm

## If seaborn installed, then load colormap directly.
#import seaborn as sns
#PALETTE = 'viridis'
#cm_data = np.asarray(sns.color_palette(PALETTE, n_colors=256))

# Otherwise load from a pre-processed numpy array. (Because Blender comes with numpy)
CMAP = 'viridis'
PATH_TO_CMAP = 'E://Documents/Professional/Blender scripts/colormaps/'+CMAP+'.npy'
cm_data = np.load(PATH_TO_CMAP)

n_tpts = 2000 # Timepoints to animate materials from trace data

#Predefined min max for spike duration
min_val = 39
max_val = 1172
spike_thresh = 0

# Load the trace data.
trace_path = 'Z://Open_data_sets/MICrONS/layer23_v185/calcium_trace.pkl'
data = pd.read_pickle(trace_path)
df = pd.DataFrame(pd.read_pickle(trace_path))
 

def map_range(value, from_min, from_max, to_min, to_max):

    # Figure out how 'wide' each range is
    from_span = from_max - from_min
    to_span = to_max - to_min

    # Convert the 'from' range into a 0-1 range (float)
    value_scaled = float(value - from_min) / float(from_span)

    # Convert the 0-1 range into a value in the 'to' range.
    return to_min + (value_scaled * to_span)    


for cell_id in tqdm(list(df.columns)):

    obj = bpy.context.scene.objects[str(cell_id)] 
    this_trace = data[cell_id]['trace']
    this_spike = data[cell_id]['spike']
    
    # Spike duration: proportion of entire trace that calcium value about threshold value.
    spike_duration = (this_spike > spike_thresh).sum() 
    
    # Map spike duration to the colormap, using predefined min and max values. 
    mapped_val = map_range(spike_duration, min_val, max_val, 0, np.shape(cm_data)[0])
    rgb = tuple(cm_data[int(mapped_val)-1])
    rgba = rgb + (1,) # Add alpha
    
    # Create a new material for each neuron

    obj.data.materials.clear() # Clear any existing materials on the object.

    mat = bpy.data.materials.new(name=obj.name)#curr_neuron) #set new material to variable
    mat.diffuse_color =  rgba#tuple(cm_data[int(mapped_val)-1]) #colors[i,:]   
    mat.blend_method = 'BLEND' # Alpha blend method for transparency

    # get the node tree and clear it
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()


    # ---
    # Programatically build the material node tree for each neuron's unique material.
    # ---


    # Volume shader
    node_volume = nodes.new(type='ShaderNodeVolumePrincipled')
    node_volume.inputs[0].default_value = rgba # Color
    node_volume.inputs[7].default_value = rgba # Emission color
    node_volume.location = -400,-200
    
    node_mix = nodes.new(type='ShaderNodeMixShader')
    node_mix.location = -400,200
    node_transparent = nodes.new(type='ShaderNodeBsdfTransparent')       
    node_transparent.location = -600,300
    
    
    # ----
    # Use the Calcium imaging data to drive material properties 
    # of the neurons through time. Here we are animating:
    # Volume density, volume emission strength, and the mix node (opacity)
    # ----
    
    for t in range(n_tpts):

        node_volume.inputs[2].default_value = this_trace[t]# Density
        node_volume.inputs[2].keyframe_insert(data_path="default_value",frame=t)

        node_volume.inputs[6].default_value = this_trace[t]# Emission strength
        node_volume.inputs[6].keyframe_insert(data_path="default_value",frame=t)
        
        node_mix.inputs[0].default_value = np.clip(this_trace[t], 0, 1) # Transparency mix
        node_mix.inputs[0].keyframe_insert(data_path="default_value",frame=t)
        
    # Refraction SBDF surface
    node_refbsdf = nodes.new(type='ShaderNodeBsdfRefraction')
    node_refbsdf.inputs[0].default_value = rgba#(colors[i,:])#  random.random(),random.random(),random.random(),1)  # green RGBA
    node_refbsdf.inputs[1].default_value  = 0.1# Roughness
    node_refbsdf.inputs[2].default_value  = 1.33#Index of refraction
    node_refbsdf.location = -600,100

    # create output node
    node_output = nodes.new(type='ShaderNodeOutputMaterial')   
    node_output.location = 200,0   

    # link nodes
    links = mat.node_tree.links
    link = links.new(node_transparent.outputs[0], node_mix.inputs[1])
    link = links.new(node_refbsdf.outputs[0], node_mix.inputs[2])
    link = links.new(node_mix.outputs[0], node_output.inputs[0])
    link = links.new(node_volume.outputs[0], node_output.inputs[1])
    obj.data.materials.append(mat) #add the material to the object 

