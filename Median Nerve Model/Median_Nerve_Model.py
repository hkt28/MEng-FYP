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


def CreateModel(length,width,height, fasc_no, cyl_radius, epi_rad, elec_dis, major_rad, minor_rad, med_diam,med_dist,med_len):
	
	# set modeling unit to mm
	model.SetLengthUnits( units.MilliMeter )  

	#Define the cylinder using diagonal points - internal epineurium
	median = model.CreateSolidCylinder( Vec3(length,((width/2)+2),height), Vec3(length,((-width/2)-2),height), cyl_radius )
	median.MaterialName = 'Nerve'
	median.Name = 'Median'
	
	# Create the fascicles at random locations with a random distribution of radii
	circles = []
	TOTAL = []
	
	# Check that cylinders drawn at random co-ordinates with random radii do not overlap 
	while len(circles) < fasc_no:
		x = random.uniform((-cyl_radius+1.25),(cyl_radius-1.25))
		y = random.uniform((-cyl_radius+1.25),(cyl_radius-1.25))
		r = random.uniform(0.3,0.7)
		print('x:',x)
		print('y:',y)
		print('r:',r)

		overlapping = False

		for i in circles:
			other = i
			d = math.sqrt(((x-other[0])**2) + ((y-other[1])**2))
			if (d < (other[2] + r)):
				overlapping = True
				print(i)
        
		if overlapping == False:
            # Add the correct combinations to a large list
			circles.append([x,y,r])
	
	# Create fascicles with random distributions of fibres
	count = 0
	for j in circles:
		CreateFascicles(j[0],width,j[1],j[2],med_diam,med_dist,[j[0],j[1]],j[2],med_len,('Fascicle'+str(count)))
		med_loc = [j[0],j[1]]
		med_rad = j[2]
		nerve_name = ('Fascicle'+str(count))
		median_axons=diameters_list(med_diam,med_dist,5)
		median_types=sensory_vs_motor(median_axons,0.15)
		axons(nerve_name,median_axons,median_types,med_loc,med_rad,med_len,2)
		count = count +1
    
	# Define the epineurium using a solid tube
	epineurium = model.CreateSolidTube(Vec3(0,((width/2)+2),0), Vec3(length,(-width-4),height), epi_rad, cyl_radius)
	epineurium.Name = 'Epineurium'
	
	
	# Create a pairs of cuff electrodes
	A_pos_elec=model.CreateSolidTube(Vec3(0,((elec_dis/2)+0.5),height/2), Vec3(0,1,0), major_rad, minor_rad)
	A_pos_elec.Name='A_pos_elec'
	A_neg_elec=model.CreateSolidTube(Vec3(0,((-elec_dis/2)-0.5),height/2), Vec3(0,1,0), major_rad, minor_rad)
	A_neg_elec.Name='A_neg_elec'
	

def CreateFascicles(length,width,height,fasc_radius,med_diam,med_dist,med_loc,med_rad,med_len,nerve_name):
	model.SetLengthUnits( units.MilliMeter )  
	fascicle = model.CreateSolidCylinder( Vec3((length),((width/2)+2),height), Vec3((length),((-width/2)-2),height), fasc_radius )
	fascicle.MaterialName = 'Nerve'
	fascicle.Name = nerve_name


def diameters_list(diameters,distribution, N_fibres):
    ## CREDIT TO LEEN JABBAN ## 
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
    ## CREDIT TO LEEN JABBAN ## 

    num_motor=len(Diameters)*perc_motor
    type=[]
    for a in range(len(Diameters)):
        if a<=num_motor:
            type.append('motor')
        else:
            type.append('sensory')
    return type
	
def axons(nerve_name,Diameters,type,centre,R,length,length_axis):
    ## CREDIT TO LEEN JABBAN ## 

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
    ## CREDIT TO LEEN JABBAN ## 

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
width=150 #mm
height=0 #mm
fasc_no = 15
cyl_radius = 3 #mm
epi_radius = cyl_radius + 0.1
elec = cyl_radius + 0.1
major_radius = elec+0.125 #mm - electrode radius
minor_radius = elec #mm - electrode radius
elec_dis=3 #mm (distance between electrodes)
electrode_radius=1 #mm
median_diameters=[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
median_distribution=[17.09,13.51,8.87,4.90,5.30,2.91,10.46,11.39,11.26,5.56,2.78,2.52,1.19,1.19,0.53,0.53] 
Median_length=[-50/2,50/2]

#Create the model
CreateModel(length,width,height, fasc_no, cyl_radius, epi_radius, elec_dis, major_radius, minor_radius,median_diameters,median_distribution,Median_length)

