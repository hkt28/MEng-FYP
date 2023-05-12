clear all
clc

% Read the csv file containing action potential data at the specified node
Test_1 = csvread('NH_EM_2_NEURON_0.05.csv');
file_size = size(Test_1);

% Calculation of percentage activation in each fascicle
percentages = zeros(15,1);
upper_counter = 1;

% Read the file in sets of 10 columns - corresponding to the 5 neurons in
% each fascicle
for i=1:10:file_size(2)
    fasc_act = zeros(5,1);
    counter = 1;

    % Read each voltage column for each neuron
    for j=i:2:(i+9)
        time = Test_1(:,j);
        voltage = Test_1(:,j+1);
        size_voltage = size(voltage);

        % Check if neuron has been activated or not
        for k=1:1:size_voltage(1)
            if voltage(k) >= 0
                activated = 1;
                break
            else
                activated = 0;
            end
        end
        fasc_act(counter,1) = activated;
        counter = counter+1;
    end
    frac = 0;
    
    % Calculate percentage activation for each fascicle
    for x=1:1:5
        if fasc_act(x) == 1
            frac = frac+1;
        end
    end
    perc = ((frac/5)*100);
    percentages(upper_counter) = perc % Display percentage activation for each fascicle
    upper_counter = upper_counter + 1;
end