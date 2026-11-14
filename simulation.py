"""
Simulation and Analysis of Sampling Theorem and Aliasing Using Python
=====================================================================
Subject : Signals & Systems (Innovative Assessment)

What this program does
----------------------
1. Generates a continuous-time reference signal   x(t) = A sin(2*pi*f*t + phi)
2. Samples it at three different rates:
       Experiment 1 : under-sampling      (fs =  6 Hz)  -> aliasing
       Experiment 2 : critical sampling   (fs = 10 Hz)  -> exactly 2f
       Experiment 3 : over-sampling       (fs = 40 Hz)  -> well above 2f
3. Reconstructs the signal from its samples using sinc interpolation.
4. Saves six PNG graphs into the folder  graphs/
5. Prints the important calculated values.

Run with:   python simulation.py
"""

import math
import os

import matplotlib
matplotlib.use("Agg")            # draw to files only, so no display is needed
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------------
# 1. SIMULATION PARAMETERS (all values given in the assignment)
# ----------------------------------------------------------------------------
AMPLITUDE = 1.0                  # A
SIGNAL_FREQ = 5.0                # f  in Hz
PHASE = math.pi / 6              # phi in radians
DURATION = 1.0                   # seconds
FS_UNDER = 6.0                   # Hz  (below Nyquist rate)
FS_CRITICAL = 10.0               # Hz  (equal to Nyquist rate = 2f)
FS_OVER = 40.0                   # Hz  (well above Nyquist rate)
DENSE_POINTS = 5000              # points used to draw the "continuous" signal
GRAPH_DIR = "graphs"             # output folder for PNG files
DPI = 200                        # image resolution

# Colours used consistently in every plot
C_ORIG, C_SAMP, C_ALIAS, C_RECON = "#1f77b4", "#d62728", "#2ca02c", "#ff7f0e"


# ----------------------------------------------------------------------------
# 2. SIGNAL GENERATION
# ----------------------------------------------------------------------------
def check_inputs(amplitude, freq, duration, fs):
    """Stop early with a clear message if a parameter is not physically valid."""
    if amplitude <= 0:
        raise ValueError("Amplitude must be positive.")
    if freq <= 0:
        raise ValueError("Signal frequency must be positive.")
    if duration <= 0:
        raise ValueError("Duration must be positive.")
    if fs <= 0:
        raise ValueError("Sampling frequency must be positive.")


def generate_continuous_signal(amplitude, freq, phase, duration, n_points=DENSE_POINTS):
    """Return (t, x) for x(t) = A sin(2*pi*f*t + phi) on a very fine time grid.
    A computer cannot store a truly continuous signal, so a dense grid
    (5000 points in 1 s) is used to stand in for it."""
    check_inputs(amplitude, freq, duration, 1.0)
    t = np.linspace(0.0, duration, n_points)
    x = amplitude * np.sin(2 * np.pi * freq * t + phase)
    return t, x


# ----------------------------------------------------------------------------
# 3. SAMPLING
# ----------------------------------------------------------------------------
def sample_signal(amplitude, freq, phase, duration, fs):
    """Sample x(t) at t = n*Ts, n = 0, 1, ..., floor(fs*duration).
    Returns (t_n, x_n) where Ts = 1/fs."""
    check_inputs(amplitude, freq, duration, fs)
    n = np.arange(0, int(math.floor(fs * duration + 1e-9)) + 1)
    t_n = n / fs
    x_n = amplitude * np.sin(2 * np.pi * freq * t_n + phase)
    return t_n, x_n


# ----------------------------------------------------------------------------
# 4. ALIAS FREQUENCY
# ----------------------------------------------------------------------------
def alias_frequency(freq, fs):
    """Apparent (alias) frequency seen after sampling a tone of frequency
    `freq` at rate `fs`:   f_alias = | f - k*fs |,  k = nearest integer to f/fs.
    The result always lies between 0 and fs/2."""
    k = math.floor(freq / fs + 0.5)
    return abs(freq - k * fs)


def alias_signal(amplitude, freq, phase, fs, t):
    """The low-frequency sinusoid that passes exactly through the samples.
    Since sin(2*pi*f*n/fs + phi) = sin(2*pi*(f - k*fs)*n/fs + phi), the alias is
    A sin(2*pi*(f - k*fs)*t + phi)  (frequency may come out negative, which just
    means the apparent waveform is phase-reversed)."""
    k = math.floor(freq / fs + 0.5)
    return amplitude * np.sin(2 * np.pi * (freq - k * fs) * t + phase)


# ----------------------------------------------------------------------------
# 5. SINC RECONSTRUCTION
# ----------------------------------------------------------------------------
def sinc_reconstruct(t_n, x_n, fs, t):
    """Whittaker-Shannon interpolation:
        x_r(t) = sum_n  x[n] * sinc( (t - n*Ts) / Ts ),   Ts = 1/fs
    np.sinc(u) = sin(pi*u)/(pi*u), exactly the normalised sinc needed here.
    The sum has only finitely many terms (one per available sample), so this
    is an APPROXIMATION of ideal reconstruction, which needs infinitely many."""
    Ts = 1.0 / fs
    # matrix of shape (len(t), len(t_n)); each column is one shifted sinc
    kernel = np.sinc((t[:, None] - t_n[None, :]) / Ts)
    return kernel @ x_n


def rms(v):
    """Root-mean-square value of an array."""
    return float(np.sqrt(np.mean(np.square(v))))


# ----------------------------------------------------------------------------
# 6. PLOTTING HELPERS
# ----------------------------------------------------------------------------
def style_axes(ax, title):
    """Apply the common label / grid / legend style to an axis."""
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Amplitude")
    ax.set_xlim(0, DURATION)
    ax.set_ylim(-1.35, 1.35)
    ax.grid(True, linestyle="--", alpha=0.5)
    # legend placed below the plot so it never hides the waveform or samples
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2,
              fontsize=8, framealpha=0.95)


def draw_signal_and_samples(ax, t, x, t_n, x_n, fs):
    """Draw the continuous signal plus sample points (stems + markers)."""
    ax.plot(t, x, color=C_ORIG, linewidth=1.8, label="Original x(t), 5 Hz")
    markerline, stemlines, baseline = ax.stem(
        t_n, x_n, linefmt=":", markerfmt="o", basefmt=" ")
    plt.setp(markerline, color=C_SAMP, markersize=6, zorder=5,
             label=f"Samples x[n] (fs = {fs:g} Hz, {len(t_n)} points)")
    plt.setp(stemlines, color=C_SAMP, linewidth=0.9, alpha=0.7)
    ax.axhline(0, color="black", linewidth=0.6)


def save_figure(fig, filename):
    """Save a figure into the graphs folder, with error handling."""
    path = os.path.join(GRAPH_DIR, filename)
    try:
        fig.tight_layout(h_pad=2.0)
        fig.savefig(path, dpi=DPI, bbox_inches="tight")
    except OSError as err:
        raise SystemExit(f"Could not save {path}: {err}")
    finally:
        plt.close(fig)
    print(f"   saved -> {path}")


# ----------------------------------------------------------------------------
# 7. THE SIX GRAPHS
# ----------------------------------------------------------------------------
def plot_original(t, x):
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(t, x, color=C_ORIG, linewidth=2, label="x(t) = sin(2π·5·t + π/6)")
    ax.axhline(0, color="black", linewidth=0.6)
    style_axes(ax, "Original Continuous-Time Signal (5 Hz Sinusoid, Phase π/6)")
    save_figure(fig, "original_signal.png")


def plot_undersampling(t, x, t_n, x_n, fs, f_alias):
    fig, ax = plt.subplots(figsize=(10, 4.8))
    draw_signal_and_samples(ax, t, x, t_n, x_n, fs)
    ax.plot(t, alias_signal(AMPLITUDE, SIGNAL_FREQ, PHASE, fs, t), "--",
            color=C_ALIAS, linewidth=2,
            label=f"Alias: apparent {f_alias:g} Hz sinusoid through the samples")
    style_axes(ax, f"Experiment 1: Under-Sampling at fs = {fs:g} Hz (Aliasing)")
    save_figure(fig, "undersampling.png")


def plot_nyquist(t, x, t_n, x_n, fs):
    fig, ax = plt.subplots(figsize=(10, 4.8))
    draw_signal_and_samples(ax, t, x, t_n, x_n, fs)
    # Another 5 Hz sinusoid that passes through exactly the same samples:
    other = AMPLITUDE * math.sin(PHASE) * np.cos(2 * np.pi * SIGNAL_FREQ * t)
    ax.plot(t, other, "--", color=C_ALIAS, linewidth=1.8,
            label="A different 5 Hz sinusoid, 0.5·cos(2π·5·t), through the same samples")
    style_axes(ax, f"Experiment 2: Critical Sampling at fs = {fs:g} Hz (Nyquist Rate)")
    save_figure(fig, "nyquist_sampling.png")


def plot_oversampling(t, x, t_n, x_n, fs):
    fig, ax = plt.subplots(figsize=(10, 4.8))
    draw_signal_and_samples(ax, t, x, t_n, x_n, fs)
    style_axes(ax, f"Experiment 3: Over-Sampling at fs = {fs:g} Hz")
    save_figure(fig, "oversampling.png")


def plot_reconstruction(t, x, cases):
    """cases: list of dicts with keys fs, t_n, x_n, x_r, label.
    Rows 1-3 show reconstruction for each fs; row 4 shows all errors together."""
    fig, axes = plt.subplots(4, 1, figsize=(10, 15))
    for ax, c in zip(axes[:3], cases):
        ax.plot(t, x, color=C_ORIG, linewidth=1.8, label="Original x(t)")
        ax.plot(t, c["x_r"], "--", color=C_RECON, linewidth=2,
                label="Sinc-reconstructed x_r(t)")
        ax.plot(c["t_n"], c["x_n"], "o", color=C_SAMP, markersize=5, zorder=5,
                label=f"Samples (fs = {c['fs']:g} Hz)")
        style_axes(ax, f"Sinc Reconstruction from {c['label']} Samples (fs = {c['fs']:g} Hz)")
    ax = axes[3]
    for c, col in zip(cases, (C_ALIAS, C_SAMP, C_ORIG)):
        ax.plot(t, np.abs(x - c["x_r"]), color=col, linewidth=1.6,
                label=f"|x(t) − x_r(t)|,  fs = {c['fs']:g} Hz")
    style_axes(ax, "Absolute Reconstruction Error for the Three Sampling Rates")
    ax.set_ylabel("Amplitude (absolute error)")
    ax.set_ylim(0, 2.1)
    save_figure(fig, "reconstruction.png")


def plot_comparison(t, x, cases):
    fig, axes = plt.subplots(3, 1, figsize=(10, 12))
    for ax, c in zip(axes, cases):
        draw_signal_and_samples(ax, t, x, c["t_n"], c["x_n"], c["fs"])
        style_axes(ax, f"{c['label']}: fs = {c['fs']:g} Hz  "
                       f"(fs/f = {c['fs'] / SIGNAL_FREQ:g})")
    fig.suptitle("Comparison of Under-, Critical and Over-Sampling of a 5 Hz Sinusoid",
                 fontsize=14, fontweight="bold", y=1.0)
    save_figure(fig, "comparison.png")


# ----------------------------------------------------------------------------
# 8. MAIN PROGRAM
# ----------------------------------------------------------------------------
def run_simulation():
    """Run all experiments, save the graphs, and return the key results."""
    os.makedirs(GRAPH_DIR, exist_ok=True)           # create graphs/ if missing

    t, x = generate_continuous_signal(AMPLITUDE, SIGNAL_FREQ, PHASE, DURATION)
    nyquist_rate = 2 * SIGNAL_FREQ

    print("=" * 66)
    print(" SAMPLING THEOREM AND ALIASING - SIMULATION RESULTS")
    print("=" * 66)
    print(f" Signal           : x(t) = {AMPLITUDE:g} sin(2*pi*{SIGNAL_FREQ:g}*t + pi/6)")
    print(f" Signal frequency : f = {SIGNAL_FREQ:g} Hz")
    print(f" Phase            : {PHASE:.4f} rad (30 degrees)")
    print(f" Duration         : {DURATION:g} s")
    print(f" Nyquist rate     : 2f = {nyquist_rate:g} Hz  (minimum rate is strictly above this)")
    print("-" * 66)

    experiments = [("Experiment 1 (Under-sampling)",    FS_UNDER),
                   ("Experiment 2 (Critical sampling)", FS_CRITICAL),
                   ("Experiment 3 (Over-sampling)",     FS_OVER)]
    short_labels = ["Under-Sampled", "Critically Sampled", "Over-Sampled"]

    cases, results = [], []
    for (name, fs), short in zip(experiments, short_labels):
        t_n, x_n = sample_signal(AMPLITUDE, SIGNAL_FREQ, PHASE, DURATION, fs)
        x_r = sinc_reconstruct(t_n, x_n, fs, t)
        f_alias = alias_frequency(SIGNAL_FREQ, fs)
        # Edge effects: compare error over the whole record with the middle part
        mid = (t >= 0.25 * DURATION) & (t <= 0.75 * DURATION)
        res = dict(name=name, fs=fs, Ts=1 / fs, nyquist_freq=fs / 2,
                   n_samples=len(t_n), f_alias=f_alias,
                   rms_total=rms(x - x_r), rms_mid=rms((x - x_r)[mid]),
                   max_err=float(np.max(np.abs(x - x_r))),
                   samples_first6=[round(float(v), 4) for v in x_n[:6]])
        results.append(res)
        cases.append(dict(fs=fs, t_n=t_n, x_n=x_n, x_r=x_r, label=short))

        print(f" {name}")
        print(f"    Sampling frequency fs  : {fs:g} Hz   (Ts = {1 / fs:.4f} s)")
        print(f"    Nyquist frequency fs/2 : {fs / 2:g} Hz")
        print(f"    Number of samples      : {len(t_n)}")
        print(f"    fs vs Nyquist rate     : "
              f"{'BELOW' if fs < nyquist_rate else 'EQUAL TO' if fs == nyquist_rate else 'ABOVE'}")
        print(f"    Alias frequency        : {f_alias:g} Hz")
        print(f"    Reconstruction RMS err : {res['rms_total']:.4f} (all)  |  "
              f"{res['rms_mid']:.4f} (middle 0.25-0.75 s)")
        print(f"    Max reconstruction err : {res['max_err']:.4f}")
        print("-" * 66)

    print(" Alias check for Experiment 1:  |5 - 1*6| = 1 Hz")
    # Numerical proof that the 1 Hz alias passes through every under-sample
    t6, x6 = cases[0]["t_n"], cases[0]["x_n"]
    diff = np.max(np.abs(x6 - alias_signal(AMPLITUDE, SIGNAL_FREQ, PHASE, FS_UNDER, t6)))
    print(f" Max |sample - alias value| at the 6 Hz sample instants = {diff:.2e}")
    print("=" * 66)

    print(" Saving graphs ...")
    plot_original(t, x)
    plot_undersampling(t, x, cases[0]["t_n"], cases[0]["x_n"], FS_UNDER, results[0]["f_alias"])
    plot_nyquist(t, x, cases[1]["t_n"], cases[1]["x_n"], FS_CRITICAL)
    plot_oversampling(t, x, cases[2]["t_n"], cases[2]["x_n"], FS_OVER)
    plot_reconstruction(t, x, cases)
    plot_comparison(t, x, cases)
    print(" Done.")
    return results


if __name__ == "__main__":
    run_simulation()
