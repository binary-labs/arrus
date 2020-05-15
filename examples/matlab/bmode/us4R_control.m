
%% Parameters
% Hardware
nArius      = 2;
probeName	= 'SL1543';

%% Initialize the system
us          = us4R(nArius,probeName);

%% Set the TX/RX parameters
us.setSeqParams(	'sequenceType',     'pwi', ...
                    'txCenterElement',  [], ...
                    'txApertureCenter', zeros(1,1), ...
                    'txApertureSize',   192, ...
                    'rxApertureSize',   192, ...
                    'txFocus',          inf(1,1), ...
                    'txAngle',          zeros(1,1), ...
                    'speedOfSound',     1450, ...
                    'txFrequency',      7e6, ...
                    'txNPeriods',       2, ...
                    'rxNSamples',       6*1024, ...
                    'txPri',            125);
                
%% Set the reconstruction parameters
[b,a] = butter(2,[0.5 1.5]*7/(65/2),'bandpass');
% del = phasez(b,a,[0 cutoffMean],acquisitionParameters.rx.samplingFrequency) ...
%     /(2*pi)/acquisitionParameters.tx.frequency*acquisitionParameters.rx.samplingFrequency;
% del = -del(2)/acquisitionParameters.rx.samplingFrequency;
del         = 0;

us.setRecParams(	'filterEnable',     true, ...
                    'filterACoeff',     a, ...
                    'filterBCoeff',     b, ...
                    'filterDelay',      del, ...
                    'iqEnable',         true, ...
                    'cicOrder',         2, ...
                    'decimation',       4, ...
                    'xGrid',            (-20:0.05:20)*1e-3, ...
                    'zGrid',            (  0:0.05:60)*1e-3);
                
%% Run the TX/RX/REC loop
us.run;
