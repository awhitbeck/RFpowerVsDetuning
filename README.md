# Genesis Resonance Control

## PowerCal650V2 — RF Power Requirements Calculator

**Source presentation:** "Power requirements for the PIP II linac," B. Chase and V. Yakovlev, Fermilab, 19 July 2018.

This script computes the RF generator power required to maintain stable accelerating fields in SRF cavities across three accelerator systems: PIP-II (325 MHz and 650 MHz) and LCLS-II / LCLS-II HE (1300 MHz). It produces three plots and prints key intermediate quantities to the terminal for cross-validation.

---

## Running the Python script

**Requirements:** Python 3, `numpy`, `matplotlib`, `scipy`.

Install dependencies if needed:

```bash
pip install numpy matplotlib scipy
```

Run the script from the project directory:

```bash
python3 PowerCal650V2.py
```

Three PNG files will be saved in the working directory and the plots will open interactively:

- `PowerCal650_fig1_650MHz_single_cavity.png`
- `PowerCal650_fig2_PIPII_annual_cost.png`
- `PowerCal650_fig3_LCLSII_annual_cost.png`

Key computed values will be printed to the terminal for each of the five blocks.

---

## Running the MATLAB script

Open `PowerCal650V2.m` in MATLAB and run it, or execute it from the MATLAB command window:

```matlab
run('PowerCal650V2.m')
```

Or from a terminal with MATLAB on the path:

```bash
matlab -batch "run('PowerCal650V2.m')"
```

Three figure windows will open and key computed values will be printed to the command window. Note: MATLAB will emit a legend warning in Block 1 because the original legend call specifies three entries but only one curve is plotted; this does not affect any computed values.

---

## Cross-validating Python against MATLAB

Both scripts print the same quantities in the same order and format. To compare, run both and diff the terminal output. All values should agree to the precision shown (6 significant figures).

---

## Background and Governing Formula

The script implements the steady-state generator power formula for a beam-loaded SRF cavity (Formula 1 of the reference presentation):

$$P = \frac{U_0^2(1+\beta_c)^2}{4\beta_c(R/Q)Q_0}\left[\left(1 + \frac{I_b\cos\phi_a\,(R/Q)Q_0}{U_0(1+\beta_c)}\right)^2 + \left(\frac{2\delta f\, Q_0}{f_0(1+\beta_c)}\right)^2\right]$$

Here $\beta_c$ is the coupling coefficient, $I_b$ is the beam current, $\phi_a$ is the synchronous (accelerating) phase, $U_0$ is the accelerating voltage, $R/Q$ is the cavity shunt impedance normalized by quality factor, $Q_0$ is the unloaded quality factor, $f_0$ is the resonant frequency, and $\delta f$ is the cavity detuning. This power is minimized when the coupling is set to:

$$\beta_c = \sqrt{\left(1 + \frac{I_b\cos\phi_a\,(R/Q)Q_0}{U_0}\right)^2 + \left(\frac{2\delta f\, Q_0}{f_0}\right)^2}$$

The total wall-plug power draw per cavity station is then:

$$P_{\text{wall plug}} = \frac{P}{1-\chi_\text{loss}} + P_\text{station}\frac{1-\eta}{\eta}$$

where $\chi_\text{loss}$ is the fractional transmission loss in the waveguide or coaxial feed, $\eta$ is the RF source efficiency, and $P_\text{station}$ is the idle (no-beam) power draw of the RF source station.

---

## What the Script Does

The script is organized into three sequential calculation blocks.

**Block 1 — 650 MHz single-cavity power curve (Figure 1).** For the 650 MHz high-beta (HB650, B92 geometry) cavity, the script computes the optimal coupling and loaded quality factor that minimize generator power at a 40 Hz static detuning offset. It then sweeps detuning from −50 Hz to +50 Hz and plots generator power in kilowatts after correcting for waveguide transmission losses (6%), DC high-voltage supply efficiency (95%), and klystron wall-plug efficiency (80%). Annotations on the figure mark the reflected-power region and the detuning at which all RF power is delivered to the beam.

**Block 2 — PIP-II total annual RF electricity cost (Figure 101).** This block computes aggregate RF power across all four SRF cryomodule families in the PIP-II linac: 16 SSR1 cryomodules (325 MHz), 35 SSR2 cryomodules (325 MHz), 36 low-beta 650 MHz (LB650) cryomodules, and 24 high-beta 650 MHz (HB650) cryomodules. For each family the optimal coupling is determined at a static detuning offset of 20 Hz. The idle RF source station power ($P_\text{station}$) for each section—7 kW (SSR1), 20 kW (SSR2), 40 kW (LB650), and 70 kW (HB650)—is added with a factor of 1.33, which equals $(1-\eta)/\eta$ for an RF source efficiency of $\eta = 0.43$ as specified in the reference presentation. The total is corrected for waveguide losses and efficiency factors, then multiplied by assumed operating hours (5600 per year) and an electricity rate ($0.08/kWh) to produce the annual RF electricity cost in millions of dollars. Both a continuous-wave (CW) and a pulsed beam scenario are plotted on the same axes.

**Block 3 — LCLS-II and LCLS-II HE annual RF cost (Figure 11).** The same methodology is applied to the 1300 MHz nine-cell cavities of the LCLS-II (280 cavities) and LCLS-II HE (184 cavities) linacs. A separate electricity rate of $0.14/kWh is used, reflecting the different operating site.

**Block 4 — Average power with Gaussian-distributed detuning.** The instantaneous power curves in Blocks 2 and 3 show power as a function of a fixed detuning offset. In practice, microphonics-driven detuning is stochastic. This block treats the cavity detuning as a zero-mean Gaussian random variable and computes the resulting average generator power analytically. Because the power formula is quadratic in detuning:

$$P(\delta f) = A\left[(1 + V_b/V_0)^2 + (\delta f / f_\text{half})^2\right]$$

the expectation over a Gaussian with RMS $\sigma$ reduces to:

$$\langle P \rangle = A\left[(1 + V_b/V_0)^2 + (\sigma / f_\text{half})^2\right]$$

Three values of $\sigma$ are evaluated: $\sigma = f_\text{half}$, $\sigma = f_\text{half}/2$, and $\sigma = f_\text{half}/4$. The resulting average annual costs are overlaid as horizontal dashed lines on Figures 2 and 3, allowing direct comparison with the instantaneous power curves.

**Block 5 — Maximum allowable RMS detuning for rare bandwidth exceedances.** This block asks: at 1 kHz sampling over one hour, how small must the RMS detuning be such that the expected number of samples with $|\delta f| > f_\text{half}$ is less than 0.1? With $N = 3{,}600{,}000$ samples, this requires:

$$P(|\delta f| > f_\text{half}) = \frac{0.1}{N} \approx 2.8 \times 10^{-8}$$

which corresponds to a threshold of $f_\text{half}/\sigma \approx 5.6$ standard deviations, i.e., $\sigma < f_\text{half}/5.6$. The absolute maximum allowable RMS detuning is printed for each cavity family.

---

## Key Assumptions

**On-crest acceleration.** The code sets the beam voltage as $V_b = I_b(R/Q)Q_L$ without a $\cos\phi_a$ factor, which is equivalent to assuming $\cos\phi_a = 1$, i.e., that all cavities are operated on crest. The reference presentation notes that $R/Q$ and $U_0$ both depend on particle velocity $\beta$, and the synchronous phase varies along the linac (from roughly −90° near injection to near 0° at high energy). The on-crest assumption will overestimate the beam-loading contribution for off-crest cavities.

**Fixed representative cavity parameters.** Each cavity family is represented by a single set of design values for $Q_0$, $R/Q$, effective cavity length, resonant frequency, and beam current. Cavity-to-cavity variation in these parameters is not modeled. The reference presentation shows that $R/Q(\beta)$ varies substantially along the linac as particle velocity increases.

**Optimal coupling at fixed detuning offset.** The external quality factor is chosen to minimize generator power at a specified static detuning: 40 Hz for the 650 MHz single-cavity plot (Block 1), 20 Hz for PIP-II cryomodule families (Block 2), and 10 Hz for LCLS-II (Block 3). The reference presentation notes that for nominal operation the power-determining quantity is the rms detuning, estimated as $\delta f_\text{rms} \approx \delta f_\text{max}/6 \approx 3.3$ Hz for a 20 Hz maximum. The values used in the code are considerably larger than this rms estimate, so the code represents a more conservative or worst-case coupling scenario rather than a nominal one.

**Steady-state detuning model.** The power formula is the steady-state expression for a single-mode resonator. It does not account for time-varying or stochastic microphonics, transient cavity fill dynamics, or the action of feedback control. The reference presentation treats $\delta f$ as a fixed offset representing r.m.s. microphonics amplitude.

**Waveguide and transmission losses.** A fixed fractional loss of 6% is applied to the 650 MHz (waveguide-fed) circuits and 10% to the 325 MHz SSR1/SSR2 (coaxial-fed) circuits. These values are taken directly from the reference presentation (slide 10).

**Power conversion efficiencies.** The code applies a DC high-voltage supply efficiency of 95% and a klystron wall-plug efficiency of 80%. The reference presentation specifies an RF source efficiency of $\eta = 0.43$ for PIP-II, which is substantially lower than 0.80. This discrepancy means the code underestimates the wall-plug power relative to the analysis in the presentation; it may reflect a different (more optimistic) klystron or solid-state amplifier efficiency assumption.

**Station idle power and the 1.33 factor.** The static power figures added per cryomodule (7 kW for SSR1, 20 kW for SSR2, 40 kW for LB650, 70 kW for HB650) represent the idle RF source station power $P_\text{station}$ from the reference presentation. These are multiplied by 1.33, which corresponds to $(1-\eta)/\eta$ evaluated at $\eta = 0.43$, the RF source efficiency given in the presentation. This term accounts for heat dissipated in the RF source even when it is not delivering useful power to the cavity.

**Pulsed duty factor.** For the PIP-II pulsed scenario, the duty factor is computed as `DutyF = 20 × (2.8 + 0.55) ms`. This follows the presentation's definition $D_{RF} = f_\text{rep}(\tau_\text{fill} + t_\text{beam})$, with a repetition rate of 20 Hz, a representative cavity fill time of 2.8 ms, and a beam-on window of 0.55 ms. The fill time is specific to a representative cavity and is not recomputed separately for each cryomodule family.

**Single-cavity independence.** All power calculations treat each cavity as independent. Inter-cavity coupling, shared klystron configurations serving multiple cavities, and cryomodule-level collective effects are not modeled.

**Operating hours and electricity cost.** Annual costs are computed assuming 5600 operating hours per year. The electricity rate is $0.08/kWh for PIP-II and $0.14/kWh for LCLS-II.

---

## Context from the Reference Presentation

The reference presentation evaluates three distinct operating regimes for PIP-II and reports their total power consumption and annual electricity cost (at 5600 hours/year and 5.8 ¢/kWh):

| Regime | Total power (MW) | Efficiency (%) | Annual cost (M$/yr) |
|---|---|---|---|
| Pulsed RF and pulsed beam | 2.6 | 0.7 | 0.84 |
| Pulsed beam, CW RF | 10 | 0.18 | 3.3 |
| CW RF and CW beam | 10.9 | 15 | 3.5 |

The presentation concludes that operating with a pulsed beam but continuous-wave RF—a scenario relevant when resonance control does not allow the RF to be gated with the beam—requires approximately 10 MW from the grid and costs roughly 2.5 M$/year more than full pulsed operation. The script computes the RF-only portion of this cost as a function of detuning, providing a tool for understanding how resonance control performance (i.e., how well detuning is suppressed) translates into operational electricity expenditure.
