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
entity__Fascicle0_0_neuron = model.AllEntities()["Fascicle0_0_neuron"]
entity__Fascicle0_1_neuron = model.AllEntities()["Fascicle0_1_neuron"]
entity__Fascicle0_2_neuron = model.AllEntities()["Fascicle0_2_neuron"]
entity__Fascicle0_3_neuron = model.AllEntities()["Fascicle0_3_neuron"]
entity__Fascicle0_4_neuron = model.AllEntities()["Fascicle0_4_neuron"]

entity__Fascicle1_0_neuron = model.AllEntities()["Fascicle1_0_neuron"]
entity__Fascicle1_1_neuron = model.AllEntities()["Fascicle1_1_neuron"]
entity__Fascicle1_2_neuron = model.AllEntities()["Fascicle1_2_neuron"]
entity__Fascicle1_3_neuron = model.AllEntities()["Fascicle1_3_neuron"]
entity__Fascicle1_4_neuron = model.AllEntities()["Fascicle1_4_neuron"]

entity__Fascicle2_0_neuron = model.AllEntities()["Fascicle2_0_neuron"]
entity__Fascicle2_1_neuron = model.AllEntities()["Fascicle2_1_neuron"]
entity__Fascicle2_2_neuron = model.AllEntities()["Fascicle2_2_neuron"]
entity__Fascicle2_3_neuron = model.AllEntities()["Fascicle2_3_neuron"]
entity__Fascicle2_4_neuron = model.AllEntities()["Fascicle2_4_neuron"]

entity__Fascicle3_0_neuron = model.AllEntities()["Fascicle3_0_neuron"]
entity__Fascicle3_1_neuron = model.AllEntities()["Fascicle3_1_neuron"]
entity__Fascicle3_2_neuron = model.AllEntities()["Fascicle3_2_neuron"]
entity__Fascicle3_3_neuron = model.AllEntities()["Fascicle3_3_neuron"]
entity__Fascicle3_4_neuron = model.AllEntities()["Fascicle3_4_neuron"]

entity__Fascicle4_0_neuron = model.AllEntities()["Fascicle4_0_neuron"]
entity__Fascicle4_1_neuron = model.AllEntities()["Fascicle4_1_neuron"]
entity__Fascicle4_2_neuron = model.AllEntities()["Fascicle4_2_neuron"]
entity__Fascicle4_3_neuron = model.AllEntities()["Fascicle4_3_neuron"]
entity__Fascicle4_4_neuron = model.AllEntities()["Fascicle4_4_neuron"]

entity__Fascicle5_0_neuron = model.AllEntities()["Fascicle5_0_neuron"]
entity__Fascicle5_1_neuron = model.AllEntities()["Fascicle5_1_neuron"]
entity__Fascicle5_2_neuron = model.AllEntities()["Fascicle5_2_neuron"]
entity__Fascicle5_3_neuron = model.AllEntities()["Fascicle5_3_neuron"]
entity__Fascicle5_4_neuron = model.AllEntities()["Fascicle5_4_neuron"]

entity__Fascicle6_0_neuron = model.AllEntities()["Fascicle6_0_neuron"]
entity__Fascicle6_1_neuron = model.AllEntities()["Fascicle6_1_neuron"]
entity__Fascicle6_2_neuron = model.AllEntities()["Fascicle6_2_neuron"]
entity__Fascicle6_3_neuron = model.AllEntities()["Fascicle6_3_neuron"]
entity__Fascicle6_4_neuron = model.AllEntities()["Fascicle6_4_neuron"]

entity__Fascicle7_0_neuron = model.AllEntities()["Fascicle7_0_neuron"]
entity__Fascicle7_1_neuron = model.AllEntities()["Fascicle7_1_neuron"]
entity__Fascicle7_2_neuron = model.AllEntities()["Fascicle7_2_neuron"]
entity__Fascicle7_3_neuron = model.AllEntities()["Fascicle7_3_neuron"]
entity__Fascicle7_4_neuron = model.AllEntities()["Fascicle7_4_neuron"]

entity__Fascicle8_0_neuron = model.AllEntities()["Fascicle8_0_neuron"]
entity__Fascicle8_1_neuron = model.AllEntities()["Fascicle8_1_neuron"]
entity__Fascicle8_2_neuron = model.AllEntities()["Fascicle8_2_neuron"]
entity__Fascicle8_3_neuron = model.AllEntities()["Fascicle8_3_neuron"]
entity__Fascicle8_4_neuron = model.AllEntities()["Fascicle8_4_neuron"]

entity__Fascicle9_0_neuron = model.AllEntities()["Fascicle9_0_neuron"]
entity__Fascicle9_1_neuron = model.AllEntities()["Fascicle9_1_neuron"]
entity__Fascicle9_2_neuron = model.AllEntities()["Fascicle9_2_neuron"]
entity__Fascicle9_3_neuron = model.AllEntities()["Fascicle9_3_neuron"]
entity__Fascicle9_4_neuron = model.AllEntities()["Fascicle9_4_neuron"]

entity__Fascicle10_0_neuron = model.AllEntities()["Fascicle10_0_neuron"]
entity__Fascicle10_1_neuron = model.AllEntities()["Fascicle10_1_neuron"]
entity__Fascicle10_2_neuron = model.AllEntities()["Fascicle10_2_neuron"]
entity__Fascicle10_3_neuron = model.AllEntities()["Fascicle10_3_neuron"]
entity__Fascicle10_4_neuron = model.AllEntities()["Fascicle10_4_neuron"]

entity__Fascicle11_0_neuron = model.AllEntities()["Fascicle11_0_neuron"]
entity__Fascicle11_1_neuron = model.AllEntities()["Fascicle11_1_neuron"]
entity__Fascicle11_2_neuron = model.AllEntities()["Fascicle11_2_neuron"]
entity__Fascicle11_3_neuron = model.AllEntities()["Fascicle11_3_neuron"]
entity__Fascicle11_4_neuron = model.AllEntities()["Fascicle11_4_neuron"]

entity__Fascicle12_0_neuron = model.AllEntities()["Fascicle12_0_neuron"]
entity__Fascicle12_1_neuron = model.AllEntities()["Fascicle12_1_neuron"]
entity__Fascicle12_2_neuron = model.AllEntities()["Fascicle12_2_neuron"]
entity__Fascicle12_3_neuron = model.AllEntities()["Fascicle12_3_neuron"]
entity__Fascicle12_4_neuron = model.AllEntities()["Fascicle12_4_neuron"]

entity__Fascicle13_0_neuron = model.AllEntities()["Fascicle13_0_neuron"]
entity__Fascicle13_1_neuron = model.AllEntities()["Fascicle13_1_neuron"]
entity__Fascicle13_2_neuron = model.AllEntities()["Fascicle13_2_neuron"]
entity__Fascicle13_3_neuron = model.AllEntities()["Fascicle13_3_neuron"]
entity__Fascicle13_4_neuron = model.AllEntities()["Fascicle13_4_neuron"]

entity__Fascicle14_0_neuron = model.AllEntities()["Fascicle14_0_neuron"]
entity__Fascicle14_1_neuron = model.AllEntities()["Fascicle14_1_neuron"]
entity__Fascicle14_2_neuron = model.AllEntities()["Fascicle14_2_neuron"]
entity__Fascicle14_3_neuron = model.AllEntities()["Fascicle14_3_neuron"]
entity__Fascicle14_4_neuron = model.AllEntities()["Fascicle14_4_neuron"]

# Adding a new AutomaticAxonNeuronSettings
automatic_axon_neuron_settings = neuron.AutomaticAxonNeuronSettings()
components = [entity__Fascicle0_0_neuron, entity__Fascicle0_1_neuron, entity__Fascicle0_2_neuron, entity__Fascicle0_3_neuron, entity__Fascicle0_4_neuron, entity__Fascicle1_0_neuron, entity__Fascicle1_1_neuron, entity__Fascicle1_2_neuron, entity__Fascicle1_3_neuron, entity__Fascicle1_4_neuron, entity__Fascicle2_0_neuron, entity__Fascicle2_1_neuron, entity__Fascicle2_2_neuron, entity__Fascicle2_3_neuron, entity__Fascicle2_4_neuron, entity__Fascicle3_0_neuron, entity__Fascicle3_1_neuron, entity__Fascicle3_2_neuron, entity__Fascicle3_3_neuron, entity__Fascicle3_4_neuron, entity__Fascicle4_0_neuron, entity__Fascicle4_1_neuron, entity__Fascicle4_2_neuron, entity__Fascicle4_3_neuron, entity__Fascicle4_4_neuron, entity__Fascicle5_0_neuron, entity__Fascicle5_1_neuron, entity__Fascicle5_2_neuron, entity__Fascicle5_3_neuron, entity__Fascicle5_4_neuron, entity__Fascicle6_0_neuron, entity__Fascicle6_1_neuron, entity__Fascicle6_2_neuron, entity__Fascicle6_3_neuron, entity__Fascicle6_4_neuron, entity__Fascicle7_0_neuron, entity__Fascicle7_1_neuron, entity__Fascicle7_2_neuron, entity__Fascicle7_3_neuron, entity__Fascicle7_4_neuron, entity__Fascicle8_0_neuron, entity__Fascicle8_1_neuron, entity__Fascicle8_2_neuron, entity__Fascicle8_3_neuron, entity__Fascicle8_4_neuron, entity__Fascicle9_0_neuron, entity__Fascicle9_1_neuron, entity__Fascicle9_2_neuron, entity__Fascicle9_3_neuron, entity__Fascicle9_4_neuron, entity__Fascicle10_0_neuron, entity__Fascicle10_1_neuron, entity__Fascicle10_2_neuron, entity__Fascicle10_3_neuron, entity__Fascicle10_4_neuron, entity__Fascicle11_0_neuron, entity__Fascicle11_1_neuron, entity__Fascicle11_2_neuron, entity__Fascicle11_3_neuron, entity__Fascicle11_4_neuron, entity__Fascicle12_0_neuron, entity__Fascicle12_1_neuron, entity__Fascicle12_2_neuron, entity__Fascicle12_3_neuron, entity__Fascicle12_4_neuron, entity__Fascicle13_0_neuron, entity__Fascicle13_1_neuron, entity__Fascicle13_2_neuron, entity__Fascicle13_3_neuron, entity__Fascicle13_4_neuron, entity__Fascicle14_0_neuron, entity__Fascicle14_1_neuron, entity__Fascicle14_2_neuron, entity__Fascicle14_3_neuron, entity__Fascicle14_4_neuron]
simulation.Add(neuron.AutomaticAxonNeuronSettings(), components)

# Adding a new SourceSettings and linking EM field from EM simulation
field_A = document.AllSimulations['Sim_A']
source_A = simulation.AddSource(field_A, "Overall Field")
source_A.Name = "Field A"
source_A.PulseType = source_A.PulseType.enum.Monopolar
source_A.Amplitude = 1

# Adding a new PointSensorSettings for recording
axons = [entity__Fascicle0_0_neuron, entity__Fascicle0_1_neuron, entity__Fascicle0_2_neuron, entity__Fascicle0_3_neuron, entity__Fascicle0_4_neuron, entity__Fascicle1_0_neuron, entity__Fascicle1_1_neuron, entity__Fascicle1_2_neuron, entity__Fascicle1_3_neuron, entity__Fascicle1_4_neuron, entity__Fascicle2_0_neuron, entity__Fascicle2_1_neuron, entity__Fascicle2_2_neuron, entity__Fascicle2_3_neuron, entity__Fascicle2_4_neuron, entity__Fascicle3_0_neuron, entity__Fascicle3_1_neuron, entity__Fascicle3_2_neuron, entity__Fascicle3_3_neuron, entity__Fascicle3_4_neuron, entity__Fascicle4_0_neuron, entity__Fascicle4_1_neuron, entity__Fascicle4_2_neuron, entity__Fascicle4_3_neuron, entity__Fascicle4_4_neuron, entity__Fascicle5_0_neuron, entity__Fascicle5_1_neuron, entity__Fascicle5_2_neuron, entity__Fascicle5_3_neuron, entity__Fascicle5_4_neuron, entity__Fascicle6_0_neuron, entity__Fascicle6_1_neuron, entity__Fascicle6_2_neuron, entity__Fascicle6_3_neuron, entity__Fascicle6_4_neuron, entity__Fascicle7_0_neuron, entity__Fascicle7_1_neuron, entity__Fascicle7_2_neuron, entity__Fascicle7_3_neuron, entity__Fascicle7_4_neuron, entity__Fascicle8_0_neuron, entity__Fascicle8_1_neuron, entity__Fascicle8_2_neuron, entity__Fascicle8_3_neuron, entity__Fascicle8_4_neuron, entity__Fascicle9_0_neuron, entity__Fascicle9_1_neuron, entity__Fascicle9_2_neuron, entity__Fascicle9_3_neuron, entity__Fascicle9_4_neuron, entity__Fascicle10_0_neuron, entity__Fascicle10_1_neuron, entity__Fascicle10_2_neuron, entity__Fascicle10_3_neuron, entity__Fascicle10_4_neuron, entity__Fascicle11_0_neuron, entity__Fascicle11_1_neuron, entity__Fascicle11_2_neuron, entity__Fascicle11_3_neuron, entity__Fascicle11_4_neuron, entity__Fascicle12_0_neuron, entity__Fascicle12_1_neuron, entity__Fascicle12_2_neuron, entity__Fascicle12_3_neuron, entity__Fascicle12_4_neuron, entity__Fascicle13_0_neuron, entity__Fascicle13_1_neuron, entity__Fascicle13_2_neuron, entity__Fascicle13_3_neuron, entity__Fascicle13_4_neuron, entity__Fascicle14_0_neuron, entity__Fascicle14_1_neuron, entity__Fascicle14_2_neuron, entity__Fascicle14_3_neuron, entity__Fascicle14_4_neuron]
nodes = []
for axon in axons:
    point_sensor_settings = simulation.AddPointSensor([axon])
    point_sensor_settings.Name = str(axon)
    sectionNames = simulation.GetSectionNames(axon)
    for n in sectionNames:
        is_node=n.startswith('node')
        if is_node==True: 
            nodes.append(n)
    # Place a point sensor only at the second to last node of the axon
    for m in range(len(nodes)):
        if m == (len(nodes) - 2):
            point_sensor_settings = simulation.AddPointSensor(axon)
            point_sensor_settings.SectionName = nodes[m]
            point_sensor_settings.RecordV= True
            point_sensor_settings.RelativePosition = 0
        else:
            print('No sensor placed')
    nodes = []

# Editing SolverSettings - provide simulation duration
solver_settings = simulation.SolverSettings
solver_settings.Duration = 0.01, units.Seconds

# Add the simulation to the UI
document.AllSimulations.Add( simulation )