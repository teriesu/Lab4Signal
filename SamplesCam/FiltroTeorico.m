clear
%Lectura archivo csv
NameCSVAcX = 'CameraSamples1.csv';

DataCSVAcX = csvread(NameCSVAcX);


eje_yAcX = DataCSVAcX(:,1);
eje_yAcY = DataCSVAcX(:,2);
% Salida acelerometros
figure, 
plot(eje_yAcX)
hold on
plot(eje_yAcY)

% Data_AcX = fft(eje_y);
% stem(Data_Acx)
% 

% dataIn = eje_y;
%% Filtro IIR

fc = 5;
fs = 200;

[b,a] = cheby1(3,1,fc/(fs/2),'low')

%freqz(b,a)
dataOutAcX = filter(b,a,eje_yAcX);
dataOutAcY = filter(b,a,eje_yAcY);

%% Salidas 

% Salida filtrada de acelerometros
figure, 
plot(dataOutAcX)
hold on
plot(dataOutAcY)

not_filter = fft(eje_yAcX);
% filtered = fft(dataOutAcX);
hold off
figure, 
stem(abs(not_filter));
% figure, 
% hold on
% stem (abs(filtered))
