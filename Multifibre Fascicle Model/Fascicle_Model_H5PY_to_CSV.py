# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

#Import s4l modules
import s4l_v1.document as document
import s4l_v1.model as model
import s4l_v1.simulation.emlf as emlf
import s4l_v1.analysis as analysis
import s4l_v1.analysis.viewers as viewers
from s4l_v1.model import Vec3
import s4l_v1.units as units
from s4l_v1 import Unit
import s4l_v1.simulation.neuron as neuron

#import other modules
import sys, os
import numpy as np
import csv
import math
import random
import h5py

# Open the H5 file to read results
to_read = r"C:\Users\harsh\OneDrive - University of Bath\Yr4 - Semester 2\Sim4Life Models\Multi_Fibre\Multi_Fibre_7\RESULTS_TEST.h5"
hf = h5py.File(to_read, 'r')
print(hf.keys())
all_results = np.array(hf.keys())
shape_1 = all_results.shape

# Function to extract properties from any axon
def AxonPropertyValues(entity,index):
	# 0 - AxonDiameter; 1 - NodeNodeSeparation; 2 - NumberOfMyelinLamellae; 3 - NodeLength; 4 - NodeDiameter
	# 5 - MYSALength; 6 - MYSADiameter; 7 - MYSAPeriaxonalSpaceWidth; 8 - FLUTLength; 9 - FLUTDiameter
	# 10 - FLUTPeriaxonalSpaceWidth; 11 - STINLength; 12 - STINDiameter; 13 - STInPeriaxonalSpaceWidth
	properties = model.GetAxonProperties(entity)
	parameter = properties[index]
	parameter_value = parameter.Value
	return parameter_value

# List of axons
axons = [entity__median_0_neuron,entity__median_1_neuron,entity__median_2_neuron,entity__median_3_neuron,entity__median_4_neuron,entity__median_5_neuron,entity__median_6_neuron,entity__median_7_neuron,entity__median_8_neuron,entity__median_9_neuron]

# Get the axon diameter and internodal separation of 2 random axons
d1 = AxonPropertyValues(entity__median_2_neuron,0)
d2 = AxonPropertyValues(entity__median_7_neuron,0)

sep1 = AxonPropertyValues(entity__median_2_neuron,1)
sep2 = AxonPropertyValues(entity__median_7_neuron,1)

# Find two nodes for recording data, at specific distances from the electrodes (only in one direction)
node_1_axon1 = math.floor((7.67*1000)/sep1)
node_2_axon1 = math.floor((8.84*1000)/sep1)

node_1_axon2 = math.floor((7.67*1000)/sep2)
node_2_axon2 = math.floor((8.84*1000)/sep2)

# Create the names to be extracted from H5 file
name_1_axon1 = 'Median_2_neuron' + '  (Median_Axon_Trajectories)@node[' + str(node_1_axon1) + ']@0.50'
name_2_axon1 = 'Median_2_neuron' + '  (Median_Axon_Trajectories)@node[' + str(node_2_axon1) + ']@0.50'

name_1_axon2 = 'Median_7_neuron' + '  (Median_Axon_Trajectories)@node[' + str(node_1_axon2) + ']@0.50'
name_2_axon2 = 'Median_7_neuron' + '  (Median_Axon_Trajectories)@node[' + str(node_2_axon2) + ']@0.50'

# Extract the point sensor data for each of those nodes and make into numpy arrays
node1_1 = np.array(hf.get(name_1_axon1))
node2_1 = np.array(hf.get(name_2_axon1))

node1_2 = np.array(hf.get(name_1_axon2))
node2_2 = np.array(hf.get(name_2_axon2))

node1_1_t = np.transpose(node1_1)
node2_1_t = np.transpose(node2_1)
node1_2_t = np.transpose(node1_2)
node2_2_t = np.transpose(node2_2)

# Make csv file names to store the point sensor node data
file1 = to_read = r"C:\Users\harsh\OneDrive - University of Bath\Yr4 - Semester 2\Sim4Life Models\Multi_Fibre\Multi_Fibre_7\Median_2_neuron_Node_38.csv"
file2 = to_read = r"C:\Users\harsh\OneDrive - University of Bath\Yr4 - Semester 2\Sim4Life Models\Multi_Fibre\Multi_Fibre_7\Median_2_neuron_Node_44.csv"
file3 = to_read = r"C:\Users\harsh\OneDrive - University of Bath\Yr4 - Semester 2\Sim4Life Models\Multi_Fibre\Multi_Fibre_7\Median_7_neuron_Node_6.csv"
file4 = to_read = r"C:\Users\harsh\OneDrive - University of Bath\Yr4 - Semester 2\Sim4Life Models\Multi_Fibre\Multi_Fibre_7\Median_7_neuron_Node_7.csv"

# Save the point sensor data to the corresponding csv files 
np.savetxt(file1,node1_1_t,delimiter=',')
np.savetxt(file2,node2_1_t,delimiter=',')
np.savetxt(file3,node1_2_t,delimiter=',')
np.savetxt(file4,node2_2_t,delimiter=',')



