# -*- coding: utf-8 -*-
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

# Function to extract the results recorded from each point sensor placed
def extract_pointsensor_results(Results, ps_name, output_type):
	sensor_extractor = Results[ps_name]
	output=sensor_extractor.Outputs[output_type]
	document.AllAlgorithms.Add(sensor_extractor)
	output.Update()
	axis=output.Data.Axis
	values =(output.Data.GetComponent(0))
	raw_data=np.stack([axis,values])
	return raw_data

# Create HDF5 file to write the results to and specify file path
to_write = r"C:\Users\harsh\OneDrive - University of Bath\Yr4 - Semester 2\Sim4Life Models\Multi_Fibre\Multi_Fibre_8\RESULTS_TEST_CV.h5"
ending_folder = h5py.File(to_write,'w')

# Run the NEURON simulation
simulation.RunSimulation()
neuron_results = simulation.Results()

# Save all NEURON results to the HDF5 file created above 
point_sensors = [sensor for sensor in neuron_results.keys() if '@node' in sensor]
for point_sensor in point_sensors:
    v = extract_pointsensor_results(neuron_results,point_sensor,"v")
    ending_folder.create_dataset(str(point_sensor),data=v)
