clear all
clc

params = csvread("NH Titration Factors.csv");
diameters = params(:,1); % diameters
ats = params(:,3)*2; % activation thresholds
ds = params(:,2);
%AT = [diameters,ats]

N = 3;
xvec = linspace(min(diameters), max(diameters), N);
yvec = linspace(min(ds), max(ds), N);
[X, Y] = ndgrid(xvec, yvec);
F = scatteredInterpolant(diameters, ds, ats);
Z = F(X, Y);

figure(1)
surf(X, Y, Z, 'edgecolor', 'none');
hold on
%c = linspace(1,10,length(diameters));
%plot3(diameters,ds,ats,'.','MarkerSize',15)
ax = gca;
ax.FontSize = 15;  % Font Size of 15
xlabel('Diameters ({\mu}m)')
ylabel('Distance from electrodes (mm)')
zlabel('Activation Thresholds (V)')
title('Activation Thresholds versus Fibre Diameter and Location')
fontname(figure(1),"Times New Roman")

% figure(2)
% c = linspace(1,10,length(diameters));
% scatter3(diameters,ds,ats,75,c,'filled')
% colorbar
% xlabel('Diameters (um)')
% ylabel('Distance from electrodes (mm)')
% zlabel('Activation Thresholds (V)')
