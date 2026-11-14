# Simulation and Analysis of Sampling Theorem and Aliasing Using Python

**Subject:** Signals & Systems (Innovative Assessment)
**Student:** _Prachi Gupta_ | **Roll No.:** _202410101150245_ | **Section:** _5D_
**University:** _Shri Ramswaroop Memorial University_ | **Department:** _Computer Science_
**Faculty:** _Mr. Sandeep Tiwari_ | **Academic Session:** _2026-27_

> Replace the bracketed placeholders above with your own details.

---

## 1. Project Overview

This project demonstrates the **Nyquist–Shannon sampling theorem** and **aliasing** with a Python simulation. A 5 Hz continuous-time sinusoid is sampled below, at and above the Nyquist rate, reconstructed with **sinc interpolation**, and analysed with graphs and error measurements. A complete technical report and a viva preparation guide accompany the code.

## 2. Objectives

- Explain what sampling is and what the sampling theorem states.
- Distinguish the **Nyquist rate** (2·f_max) from the **Nyquist frequency** (f_s / 2).
- Show why aliasing occurs and calculate the alias frequency.
- Compare under-sampling, critical sampling and over-sampling.
- Reconstruct the signal with sinc interpolation and measure the error.
- Explain why a finite number of samples cannot give perfect reconstruction.
- Relate the theory to real-world applications.

## 3. Technologies Used

| Tool | Use |
|---|---|
| Python 3 | Programming language |
| NumPy | Numerical computation (time vectors, samples, sinc kernel, errors) |
| Matplotlib | Graphs saved as PNG files |

SciPy is **not** needed.

## 4. Theoretical Background

- **Sampling:** x[n] = x(nT_s) = A sin(2πf·n/f_s + φ), with T_s = 1 / f_s.
- **Sampling theorem:** a band-limited signal can be reconstructed from its samples if **f_s > 2·f_max**.
- **Nyquist rate:** 2·f_max (a property of the signal). **Nyquist frequency:** f_s / 2 (a property of the sampler).
- **Aliasing:** if f_s is too low, a frequency f appears at **f_a = |f − k·f_s|**, with k the integer nearest to f / f_s.
- **Sinc interpolation:** x_r(t) = Σ x[n] · sinc((t − nT_s) / T_s), where sinc(u) = sin(πu) / (πu).
- Ideal reconstruction needs an **infinite** number of samples. With a finite record, the result is an approximation and shows edge errors.

## 5. Simulation Experiments

Reference signal: **x(t) = sin(2π·5·t + π/6)**, duration 1 s. Nyquist rate = 10 Hz.

| Experiment | f_s | Condition | Expected result |
|---|---|---|---|
| 1. Under-sampling | 6 Hz | f_s < 2f | Aliasing: the 5 Hz tone appears as \|5 − 6\| = **1 Hz** |
| 2. Critical sampling | 10 Hz | f_s = 2f | Samples alternate ±0.5 (= ±A sin φ); amplitude and phase are ambiguous |
| 3. Over-sampling | 40 Hz | f_s > 2f | Dense representation; accurate reconstruction away from the ends |

## 6. Installation

1. Install **Python 3.8 or later** from <https://www.python.org>.
2. Download or clone this repository:
   ```bash
   git clone https://github.com/<your-username>/Sampling-Theorem-and-Aliasing.git
   cd Sampling-Theorem-and-Aliasing
   ```
3. (Optional) create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate          # Windows
   source venv/bin/activate       # macOS / Linux
   ```
4. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

## 7. Execution

```bash
python simulation.py
```

No manual changes are needed. The `graphs/` folder is created automatically (if missing) and the six PNG files are saved in it. The program also prints the signal frequency, Nyquist rate, sampling frequencies, alias frequencies and reconstruction errors.

## 8. Sample Output

Console output from an actual run (abridged):

```
 Signal frequency : f = 5 Hz
 Nyquist rate     : 2f = 10 Hz
 Experiment 1 (Under-sampling)   fs = 6 Hz   samples = 7   alias = 1 Hz
 Experiment 2 (Critical sampling) fs = 10 Hz  samples = 11  alias = 5 Hz
 Experiment 3 (Over-sampling)    fs = 40 Hz  samples = 41  alias = 5 Hz
 Max |sample - alias value| at the 6 Hz sample instants = 3.61e-15
```

The full output (including reconstruction errors) is printed when you run the program.

Generated graphs:

| File | What it shows |
|---|---|
| `graphs/original_signal.png` | The continuous-time 5 Hz reference signal |
| `graphs/undersampling.png` | 6 Hz samples and the 1 Hz alias passing through them |
| `graphs/nyquist_sampling.png` | 10 Hz samples (alternating ±0.5) and a different 5 Hz sinusoid through the same samples |
| `graphs/oversampling.png` | 40 Hz samples densely following the signal |
| `graphs/reconstruction.png` | Sinc reconstruction for all three rates, plus absolute error |
| `graphs/comparison.png` | The three sampling conditions stacked for comparison |

## 9. Repository Structure

```
Sampling-Theorem-and-Aliasing/
├── simulation.py
├── requirements.txt
├── README.md
├── Technical_Report.pdf
├── Technical_Report.docx          (editable version: fill in your details here)
├── graphs/
│   ├── original_signal.png
│   ├── undersampling.png
│   ├── nyquist_sampling.png
│   ├── oversampling.png
│   ├── reconstruction.png
│   └── comparison.png
└── documentation/
    ├── methodology.md
    ├── Viva_Preparation.pdf
    └── Viva_Preparation.docx      (editable version)
```

## 10. Conclusion

The simulation confirms the sampling theorem: sampling at 6 Hz (below the 10 Hz Nyquist rate) turns the 5 Hz tone into a 1 Hz alias; sampling at exactly 10 Hz leaves amplitude and phase ambiguous; and sampling at 40 Hz represents the signal densely and allows accurate reconstruction in the interior of the record. Because only a finite number of samples is available, the sinc reconstruction is an approximation with larger errors near the ends. Perfect reconstruction is a property of the infinite ideal case only.

## References

1. A. V. Oppenheim, A. S. Willsky, S. H. Nawab, *Signals and Systems*, 2nd ed., Prentice Hall, 1997.
2. C. E. Shannon, "Communication in the presence of noise," *Proc. IRE*, vol. 37, no. 1, pp. 10–21, 1949.
3. H. Nyquist, "Certain topics in telegraph transmission theory," *Trans. AIEE*, vol. 47, no. 2, pp. 617–644, 1928.
