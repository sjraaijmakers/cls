function RMSE = test(P)

%%%%% This tuning template is ONLY meant for nonadaptive network models
%%%%% For adaptive network models, use the other tuning template NOMEtuningadaptive

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% STEP-I %%%% Do You Want to save RMSE value along with the tuned parameter values P?
%%%%% Specify true / false

save_RMSE_Value = true;

%%%%% STEP-II %%%%%% Copy your Empirical Data by the following initializations
%%%%% GIVE: 
%%%%% a) the timepoints list 
%%%%% b) the stateselection list  
%%%%% c) the related empirical data matrix 
 
timepoints=[3.1 11.9 20.2 25.2 28 30];
stateselection=[3 5 9 10 11];
empirical_data = [0.92	0.85	0.81	0.79	0.78	0.77
0.75	0.74	0.73	0.71	0.71	0.7
0.4	0.55	0.61	0.64	0.65	0.65
0.25	0.28	0.3	0.31	0.32	0.32
0.18	0.32	0.39	0.41	0.42	0.43];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  Selection of combination functions for the overall model  %%
mcf=[30];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%% STEP-III %%%%% Copy here your tuning matrices into the following %%%%%%
%%%%%%% a) mcwtuning 
%%%%%%% b) mcfptuning 
%%%%%%% c) mcfwtuning
%%%%%%% d) mstuning 
%%%%%%% e) ivtuning 
%%%%% Here by indicating numbers 1, 2, ... in some cells over all matrices, 
%%%%% the values are selected to be parameters P(1), P(2), ... used for tuning
%%%%% Note that there are ONLY the tuning matrices above for the value %%%%
%%%%%%% role matrices and iv, NOT for mb or adaptation role matrices %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

mcwtuning = [NaN NaN NaN NaN NaN NaN NaN
NaN	NaN	NaN	NaN	NaN	NaN	NaN
NaN	NaN	NaN	NaN	NaN	NaN	NaN
NaN	NaN	NaN	NaN	NaN	NaN	NaN
NaN	NaN	NaN	NaN	NaN	NaN	NaN
NaN	NaN	NaN	NaN	NaN	NaN	NaN
NaN	NaN	NaN	NaN	NaN	NaN	NaN
NaN	NaN	NaN	NaN	NaN	NaN	NaN
NaN	NaN	NaN	NaN	NaN	NaN	NaN
NaN	NaN	NaN	NaN	NaN	NaN	NaN
NaN	NaN	NaN	NaN	NaN	NaN	NaN
NaN	NaN	NaN	NaN	NaN	NaN	NaN
];
mcfptuning = cat(3,[NaN NaN
NaN	NaN
NaN	NaN
NaN	NaN
NaN	NaN
NaN	NaN
NaN	NaN
NaN	NaN
NaN	NaN
NaN	NaN
NaN	NaN
NaN	NaN
]);
mcfwtuning = [NaN
NaN
NaN
NaN
NaN
NaN
NaN
NaN
NaN
NaN
NaN
NaN
];
mstuning = [1
2
3
4
5
6
7
8
9
10
11
12
];
ivtuning =  [NaN
NaN
NaN
NaN
NaN
NaN
NaN
NaN
NaN
NaN
NaN
NaN];

%STEP-IV%% Copy here the role matrices and initial values of your model, as in the normal NOME template %% 
%%%%%%%%%%%%%%%%%%%%% a) mb, b) mcwv, c) mcfwv,  d) mcfpv, e) ms, f) iv  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

   mb=[ 2   3   4   5   NaN NaN NaN
        1   5   6   NaN NaN NaN NaN
        1   5   7   NaN NaN NaN NaN
        1   7   8   9   NaN NaN NaN
        1   2   3   6   7   10  11
        2   5   10  12  NaN NaN NaN
        3   4   5   8   11  NaN NaN
        4   7   9   11  NaN NaN NaN
        4   8   NaN NaN NaN NaN NaN
        5   6   11  12  NaN NaN NaN
        5   7   8   10  12  NaN NaN
        6   10  11  NaN NaN NaN NaN];
mcwv=[  0.7  0.5  0.6  0.3  NaN  NaN  NaN
        0.6  0.5  0.6  NaN  NaN  NaN  NaN
        0.8  0.4  1    NaN  NaN  NaN  NaN
        1    0.2  0.5  0.9  NaN  NaN  NaN
        0.5  0.4  1    0.3  0.3  0.4  0.3
        0.8  0.3  0.7  0.9  NaN  NaN  NaN
        0.9  0.4  0.1  0.4  0.2  NaN  NaN
        0.8  0.1  1    0.3  NaN  NaN  NaN
        0.7  0.8  NaN  NaN  NaN  NaN  NaN
        0.7  0.7  0.1  0.8  NaN  NaN  NaN
        0.3  0.2  0.5  0.9  0.9  NaN  NaN
        0.2  0.7  0.2  NaN  NaN  NaN  NaN];
    
mcfwv=[1
       1
       1
       1
       1
       1
       1
       1
       1
       1
       1
       1];
  
  
mcfpv = cat(3,[ 2.1 NaN
                1.7 NaN
                2.2 NaN
                2.6 NaN
                3.2 NaN
                2.7 NaN
                2.0 NaN
                2.2 NaN
                1.5 NaN
                2.3 NaN
                2.8 NaN
                1.1 NaN]);
msv=[0.1
     0.1
     0.1
     0.05
     0.05
     0.05
     0.5
     0.1
     0.1
     0.01
     0.1
     0.5];
 
 iv =  [1
        1
        0.9
        0.8
        0.7
        0.6
        0.5
        0.4
        0.3
        0.2
        0.1
        0];
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% For an adaptive model use the NOMEtuningadaptive template %%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%   Fill dt and endtimeofsimulation %%%%%%
dt = 0.5   ;
endtimeofsimulation =  30;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%% AFTER THIS POINT YOU SHOULD NOT MODIFY ANYTHING %%%%%%%%%%%%%%%%%%%%%%%%% 

%%%%%%%%% UPDATING THE PARAMETERS BASED ON P GENERATED BY THE OPTIMISATION TOOL %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(DONT CHANGE)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%Updating mcwv
[rows,cols] = size(mcwtuning);

for i = 1: rows
    for j = 1:cols
        if (~isnan(mcwtuning(i,j)))
            index = mcwtuning(i,j);
            mcwv(i,j) = P(index);
        end
    end
     
end 

%%%%Updating mcfwv
[rows,cols] = size(mcfwtuning);
for j = 1:rows
    for m=1:cols
        if not(isnan(mcfwtuning(j, m))) 
            index = mcfwtuning(j, m);
            mcfwv(j, m) = P(index);   
        end
    end
end


%%%%Updating mcfpv
nocf = numel(mcf);
nocfp = size(mcfpv,2);

for j = 1:size(mcfpv)
    for p=1:1:nocfp  
        for m=1:1:nocf 
            if not(isnan(mcfptuning(j, p, m))) 
                index = mcfptuning(j, p, m);
                mcfpv(j, p, m) = P(index);
             end
         end
    end
end

%%%%Updating msv

nostates = size(mstuning);

for i = 1: nostates
 if (~isnan(mstuning(i)))
     index = mstuning(i);
     msv(i) = P(index);
 end
     
end    

%%%%Updating iv

nostates = size(ivtuning);

for i = 1: nostates
 if (~isnan(ivtuning(i)))
     index = ivtuning(i);
     iv(i) = P(index);
 end
     
end

%%%%%%%%%% Simulating the model using the parameters P generated by the Optimisation Tool %%%%%%%%%%%
   
nos = numel(iv);
nocf = numel(mcf);
nocfp = size(mcfpv,2);

% Initialisation of all state values
base_model(:,1)=iv;
X = base_model;
t(1)=0;

for k=1:endtimeofsimulation/dt
    
        % First the values from the prespecified role matrices representing the 
        % characteristics of the network are read. These prespecified matrices are 
        %     msv, mbv, mcwv, mcfwv, mcfpv 
        % for the values of static network characteristics. If a NaN value is
        % found,a default value 0 or 1 is chosen.
       
    for j = 1:nos

    if not(isnan(msv(j, 1))) 
        s(j, k) = msv(j, 1);
    elseif isnan(msv(j, 1)) 
        s(j, k) = 0;
    end

    for p=1:1:size(mb,2)
        if not(isnan(mb(j, p)))
            b(j, p, k) = X(mb(j,p), k);
        elseif isnan(mb(j, p))
            b(j, p, k) = 0;
        end
    end
    for p=1:1:size(mcwv,2)
        if not(isnan(mcwv(j, p))) 
            cw(j, p, k) = mcwv(j, p);
        elseif isnan(mcwv(j, p)) 
            cw(j, p, k) = 0;
        end
    end
    for m=1:1:nocf
        if not(isnan(mcfwv(j, m))) 
            cfw(j, m, k) = mcfwv(j, m);   
        elseif isnan(mcfwv(j, m)) 
            cfw(j, m, k) = 0;
        end
    end
    for p=1:1:nocfp  
        for m=1:1:nocf 
           if not(isnan(mcfpv(j, p, m))) 
                cfp(j, p, m, k) = mcfpv(j, p, m);
           elseif isnan(mcfpv(j, p, m)) 
                cfp(j, p, m, k) = 1;
           end
        end
    end
    
            % Next, the actual simulation step follows. 
            % Here, first
            %       squeeze(cw(j, :, k)).*squeeze(b(j, :, k)) 
            % indicates the vector v of single impacts for state j at k
            % used as values in the m-th selected combination function bcf(mcf(m),p,v). 
            % (See Book 2, Chapter 2, Section 2.3.1, Table 2.2, second row)
            % This v is the calculated as the elementwise multiplication of the vectors 
            %       squeeze(cw(j, :, k)) and  squeeze(b(j, :, k))
            % of connection weights and of state values, respectively.
            % Moreover,
            %       squeeze(cfp(j, :, m, k)) 
            % is the vector p of parameter values for combination function
            % bcf(mcf(m),p,v) for state j at k.
            % This calculates the combination function values cfv(j,m,k)for each selected  
            % combination function bcf(mcf(m),p,v) for state j at k
        for m=1:1:nocf
                cfv(j,m,k) = bcf(mcf(m), squeeze(cfp(j, :, m, k)), squeeze(cw(j, :, k)).*squeeze(b(j, :, k)));
        end
           
        aggimpact(j, k) = dot(cfw(j, :, k), cfv(j, :, k))/sum(cfw(j, :, k));
            % The aggregated impact for state j at k is calculated as dotproduct (inproduct) of
            % combination function weights and combination function values
            % scaled by the sum of these weights.
            % (See Book 2, Chapter 2, Section 2.3.1, Table 2.2, third row, and formula (2) in Section 2.3.2)
        
        X(j,k+1) = X(j,k) + s(j,k)*(aggimpact(j,k) - X(j,k))*dt;
            % This is the actual iteration step from k to k+1 for state j;
            % (See Book 2, Chapter 2, Section 2.3.1, Table 2.2, third row)
            
        t(k+1) = t(k)+dt;
            % This keeps track on time t;
            
    end
end


%%%%%%%%%%%%%%%%%%%% Extracting the right portion of the model %%%%%%%%%%%%%%%%%%%%%
%%%%%% to get specific data from the simulation corresponding to the data set %%%%%%
    for j=1:length(stateselection)
        for i=1:length(timepoints)
            Y(j,i)=X(stateselection(j),1+round(timepoints(i)/dt));
        end
            model_data = Y;
    end
    
    %%%%%%%%%%%%%%%%%%%% Computing RMSE %%%%%%%%%%%%%%%%%%%%%%%%%%%%
[e_row,e_col] = size(empirical_data);
   RMSE = sqrt(nansum(nansum((model_data - empirical_data).^2))/(e_col * e_row)) %average deviation
   if(save_RMSE_Value == true)
    saveRMSE(RMSE, P);
   end
end 

function saveRMSE(RMSE, P)
name = "PTuning";
sheet = 1;
  % Create output data.

data = {'RMSE',mat2str(RMSE),'for P =',mat2str(P)};
  
filename = fullfile('RMSE_'+ name+'_Traced.xlsx');
if(~exist(filename,'file'))
     xlRange = sprintf('A%d', 2);
else
    [numbers, strings, raw] = xlsread(filename);
    lastRow = size(raw, 1);
    xlRange = sprintf('A%d', lastRow+2);
end
  dlmwrite("new_empirical.xls",RMSE,'-append')
end





