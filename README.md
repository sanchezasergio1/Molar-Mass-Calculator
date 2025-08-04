# ⚗️ Molar Mass Calculator

This Python project allows you to calculate the **molar mass** of chemical compounds, including support for:

- Parentheses and nested groups
- Hydration dots (e.g., `CuSO4·5H2O`)
- Ionic compounds with net charges (e.g., `NH4^+`, `SO4^2-`)

The core logic is implemented in a standalone module (`chem_utils.py`) and can be used both in terminal mode or in a Jupyter Notebook (`molar_mass_calculator.ipynb`).

---

## 📦 Features

- Parses complex chemical formulas.
- Accepts hydrates using `·` notation.
- Accepts charges **only** in caret (`^`) notation, e.g. `Fe^3+`, `SO4^2-`.
- Gracefully ignores invalid charge formats and notifies the user.
- Modular design: logic separated from interface.
- Ready to run in terminal or in a Jupyter environment.

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/molar-mass-calculator.git
cd molar-mass-calculator
