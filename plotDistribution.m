close all
clear
clc

while 1
    try
        data = load('distribution.csv');
        surf(data)
        view(0, 90)
        axis ij
        colorbar
        pause(0.1)
    catch
        pause(0.01)
    end
end