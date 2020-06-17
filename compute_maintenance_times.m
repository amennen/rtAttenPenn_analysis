% compute maintenance on each category

%% GIVEN subject attends to one of the categories, how long are they persisting on it (insted of total time spent)

% input is each matlab file and subject, go through their files and then save results?'
%%% SPECIFY SCREEN PARAMETERS %%
screenX = 1280;
screenY = 1024;
centerX = screenX/2; centerY = screenY/2;
imageSize2 = [300 300];
imageSize = imageSize2;
actual_imageSize =[400 400];

%imageSize2 = imageSize;
imageRect = [0 0 actual_imageSize(1) actual_imageSize(2)];
% placeholder for images
%border = screenX/20;
% try to scale border to area of screen
% maybe make a little bigger?
%border = (screenY - imageSize(2)*2)/2;
border = (screenY - imageSize(2)*2)/1.5;
% try 2/28 make border bigger
borderH = border/2;
% for upper right
X1 = centerX + borderH;
X2 = X1 + imageSize2(1);
Y2 = centerY - borderH;
Y1 = Y2 - imageSize2(2);
imPos(1,:) = [X1,Y1,X2,Y2];
% for upper left
X2 = centerX - borderH;
X1 = X2 - imageSize2(1);
Y2 = centerY - borderH;
Y1 = Y2 - imageSize2(2);
imPos(2,:) = [X1,Y1,X2,Y2];
% for lower left
X2 = centerX - borderH;
X1 = X2 - imageSize2(1);
Y1 = centerY + borderH;
Y2 = Y1 + imageSize2(2);
imPos(3,:) = [X1,Y1,X2,Y2];
% for lower right
X1 = centerX + borderH;
X2 = X1 + imageSize2(1);
Y1 = centerY + borderH;
Y2 = Y1 + imageSize2(2);
imPos(4,:) = [X1,Y1,X2,Y2];
resvec = [screenX screenY screenX screenY];
pos_1 = imPos(1,:)./resvec;
pos_2 = imPos(2,:)./resvec;
pos_3 = imPos(3,:)./resvec;
pos_4 = imPos(4,:)./resvec;
DYSPHORIC = 1;
THREAT = 2;
NEUTRAL = 3;
POSITIVE = 4;

subjects = [1,2,3,4,101,102,103,104,105, 106,107,108];
nsub = length(subjects);
ntrials = 20;
ndays=3; % eventually add 4
all_gaze_ratios = zeros(nsub,12,4,ndays);
all_neutral_ratios = zeros(nsub,8,4,ndays);
all_ratio_pts = zeros(nsub,20,ndays);


for s = 1:nsub
        subjectNum = subjects(s);
        for d_ind = 1:ndays
                subjectDay = d_ind;
                dataDir = ['subject' num2str(subjectNum) '/day' num2str(subjectDay) '/'];
                filename = findNewestFile(dataDir,[dataDir '/gazedata*.mat'])
                d = load(filename);
                vCount=0;
                fCount=0;
                for trial = 1:20
                        remote_start = d.timing.gaze.pic(trial);
                        remote_stop = d.timing.gaze.off(trial);
                        % now find the data between these time points
                        time_trial = d.GazeData.Timing.Remote{trial}; % 709 points
                        trial_rows = intersect(find(time_trial>=remote_start), find(time_trial<=remote_stop));

                        rightEyeAll = d.GazeData.Right{trial}(trial_rows,:);
                        leftEyeAll = d.GazeData.Left{trial}(trial_rows,:);
                        rightGazePoint2d.x = rightEyeAll(:,7);
                        rightGazePoint2d.y = rightEyeAll(:,8);
                        leftGazePoint2d.x = leftEyeAll(:,7);
                        leftGazePoint2d.y = leftEyeAll(:,8);
                        badrightX = find(rightGazePoint2d.x == -1);
                        badrightY = find(rightGazePoint2d.y == -1);
                        badleftX = find(leftGazePoint2d.x == -1);
                        badleftY = find(leftGazePoint2d.y == -1);
                        rightGazePoint2d.x(badrightX) = nan;
                        rightGazePoint2d.y(badrightY) = nan;
                        leftGazePoint2d.x(badleftX) = nan;
                        leftGazePoint2d.y(badrightY) = nan;
                        gaze.x = nanmean([rightGazePoint2d.x, leftGazePoint2d.x],2);
                        gaze.y = nanmean([rightGazePoint2d.y, leftGazePoint2d.y],2);

                        n_points = length(find(gaze.x > 0 | gaze.y >0));
                        % now instead of getting total number of points get timeseries first

                        all_ratio_pts(s,trial,d_ind) = n_points/length(gaze.x);
                        n_pos1 = find((gaze.x >= pos_1(1) & gaze.x<=pos_1(3)) & (gaze.y >= pos_1(2) & gaze.y<=pos_1(4)));
                        n_pos2 = find((gaze.x >= pos_2(1) & gaze.x<=pos_2(3)) & (gaze.y >= pos_2(2) & gaze.y<=pos_2(4)));
                        n_pos3 = find((gaze.x >= pos_3(1) & gaze.x<=pos_3(3)) & (gaze.y >= pos_3(2) & gaze.y<=pos_3(4)));
                        n_pos4 = find((gaze.x >= pos_4(1) & gaze.x<=pos_4(3)) & (gaze.y >= pos_4(2) & gaze.y<=pos_4(4)));

                        continuous_1 = length(find(diff(n_pos1) == 1));
                        continuous_2 = length(find(diff(n_pos2) == 1));
                        continuous_3 = length(find(diff(n_pos2) == 1));
                        continuous_4 = length(find(diff(n_pos2) == 1));
                        % should it be over points recorded or over when looking at one of the
                        % pictures?
                        total_time_images = length(n_pos1) + length(n_pos2) + length(n_pos3) + length(n_pos4);
                        r_pos1 = continuous_1/total_time_images;
                        r_pos2 = continuous_2/total_time_images;
                        r_pos3 = continuous_3/total_time_images;
                        r_pos4 = continuous_4/total_time_images;
                        allratios = [r_pos1 r_pos2 r_pos3 r_pos4];
                        if d.stim.trialType(trial) == 1
                                vCount = vCount + 1;
                                % then we have a valence trial
                                % do it a different way
                                all_gaze_ratios(s,vCount,d.stim.position(vCount,1),d_ind) = allratios(1);
                                all_gaze_ratios(s,vCount,d.stim.position(vCount,2),d_ind) = allratios(2);
                                all_gaze_ratios(s,vCount,d.stim.position(vCount,3),d_ind) = allratios(3);
                                all_gaze_ratios(s,vCount,d.stim.position(vCount,4),d_ind) = allratios(4);

                        else
                                % neutral filler trial
                                fCount = fCount + 1;
                                all_neutral_ratios(s,fCount,:,d_ind) = allratios;
                        end
                end
        end
end

% Save subject results to .mat file
save('maintenance_ratios.mat', 'all_gaze_ratios', 'all_neutral_ratios')