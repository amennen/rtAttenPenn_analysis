% Purpose: make AFNI time descriptions given timing files

%% SPECIFY THESE THINGS FIRTST
subjectId = 'RT035';
subjectNum=112;
%subjectDay= 2; % PUT 1 OR 2 for FACES ---> day 1 or day 3 of scanning, but day 2 of the faces task
%% MAKE SURE CORTRECT
for subjectDay=1:2
%% now to through eveyrthing
task_path = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/behavdata/faces';
save_path = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/timing_files';

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

% instead of doing separete runs, analyze runs togethet
fileID_A1 = fopen(sprintf('%s/neutral.txt',save_file_path), 'w');
fileID_A2 = fopen(sprintf('%s/object.txt',save_file_path), 'w');
fileID_A3 = fopen(sprintf('%s/happy.txt',save_file_path), 'w');
fileID_A4 = fopen(sprintf('%s/fearful.txt',save_file_path), 'w');
fileID_A5 = fopen(sprintf('%s/fixation.txt',save_file_path), 'w');

Aind=0;
Bind=0;
n_neutral_A = 0;
n_object_A = 0;
n_happy_A = 0;
n_fearful_A = 0;
n_neutral_B = 0;
n_object_B = 0;
n_happy_B = 0;
n_fearful_B = 0;
NEUTRAL = 1;
OBJECT = 2;
HAPPY = 3;
FEARFUL = 4;
A_times = [];
B_times = [];


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
            % want: print ONLY start times of each trial
            % the A run should be row 1 and the B run should be row 2
            if cond==1
                % Neutral
                n_neutral_A = n_neutral_A + 1;
                A_times(NEUTRAL,n_neutral_A) = real_start;
                %fprintf(fileID_A1,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            elseif cond==2
                % OBJECT
                n_object_A = n_object_A + 1;
                A_times(OBJECT,n_object_A) = real_start;
                %fprintf(fileID_A2,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            elseif cond==3
                %fprintf(fileID_A3,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
                n_happy_A = n_happy_A + 1;
                A_times(HAPPY,n_happy_A) = real_start;
            elseif cond==4
                %fprintf(fileID_A4,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
                n_fearful_A = n_fearful_A + 1;
                A_times(FEARFUL,n_fearful_A) = real_start;
            elseif cond==5
                %fprintf(fileID_A5,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            end
            %fprintf('trial %i\t cond %i\t%8.4f\t%6.4f\t1\n', Aind,cond, real_start,actual_timing);
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
                %fprintf(fileID_B1,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
                n_neutral_B = n_neutral_B + 1;
                B_times(NEUTRAL,n_neutral_B) = real_start;
            elseif cond==2
                %fprintf(fileID_B2,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
                n_object_B = n_object_B + 1;
                B_times(OBJECT,n_object_B) = real_start;
            elseif cond==3
                %fprintf(fileID_B3,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
                n_happy_B = n_happy_B + 1;
                B_times(HAPPY,n_happy_B) = real_start;
            elseif cond==4
                %fprintf(fileID_B4,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
                n_fearful_B = n_fearful_B + 1;
                B_times(FEARFUL,n_fearful_B) = real_start;
            elseif cond==5
                %fprintf(fileID_B5,'%8.4f\t%6.4f\t1\n', real_start,actual_timing);
            end
            %fprintf('trial %i\t cond %i\t%8.4f\t%6.4f\t1\n', Bind,cond, real_start,actual_timing);
        end
        % now get timing--look to next file
    end
end
fprintf(fileID_A1,'%8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f\n', A_times(NEUTRAL,1), A_times(NEUTRAL,2), A_times(NEUTRAL,3), A_times(NEUTRAL,4), A_times(NEUTRAL,5),A_times(NEUTRAL,6),A_times(NEUTRAL,7),A_times(NEUTRAL,8),A_times(NEUTRAL,9),A_times(NEUTRAL,10),A_times(NEUTRAL,11),A_times(NEUTRAL,12),A_times(NEUTRAL,13),A_times(NEUTRAL,14),A_times(NEUTRAL,15),A_times(NEUTRAL,16),A_times(NEUTRAL,17),A_times(NEUTRAL,18))
fprintf(fileID_A1,'%8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f', B_times(NEUTRAL,1), B_times(NEUTRAL,2), B_times(NEUTRAL,3), B_times(NEUTRAL,4), B_times(NEUTRAL,5),B_times(NEUTRAL,6),B_times(NEUTRAL,7),B_times(NEUTRAL,8),B_times(NEUTRAL,9),B_times(NEUTRAL,10),B_times(NEUTRAL,11),B_times(NEUTRAL,12),B_times(NEUTRAL,13),B_times(NEUTRAL,14),B_times(NEUTRAL,15),B_times(NEUTRAL,16),B_times(NEUTRAL,17),B_times(NEUTRAL,18))

fprintf(fileID_A2,'%8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f\n', A_times(OBJECT,1), A_times(OBJECT,2), A_times(OBJECT,3), A_times(OBJECT,4), A_times(OBJECT,5),A_times(OBJECT,6),A_times(OBJECT,7),A_times(OBJECT,8),A_times(OBJECT,9),A_times(OBJECT,10),A_times(OBJECT,11),A_times(OBJECT,12),A_times(OBJECT,13),A_times(OBJECT,14),A_times(OBJECT,15),A_times(OBJECT,16),A_times(OBJECT,17),A_times(OBJECT,18))
fprintf(fileID_A2,'%8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f', B_times(OBJECT,1), B_times(OBJECT,2), B_times(OBJECT,3), B_times(OBJECT,4), B_times(OBJECT,5),B_times(OBJECT,6),B_times(OBJECT,7),B_times(OBJECT,8),B_times(OBJECT,9),B_times(OBJECT,10),B_times(OBJECT,11),B_times(OBJECT,12),B_times(OBJECT,13),B_times(OBJECT,14),B_times(OBJECT,15),B_times(OBJECT,16),B_times(OBJECT,17),B_times(OBJECT,18))

fprintf(fileID_A3,'%8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f\n', A_times(HAPPY,1), A_times(HAPPY,2), A_times(HAPPY,3), A_times(HAPPY,4), A_times(HAPPY,5),A_times(HAPPY,6),A_times(HAPPY,7),A_times(HAPPY,8),A_times(HAPPY,9),A_times(HAPPY,10),A_times(HAPPY,11),A_times(HAPPY,12),A_times(HAPPY,13),A_times(HAPPY,14),A_times(HAPPY,15),A_times(HAPPY,16),A_times(HAPPY,17),A_times(HAPPY,18))
fprintf(fileID_A3,'%8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f', B_times(HAPPY,1), B_times(HAPPY,2), B_times(HAPPY,3), B_times(HAPPY,4), B_times(HAPPY,5),B_times(HAPPY,6),B_times(HAPPY,7),B_times(HAPPY,8),B_times(HAPPY,9),B_times(HAPPY,10),B_times(HAPPY,11),B_times(HAPPY,12),B_times(HAPPY,13),B_times(HAPPY,14),B_times(HAPPY,15),B_times(HAPPY,16),B_times(HAPPY,17),B_times(HAPPY,18))

fprintf(fileID_A4,'%8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f\n', A_times(FEARFUL,1), A_times(FEARFUL,2), A_times(FEARFUL,3), A_times(FEARFUL,4), A_times(FEARFUL,5),A_times(FEARFUL,6),A_times(FEARFUL,7),A_times(FEARFUL,8),A_times(FEARFUL,9),A_times(FEARFUL,10),A_times(FEARFUL,11),A_times(FEARFUL,12),A_times(FEARFUL,13),A_times(FEARFUL,14),A_times(FEARFUL,15),A_times(FEARFUL,16),A_times(FEARFUL,17),A_times(FEARFUL,18))
fprintf(fileID_A4,'%8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f', B_times(FEARFUL,1), B_times(FEARFUL,2), B_times(FEARFUL,3), B_times(FEARFUL,4), B_times(FEARFUL,5),B_times(FEARFUL,6),B_times(FEARFUL,7),B_times(FEARFUL,8),B_times(FEARFUL,9),B_times(FEARFUL,10),B_times(FEARFUL,11),B_times(FEARFUL,12),B_times(FEARFUL,13),B_times(FEARFUL,14),B_times(FEARFUL,15),B_times(FEARFUL,16),B_times(FEARFUL,17),B_times(FEARFUL,18))

end
% should be 18/stim

