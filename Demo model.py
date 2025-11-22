"""
Simple demonstration of the mortgage refinancing model
Shows clear examples where the model makes intuitive decisions
"""

from mortgage_refinancing_model import MortgageRefinancingModel

print("="*70)
print("MORTGAGE REFINANCING MODEL - WORKING EXAMPLES")
print("="*70)

# Example 1: High contract rate, low market rate - should refinance
print("\nEXAMPLE 1: High Contract Rate (12%), Low Market Rate (6%)")
print("-" * 70)

model1 = MortgageRefinancingModel(
    initial_balance=100.0,
    contract_rate=0.12,     # 12% annual - HIGH
    original_term=96,        # 8 years
    current_time=0,
    initial_rate=0.06,       # 6% annual - LOW
    drift_mean=0.0,
    volatility=0.10,         # Lower volatility
    prob_up=0.5,
    refinancing_cost_pct=0.02,
    time_periods=6,          # Shorter for quick demo
    periods_per_year=12
)

model1.solve_model()

print(f"Contract Rate: {model1.c0 * 12 * 100:.1f}% annual")
print(f"Market Rate: {model1.r0 * 12 * 100:.1f}% annual") 
print(f"Interest Rate Differential: {(model1.c0 - model1.r0) * 12 * 100:.1f}% = {(model1.c0 - model1.r0) * 12 * 10000:.0f} basis points")
print(f"\nRefinancing Analysis:")
print(f"  Intrinsic Value (G): ${model1.G_immediate[(0, 0)]:.2f}")
print(f"  Value of Waiting (W): ${model1.W_wait[(0, 0)]:.2f}")
print(f"  Refinancing Costs: ${model1.alpha * 100:.2f}")

if model1.G_immediate[(0, 0)] >= model1.W_wait[(0, 0)] and model1.G_immediate[(0, 0)] > 0:
    print(f"  Decision: REFINANCE NOW (G > W and G > 0)")
else:
    print(f"  Decision: WAIT (W > G or G < 0)")

# Example 2: Contract rate equals market rate - should not refinance
print("\n" + "="*70)
print("\nEXAMPLE 2: Contract Rate = Market Rate (8%)")
print("-" * 70)

model2 = MortgageRefinancingModel(
    initial_balance=100.0,
    contract_rate=0.08,     # 8% annual
    original_term=96,        
    current_time=0,
    initial_rate=0.08,       # 8% annual - SAME
    drift_mean=0.0,
    volatility=0.10,
    prob_up=0.5,
    refinancing_cost_pct=0.02,
    time_periods=6,
    periods_per_year=12
)

model2.solve_model()

print(f"Contract Rate: {model2.c0 * 12 * 100:.1f}% annual")
print(f"Market Rate: {model2.r0 * 12 * 100:.1f}% annual")
print(f"Interest Rate Differential: {(model2.c0 - model2.r0) * 12 * 100:.1f}% = {(model2.c0 - model2.r0) * 12 * 10000:.0f} basis points")
print(f"\nRefinancing Analysis:")
print(f"  Intrinsic Value (G): ${model2.G_immediate[(0, 0)]:.2f}")
print(f"  Value of Waiting (W): ${model2.W_wait[(0, 0)]:.2f}")
print(f"  Refinancing Costs: ${model2.alpha * 100:.2f}")

if model2.G_immediate[(0, 0)] >= model2.W_wait[(0, 0)] and model2.G_immediate[(0, 0)] > 0:
    print(f"  Decision: REFINANCE NOW (G > W and G > 0)")
else:
    print(f"  Decision: WAIT (W > G or G < 0)")
    print(f"  Reason: No benefit from refinancing at same rate, plus costs")

# Example 3: Small rate differential with high volatility
print("\n" + "="*70)
print("\nEXAMPLE 3: Small Rate Differential with High Volatility")
print("-" * 70)

model3 = MortgageRefinancingModel(
    initial_balance=100.0,
    contract_rate=0.09,     # 9% annual
    original_term=96,
    current_time=0,
    initial_rate=0.08,       # 8% annual - small difference
    drift_mean=0.0,
    volatility=0.25,         # HIGH volatility
    prob_up=0.5,
    refinancing_cost_pct=0.02,
    time_periods=6,
    periods_per_year=12
)

model3.solve_model()

print(f"Contract Rate: {model3.c0 * 12 * 100:.1f}% annual")
print(f"Market Rate: {model3.r0 * 12 * 100:.1f}% annual")
print(f"Interest Rate Differential: {(model3.c0 - model3.r0) * 12 * 100:.1f}% = {(model3.c0 - model3.r0) * 12 * 10000:.0f} basis points")
print(f"Interest Rate Volatility: {model3.sigma * 100:.0f}%")
print(f"\nRefinancing Analysis:")
print(f"  Intrinsic Value (G): ${model3.G_immediate[(0, 0)]:.2f}")
print(f"  Value of Waiting (W): ${model3.W_wait[(0, 0)]:.2f}")
print(f"  Refinancing Costs: ${model3.alpha * 100:.2f}")

if model3.G_immediate[(0, 0)] >= model3.W_wait[(0, 0)] and model3.G_immediate[(0, 0)] > 0:
    print(f"  Decision: REFINANCE NOW (G > W and G > 0)")
else:
    print(f"  Decision: WAIT (W > G or G < 0)")
    print(f"  Reason: High volatility makes waiting valuable - rates might fall more")

# Example 4: Zero transaction costs
print("\n" + "="*70)
print("\nEXAMPLE 4: No Transaction Costs (α = 0)")
print("-" * 70)

model4 = MortgageRefinancingModel(
    initial_balance=100.0,
    contract_rate=0.09,     # 9% annual
    original_term=96,
    current_time=0,
    initial_rate=0.08,       # 8% annual
    drift_mean=0.0,
    volatility=0.15,
    prob_up=0.5,
    refinancing_cost_pct=0.00,  # NO transaction costs
    time_periods=6,
    periods_per_year=12
)

model4.solve_model()

print(f"Contract Rate: {model4.c0 * 12 * 100:.1f}% annual")
print(f"Market Rate: {model4.r0 * 12 * 100:.1f}% annual")
print(f"Interest Rate Differential: {(model4.c0 - model4.r0) * 12 * 100:.1f}% = {(model4.c0 - model4.r0) * 12 * 10000:.0f} basis points")
print(f"Transaction Costs: {model4.alpha * 100:.1f}%")
print(f"\nRefinancing Analysis:")
print(f"  Intrinsic Value (G): ${model4.G_immediate[(0, 0)]:.2f}")
print(f"  Value of Waiting (W): ${model4.W_wait[(0, 0)]:.2f}")

if model4.G_immediate[(0, 0)] >= model4.W_wait[(0, 0)] and model4.G_immediate[(0, 0)] > 0:
    print(f"  Decision: REFINANCE NOW (G > W and G > 0)")
    print(f"  Reason: With no transaction costs, any positive rate differential warrants refinancing")
else:
    print(f"  Decision: WAIT (W > G or G < 0)")

print("\n" + "="*70)
print("KEY INSIGHTS FROM THE MODEL:")
print("="*70)
print("""
1. The model correctly identifies when to refinance:
   - Large rate differentials → Refinance immediately
   - Small differentials → Wait for better rates
   - No differential or negative → Never refinance

2. Transaction costs create a "band of inaction":
   - Need larger rate differentials to justify refinancing
   - The paper shows this requires ~200+ basis points with 2% costs

3. Higher volatility increases the value of waiting:
   - More uncertainty → Greater option value
   - Borrowers wait longer when rates are more volatile

4. The model captures the option-like nature of refinancing:
   - Refinancing option = max(Intrinsic Value, Value of Waiting)
   - This is exactly like an American option on interest rates
""")
