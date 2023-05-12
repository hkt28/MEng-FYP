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
import numpy
import csv
import math
import random

###############################################################################
######################## NEURON SIMULATION ####################################
###############################################################################

# Creating the simulation
simulation = neuron.Simulation()

# Mapping the components and entities
entity__Axon_1_Neuron = model.AllEntities()["Axon_1_Neuron"]

# Adding a new AutomaticAxonNeuronSettings - add the neuron to the simulation
automatic_axon_neuron_settings = neuron.AutomaticAxonNeuronSettings()
component = [entity__Axon_1_Neuron]
simulation.Add(neuron.AutomaticAxonNeuronSettings(), component)

# Adding a new SourceSettings
# Link the EM field from EM simulation to the NEURON simulation
field_A = document.AllSimulations['Sim_A']
source_A = simulation.AddSource(field_A, "Overall Field")
source_A.Name = "Field A"

# Set up modulating pulse type and amplitude
source_A.PulseType = source_A.PulseType.enum.Monopolar
source_A.Amplitude = 1

axons = [entity__Axon_1_Neuron]
# Adding a new PointSensorSettings for recording
for axon in axons:
    sectionNames = simulation.GetSectionNames(axon)
    print(sectionNames)

    # Check each section of the axon and place a point sensor at each node
    for n in sectionNames:
        is_node=n.startswith('node')
        if is_node==True: 
            point_sensor_settings = simulation.AddPointSensor(axon)
            point_sensor_settings.SectionName = n
            point_sensor_settings.RecordV= True

# Editing SolverSettings - set duration of simulation
solver_settings = simulation.SolverSettings
solver_settings.Duration = 0.005, units.Seconds

# Add the simulation to the UI
document.AllSimulations.Add( simulation )