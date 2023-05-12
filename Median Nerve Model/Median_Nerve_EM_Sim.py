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
import s4l_v1.materials.database as database

#import other modules
import sys, os
import numpy
import csv
import math
import random

def EM_Sim(setup,structure, outer_sheath, pos_elec, neg_elec, fascicles):

	#Create the simulation 
	sim = emlf.ElectroQsOhmicSimulation()
	sim.Name = setup['Name']

	#Set simulation frequncy
	sim.SetupSettings.Frequency = setup['Frequency']

	#Set material properties
	# Nerve - Internal epineurium
	nerve_settings = emlf.MaterialSettings()
	component_1 = [structure]
	nerve_settings.ElectricProps.Conductivity = setup['Median_Conductivity'], Unit("S/m")
	sim.Add(nerve_settings, component_1)
	
	# Outer tube - Epineurium
	epineurium_settings = emlf.MaterialSettings()
	component_2 = [outer_sheath]
	epineurium_settings.ElectricProps.Conductivity = setup['Epineurium_Conductivity'], Unit("S/m")
	sim.Add(epineurium_settings, component_2)
	count = 0
	
	# Fascicles
	for i in fascicles:
		fascicle_settings = emlf.MaterialSettings()
		mat = database["IT'IS LF 4.1"]["Nerve"]
		component = [i]
		fascicle_settings.Name = "Nerve" + str(count)
		fascicle_settings.MassDensity = 1075.0, Unit("kg/m^3")
		fascicle_settings.ElectricProps.Conductivity = setup['Fascicle_Conductivity(l)'], Unit("S/m")
		fascicle_settings.ElectricProps.RelativePermittivity = 8070774.918683227
		count = count +1
		sim.Add(fascicle_settings, component)

	#Set boundary conditions
	boundary_pos = sim.AddBoundarySettings(pos_elec)
	boundary_pos.DirichletValue = setup['Magnitude']
	boundary_pos.Name = 'Dirichlet +'

	boundary_neg = sim.AddBoundarySettings(neg_elec)
	boundary_neg.DirichletValue = -1*setup['Magnitude']
	boundary_neg.Name = 'Dirichlet -'

	# Grid Settings
	sim.GlobalGridSettings.ManualDiscretization = True
	sim.GlobalGridSettings.MaxStep = numpy.array([1, 1, 1]), units.MilliMeters
	sim.GlobalGridSettings.Resolution = numpy.array([0.1, 0.1, 0.1]), units.MilliMeters
	sim.GlobalGridSettings.ManualPadding = True
	sim.GlobalGridSettings.BottomPadding = sim.GlobalGridSettings.TopPadding = numpy.array([10, 10, 10]), units.MilliMeters
	
	# Nerve
	manual_grid_settings = sim.AddManualGridSettings([structure])
	manual_grid_settings.MaxStep = numpy.array([0.1, 0.1, 0.1]), units.MilliMeters
	manual_grid_settings.Resolution = numpy.array([0.1, 0.1, 0.1]), units.MilliMeters
	
	# Epineurium
	manual_grid_settings = sim.AddManualGridSettings([outer_sheath])
	manual_grid_settings.MaxStep = numpy.array([0.1, 0.1, 0.1]), units.MilliMeters
	manual_grid_settings.Resolution = numpy.array([0.1, 0.1, 0.1]), units.MilliMeters
	
	# Fascicles
	for i in fascicles:
		manual_grid_settings = sim.AddManualGridSettings([i])
		manual_grid_settings.MaxStep = numpy.array([0.1, 0.1, 0.1]), units.MilliMeters
		manual_grid_settings.Resolution = numpy.array([0.1, 0.1, 0.1]), units.MilliMeters
	
	# Voxels
	# Removing AutomaticVoxelerSettings Automatic Voxeler Settings
	automatic_voxeler_settings = [x for x in sim.AllSettings if isinstance(x, emlf.AutomaticVoxelerSettings) and x.Name == "Automatic Voxeler Settings"][0]
	sim.RemoveSettings(automatic_voxeler_settings)

	# Adding a new ManualVoxelerSettings - Nerve
	manual_voxeler_settings = emlf.ManualVoxelerSettings()
	components = [structure]
	manual_voxeler_settings.Name = "Structure"
	manual_voxeler_settings.Priority = 1
	sim.Add(manual_voxeler_settings, components)
	
	# Adding a new ManualVoxelerSettings - Epineurium
	manual_voxeler_settings = emlf.ManualVoxelerSettings()
	components = [outer_sheath]
	manual_voxeler_settings.Name = "Outer Sheath"
	manual_voxeler_settings.Priority = 2
	sim.Add(manual_voxeler_settings, components)

	# Adding a new ManualVoxelerSettings - Electrodes
	manual_voxeler_settings = emlf.ManualVoxelerSettings()
	components = [pos_elec, neg_elec]
	manual_voxeler_settings.Name = "Electrodes"
	manual_voxeler_settings.Priority = 3
	sim.Add(manual_voxeler_settings, components)
	
	# Adding a new ManualVoxelerSettings - Fascicles
	manual_voxeler_settings = emlf.ManualVoxelerSettings()
	components = fascicles
	manual_voxeler_settings.Name = "Fascicles"
	manual_voxeler_settings.Priority = 4
	sim.Add(manual_voxeler_settings, components)

	# Solver settings
	sim.SolverSettings.PredefinedTolerances = sim.SolverSettings.PredefinedTolerances.enum.High

	# Update the materials with the new frequency parameters
	sim.UpdateAllMaterials()

	# Update the grid with the new parameters
	sim.UpdateGrid()

	#Add simulation to document 
	document.AllSimulations.Add( sim )
	sim.CreateVoxels()
	sim.RunSimulation()
	results = sim.Results()
	return results


#Define EM Stimulation parameters 
magnitude= 2 #v
ep_conductivity= 0.083 #S/m, epineurium
med_conductivity = 0.083 #S/m, epineurium (internal)
l_fasc_conductivity = 0.57 #S/m, endoneurium longitudinal
t_fasc_conductivity = 0.08 #S/m, endoneurium transverse
frequency=20 #Hz

#Define the entities
entities = model.AllEntities()
Median = entities['Median']
Epineurium = entities['Epineurium']
Fascicle0 = entities['Fascicle0']
Fascicle1 = entities['Fascicle1']
Fascicle2 = entities['Fascicle2']
Fascicle3 = entities['Fascicle3']
Fascicle4 = entities['Fascicle4']
Fascicle5 = entities['Fascicle5']
Fascicle6 = entities['Fascicle6']
Fascicle7 = entities['Fascicle7']
Fascicle8 = entities['Fascicle8']
Fascicle9 = entities['Fascicle9']
Fascicle10 = entities['Fascicle10']
Fascicle11 = entities['Fascicle11']
Fascicle12 = entities['Fascicle12']
Fascicle13 = entities['Fascicle13']
Fascicle14 = entities['Fascicle14']
A_pos_elec = entities['A_pos_elec']
A_neg_elec = entities['A_neg_elec']

fascicles = [Fascicle0, Fascicle1, Fascicle2, Fascicle3, Fascicle4, Fascicle5, Fascicle6, Fascicle7, Fascicle8, Fascicle9, Fascicle10, Fascicle11, Fascicle12, Fascicle13, Fascicle14]

#Define simulation settings [frequency, magnitude, conductivity]
sim_A_name='Sim_A'

settings_A={'Frequency':frequency,'Magnitude':magnitude,'Epineurium_Conductivity':ep_conductivity, 'Median_Conductivity':med_conductivity, 'Fascicle_Conductivity(l)': l_fasc_conductivity, 'Fascicle_Conductivity(t)': t_fasc_conductivity, 'Name':sim_A_name }

#Create Electromagnetic simulation
Sim_A_results=EM_Sim(settings_A,Median,Epineurium, A_pos_elec, A_neg_elec, fascicles)



