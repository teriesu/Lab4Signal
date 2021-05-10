imageFileNames = {'B:\Documents\Trabajos\Expedientes semestrales\2021-1\Señales\Fifth Laboratory\Images\im_2\2021-05-10_17-03-15.jpg',...
    'Images\im_2\2021-05-10_17-03-45.jpg',...
    'Images\im_2\2021-05-10_17-03-50.jpg',...
    'Images\im_2\2021-05-10_17-03-58.jpg',...
    'Images\im_2\2021-05-10_17-04-06.jpg',...
    'Images\im_2\2021-05-10_17-04-09.jpg',...
    'Images\im_2\2021-05-10_17-04-14.jpg',...
    'Images\im_2\2021-05-10_17-04-20.jpg',...
    'Images\im_2\2021-05-10_17-04-27.jpg',...
    'Images\im_2\2021-05-10_17-05-43.jpg',...
    }; %Pay attention to change the file directory!!

% Detect checkerboards in images
[imagePoints, boardSize, imagesUsed] = detectCheckerboardPoints(imageFileNames);
imageFileNames = imageFileNames(imagesUsed);

% Read the first image to obtain image size
originalImage = imread(imageFileNames{1});
[mrows, ncols, ~] = size(originalImage);

% Generate world coordinates of the corners of the squares
squareSize = 25;  % in units of 'millimeters'
worldPoints = generateCheckerboardPoints(boardSize, squareSize);

% Calibrate the camera
[cameraParams, imagesUsed, estimationErrors] = estimateCameraParameters(imagePoints, worldPoints, ...
    'EstimateSkew', false, 'EstimateTangentialDistortion', false, ...
    'NumRadialDistortionCoefficients', 2, 'WorldUnits', 'millimeters', ...
    'InitialIntrinsicMatrix', [], 'InitialRadialDistortion', [], ...
    'ImageSize', [mrows, ncols]);

% View reprojection errors
h1=figure; showReprojectionErrors(cameraParams);

% Visualize pattern locations
h2=figure; showExtrinsics(cameraParams, 'CameraCentric');

% Display parameter estimation errors
displayErrors(estimationErrors, cameraParams);

% For example, you can use the calibration data to remove effects of lens distortion.
undistortedImage = undistortImage(originalImage, cameraParams);

