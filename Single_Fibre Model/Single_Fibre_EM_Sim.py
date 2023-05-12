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
import numpy


def EM_Sim(setup,structure, pos_elec, neg_elec):

	#Create the simulation and create a name
	sim = emlf.ElectroQsOhmicSimulation()
	sim.Name = setup['Name']

	#Set simulation frequncy
	sim.SetupSettings.Frequency = setup['Frequency']

	#Set material properties for the nerve
	nerve_settings = emlf.MaterialSettings()
	nerve_settings.Name = "Nerve"
	component_1 = [structure]
	nerve_settings.ElectricProps.Conductivity = setup['Conductivity(l)'], Unit("S/m")
	sim.Add(nerve_settings, component_1)

	#Set boundary conditions and provide magnitude values for the stimulating electrodes
	boundary_pos = sim.AddBoundarySettings(pos_elec)
	boundary_pos.DirichletValue = setup['Magnitude']
	boundary_pos.Name = 'Dirichlet +'

	boundary_neg = sim.AddBoundarySettings(neg_elec)
	boundary_neg.DirichletValue = -1*setup['Magnitude']
	boundary_neg.Name = 'Dirichlet -'

	## Grid Settings ##
	sim.GlobalGridSettings.ManualDiscretization = True
	sim.GlobalGridSettings.MaxStep = numpy.array([1, 1, 1]), units.MilliMeters
	sim.GlobalGridSettings.Resolution = numpy.array([0.1, 0.1, 0.1]), units.MilliMeters
	sim.GlobalGridSettings.ManualPadding = True
	sim.GlobalGridSettings.BottomPadding = sim.GlobalGridSettings.TopPadding = numpy.array([10, 10, 10]), units.MilliMeters
	
	# Nerve grid settings
	manual_grid_settings = sim.AddManualGridSettings([structure])
	manual_grid_settings.MaxStep = numpy.array([0.1, 0.1, 0.1]), units.MilliMeters
	manual_grid_settings.Resolution = numpy.array([0.1, 0.1, 0.1]), units.MilliMeters
	
	## Voxel Settings ##

	# Removing AutomaticVoxelerSettings Automatic Voxeler Settings
	automatic_voxeler_settings = [x for x in sim.AllSettings if isinstance(x, emlf.AutomaticVoxelerSettings) and x.Name == "Automatic Voxeler Settings"][0]
	sim.RemoveSettings(automatic_voxeler_settings)

	# Adding a new ManualVoxelerSettings - Nerve
	manual_voxeler_settings = emlf.ManualVoxelerSettings()
	components = [structure]
	manual_voxeler_settings.Name = "Structure"
	manual_voxeler_settings.Priority = 1
	sim.Add(manual_voxeler_settings, components)

	# Adding a new ManualVoxelerSettings - Electrodes
	manual_voxeler_settings = emlf.ManualVoxelerSettings()
	components = [pos_elec, neg_elec]
	manual_voxeler_settings.Name = "Electrodes"
	manual_voxeler_settings.Priority = 2
	sim.Add(manual_voxeler_settings, components)

	# Solver settings
	sim.SolverSettings.PredefinedTolerances = sim.SolverSettings.PredefinedTolerances.enum.High

	# Update the materials with the new frequency parameters
	sim.UpdateAllMaterials()

	# Update the grid with the new parameters
	sim.UpdateGrid()

	#Add simulation to document and create voxels
	document.AllSimulations.Add( sim )
	sim.CreateVoxels()
	sim.RunSimulation()
	results = sim.Results()
	return results


#Define EM Stimulation parameters 
magnitude= 0.5 #v
conductivity= 1 #S/m
frequency=10 #Hz
sim_A_name='Sim_A'

#Define the entities
entities = model.AllEntities()
Median = entities['Median']
Epineurium = entities['Epineurium']
A_pos_elec = entities['A_pos_elec']
A_neg_elec = entities['A_neg_elec']

settings_A={'Frequency':frequency,'Magnitude':magnitude,'Conductivity':conductivity, 'Name':sim_A_name }

#Create Electromagnetic simulation
Sim_A_results=EM_Sim(settings_A,Median,Epineurium, A_pos_elec, A_neg_elec)