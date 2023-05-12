clear all
clc

% Read .csv file with time of first spike information
spikes = csvread("Titration_Spike_Time_Factor.csv");
neurons = spikes(:,1);
spike_times = spikes(:,2);
figure(1)
hold on

% Create raster plot for each waveform stimulus
scatter(spike_times(41:50),neurons(41:50),75,'o',"filled",'MarkerFaceColor','#BEA9DF')
scatter(spike_times(31:40),neurons(31:40),75,'o',"filled",'MarkerFaceColor','#779ECB')
scatter(spike_times(21:30),neurons(21:30),75,'o',"filled",'MarkerFaceColor','#BDD7EE')
scatter(spike_times(11:20),neurons(11:20),75,'o',"filled",'MarkerFaceColor','#C5E0B4')
scatter(spike_times(1:10),neurons(1:10),75,'o',"filled",'MarkerFaceColor','#FFE699')

sz = size(spike_times)

xlabel('Time (ms)','FontSize',18)
title('Time of First Spike','FontSize',18)
set(gca, 'YTick', [])
fontname(figure(1),"Times New Roman")
