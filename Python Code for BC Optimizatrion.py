import pandas as pd
from scipy.optimize import linprog
import numpy as np

# Load the data from the Excel file
file_path = 'Auto Select BC Candidates_for Python.xlsx'
with pd.ExcelFile(file_path) as xls:
    candidate_wells = pd.read_excel(xls, 'Candidate Wells')
    constraints = pd.read_excel(xls, 'Constraints')
    output_data = pd.read_excel(xls, 'Output')

# Function to run optimization for each platform
def optimize_wells(platform, mode, candidate_wells, constraints):
    # Filter candidate wells by platform
    platform_wells = candidate_wells[candidate_wells['Platform'] == platform]
    if platform_wells.empty:
        return "Unable to optimize", 0, 0, 0, 0, 0

    # Get constraints for the platform
    platform_constraints = constraints[constraints['WP'] == platform]
    if platform_constraints.empty:
        return "Unable to optimize", 0, 0, 0, 0, 0

    # Define constraint values
    gas_limit = platform_constraints['BC Gas Limit (MMSCF/d)'].values[0]
    liquid_limit = platform_constraints['BC Liquid Limit (STB/d)'].values[0]
    co2_limit = platform_constraints['BC CO2 Limit (%)'].values[0]

    # Extract columns for optimization
    qg = platform_wells['BC Qg_MMSCFD'].values
    ql = platform_wells['BC Ql_BBLD'].values
    co2 = platform_wells['CO2_%'].values
    norm_qg_gain = platform_wells['Norm_Qg gain_MMSCFD'].values
    qc_gain = platform_wells['Qc gain_MMSCFD'].values

    # Objective and constraints based on mode
    if mode == "Max Gas":
        objective = -norm_qg_gain  # Maximize Norm_Qg gain
    elif mode == "Max Condensate":
        objective = -qc_gain  # Maximize Qc gain
    else:
        return "Unable to optimize", 0, 0, 0, 0, 0

    # Set up constraints
    A = [
        qg.sum(),             # Gas constraint
        ql.sum(),             # Liquid constraint
        (qg * co2).sum() / qg.sum()  # CO2 constraint
    ]
    b = [gas_limit, liquid_limit, co2_limit]

    # Bounds for the selection (binary choice)
    bounds = [(0, 1) for _ in range(len(qg))]

    # Run the optimization using linprog for binary selection
    result = linprog(objective, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if result.success:
        selected_indices = result.x.round().astype(bool)
        selected_wells = platform_wells['Well'][selected_indices].tolist()

        total_bc_gas = qg[selected_indices].sum()
        total_bc_liquid = ql[selected_indices].sum()
        blended_co2 = (qg[selected_indices] * co2[selected_indices]).sum() / total_bc_gas
        total_normalized_gas_gain = norm_qg_gain[selected_indices].sum()
        total_condensate_gain = qc_gain[selected_indices].sum()

        return (
            ', '.join(selected_wells),
            total_bc_gas,
            total_bc_liquid,
            total_normalized_gas_gain,
            total_condensate_gain,
            blended_co2
        )
    else:
        return "Unable to optimize", 0, 0, 0, 0, 0

# Loop through each row in the output table and run the optimization
output_results = []
for _, row in output_data.iterrows():
    platform = row['Platform']
    mode = row['Optimization mode']
    selected_wells, total_bc_gas, total_bc_liquid, total_normalized_gas_gain, total_condensate_gain, blended_co2 = optimize_wells(
        platform, mode, candidate_wells, constraints
    )
    
    output_results.append({
        "Platform": platform,
        "Optimization mode": mode,
        "Selected Wells": selected_wells,
        "Total BC Gas": total_bc_gas,
        "Total BC Liquid": total_bc_liquid,
        "Total Normalized Gas Gain": total_normalized_gas_gain,
        "Total Condensate Gain": total_condensate_gain,
        "Blended CO2": blended_co2
    })

# Save the results to a new Excel file
output_df = pd.DataFrame(output_results)
with pd.ExcelWriter('Optimized_Output.xlsx') as writer:
    output_df.to_excel(writer, index=False, sheet_name='Output')
print("Running Successful")    
