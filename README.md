# My-Engineering-Projects
The examples of engineering projects I completed to improve work processes.

# BC Optimization Project

## Overview
This project aims to optimize the selection of candidate wells for connecting to booster compressors in offshore platforms. The optimization process uses linear programming techniques to maximize production while adhering to platform-specific constraints.

## Files
- **Auto Select BC Candidates_for Python.xlsx**: Excel file containing the input data for candidate wells, constraints, and output specifications.
- **Optimized_Output.xlsx**: Excel file where the optimization results are saved.

## Dependencies
- Python 3.x
- pandas
- scipy
- numpy

## Installation
1. Ensure you have Python 3.x installed.
2. Install the required libraries using pip: pip install pandas scipy numpy

## Usage
1. Place the `Auto Select BC Candidates_for Python.xlsx` file in the same directory as the script.
2. Run the script to perform the optimization:
   ```bash
   python optimize_wells.py
   ```
3. The results will be saved in `Optimized_Output.xlsx`.

## Script Details

### Loading Data
The script loads data from the Excel file:
```python
file_path = 'Auto Select BC Candidates_for Python.xlsx'
with pd.ExcelFile(file_path) as xls:
    candidate_wells = pd.read_excel(xls, 'Candidate Wells')
    constraints = pd.read_excel(xls, 'Constraints')
    output_data = pd.read_excel(xls, 'Output')
```

### Optimization Function
The `optimize_wells` function performs the optimization for each platform based on the specified mode (Max Gas or Max Condensate):
```python
def optimize_wells(platform, mode, candidate_wells, constraints):
    # Function implementation
```

### Running the Optimization
The script loops through each row in the output table and runs the optimization:
```python
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
```

### Saving Results
The results are saved to a new Excel file:
```python
output_df = pd.DataFrame(output_results)
with pd.ExcelWriter('Optimized_Output.xlsx') as writer:
    output_df.to_excel(writer, index=False, sheet_name='Output')
```

## Conclusion
This project provides a systematic approach to optimizing well selection for offshore platforms, ensuring maximum production efficiency while adhering to operational constraints.
