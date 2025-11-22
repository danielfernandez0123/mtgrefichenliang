"""
Test script to verify the mortgage refinancing model against Table 1 from Chen & Ling (1989)
This script runs the model with parameters matching the paper's example.
"""

import numpy as np
import sys

# Import our model (assuming it's in the same directory)
from mortgage_refinancing_model import MortgageRefinancingModel

print("="*70)
print("VERIFICATION AGAINST CHEN & LING (1989) TABLE 1")
print("="*70)

# Table 1 from the paper (α = 0.02 case, initial rate = 8%)
# Contract Rate | G_t | W_t | V^nc | M_t | LM_t
paper_results = {
    8.00: {"G": "(3.02)", "W": 2.24, "V": 98.97, "M": 96.72, "LM": 95.88},
    8.50: {"G": "(0.19)", "W": 3.13, "V": 101.81, "M": 98.49, "LM": 97.48},
    8.53: {"G": 0.00, "W": 3.39, "V": 102.00, "M": 98.61, "LM": 97.58},
    9.00: {"G": 2.65, "W": 4.69, "V": 104.66, "M": 99.97, "LM": 98.72},
    9.50: {"G": 5.52, "W": 6.44, "V": 107.52, "M": 101.07, "LM": 99.55},
    10.00: {"G": 8.39, "W": 8.63, "V": 110.40, "M": 101.76, "LM": 100.01},
    10.28: {"G": 10.06, "W": 10.06, "V": 112.07, "M": 102.00, "LM": 100.00},
    10.50: {"G": 11.28, "W": 11.17, "V": 113.29, "M": 102.00, "LM": 100.00},
    11.00: {"G": 14.18, "W": 13.95, "V": 116.19, "M": 102.00, "LM": 100.00},
}

print("\nExpected values from Table 1 (α = 0.02, initial rate = 8%):")
print("-" * 70)
print(f"{'Contract Rate':<15} {'G_t':<10} {'W_t':<10} {'V^nc':<10} {'M_t':<10} {'LM_t':<10}")
print("-" * 70)

for rate, values in paper_results.items():
    print(f"{rate:<15.2f} {str(values['G']):<10} {values['W']:<10.2f} "
          f"{values['V']:<10.2f} {values['M']:<10.2f} {values['LM']:<10.2f}")

# Now run our model with contract rate = 10% (matching one row from the table)
print("\n" + "="*70)
print("RUNNING MODEL WITH CONTRACT RATE = 10% (matching paper's parameters)")
print("="*70)

# Create model with paper's parameters
model = MortgageRefinancingModel(
    initial_balance=100.0,
    contract_rate=0.10,  # 10% annual
    original_term=96,     # 8 years
    current_time=0,
    initial_rate=0.08,    # 8% annual
    drift_mean=0.0,
    volatility=0.15,
    prob_up=0.5,
    refinancing_cost_pct=0.02,  # α = 2%
    time_periods=12,      # Run for 12 periods initially for computational speed
    periods_per_year=12
)

# Solve the model
model.solve_model()

# Get initial values
balance = model.calculate_balance(0)
G = model.G_immediate.get((0, 0), 0)
W = model.W_wait.get((0, 0), 0)
V = model.V_refinance.get((0, 0), 0)
M = model.M_liability.get((0, 0), 0)
LM = model.LM_lender.get((0, 0), 0)

print(f"\nModel Results (t=0, initial state):")
print(f"  Initial Balance: ${balance:.2f}")
print(f"  Contract Rate: {model.c0 * 12 * 100:.1f}%")
print(f"  Market Rate: {model.r0 * 12 * 100:.1f}%")
print(f"  G_t (Intrinsic value): ${G:.2f}")
print(f"  W_t (Value of waiting): ${W:.2f}")
print(f"  V (Refinancing option): ${V:.2f}")
print(f"  M_t (Liability to borrower): ${M:.2f}")
print(f"  LM_t (Market value to lender): ${LM:.2f}")

print("\n" + "="*70)
print("COMPARISON WITH PAPER (Contract Rate = 10%, Initial Rate = 8%):")
print("="*70)
print(f"{'Metric':<30} {'Paper':<15} {'Model':<15} {'Difference':<15}")
print("-" * 70)

paper_10pct = paper_results[10.00]
print(f"{'G_t (Intrinsic value)':<30} ${paper_10pct['G']:<14.2f} ${G:<14.2f} ${G - paper_10pct['G']:<14.2f}")
print(f"{'W_t (Value of waiting)':<30} ${paper_10pct['W']:<14.2f} ${W:<14.2f} ${W - paper_10pct['W']:<14.2f}")
print(f"{'M_t (Liability)':<30} ${paper_10pct['M']:<14.2f} ${M:<14.2f} ${M - paper_10pct['M']:<14.2f}")
print(f"{'LM_t (Market value)':<30} ${paper_10pct['LM']:<14.2f} ${LM:<14.2f} ${LM - paper_10pct['LM']:<14.2f}")

print("\n" + "="*70)
print("NOTES ON COMPARISON:")
print("="*70)
print("""
1. The paper uses a continuous-time approximation with specific assumptions
   about the term structure that may differ slightly from our binomial implementation.

2. Small differences are expected due to:
   - Discretization effects (binomial vs continuous model)
   - Different numerical methods (our backward induction vs paper's method)
   - Potential differences in how the term structure is modeled

3. The key insight from the paper remains valid:
   - With transaction costs, borrowers wait for larger rate differentials
   - The refinancing option has significant value
   - The minimum IRD required increases with transaction costs

4. According to the paper (page 291):
   - With α = 0.02 and c0 = 10%, the intrinsic value G_t = $8.39
   - The value of waiting W_t = $8.63
   - Since W_t > G_t, optimal decision is to WAIT
   - The refinancing option continues until c0 = 10.28% where G_t = W_t
""")

# Calculate the minimum IRD
min_ird, trigger_df = model.calculate_optimal_trigger_rate()
if min_ird is not None:
    print(f"\nMinimum IRD for optimal refinancing: {min_ird:.0f} basis points")
    print(f"Paper reports: 228 basis points for α = 0.02 (see Table 2)")
