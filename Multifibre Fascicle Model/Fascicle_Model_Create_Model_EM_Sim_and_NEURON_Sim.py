# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
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
import s4l_v1.materials.database as database

#import other modules
import sys, os
import numpy
import csv
import math
import random

def CreateModel(length,width,height,cyl_radius, per_rad, elec_dis, major_rad, minor_rad, radius, med_diam,med_dist,med_loc,med_rad,med_len):
	
	# set modeling unit to mm
	model.SetLengthUnits( units.MilliMeter )  

	# Endoneurium - Define the cylinder using diagonal points
	endoneurium = model.CreateSolidCylinder( Vec3(length,width/2,height), Vec3(length,-width/2,height), cyl_radius )
	endoneurium.Name = 'Endoneurium'
	
	# Perineurium -  Define using a solid tube
	perineurium = model.CreateSolidTube(Vec3(0,width/2,0), Vec3(length,-width,height), per_rad, cyl_radius)
	perineurium.Name = 'Perineurium'
	
	# Create a pair of cuff electrodes
	A_pos_elec=model.CreateSolidTube(Vec3(0,elec_dis/2,height/2), Vec3(0,1,0), major_rad, minor_rad)
	A_pos_elec.Name='A_pos_elec'
	A_neg_elec=model.CreateSolidTube(Vec3(0,-elec_dis/2,height/2), Vec3(0,1,0), major_rad, minor_rad)
	A_neg_elec.Name='A_neg_elec'
	
	# Creating axon distribution
	median_axons=diameters_list(med_diam,med_dist,10)
	median_types=sensory_vs_motor(median_axons,0.15)
	axons('Median',median_axons,median_types,med_loc,med_rad,med_len,2)
	
		
def EM_Sim(setup,structure, outer_sheath, pos_elec, neg_elec):

	#Create the simulation 
	sim = emlf.ElectroQsOhmicSimulation()
	sim.Name = setup['Name']

	#Set simulation frequncy
	sim.SetupSettings.Frequency = setup['Frequency']

	#Set material properties
	tissue_settings = emlf.MaterialSettings()
	component_1 = [structure]
	tissue_settings.Name = "Nerve"
	tissue_settings.ElectricProps.ConductivityAnisotropic = True
	long = setup['Endoneurium_Conductivity_Longitudinal'], Unit("S/m")
	tran = setup['Endoneurium_Conductivity_Transverse'], Unit("S/m")
	tissue_settings.ElectricProps.ConductivityDiagonalElements = numpy.array([long, 0.0, 0.0]), Unit("S/m") # xx, yy, zz
	tissue_settings.ElectricProps.ConductivityOffDiagonalElements = numpy.array([tran, 0.0, 0.0]), Unit("S/m") #xy, yz, zx
	sim.Add(tissue_settings, component_1)
	
	perineurium_settings = emlf.MaterialSettings()
	component_2 = [outer_sheath]
	perineurium_settings.ElectricProps.Conductivity = setup['Perineurium_Conductivity'], Unit("S/m")
	sim.Add(perineurium_settings, component_2)

	#Set boundary conditions
	boundary_pos = sim.AddBoundarySettings(pos_elec)
	boundary_pos.DirichletValue = setup['Magnitude']
	boundary_pos.Name = 'Dirichlet +'

	boundary_neg = sim.AddBoundarySettings(neg_elec)
	boundary_neg.DirichletValue = -1*setup['Magnitude']
	boundary_neg.Name = 'Dirichlet -'

	# Grid
	sim.GlobalGridSettings.ManualDiscretization = True
	sim.GlobalGridSettings.MaxStep = numpy.array([1, 1, 1]), units.MilliMeters
	sim.GlobalGridSettings.Resolution = numpy.array([0.01, 0.01, 0.01]), units.MilliMeters
	sim.GlobalGridSettings.ManualPadding = True
	sim.GlobalGridSettings.BottomPadding = sim.GlobalGridSettings.TopPadding = numpy.array([10, 10, 10]), units.MilliMeters

	manual_grid_settings = sim.AddManualGridSettings([structure])
	manual_grid_settings.MaxStep = numpy.array([0.06, 0.06, 0.06]), units.MilliMeters
	manual_grid_settings.Resolution = numpy.array([0.01, 0.01, 0.01]), units.MilliMeters
	
	manual_grid_settings = sim.AddManualGridSettings([outer_sheath])
	manual_grid_settings.MaxStep = numpy.array([0.06, 0.06, 0.06]), units.MilliMeters
	manual_grid_settings.Resolution = numpy.array([0.01, 0.01, 0.01]), units.MilliMeters

	# Voxels
	# Removing AutomaticVoxelerSettings Automatic Voxeler Settings
	automatic_voxeler_settings = [x for x in sim.AllSettings if isinstance(x, emlf.AutomaticVoxelerSettings) and x.Name == "Automatic Voxeler Settings"][0]
	sim.RemoveSettings(automatic_voxeler_settings)

	# Adding a new ManualVoxelerSettings
	manual_voxeler_settings = emlf.ManualVoxelerSettings()
	components = [structure]
	manual_voxeler_settings.Name = "Structure"
	manual_voxeler_settings.Priority = 3
	sim.Add(manual_voxeler_settings, components)
	
	# Adding a new ManualVoxelerSettings
	manual_voxeler_settings = emlf.ManualVoxelerSettings()
	components = [outer_sheath]
	manual_voxeler_settings.Name = "Outer Sheath"
	manual_voxeler_settings.Priority = 2
	sim.Add(manual_voxeler_settings, components)

	# Adding a new ManualVoxelerSettings
	manual_voxeler_settings = emlf.ManualVoxelerSettings()
	components = [pos_elec, neg_elec]
	manual_voxeler_settings.Name = "Electrodes"
	manual_voxeler_settings.Priority = 1
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

def diameters_list(diameters,distribution, N_fibres):
	### CREDIT TO LEEN JABBAN ### 

    # Get the number of fibres for each diameter 
    scaled_distribution=[element*(N_fibres/100) for element in distribution]
    rounded_distribution=[int(math.floor(element)) for element in scaled_distribution]
    check_sum=sum(rounded_distribution)

    # sort based on highest distribution first (for the next step)
    rounded_distribution,diameters=zip(*sorted(zip(rounded_distribution,diameters),reverse=True))
    
    # Change back to a list 
    rounded_distribution=list(rounded_distribution)
    diameters=list(diameters)

    # A way to get to the right number. Not great, but those numbers are an estimate anyway
    n=0
    while check_sum < N_fibres:
        rounded_distribution[n]=rounded_distribution[n]+1
        n=n+1
        check_sum=sum(rounded_distribution)

    # Create a list of fibre diameters
    result=[] 

    for i in range(len(diameters)):
        n=0
        while n< rounded_distribution[i]:
            result.append(diameters[i])
            n=n+1
          
    random.shuffle(result)
    return result

def sensory_vs_motor(Diameters, perc_motor):
    ### CREDIT TO LEEN JABBAN ### 
    num_motor=len(Diameters)*perc_motor
    type=[]
    for a in range(len(Diameters)):
        if a<=num_motor:
            type.append('motor')
        else:
            type.append('sensory')
    return type
	
def axons(nerve_name,Diameters,type,centre,R,length,length_axis):
    ### CREDIT TO LEEN JABBAN ### 
    folder=model.CreateGroup(nerve_name+'_Axon_Trajectories')
    a=0
    while a<len(Diameters):
        x=2*R*(-0.5+numpy.random.rand())
        y=2*R*(-0.5+numpy.random.rand())
        if (x*x+y*y<R*R):
            if length_axis==3:
                axon=model.CreatePolyLine([Vec3(centre[0]+x,centre[1]+y,length[0]),Vec3(centre[0]+x,centre[1]+y,length[1])])
            elif length_axis==2:
                axon=model.CreatePolyLine([Vec3(centre[0]+x,length[0],centre[1]+y),Vec3(centre[0]+x,length[1],centre[1]+y)])
            axon.Name=nerve_name+'_'+str(a)
            folder.Add(axon)
            DiscretizeAxonModel(axon.Name, Diameters[a],type[a],folder)
            a+=1

def DiscretizeAxonModel(Axon_name, Diameter, type,folder):
    ### CREDIT TO LEEN JABBAN ### 
	
    axon_entity = model.AllEntities()[Axon_name]

    if type=='motor':
        model_properties=model.MotorMrgNeuronProperties()
    elif type=='sensory':
        model_properties=model.SensoryMrgNeuronProperties()
    else:
        model_properties=model.MotorNeuronProperties()
    
    model_properties.AxonDiameter=Diameter
    discretized_axon = model.CreateAxonNeuron(axon_entity,model_properties)
    discretized_axon.Name = Axon_name +'_neuron'
    folder.Add(discretized_axon)

###################################
#############  Start  #############
###################################

#Define model parameters 
length=0 #mm
width=30 #mm
height=0 #mm
cyl_radius = 1.7 #mm
per_radius = cyl_radius + 0.1 #mm
major_radius = per_radius+0.125 #mm - electrode radius
minor_radius = per_radius #mm - electrode radius
elec_dis=3 #mm (distance between electrodes)
electrode_radius=1 #mm
time = 5 #ms
median_diameters=[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19] #um
median_distribution=[17.09,13.51,8.87,4.90,5.30,2.91,10.46,11.39,11.26,5.56,2.78,2.52,1.19,1.19,0.53,0.53] 
Median_nerve_location=[0,0]
Median_radius = cyl_radius
Median_length=[-20/2,20/2]

#Create the model
CreateModel(length,width,height,cyl_radius, per_radius, elec_dis, major_radius, minor_radius, electrode_radius,median_diameters,median_distribution,Median_nerve_location,Median_radius,Median_length)

#Define the entities
entities = model.AllEntities()
Endoneurium = entities['Endoneurium']
Perineurium = entities['Perineurium']
A_pos_elec = entities['A_pos_elec']
A_neg_elec = entities['A_neg_elec']

#Define EM simulation settings [frequency, magnitude, conductivity]
magnitude= 2 #v
p_conductivity= 0.002 #S/m
en_conductivity_l = 0.57 #S/m
en_conductivity_t = 0.08 #S/m
frequency=10 #Hz
sim_A_name='Sim_A'

settings_A={'Frequency':frequency,'Magnitude':magnitude,'Perineurium_Conductivity':p_conductivity, 'Endoneurium_Conductivity_Longitudinal':en_conductivity_l, 'Endoneurium_Conductivity_Transverse':en_conductivity_t, 'Name':sim_A_name }

#Create Electromagnetic simulation
Sim_A_results=EM_Sim(settings_A,Endoneurium,Perineurium, A_pos_elec, A_neg_elec)

###############################################################################
######################## NEURON SIMULATION ####################################
###############################################################################

# Creating the simulation
simulation = neuron.Simulation()

# Mapping the components and entities
entity__median_2_neuron = model.AllEntities()["Median_2_neuron"]
entity__median_7_neuron = model.AllEntities()["Median_7_neuron"]
entity__median_8_neuron = model.AllEntities()["Median_8_neuron"]
entity__median_4_neuron = model.AllEntities()["Median_4_neuron"]
entity__median_1_neuron = model.AllEntities()["Median_1_neuron"]
entity__median_9_neuron = model.AllEntities()["Median_9_neuron"]
entity__median_6_neuron = model.AllEntities()["Median_6_neuron"]
entity__median_3_neuron = model.AllEntities()["Median_3_neuron"]
entity__median_0_neuron = model.AllEntities()["Median_0_neuron"]
entity__median_5_neuron = model.AllEntities()["Median_5_neuron"]

# Adding a new AutomaticAxonNeuronSettings - add all neurons to the simulation
automatic_axon_neuron_settings = neuron.AutomaticAxonNeuronSettings()
components = [entity__median_0_neuron,entity__median_1_neuron,entity__median_2_neuron,entity__median_3_neuron,entity__median_4_neuron,entity__median_5_neuron,entity__median_6_neuron,entity__median_7_neuron,entity__median_8_neuron,entity__median_9_neuron]
simulation.Add(neuron.AutomaticAxonNeuronSettings(), components)

# Adding a new SourceSettings
# Link the EM field from EM simulation to the NEURON simulation
field_A = document.AllSimulations['Sim_A']
source_A = simulation.AddSource(field_A, "Overall Field")
source_A.Name = "Field A"

# Set up modulating pulse type and amplitude: two options provided, one for monopolar pulse and one for user defined waveforms for verification testing
## Monopolar pulse
source_A.PulseType = source_A.PulseType.enum.Monopolar
source_A.Amplitude = 1

## User-defined pulse for verification tests
#source_A.PulseType = source_A.PulseType.enum.UserDefined
#source_A.StimulusFilePath = u"C:\\Users\\harsh\\OneDrive - University of Bath\\Yr4 - Semester 2\\Sim4Life Models\\Multi_Fibre\\WORKING MODEL\\1MS_5V_1MS_7MS\\Mod_Pulse.txt"
#simulation.Add(source_A, components)

axons = [entity__median_0_neuron,entity__median_1_neuron,entity__median_2_neuron,entity__median_3_neuron,entity__median_4_neuron,entity__median_5_neuron,entity__median_6_neuron,entity__median_7_neuron,entity__median_8_neuron,entity__median_9_neuron]

# Adding a new PointSensorSettings for recording
for axon in axons:
    sectionNames = simulation.GetSectionNames(axon)
    print(sectionNames)
    
    # Check each section of the axon and place a point sensor at each node
    for n in sectionNames:
        #Only compute at nodes
        is_node=n.startswith('node')
        if is_node==True: 
            point_sensor_settings = simulation.AddPointSensor(axon)
            point_sensor_settings.SectionName = n
            point_sensor_settings.RecordV= True

# Editing SolverSettings - simulation duration 
solver_settings = simulation.SolverSettings
solver_settings.Duration = 0.005, units.Seconds

# Add the simulation to the UI
document.AllSimulations.Add( simulation )