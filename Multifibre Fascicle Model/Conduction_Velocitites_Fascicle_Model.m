clear all
clc

figure(1)

% Read file for conduction velocities
parameters = csvread("NH Parameters.csv")
diameters = parameters(:,1);
d_p = parameters(:,5); % Read diameters
CVs = parameters(:,6); % Read calculated conduction velocity column (from model)
expected_CVs = parameters (:,4); % Read expected conduction velocity column

hold on
plot(diameters,expected_CVs,'--','LineWidth',3, 'color',"#8FAADC") % Plot expected conduction velocities
scatter(d_p,CVs,130,'*',"k") % Scatter calculated conduction velocities
legend('Experimental Data','Model Data')
xlabel('Fibre Diameter (um)')
ylabel('Conduction Velocity (ms)')
title('Conduction Velocities')
fontname(figure(1),"Times New Roman")
hold off
