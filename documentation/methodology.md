# Methodology

This document explains **how** the simulation was designed and **why** each choice was made, so that it can be explained confidently in an evaluation.

## 1. Signal and parameters

| Parameter | Value | Reason |
|---|---|---|
| Waveform | x(t) = A sin(2πft + φ) | Single tone: the alias can be calculated by hand |
| Amplitude A | 1 | Normalised |
| Frequency f | 5 Hz | Nyquist rate is a simple 10 Hz |
| Phase φ | π/6 | A non-zero phase makes the critical-sampling problem visible (samples = ±A sin φ = ±0.5) |
| Duration | 1 s | Five full cycles |
| Sampling rates | 6, 10, 40 Hz | Below, equal to, and well above the Nyquist rate |

## 2. Representing a "continuous" signal

A computer cannot hold a truly continuous signal. The program evaluates x(t) on a **dense grid of 5000 points** over one second (spacing about 0.2 ms, an effective rate of about 5000 Hz, a thousand times the signal frequency). This grid stands in for the continuous signal in the plots and in the error calculation.

## 3. Sampling

Samples are taken at t = n / f_s for n = 0, 1, …, floor(f_s · T), so both end points of the interval are included. This gives 7, 11 and 41 samples for 6, 10 and 40 Hz. A tiny constant (1e-9) inside the `floor` avoids a rounding problem when f_s · T is an exact integer.

## 4. Alias frequency

For a tone of frequency f sampled at f_s:

    f_a = | f − k · f_s |,   k = nearest integer to f / f_s

This works because sin(2πf·n/f_s + φ) = sin(2π(f − k·f_s)·n/f_s + φ): adding a whole number of cycles does not change a sine. For f = 5 Hz and f_s = 6 Hz, k = 1 and f_a = 1 Hz.

The program also builds the alias sinusoid A·sin(2π(f − k·f_s)t + φ) and checks that it passes through every one of the seven 6 Hz samples. The difference is about 4e-15, i.e. floating-point round-off only.

At f_s = 10 Hz the signal frequency is exactly the folding frequency f_s / 2. The samples are x[n] = A sin φ · (−1)ⁿ = ±0.5. The sine part of the signal, A cos φ · sin(2πft), is zero at all sample instants, so it is invisible to the sampler. The code draws a second sinusoid, 0.5·cos(2π·5·t), that passes through exactly the same samples, to show that the original is not uniquely determined.

## 5. Sinc reconstruction

Whittaker–Shannon interpolation:

    x_r(t) = Σ x[n] · sinc((t − n·T_s) / T_s),   sinc(u) = sin(πu) / (πu)

`np.sinc` is exactly this normalised sinc. A matrix of shape (number of time points, number of samples) is built in which each column is one shifted sinc; multiplying it by the vector of samples gives the weighted sum for all time points in one step.

**Limitation (important):** the formula needs samples for all n from −∞ to +∞. The simulation only has samples from t = 0 to t = 1 s, so the sum is truncated. Contributions from the missing samples are absent, so the reconstruction is an **approximation** whose error is largest near t = 0 and t = 1 s. The project never claims perfect reconstruction from a finite record.

## 6. Error measurement

- **RMS error** over the whole record, and over the middle section 0.25 s ≤ t ≤ 0.75 s (to separate edge effects from interior accuracy).
- **Maximum absolute error.**

## 7. Plots

Every plot has a title, axis labels (Time (seconds), Amplitude), a legend (placed below the axes so that it never hides data), grid lines and 200 dpi resolution. Colours are consistent: blue = original signal, red = samples, green = alias / alternative signal, orange = reconstruction. Plotting uses the non-interactive `Agg` back-end, so the program works without a display. Graphs are saved automatically in `graphs/`.

## 8. Code structure

| Function | Responsibility |
|---|---|
| `check_inputs` | Validates parameters |
| `generate_continuous_signal` | Dense reference signal |
| `sample_signal` | Sample times and values |
| `alias_frequency`, `alias_signal` | Alias calculation and alias waveform |
| `sinc_reconstruct` | Sinc interpolation |
| `rms` | RMS error helper |
| `plot_*`, `save_figure` | Graph creation and saving |
| `run_simulation` | Runs the three experiments, prints values, saves graphs |

## 9. Validation

- Nyquist rate: 2 × 5 Hz = 10 Hz (checked by hand and printed by the program).
- Alias at 6 Hz: |5 − 6| = 1 Hz (checked by hand and verified numerically against the samples).
- Critical-sampling samples: ±0.5 = ±A sin(π/6), matching the printed values.
- All six graph files are produced by one run of `python simulation.py`.
- Values in the report and viva guide were taken from the program output, not typed in by hand.

## 10. Known limitations

- Single-tone signal only.
- Finite record, so reconstruction has edge errors.
- No noise, quantisation, jitter, anti-aliasing filter or practical hold circuit.
