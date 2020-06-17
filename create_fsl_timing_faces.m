%% SPECIFY THESE THINGS FIRTST
subjectId = 'RT025';
subjectNum=5;
%subjectDay= 2; % PUT 1 OR 2 for FACES ---> day 1 or day 3 of scanning, but day 2 of the faces task
%% MAKE SURE CORTRECT
for subjectDay=1:2
%% now to through eveyrthing
task_path = '/data/jag/cnds/amennen/rtAttenPenn/fmridata/behavdata/faces';
save_path = '/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level/timing_files';

filePath = [task_path '/' subjectId];
% first we need to copy as a text file because importdata doesn't like log files here for some reason
fileToDir = [filePath '/' subjectId '_Day' num2str(subjectDay) '_Scanner_ABCD_AB_FaceMatching'];
fileToLoad = findNewestFile(filePath,[fileToDir '*.log']);
unix(sprintf('cp %s.log %s.txt',fileToLoad(1:end-4),fileToLoad(1:end-4)));
fileToLoad = findNewestFile(filePath, [fileToDir '*.txt'])

if ~isempty(fileToLoad)
    d = importdata(fileToLoad);
else
    error('Wrong file name!!!');
end

%% first just get all timing
tr = 2;
nVols=5;
toDel = tr * nVols;
trigger_str = 'Keypress: 5';
start_str = 'Keypress: q';
trial = 'New trial';
nentries = size(d,1);
trial_startA = [];
trial_startB = [];
condition_A = [];
condition_B = [];
LOOKFORTRIGA = 1;
LOOKFORTRIGB = 1;
for e=1:nentries
    thisrow = d{e};
    if LOOKFORTRIGA
        if ~isempty(strfind(thisrow, trigger_str)) % first trigger
            split_row = strsplit(thisrow, ' ');
            trig_timeA = str2num(split_row{1});
            LOOKFORTRIGA = 0;
        end
    end
    if ~isempty(strfind(thisrow, start_str)) && ~LOOKFORTRIGA
        frontind = 0;
        while LOOKFORTRIGB
            frontind = frontind + 1;
            frontrow = d{e+frontind};
            if ~isempty(strfind(frontrow,trigger_str))
                split_row = strsplit(frontrow, ' ');
                trig_timeB = str2num(split_row{1});
                LOOKFORTRIGB = 0;
            end
        end
    end
    % now get every trial start
    if ~isempty(strfind(thisrow, trial))
        split_row = strsplit(thisrow, ' ');
        AB = split_row{8};
        
        
        if ~isempty(strfind(AB,'A')) % then in the A run
            trial_startA(end+1) = str2num(split_row{1});
        elseif ~isempty(strfind(AB,'B'))
            trial_startB(end+1) = str2num(split_row{1});
        end
    end
end

%%
bids_id = sprintf('sub-%.3i', subjectNum);
if subjectDay==2
    subjectDay=3;
end
ses_id = sprintf('ses-%.2i', subjectDay) % this is because scanning session 3 is day 2 for them doing the task
save_file_path = [save_path '/' bids_id '/' ses_id ];
if ~exist(save_file_path)
    mkdir(save_file_path);
end;
fileID_A1 = fopen(sprintf('%s/A_neutral.txt',save_file_path), 'w');
fileID_A2 = fopen(sprintf('%s/A_object.txt',save_file_path), 'w');
fileID_A3 = fopen(sprintf('%s/A_happy.txt',save_file_path), 'w');
fileID_A4 = fopen(sprintf('%s/A_fearful.txt',save_file_path), 'w');
fileID_A5 = fopen(sprintf('%s/A_fixation.txt',save_file_path), 'w');

fileID_B1 = fopen(sprintf('%s/B_neutral.txt',save_file_path), 'w');
fileID_B2 = fopen(sprintf('%s/B_object.txt',save_file_path), 'w');
fileID_B3 = fopen(sprintf('%s/B_happy.txt',save_file_path), 'w');
fileID_B4 = fopen(sprintf('%s/B_fearful.txt',save_file_path), 'w');
fileID_B5 = fopen(sprintf('%s/B_fixation.txt',save_file_path), 'w');
%%
Aind=0;
Bind=0;
trigger_str = 'Keypress: 5';
start_str = 'Keypress: q';
trial = 'New trial';
nentries = size(d,1);
condition_A = [];
condition_B = [];
LOOKFORTRIGA = 1;
LOOKFORTRIGB = 1;
for e=1:nentries
    thisrow = d{e};
    if LOOKFORTRIGA
        if ~isempty(strfind(thisrow, trigger_str)) % first trigger
            split_row = strsplit(thisrow, ' ');
            trig_timeA = str2num(split_row{1});
            LOOKFORTRIGA = 0;
        end
    end
    if ~isempty(strfind(thisrow, start_str)) && ~LOOKFORTRIGA
        frontind = 0;
        while LOOKFORTRIGB
            frontind = frontind + 1;
            frontrow = d{e+frontind};
            if ~isempty(strfind(frontrow,trigger_str))
                split_row = strsplit(frontrow, ' ');
                trig_timeB = str2num(split_row{1});
                LOOKFORTRIGB = 0;
            end
        end
    end
    % now get every trial start
    if ~isempty(strfind(thisrow, trial))
        split_row = strsplit(thisrow, ' ');
        AB = split_row{8};
        condition_str = split_row{18};
        if strfind(condition_str, 'Neutral')
            cond=1;
        elseif strfind(condition_str, 'Fixation')
            cond=5;
        elseif strfind(condition_str, 'Happy')
            cond=3;
        elseif strfind(condition_str, 'Fearful')
            cond=4;
        elseif strfind(condition_str, 'Object')
            cond=2;
        end
        
        if ~isempty(strfind(AB,'A')) % then in the A run
            Aind = Aind + 1;
            if Aind < 90
                actual_timing = trial_startA(Aind+1) - trial_startA(Aind);
            else
                % have to look for when it said wait
%                 keep_looking_for_a_stop=1;
%                 nr=e+1;
%                 while keep_looking_for_a_stop
%                     thisnewrow = d{nr};
%                     if ~isempty(strfind(thisnewrow, 'Waiting for the experimenter.'))
%                         split_row = strsplit(thisnewrow, ' ');
%                         tstop = split_row{1};
%                         keep_looking_for_a_stop=0;
%                     end
%                     nr = nr + 1;
%                 end
                %actual_timing = str2num(tstop) - trial_startA(Aind);
                actual_timing=3;
            end
            real_start = trial_startA(Aind) - trig_timeA - toDel;
            %trial_startA(end+1) = str2num(split_row{1});
            if cond==1
                fprintf(fileID_A1,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            elseif cond==2
                fprintf(fileID_A2,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            elseif cond==3
                fprintf(fileID_A3,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            elseif cond==4
                fprintf(fileID_A4,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            elseif cond==5
                fprintf(fileID_A5,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            end
            fprintf('trial %i\t cond %i\t%8.4f\t%6.4f\t1\n', Aind,cond, real_start,actual_timing);
        elseif ~isempty(strfind(AB,'B'))
            %trial_startB(end+1) = str2num(split_row{1});
            Bind = Bind + 1;
            if Bind < 90
                actual_timing = trial_startB(Bind+1) - trial_startB(Bind);
            else
                % have to look for when it said wait
%                 keep_looking_for_b_stop=1;
%                 nr=e+1;
%                 while keep_looking_for_b_stop
%                     thisnewrow = d{nr};
%                     if ~isempty(strfind(thisnewrow, 'top: autoDraw = False'))
%                         split_row = strsplit(thisnewrow, ' ');
%                         tstop = split_row{1};
%                         keep_looking_for_b_stop=0;
%                     end
%                     nr = nr + 1;
%                 end
                %actual_timing = str2num(tstop) - trial_startB(Bind);
                actual_timing = 3;
            end
            real_start = trial_startB(Bind) - trig_timeB - toDel;
            if cond==1
                fprintf(fileID_B1,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            elseif cond==2
                fprintf(fileID_B2,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            elseif cond==3
                fprintf(fileID_B3,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            elseif cond==4
                fprintf(fileID_B4,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            elseif cond==5
                fprintf(fileID_B5,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            end
            fprintf('trial %i\t cond %i\t%8.4f\t%6.4f\t1\n', Bind,cond, real_start,actual_timing);
        end
        % now get timing--look to next file
    end
end
end
