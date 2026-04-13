%% Author: Crispin Contreras-Martinez
%% Institute: Fermialb
%% Date: 2025

Qext=1E5:5000:1E9;  % This the Q value for the coupler
Q0=2.7e10; %260/(6*10^-9);          %Unloaded Q0=G/Rs   
B=Q0./Qext;           %Coupling constant
QL=Q0./(1+B);         %Loaded Q
Ib=2*10^-3;       %Beam Current   
RQ=610;              %R/Q B92
V0=18.8*10^6*1.061;        %Accelerating Voltage, 18.7 MV/m Leff=1.061 b92 , b61 Leff=0.704 Eacc=16.8 MV/m
PC=V0^2./(RQ.*QL);     %Power dissipated in the cavity 
f0=650*10^6;         %resosnant frequency
Vb=Ib*(RQ.*QL);       %Beam voltage
Vb0=Ib*(RQ*Q0);
duty_factor = 0.011;
dF=40;
betaopt=sqrt((Vb0/V0)^2+(2*dF*Q0/f0)^2);
QLopt=Q0/(1+betaopt);
fhalf=f0/(2*QLopt);
Vbopt=Ib*RQ*QLopt;
dF1=-50:0.1:50;
PGopt0=1e-3*(V0^2*(1+betaopt)/(4*betaopt*RQ*QLopt))*((1+Vbopt/V0)^2+(dF1/fhalf).^2); %Units in kW
xloss650=0.06;

etaDCHV=0.95;
etaW=0.8;
%% Numerical output — Block 1
i0 = find(dF1 == 0);  % index of dF=0
fprintf('=== BLOCK 1: HB650 single cavity (650 MHz) ===\n')
fprintf('  betaopt                    = %.6e\n', betaopt)
fprintf('  QLopt                      = %.6e\n', QLopt)
fprintf('  fhalf (Hz)                 = %.6f\n', fhalf)
fprintf('  Vbopt (V)                  = %.6e\n', Vbopt)
fprintf('  PGopt0 at dF=0 (kW)        = %.6f\n', PGopt0(i0))
fprintf('  Wall-plug power at dF=0 (kW) = %.6f\n', PGopt0(i0)*(1-xloss650)^-1/etaDCHV/etaW)

figure(1)
plot(dF1,(1-xloss650)^-1*PGopt0/etaDCHV/etaW)
%plot(dF1,PGopt0)
hold on 
xlabel('Detuning [Hz]')
ylabel('RF Power [kW]')
legend('BW = 40 Hz','BW = 44 Hz','BW = 88 Hz')
legend('boxoff')
set(gca,'FontSize',14)

% Create line
annotation('line',[0.214880952380952 0.882738095238095],...
    [0.225396825396826 0.215873015873016],'LineStyle',':');

% Create textarrow
annotation('textarrow',[0.613690476190476 0.547023809523809],...
    [0.171428571428571 0.214285714285714],'String',{'All RF Power to Beam'},...
    'FontSize',12);

% Create arrow
annotation('arrow',[0.343452380952381 0.344642857142857],...
    [0.22915873015873 0.323809523809524]);

% Create textbox
annotation('textbox',...
    [0.208738095238095 0.719047619047619 0.301380952380952 0.198412698412701],...
    'String',{'f_0 = 650 MHz','i_b = 2 mA','E_{acc} = 18.7 MV/m'},...
    'LineStyle','none',...
    'FontSize',12,...
    'FitBoxToText','off');

% Create textbox
annotation('textbox',...
    [0.112309523809524 0.268253968253969 0.301380952380952 0.0412698412698466],...
    'String','Reflected Power',...
    'LineStyle','none',...
    'FontSize',12,...
    'FitBoxToText','off');



Ib=2*10^-3;       %Beam Current   
Q0SSR=8.2e9; %260/(6*10^-9);          %Unloaded Q0=G/Rs   
V0SSR1=10*10^6*0.205;        %Accelerating Voltage, 18.7 MV/m Leff=1.061 b92 , b61 Leff=0.704 Eacc=16.8 MV/m   
fSSR=325*10^6;   
V0SSR2=11.5*10^6*0.436;
RQSSR1=242;
RQSSR2=305;
Vb0SSR1=Ib*(RQSSR1*Q0SSR);
Vb0SSR2=Ib*(RQSSR2*Q0SSR);
dF13=20;
betaoptSSR1=sqrt((1+Vb0SSR1/V0SSR1)^2+(2*dF13*Q0SSR/fSSR)^2);
betaoptSSR2=sqrt((1+Vb0SSR2/V0SSR2)^2+(2*dF13*Q0SSR/fSSR)^2);

QLoptSSR1=Q0SSR/(1+betaoptSSR1);
QLoptSSR2=Q0SSR/(1+betaoptSSR2);

fhalfSSR1=fSSR/(2*QLoptSSR1);
fhalfSSR2=fSSR/(2*QLoptSSR2);

VboptSSR1=Ib*RQSSR1*QLoptSSR1;
VboptSSR2=Ib*RQSSR2*QLoptSSR2;

dF1=-50:0.1:50;
PGoptSSR1=(V0SSR1^2*(1+betaoptSSR1)/(4*betaoptSSR1*RQSSR1*QLoptSSR1))*((1+VboptSSR1/V0SSR1)^2+(dF1/fhalfSSR1).^2); %Units in kW
PGoptSSR2=(V0SSR2^2*(1+betaoptSSR2)/(4*betaoptSSR2*RQSSR2*QLoptSSR2))*((1+VboptSSR2/V0SSR2)^2+(dF1/fhalfSSR2).^2); %Units in kW


Q0LB=2.4e10; %260/(6*10^-9);          %Unloaded Q0=G/Rs   
Q0HB=3.3e10; %260/(6*10^-9);          %Unloaded Q0=G/Rs   
f650=650*10^6;   
V0LB=16.8*10^6*0.704;
V0HB=18.7*10^6*1.061;
RQLB=341;
RQHB=610;
Vb0LB=Ib*(RQLB*Q0LB);
Vb0HB=Ib*(RQHB*Q0HB);
dF13=20;

betaoptLB=sqrt((1+Vb0LB/V0LB)^2+(2*dF13*Q0LB/f650)^2);
betaoptHB=sqrt((1+Vb0HB/V0HB)^2+(2*dF13*Q0HB/f650)^2);

QLoptLB=Q0LB/(1+betaoptLB);
QLoptHB=Q0HB/(1+betaoptHB);

fhalfLB=f650/(2*QLoptLB);
fhalfHB=f650/(2*QLoptHB);

VboptLB=Ib*RQLB*QLoptLB;
VboptHB=Ib*RQHB*QLoptHB;

PGoptLB=(V0LB^2*(1+betaoptLB)/(4*betaoptLB*RQLB*QLoptLB))*((1+VboptLB/V0LB)^2+(dF1/fhalfLB).^2); %Units in kW
PGoptHB=(V0HB^2*(1+betaoptHB)/(4*betaoptHB*RQHB*QLoptHB))*((1+VboptHB/V0HB)^2+(dF1/fhalfHB).^2); %Units in kW

xlossSSR1=.1;
xloss650=0.06;
PSSR=16*(PGoptSSR1+1.33*7000)+35*(PGoptSSR2+1.33*20000);
P650=36*(PGoptLB+1.33*40000)+24*(PGoptHB+70000*1.33);
PAll_PIPII=((1/(1-xlossSSR1))*PSSR+(1/(1-xloss650))*P650)*1e-3; %units of kW
etaDCHV=0.95;
etaW=0.8;
DutyF=20*(2.8+.55)*1e-3;
cost_electricity  = 0.08; % units of $/kWh
hours_on = 5600;
%% Numerical output — Block 2
fprintf('\n=== BLOCK 2: PIP-II full linac (325 + 650 MHz) ===\n')
fprintf('  betaoptSSR1                = %.6e\n', betaoptSSR1)
fprintf('  betaoptSSR2                = %.6e\n', betaoptSSR2)
fprintf('  betaoptLB                  = %.6e\n', betaoptLB)
fprintf('  betaoptHB                  = %.6e\n', betaoptHB)
fprintf('  QLoptSSR1                  = %.6e\n', QLoptSSR1)
fprintf('  QLoptSSR2                  = %.6e\n', QLoptSSR2)
fprintf('  QLoptLB                    = %.6e\n', QLoptLB)
fprintf('  QLoptHB                    = %.6e\n', QLoptHB)
fprintf('  fhalfSSR1 (Hz)             = %.6f\n', fhalfSSR1)
fprintf('  fhalfSSR2 (Hz)             = %.6f\n', fhalfSSR2)
fprintf('  fhalfLB (Hz)               = %.6f\n', fhalfLB)
fprintf('  fhalfHB (Hz)               = %.6f\n', fhalfHB)
fprintf('  PGoptSSR1 at dF=0 (W)      = %.6f\n', PGoptSSR1(i0))
fprintf('  PGoptSSR2 at dF=0 (W)      = %.6f\n', PGoptSSR2(i0))
fprintf('  PGoptLB at dF=0 (W)        = %.6f\n', PGoptLB(i0))
fprintf('  PGoptHB at dF=0 (W)        = %.6f\n', PGoptHB(i0))
fprintf('  PAll_PIPII at dF=0 (kW)    = %.6f\n', PAll_PIPII(i0))
CW_cost_at_zero    = (PAll_PIPII(i0)/etaDCHV/etaW)*hours_on*cost_electricity*1e-6;
pulse_cost_at_zero = DutyF*CW_cost_at_zero;
fprintf('  CW annual cost at dF=0 (M$)     = %.6f\n', CW_cost_at_zero)
fprintf('  Pulsed annual cost at dF=0 (M$) = %.6f\n', pulse_cost_at_zero)
fprintf('  DutyF                      = %.6f\n', DutyF)

figure(101)
plot(dF1,(PAll_PIPII/etaDCHV/etaW)*hours_on*cost_electricity*1e-6) %factor of 1e-6 is used to get M$
ylabel('CW Annual RF Cost [M$]')
%yyaxis right 
hold on 
plot(dF1,DutyF*(PAll_PIPII/etaDCHV/etaW)*hours_on*cost_electricity*1e-6)
xlabel('Detuning [Hz]')
ylabel('Pulse Annual RF Cost [M$]')
set(gca,'FontSize',12)
xlim([0 40])
legend('CW','Pulsed Operation')
legend('boxoff')

%*************************************************************************
% LCLS-II and LCLS-II HE
%*************************************************************************


Ib13=0.3*10^-3;       %Beam Current   
RQ13=1036;%R/Q B92
Leff13=1.038;
Q013=2.7e10;
V013=16e6*Leff13;
f13=1300e6;
Vb013=Ib13*(RQ13*Q013);
dF13=10;
betaopt13=sqrt((1+Vb013/V013)^2+(2*dF13*Q013/f13)^2);
QLopt13=Q013/(1+betaopt13);
fhalf13=f13/(2*QLopt13);
Vbopt13=Ib13*RQ13*QLopt13;
dF1=-50:0.1:50;

V013HE=21e6*Leff13;
betaopt13HE=sqrt((1+Vb013/V013HE)^2+(2*dF13*Q013/f13)^2);
QLopt13HE=Q013/(1+betaopt13HE);
fhalf13HE=f13/(2*QLopt13HE);
Vbopt13HE=Ib13*RQ13*QLopt13HE;


PGopt013=(V013^2*(1+betaopt13)/(4*betaopt13*RQ13*QLopt13))*((1+Vbopt13/V013)^2+(dF1/fhalf13).^2); 
PGopt013HE=(V013HE^2*(1+betaopt13HE)/(4*betaopt13HE*RQ13*QLopt13HE))*((1+Vbopt13HE/V013HE)^2+(dF1/fhalf13HE).^2); 

p13ALL=(1-xloss650)^-1*(280*PGopt013+184*PGopt013HE)*1e-3; %units of Kw

%% Numerical output — Block 3
fprintf('\n=== BLOCK 3: LCLS-II + LCLS-II HE (1300 MHz) ===\n')
fprintf('  betaopt13                  = %.6e\n', betaopt13)
fprintf('  betaopt13HE                = %.6e\n', betaopt13HE)
fprintf('  QLopt13                    = %.6e\n', QLopt13)
fprintf('  QLopt13HE                  = %.6e\n', QLopt13HE)
fprintf('  fhalf13 (Hz)               = %.6f\n', fhalf13)
fprintf('  fhalf13HE (Hz)             = %.6f\n', fhalf13HE)
fprintf('  PGopt013 at dF=0 (W)       = %.6f\n', PGopt013(i0))
fprintf('  PGopt013HE at dF=0 (W)     = %.6f\n', PGopt013HE(i0))
fprintf('  p13ALL at dF=0 (kW)        = %.6f\n', p13ALL(i0))
fprintf('  Annual cost at dF=0 (M$)   = %.6f\n', p13ALL(i0)*5600*0.14*1e-6)

figure(11)
plot(dF1,p13ALL*5600*.14*1e-6,'LineWidth',2) %operate for 5600 hrs eletricit rate of 0.14 $/kWh
xlabel('Detuning [Hz]')
ylabel('Annual RF Cost [M$]')
set(gca,'FontSize',12)
xlim([0 10])
