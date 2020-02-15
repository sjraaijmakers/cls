
% Network-Oriented Modeling based on temporal-causal network models is described 
% in the following books (indicated by Book 1 and Book 2, respectively):

%       Treur, J. (2016). Network-Oriented Modeling: Addressing Complexity  
%           of Cognitive, Affective and Social Interactions. Springer Publishers. 
%           Downloadable at http://link.springer.com/book/10.1007/978-3-319-45213-5
%           Table of Contents for this Book 1 with links to abstracts and   
%           slides per chapter: https://www.researchgate.net/publication/305930006
%       Treur, J. (2020). Network-Oriented Modeling for Adaptive Networks: 
%           Designing Higher-Order Adaptive Biological, Mental, and Social  
%           Network Models. Springer Publishers. Available by the end of October 2019.
%           Table of Contents for this Book 2 with links to abstracts and 
%           slides per chapter: https://www.researchgate.net/publication/334576216

% This particular Network-Oriented Modeling Environment NOMEadaptive is a 
% software environment for multi-order adaptive networks based on
% reified temporal-causal network models, implemented by 
% the author, as described in Book 2.

dbstop if error;
clearvars;
global dt;
global k;

%\\\\\\\\\\\\\\\\\\ TO BE FILLED \\\\\\\\\\\\\\\\\\\%
%%%%%%%%%%%%%% Combination functions used %%%%%%%%%%%%
mcf=[1 3]
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%///////////////////////////////////////////////////%

% This vector mcf makes the selection of the specific combination functions  
% from the library used for this particular network model. The entries of this 
% vector can be any numbers from 1 to 35, as the library currently has 35  
% basic combination functions. For an overview of the library, see
% https://www.researchgate.net/publication/333662169 

% Next, the role matrices for the base connectivity and the different network   
% characteristics according to their roles are specified (See Book 2, Chapter 9, 
% Section 9.4.1, and examples in Tables 9.2 to 9.4):

% 1. The role matrix for base connectivity and role matrices for nonadaptive 
%    network characteristics:
%       mb      for base connectivity 
%       mcwv    for nonadaptive connection weight values 
%       msv     for nonadaptive speed factor values
%       mcfwv	for nonadaptive combination function weight values 
%       mcfpv   for nonadaptive combination function parameter values

% 2. The role matrices for adaptive network characteristics:
%       mcwa    for adaptive connection weights 
%       msa     for adaptive speed factors
%       mcfwa	for adaptive combination function weights 
%       mcfpa   for adaptive combination function parameters

% Note that: 
% a) for each cell in a role matrix for adaptive network characteristics, if it  
% indicates a value not NaN, then the same cell of the corresponding role matrix  
% for nonadaptive network characteristics indicates NaN. 
% b) for each cell in a role matrix for nonadaptive network characteristics, if it 
% indicates a value not NaN, then the same cell of the corresponding role matrix  
% for adaptive network characteristics indicates NaN. 

% Moreover,note that here as an illustration the (differentiated) role matrices of the 
% example reified network model shown in Book 2, Chapter 4, Section 4.4.2, Box 4.1 
% are filled in these matrices. These entries can be removed and 
% replaced by other entries.

%\\\\\\\\\\\\\\\\\\ TO BE FILLED \\\\\\\\\\\\\\\\\\\%
%%%%%%%%% Value and Adaptation role matrices %%%%%%%
%%%%%%%%%%%%%% and Initial values %%%%%%%%%%%%%%%%%%%

mb=[1	NaN	NaN	
4	NaN	NaN	
2	NaN	NaN	
3	NaN	NaN	
1	6	NaN	
5	NaN	NaN	
3	9	10	
6	7	NaN	
3	8	NaN	
8	9	NaN	
9	7	11	
6	8	12	
]
mcwa=[NaN NaN NaN ;NaN NaN NaN ;NaN NaN NaN ;NaN NaN NaN ;NaN NaN NaN ;NaN NaN NaN ;NaN 11 NaN ;12 NaN NaN ;NaN NaN NaN ;NaN NaN NaN;NaN NaN NaN ;NaN NaN NaN]
msa=[NaN; NaN;  NaN;  NaN;  NaN;  NaN;  NaN;  NaN;  NaN; NaN;  NaN; NaN]
mcfwa=[NaN NaN; NaN NaN; NaN NaN; NaN NaN; NaN NaN; NaN NaN; NaN NaN; NaN NaN ; NaN NaN; NaN NaN; NaN NaN; NaN NaN]
mcfpa=cat(3,[NaN NaN; NaN NaN; NaN NaN; NaN NaN; NaN NaN;NaN NaN; NaN NaN; NaN NaN; NaN NaN; NaN NaN; NaN NaN; NaN NaN],[NaN NaN; NaN NaN; NaN NaN; NaN NaN; NaN NaN;NaN NaN; NaN NaN; NaN NaN; NaN NaN; NaN NaN; NaN NaN; NaN NaN])

mcwv=[1	NaN	NaN	
1	NaN	NaN	
1	NaN	NaN	
1	NaN	NaN	
0.8	0.7	NaN	
1	NaN	NaN	
0.8	NaN	0.6	
NaN	0.6	NaN	
0.2	0.7	NaN	
0.5	0.3	NaN	
1	1	1	
1	1	1	
]
msv=[0.5 
    0.5	
    0.5	
    0.5	
    0.5	
    0.5	
    0.5	
    0.5	
    0.5	
    0.5
    0.5	
    0.5]
mcfwv=[1 0		
1 0		
1 0		
1 0		
1 0		
1 0		
1 0		
1 0		
1 0		
1 0
0 1
0 1
]	 

mcfpv = cat(3,[1	1
1	1
1	1
1	1
1	1.5
1	1
1	2
1	1.4
1	0.9
1	0.8
NaN NaN
NaN NaN
],[NaN NaN
NaN NaN
NaN NaN
NaN NaN
NaN NaN
NaN NaN
NaN NaN
NaN NaN
NaN NaN
NaN NaN
0.4	NaN
0.4	NaN
])

iv = [0.8	
    0.9	
    0.5	
    0.1	
    0.7	
    0.5	
    0.3	
    0.6	
    0.8	
    0.7 
    0.6 
    0.8
]

% This is the vector of initial values for all states
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%///////////////////////////////////////////////////%


%\\\\\\\\\\\\\\\\\\ TO BE FILLED \\\\\\\\\\\\\\\\\\\%
%%%%%%%%%%%%% End time and Step size dt %%%%%%%%%%%%%
endtimeofsimulation=300;
dt=0.5;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%///////////////////////////////////////////////////%

% dt is the time difference for each of the steps
% note that the time t is k*dt with k = the number of 
% steps made in the simulation


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%% Initialisation for states and time %%%%%%%%
X(:,1)=iv
t(1)=0
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%% Setting dimensions %%%%%%%%%%%%%%%%%
nos = numel(iv);
nocf = numel(mcf);
nocfp = size(mcfpv,2);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% This identifies some of the dimensions of the vectors and matrices
% nos = number of states
% nocf = number of combination functions used
% nocfp = number of combination function parameters used

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%% Simulation steps %%%%%%%%%%%%%%%%%

for k=1:endtimeofsimulation/dt
    
        % Reading the values from the prespecified matrices representing the 
        % characteristics of the network. As indicated above, these prespecified 
        % matrices are:
        % 1. The base connectivity and nonadaptive values role matrices:
        %       mb, msv, mcwv, mcfwv, mcfpv 
        % for the base connectivity and values of the nonadaptive characteristics   
        % (speed factors, connection weights, combination function 
        % weights, and combination function parameters), and
        % 2. The adaptivity role matrices:
        %       msa,  mcwa,  mcfwa,  mcfpa 
        % for adaptive network characteristics. 
        % If only a NaN value is found in both types of role matrices, 
        % a default value 0 or 1 is chosen.
        
    for j = 1:nos

    if not(isnan(msa(j, 1)))  
        s(j, k) = X(msa(j, 1), k);  
    elseif not(isnan(msv(j, 1))) 
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
        if not(isnan(mcwa(j, p)))
            cw(j, p, k) = X(mcwa(j,p), k);
        elseif not(isnan(mcwv(j, p))) 
            cw(j, p, k) = mcwv(j, p);
        elseif isnan(mcwv(j, p)) 
            cw(j, p, k) = 0;
        end
    end
    for m=1:1:nocf
        if not(isnan(mcfwa(j, m)))
            cfw(j, m, k) = X(mcfwa(j, m), k);  
        elseif not(isnan(mcfwv(j, m))) 
            cfw(j, m, k) = mcfwv(j, m);   
        elseif isnan(mcfwv(j, m)) 
            cfw(j, m, k) = 0;
        end
    end
    for p=1:1:nocfp  
        for m=1:1:nocf 
            if not(isnan(mcfpa(j, p, m))) 
                cfp(j, p, m, k) = X(mcfpa(j, p, m), k);  
            elseif not(isnan(mcfpv(j, p, m))) 
                cfp(j, p, m, k) = mcfpv(j, p, m);
            elseif isnan(mcfpv(j, p, m)) 
                cfp(j, p, m, k) = 1;
            end
        end
    end
    
% The actual simulation
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
       end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%\\\\\\\\\\\\\\\\\ TO BE FILLED \\\\\\\\\\\\\\\\\\\\%
%%%%%%%%%%%% Plot graph and store data %%%%%%%%%%%%%%
% Plot with vertical legend: 
% legend(plot([t;t;t;t;t;t;t;t;t;t;t;t]', [X(1,:);X(2,:);X(3,:);X(4,:); X(5,:);X(6,:);X(7,:);X(8,:);X(9,:);X(10,:);X(11,:);X(12,:)]'),{'X1','X2','X3','X4','X5','X6','X7','X8','X9','X10','X11','X12'});
% Plot with horizontal legend: 
legend(plot([t;t;t;t;t;t;t;t;t;t;t;t]', [X(1,:);X(2,:);X(3,:);X(4,:); X(5,:);X(6,:);X(7,:);X(8,:);X(9,:);X(10,:);X(11,:);X(12,:)]'),{'X1','X2','X3','X4','X5','X6','X7','X8','X9','X10','X11','X12'},'Orientation','horizontal');
% Store data in Excel file:
xlswrite('hebian.xls',X');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%///////////////////////////////////////////////////%

    % This generates a graph of the simulation results; note that it has to be
    % indicated which states are displayed; the number of t's should be the same number.
    %%%%%% If you prefer a horizontal legend, leave out the % for the horizontal legend
    %%%%%% If you prefer a vertical legend, leave out the % for the vertical legend
    %%%%%% If you want to have the data in Excel, leave out the % in front of
    %%%%%% the line xlswrite('example.xls',X');
    % You get the simulation data in the xls file 'example.xls' (also other names possible)   
    % which can be opened in Excel and used to make your own graphs, or to just inspect or 
    % analyse the numbers. 
    % Note that this makes the simulation a bit slower as Matlab takes time to write  
    % or read xls data files; also note that during the simulation the xls file  
    % should not be open in Excel, as then it is not writable from Matlab. 
