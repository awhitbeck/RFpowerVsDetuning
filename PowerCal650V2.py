"""
Author: Crispin Contreras-Martinez
Institute: Fermilab
Date: 2025
Converted to Python from MATLAB.
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Block 1 — 650 MHz HB cavity: single-cavity power vs. detuning
# =============================================================================

Qext = np.arange(1e5, 1e9 + 5000, 5000)  # Q values for the coupler
Q0 = 2.7e10                               # Unloaded Q0 = G/Rs
B = Q0 / Qext                             # Coupling constant
QL = Q0 / (1 + B)                         # Loaded Q
Ib = 2e-3                                 # Beam current (A)
RQ = 610                                  # R/Q B92 (Ohm)
V0 = 18.8e6 * 1.061                       # Accelerating voltage (V); Eacc=18.7 MV/m, Leff=1.061 m (B92)
PC = V0**2 / (RQ * QL)                    # Power dissipated in cavity (W)
f0 = 650e6                                # Resonant frequency (Hz)
Vb = Ib * (RQ * QL)                       # Beam voltage (V)
Vb0 = Ib * (RQ * Q0)
duty_factor = 0.011
dF = 40                                   # Static detuning offset for optimal coupling (Hz)

betaopt = np.sqrt((Vb0 / V0)**2 + (2 * dF * Q0 / f0)**2)
QLopt = Q0 / (1 + betaopt)
fhalf = f0 / (2 * QLopt)
Vbopt = Ib * RQ * QLopt

dF1 = np.arange(-50, 50.1, 0.1)          # Detuning sweep (Hz)

# Generator power in kW (at optimal coupling)
PGopt0 = 1e-3 * (V0**2 * (1 + betaopt) / (4 * betaopt * RQ * QLopt)) \
         * ((1 + Vbopt / V0)**2 + (dF1 / fhalf)**2)

xloss650 = 0.06    # Waveguide transmission loss (650 MHz, 6%)
etaDCHV = 0.95     # DC high-voltage supply efficiency
etaW = 0.80        # Klystron wall-plug efficiency

fig1, ax1 = plt.subplots(num=1)
ax1.plot(dF1, (1 - xloss650)**-1 * PGopt0 / etaDCHV / etaW)
ax1.set_xlabel('Detuning [Hz]')
ax1.set_ylabel('RF Power [kW]')
ax1.set_title(
    'HB650 single cavity — wall-plug RF power vs. detuning\n'
    r'$f_0$ = 650 MHz, $I_b$ = 2 mA, $E_{acc}$ = 18.7 MV/m, $Q_0$ = 2.7×10$^{10}$, '
    r'coupling optimised at $\delta f$ = 40 Hz',
    fontsize=11
)
ax1.legend(['BW = 40 Hz'], frameon=False)
ax1.tick_params(labelsize=14)

# Annotations (approximate positions converted from normalised figure coordinates)
i0 = np.argmin(np.abs(dF1))  # index closest to dF=0
P_at_zero = PGopt0[i0] * (1 - xloss650)**-1 / etaDCHV / etaW
ax1.axhline(y=P_at_zero, linestyle=':', color='black', linewidth=0.8)
ax1.annotate(
    'All RF Power to Beam',
    xy=(0, P_at_zero),
    xytext=(15, P_at_zero * 0.65),
    fontsize=12,
    arrowprops=dict(arrowstyle='->', color='black')
)
ax1.text(
    -48, P_at_zero * 3.5,
    '$f_0$ = 650 MHz\n$i_b$ = 2 mA\n$E_{acc}$ = 18.7 MV/m',
    fontsize=12
)

# =============================================================================
# Block 2 — PIP-II full linac: annual RF electricity cost vs. detuning
# =============================================================================

Ib = 2e-3            # Beam current (A)
Q0SSR = 8.2e9        # Unloaded Q0 for SSR cavities
V0SSR1 = 10e6 * 0.205   # Accelerating voltage SSR1 (V)
fSSR = 325e6             # SSR resonant frequency (Hz)
V0SSR2 = 11.5e6 * 0.436  # Accelerating voltage SSR2 (V)
RQSSR1 = 242         # R/Q SSR1 (Ohm)
RQSSR2 = 305         # R/Q SSR2 (Ohm)

Vb0SSR1 = Ib * (RQSSR1 * Q0SSR)
Vb0SSR2 = Ib * (RQSSR2 * Q0SSR)
dF13 = 20            # Static detuning for optimal coupling, SSR cavities (Hz)

betaoptSSR1 = np.sqrt((1 + Vb0SSR1 / V0SSR1)**2 + (2 * dF13 * Q0SSR / fSSR)**2)
betaoptSSR2 = np.sqrt((1 + Vb0SSR2 / V0SSR2)**2 + (2 * dF13 * Q0SSR / fSSR)**2)

QLoptSSR1 = Q0SSR / (1 + betaoptSSR1)
QLoptSSR2 = Q0SSR / (1 + betaoptSSR2)

fhalfSSR1 = fSSR / (2 * QLoptSSR1)
fhalfSSR2 = fSSR / (2 * QLoptSSR2)

VboptSSR1 = Ib * RQSSR1 * QLoptSSR1
VboptSSR2 = Ib * RQSSR2 * QLoptSSR2

PGoptSSR1 = (V0SSR1**2 * (1 + betaoptSSR1) / (4 * betaoptSSR1 * RQSSR1 * QLoptSSR1)) \
            * ((1 + VboptSSR1 / V0SSR1)**2 + (dF1 / fhalfSSR1)**2)
PGoptSSR2 = (V0SSR2**2 * (1 + betaoptSSR2) / (4 * betaoptSSR2 * RQSSR2 * QLoptSSR2)) \
            * ((1 + VboptSSR2 / V0SSR2)**2 + (dF1 / fhalfSSR2)**2)

Q0LB = 2.4e10        # Unloaded Q0 LB650
Q0HB = 3.3e10        # Unloaded Q0 HB650
f650 = 650e6         # 650 MHz resonant frequency (Hz)
V0LB = 16.8e6 * 0.704   # Accelerating voltage LB650 (V)
V0HB = 18.7e6 * 1.061   # Accelerating voltage HB650 (V)
RQLB = 341           # R/Q LB650 (Ohm)
RQHB = 610           # R/Q HB650 (Ohm)

Vb0LB = Ib * (RQLB * Q0LB)
Vb0HB = Ib * (RQHB * Q0HB)

betaoptLB = np.sqrt((1 + Vb0LB / V0LB)**2 + (2 * dF13 * Q0LB / f650)**2)
betaoptHB = np.sqrt((1 + Vb0HB / V0HB)**2 + (2 * dF13 * Q0HB / f650)**2)

QLoptLB = Q0LB / (1 + betaoptLB)
QLoptHB = Q0HB / (1 + betaoptHB)

fhalfLB = f650 / (2 * QLoptLB)
fhalfHB = f650 / (2 * QLoptHB)

VboptLB = Ib * RQLB * QLoptLB
VboptHB = Ib * RQHB * QLoptHB

PGoptLB = (V0LB**2 * (1 + betaoptLB) / (4 * betaoptLB * RQLB * QLoptLB)) \
          * ((1 + VboptLB / V0LB)**2 + (dF1 / fhalfLB)**2)
PGoptHB = (V0HB**2 * (1 + betaoptHB) / (4 * betaoptHB * RQHB * QLoptHB)) \
          * ((1 + VboptHB / V0HB)**2 + (dF1 / fhalfHB)**2)

xlossSSR1 = 0.10     # Coaxial line transmission loss (SSR, 10%)
xloss650 = 0.06      # Waveguide transmission loss (650 MHz, 6%)

# Aggregate power across all PIP-II cryomodule families (W):
#   16 SSR1 + 35 SSR2 + 36 LB650 + 24 HB650
#   Station idle power per cryomodule added with factor 1.33 = (1-eta)/eta for eta=0.43
PSSR = 16 * (PGoptSSR1 + 1.33 * 7000) + 35 * (PGoptSSR2 + 1.33 * 20000)
P650 = 36 * (PGoptLB + 1.33 * 40000) + 24 * (PGoptHB + 70000 * 1.33)

PAll_PIPII = ((1 / (1 - xlossSSR1)) * PSSR + (1 / (1 - xloss650)) * P650) * 1e-3  # kW

etaDCHV = 0.95
etaW = 0.80
DutyF = 20 * (2.8 + 0.55) * 1e-3   # RF duty factor: f_rep*(tau_fill + t_beam)
cost_electricity = 0.08              # $/kWh
hours_on = 5600                      # Operating hours per year

fig2, ax2 = plt.subplots(num=101)
ax2.plot(dF1, (PAll_PIPII / etaDCHV / etaW) * hours_on * cost_electricity * 1e-6,
         label='CW')
ax2.plot(dF1, DutyF * (PAll_PIPII / etaDCHV / etaW) * hours_on * cost_electricity * 1e-6,
         label='Pulsed')
ax2.set_xlabel('Detuning [Hz]')
ax2.set_ylabel('Annual RF Cost [M$]')
ax2.set_xlim([0, 40])
ax2.set_title(
    'PIP-II full linac — annual RF electricity cost vs. detuning\n'
    r'$I_b$ = 2 mA, 16×SSR1 + 35×SSR2 (325 MHz) + 36×LB650 + 24×HB650, '
    r'coupling optimised at $\delta f$ = 20 Hz' + '\n'
    '5600 operating hours/year, $0.08/kWh, '
    r'$\eta_{DC}$ = 0.95, $\eta_w$ = 0.80',
    fontsize=10
)
ax2.legend(frameon=False)
ax2.tick_params(labelsize=12)

# =============================================================================
# Block 3 — LCLS-II and LCLS-II HE: annual RF electricity cost vs. detuning
# =============================================================================

Ib13 = 0.3e-3        # Beam current (A)
RQ13 = 1036          # R/Q 1300 MHz nine-cell cavity (Ohm)
Leff13 = 1.038       # Effective cavity length (m)
Q013 = 2.7e10        # Unloaded Q0
V013 = 16e6 * Leff13  # Accelerating voltage LCLS-II (V)
f13 = 1300e6         # Resonant frequency (Hz)

Vb013 = Ib13 * (RQ13 * Q013)
dF13 = 10            # Static detuning for optimal coupling, LCLS-II (Hz)

betaopt13 = np.sqrt((1 + Vb013 / V013)**2 + (2 * dF13 * Q013 / f13)**2)
QLopt13 = Q013 / (1 + betaopt13)
fhalf13 = f13 / (2 * QLopt13)
Vbopt13 = Ib13 * RQ13 * QLopt13

V013HE = 21e6 * Leff13  # Accelerating voltage LCLS-II HE (V)
betaopt13HE = np.sqrt((1 + Vb013 / V013HE)**2 + (2 * dF13 * Q013 / f13)**2)
QLopt13HE = Q013 / (1 + betaopt13HE)
fhalf13HE = f13 / (2 * QLopt13HE)
Vbopt13HE = Ib13 * RQ13 * QLopt13HE

PGopt013 = (V013**2 * (1 + betaopt13) / (4 * betaopt13 * RQ13 * QLopt13)) \
           * ((1 + Vbopt13 / V013)**2 + (dF1 / fhalf13)**2)
PGopt013HE = (V013HE**2 * (1 + betaopt13HE) / (4 * betaopt13HE * RQ13 * QLopt13HE)) \
             * ((1 + Vbopt13HE / V013HE)**2 + (dF1 / fhalf13HE)**2)

# 280 LCLS-II cavities + 184 LCLS-II HE cavities; same 6% loss factor applied
p13ALL = (1 - xloss650)**-1 * (280 * PGopt013 + 184 * PGopt013HE) * 1e-3  # kW

fig3, ax3 = plt.subplots(num=11)
ax3.plot(dF1, p13ALL * 5600 * 0.14 * 1e-6, linewidth=2, label='Instantaneous')  # 5600 hrs, $0.14/kWh
ax3.set_xlabel('Detuning [Hz]')
ax3.set_ylabel('Annual RF Cost [M$]')
ax3.set_xlim([0, 10])
ax3.set_title(
    'LCLS-II + LCLS-II HE — annual RF electricity cost vs. detuning\n'
    r'$f_0$ = 1300 MHz, $I_b$ = 0.3 mA, 280 cavities (16 MV/m) + 184 HE cavities (21 MV/m), '
    r'$Q_0$ = 2.7×10$^{10}$, coupling optimised at $\delta f$ = 10 Hz'
    '\n5600 operating hours/year, $0.14/kWh',
    fontsize=10
)
ax3.tick_params(labelsize=12)

# =============================================================================
# Numerical output for cross-validation with MATLAB
# =============================================================================

i0 = np.argmin(np.abs(dF1))  # index of dF closest to 0

print("=== BLOCK 1: HB650 single cavity (650 MHz) ===")
print(f"  betaopt                    = {betaopt:.6e}")
print(f"  QLopt                      = {QLopt:.6e}")
print(f"  fhalf (Hz)                 = {fhalf:.6f}")
print(f"  Vbopt (V)                  = {Vbopt:.6e}")
print(f"  PGopt0 at dF=0 (kW)        = {PGopt0[i0]:.6f}")
print(f"  Wall-plug power at dF=0 (kW) = {PGopt0[i0] * (1-xloss650)**-1 / etaDCHV / etaW:.6f}")

print()
print("=== BLOCK 2: PIP-II full linac (325 + 650 MHz) ===")
print(f"  betaoptSSR1                = {betaoptSSR1:.6e}")
print(f"  betaoptSSR2                = {betaoptSSR2:.6e}")
print(f"  betaoptLB                  = {betaoptLB:.6e}")
print(f"  betaoptHB                  = {betaoptHB:.6e}")
print(f"  QLoptSSR1                  = {QLoptSSR1:.6e}")
print(f"  QLoptSSR2                  = {QLoptSSR2:.6e}")
print(f"  QLoptLB                    = {QLoptLB:.6e}")
print(f"  QLoptHB                    = {QLoptHB:.6e}")
print(f"  fhalfSSR1 (Hz)             = {fhalfSSR1:.6f}")
print(f"  fhalfSSR2 (Hz)             = {fhalfSSR2:.6f}")
print(f"  fhalfLB (Hz)               = {fhalfLB:.6f}")
print(f"  fhalfHB (Hz)               = {fhalfHB:.6f}")
print(f"  PGoptSSR1 at dF=0 (W)      = {PGoptSSR1[i0]:.6f}")
print(f"  PGoptSSR2 at dF=0 (W)      = {PGoptSSR2[i0]:.6f}")
print(f"  PGoptLB at dF=0 (W)        = {PGoptLB[i0]:.6f}")
print(f"  PGoptHB at dF=0 (W)        = {PGoptHB[i0]:.6f}")
print(f"  PAll_PIPII at dF=0 (kW)    = {PAll_PIPII[i0]:.6f}")
CW_cost_at_zero   = (PAll_PIPII[i0] / etaDCHV / etaW) * hours_on * cost_electricity * 1e-6
pulse_cost_at_zero = DutyF * CW_cost_at_zero
print(f"  CW annual cost at dF=0 (M$)     = {CW_cost_at_zero:.6f}")
print(f"  Pulsed annual cost at dF=0 (M$) = {pulse_cost_at_zero:.6f}")
print(f"  DutyF                      = {DutyF:.6f}")

print()
print("=== BLOCK 3: LCLS-II + LCLS-II HE (1300 MHz) ===")
print(f"  betaopt13                  = {betaopt13:.6e}")
print(f"  betaopt13HE                = {betaopt13HE:.6e}")
print(f"  QLopt13                    = {QLopt13:.6e}")
print(f"  QLopt13HE                  = {QLopt13HE:.6e}")
print(f"  fhalf13 (Hz)               = {fhalf13:.6f}")
print(f"  fhalf13HE (Hz)             = {fhalf13HE:.6f}")
print(f"  PGopt013 at dF=0 (W)       = {PGopt013[i0]:.6f}")
print(f"  PGopt013HE at dF=0 (W)     = {PGopt013HE[i0]:.6f}")
print(f"  p13ALL at dF=0 (kW)        = {p13ALL[i0]:.6f}")
print(f"  Annual cost at dF=0 (M$)   = {p13ALL[i0] * 5600 * 0.14 * 1e-6:.6f}")

# =============================================================================
# Block 4 — Average power with Gaussian detuning
#
# The generator power is quadratic in detuning:
#   P(df) = A * [(1 + Vbopt/V0)^2 + (df/fhalf)^2]
# For a zero-mean Gaussian df with RMS sigma, E[df^2] = sigma^2, so:
#   E[P] = A * [(1 + Vbopt/V0)^2 + (sigma/fhalf)^2]
# Two cases: sigma = fhalf/2  ->  (sigma/fhalf)^2 = 1/4
#            sigma = fhalf/4  ->  (sigma/fhalf)^2 = 1/16
# =============================================================================

def avg_power(A, beam_term, sigma_over_fhalf):
    """Average generator power (W) for Gaussian detuning."""
    return A * (beam_term**2 + sigma_over_fhalf**2)

# --- prefactors A for each cavity family ---
A_HB650  = V0**2    * (1 + betaopt)    / (4 * betaopt    * RQ    * QLopt)    * 1e-3  # kW
A_SSR1   = V0SSR1**2 * (1 + betaoptSSR1) / (4 * betaoptSSR1 * RQSSR1 * QLoptSSR1)
A_SSR2   = V0SSR2**2 * (1 + betaoptSSR2) / (4 * betaoptSSR2 * RQSSR2 * QLoptSSR2)
A_LB650  = V0LB**2  * (1 + betaoptLB)  / (4 * betaoptLB  * RQLB  * QLoptLB)
A_HB650b = V0HB**2  * (1 + betaoptHB)  / (4 * betaoptHB  * RQHB  * QLoptHB)
A_13     = V013**2   * (1 + betaopt13)  / (4 * betaopt13  * RQ13  * QLopt13)
A_13HE   = V013HE**2 * (1 + betaopt13HE) / (4 * betaopt13HE * RQ13 * QLopt13HE)

# --- beam-loading terms (1 + Vbopt/V0) for each family ---
bt_HB650  = 1 + Vbopt      / V0
bt_SSR1   = 1 + VboptSSR1  / V0SSR1
bt_SSR2   = 1 + VboptSSR2  / V0SSR2
bt_LB650  = 1 + VboptLB    / V0LB
bt_HB650b = 1 + VboptHB    / V0HB
bt_13     = 1 + Vbopt13    / V013
bt_13HE   = 1 + Vbopt13HE  / V013HE

for label, sigma_ratio in [('sigma = BW    (sigma/fhalf = 1)',   1.0),
                            ('sigma = BW/2  (sigma/fhalf = 1/2)', 0.5),
                            ('sigma = BW/4  (sigma/fhalf = 1/4)', 0.25)]:

    print()
    print(f"=== BLOCK 4: Gaussian detuning — {label} ===")

    # -- HB650 single cavity --
    P_avg_HB650 = avg_power(A_HB650, bt_HB650, sigma_ratio)  # kW
    wp_avg_HB650 = P_avg_HB650 * (1 - xloss650)**-1 / etaDCHV / etaW
    print(f"  HB650 avg generator power (kW)       = {P_avg_HB650:.4f}")
    print(f"  HB650 avg wall-plug power (kW)       = {wp_avg_HB650:.4f}")

    # -- PIP-II aggregate --
    P_avg_SSR1   = avg_power(A_SSR1,   bt_SSR1,   sigma_ratio)
    P_avg_SSR2   = avg_power(A_SSR2,   bt_SSR2,   sigma_ratio)
    P_avg_LB650  = avg_power(A_LB650,  bt_LB650,  sigma_ratio)
    P_avg_HB650b = avg_power(A_HB650b, bt_HB650b, sigma_ratio)

    PSSR_avg = 16 * (P_avg_SSR1 + 1.33 * 7000)  + 35 * (P_avg_SSR2 + 1.33 * 20000)
    P650_avg = 36 * (P_avg_LB650 + 1.33 * 40000) + 24 * (P_avg_HB650b + 70000 * 1.33)
    PAll_PIPII_avg = ((1 / (1 - xlossSSR1)) * PSSR_avg
                    + (1 / (1 - xloss650))  * P650_avg) * 1e-3  # kW

    CW_cost_avg    = (PAll_PIPII_avg / etaDCHV / etaW) * hours_on * cost_electricity * 1e-6
    pulse_cost_avg = DutyF * CW_cost_avg

    print(f"  PIP-II avg total power CW (kW)       = {PAll_PIPII_avg:.2f}")
    print(f"  PIP-II CW annual cost (M$/yr)        = {CW_cost_avg:.4f}")
    print(f"  PIP-II pulsed annual cost (M$/yr)    = {pulse_cost_avg:.4f}")

    # -- LCLS-II aggregate --
    P_avg_13   = avg_power(A_13,   bt_13,   sigma_ratio)
    P_avg_13HE = avg_power(A_13HE, bt_13HE, sigma_ratio)

    p13ALL_avg = (1 - xloss650)**-1 * (280 * P_avg_13 + 184 * P_avg_13HE) * 1e-3  # kW
    cost13_avg = p13ALL_avg * 5600 * 0.14 * 1e-6

    print(f"  LCLS-II avg total power (kW)         = {p13ALL_avg:.2f}")
    print(f"  LCLS-II annual cost (M$/yr)          = {cost13_avg:.4f}")

# --- Overlay Gaussian average lines on existing fig2 (PIP-II) and fig3 (LCLS-II) ---
sigma_ratios = [1.0, 0.5, 0.25]
colors       = ['tab:red', 'tab:orange', 'tab:green']
labels_avg   = [r'CW avg, $\sigma$ = BW',
                r'CW avg, $\sigma$ = BW/2',
                r'CW avg, $\sigma$ = BW/4']

for sr, col, lbl in zip(sigma_ratios, colors, labels_avg):
    # PIP-II
    P_SSR1_   = avg_power(A_SSR1,   bt_SSR1,   sr)
    P_SSR2_   = avg_power(A_SSR2,   bt_SSR2,   sr)
    P_LB650_  = avg_power(A_LB650,  bt_LB650,  sr)
    P_HB650_  = avg_power(A_HB650b, bt_HB650b, sr)
    PSSR_  = 16 * (P_SSR1_  + 1.33 * 7000)  + 35 * (P_SSR2_  + 1.33 * 20000)
    P650_  = 36 * (P_LB650_ + 1.33 * 40000) + 24 * (P_HB650_ + 70000 * 1.33)
    avg_kW = ((1/(1-xlossSSR1))*PSSR_ + (1/(1-xloss650))*P650_) * 1e-3
    avg_cost = (avg_kW / etaDCHV / etaW) * hours_on * cost_electricity * 1e-6
    ax2.axhline(avg_cost, linestyle='--', color=col, label=lbl)

    # LCLS-II
    P_13_   = avg_power(A_13,   bt_13,   sr)
    P_13HE_ = avg_power(A_13HE, bt_13HE, sr)
    avg_kW  = (1 - xloss650)**-1 * (280 * P_13_ + 184 * P_13HE_) * 1e-3
    avg_cost_13 = avg_kW * 5600 * 0.14 * 1e-6
    ax3.axhline(avg_cost_13, linestyle='--', color=col, label=lbl.replace('CW avg, ', ''))

ax2.legend(frameon=False)
ax3.legend(frameon=False)

# =============================================================================
# Block 5 — Required RMS detuning for <0.1 expected bandwidth exceedances per hour
#
# At 1 kHz sampling over 1 hour there are 3,600,000 samples.
# Expected exceedances = N * P(|df| > fhalf) = 0.1
# => P(|df| > fhalf) = 0.1 / N = 2*(1 - Phi(fhalf/sigma))
# => fhalf/sigma = Phi_inv(1 - 0.1/(2*N))
# =============================================================================
from scipy.stats import norm as _norm

sample_rate    = 1000          # Hz
duration_hours = 1
N_samples      = sample_rate * 3600 * duration_hours
target_exceedances = 0.1

p_required = target_exceedances / N_samples
z_required = _norm.ppf(1 - p_required / 2)   # fhalf/sigma threshold

fhalfs = {
    'SSR1  (325 MHz)'        : fhalfSSR1,
    'SSR2  (325 MHz)'        : fhalfSSR2,
    'LB650 (650 MHz)'        : fhalfLB,
    'HB650 (650 MHz)'        : fhalfHB,
    'LCLS-II (1300 MHz)'     : fhalf13,
    'LCLS-II HE (1300 MHz)'  : fhalf13HE,
}

print()
print("=== BLOCK 5: Max RMS detuning for <0.1 bandwidth exceedances per hour ===")
print(f"  Sampling rate:              {sample_rate} Hz")
print(f"  Duration:                   {duration_hours} hour")
print(f"  Total samples:              {N_samples:,}")
print(f"  Target expected exceedances:{target_exceedances}")
print(f"  Required P(|df|>BW):        {p_required:.4e}")
print(f"  Required fhalf/sigma (z):   {z_required:.4f}  (i.e. sigma < BW/{z_required:.1f})")
print()
print(f"  {'Cavity':<26}  {'f_half (Hz)':>12}  {'Max sigma (Hz)':>14}")
print("  " + "-" * 56)
for name, fh in fhalfs.items():
    print(f"  {name:<26}  {fh:>12.2f}  {fh/z_required:>14.4f}")

fig1.savefig('PowerCal650_fig1_650MHz_single_cavity.png', dpi=150, bbox_inches='tight')
fig2.savefig('PowerCal650_fig2_PIPII_annual_cost.png', dpi=150, bbox_inches='tight')
fig3.savefig('PowerCal650_fig3_LCLSII_annual_cost.png', dpi=150, bbox_inches='tight')

plt.show()
