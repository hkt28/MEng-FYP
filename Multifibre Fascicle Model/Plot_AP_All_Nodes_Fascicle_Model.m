clc
clear all

% Read all csv files in the present folder and extract data
files = dir('*.csv');
num_files = length(files);
results = cell(length(files), 1);
names = cell(length(files), 1);
titles = cell(length(files), 1);
for i = 1:num_files
  results{i} = xlsread(files(i).name);
  names{i} = files(i).name;
end

% Create titles for graphs
for i = 1:num_files
    titles{i} = strrep(names{i},'.csv',' ')
end

% Plot AP data for each neuron
num = length(results);
for i = 1:num
    f = cell2mat(results(i,1));
    s = size(f);
    k = 0.02;
    temp = titles(i,1);
    temp_label = diameters(i,1);
    figure(i)
    for j = 1:2:s(2)
        time = f(:,j);
        voltage = f(:,j+1) + k;
        hold on
        plot(time,voltage,'LineWidth',1)
        xlabel('Time (ms)')
        ylabel('Voltage (V)')
        title(string(temp),string(temp_label))
        fontname(figure(i),"Times New Roman")
        k = k + 0.02;
        hold off 
    end
end

