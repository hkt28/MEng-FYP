# -*- coding: utf-8 -*
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


# Function to get the properties of any axon 
def AxonPropertyValues(entity,index):
	# 0 - AxonDiameter; 1 - NodeNodeSeparation; 2 - NumberOfMyelinLamellae; 3 - NodeLength; 4 - NodeDiameter
	# 5 - MYSALength; 6 - MYSADiameter; 7 - MYSAPeriaxonalSpaceWidth; 8 - FLUTLength; 9 - FLUTDiameter
	# 10 - FLUTPeriaxonalSpaceWidth; 11 - STINLength; 12 - STINDiameter; 13 - STInPeriaxonalSpaceWidth
	properties = model.GetAxonProperties(entity)
	parameter = properties[index]
	parameter_value = parameter.Value
	return parameter_value

# list of axons
axons = [entity__median_0_neuron,entity__median_1_neuron,entity__median_2_neuron,entity__median_3_neuron,entity__median_4_neuron,entity__median_5_neuron,entity__median_6_neuron,entity__median_7_neuron,entity__median_8_neuron,entity__median_9_neuron, entity__median_10_neuron,entity__median_11_neuron,entity__median_12_neuron,entity__median_13_neuron,entity__median_14_neuron,entity__median_15_neuron,entity__median_16_neuron,entity__median_17_neuron,entity__median_18_neuron,entity__median_19_neuron, entity__median_20_neuron,entity__median_21_neuron,entity__median_22_neuron,entity__median_23_neuron,entity__median_24_neuron,entity__median_25_neuron,entity__median_26_neuron,entity__median_27_neuron,entity__median_28_neuron,entity__median_29_neuron]# components = [entity__median_0_neuron_1, entity__median_10_neuron, entity__median_11_neuron, entity__median_12_neuron_1, entity__median_13_neuron_2, entity__median_14_neuron, entity__median_15_neuron, entity__median_16_neuron_1, entity__median_17_neuron_1, entity__median_18_neuron_1, entity__median_19_neuron, entity__median_1_neuron_1, entity__median_2_neuron_1, entity__median_3_neuron, entity__median_4_neuron, entity__median_5_neuron, entity__median_6_neuron, entity__median_7_neuron_1, entity__median_8_neuron, entity__median_9_neuron]
diameters = []
separations = []

# Use function to obtain diameters and internodal separation values
for axon in axons:
	d = AxonPropertyValues(axon,0)
	s = AxonPropertyValues(axon,1)
	diameters.append(d)
	separations.append(s)
	
print(diameters)
print(separations)

# Save to a .csv file
test = np.transpose([diameters,separations])
print(test)

file1 = r"C:\Users\harsh\OneDrive - University of Bath\Yr4 - Semester 2\Sim4Life Models\Fasc_1D_Long\Parameters.csv"
np.savetxt(file1,test,delimiter=',')
