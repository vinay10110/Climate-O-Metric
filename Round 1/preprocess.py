import pandas as pd
import numpy as np
import os

def replace_zeros_with_mean(df, dataset_name):
    """Replace zero values with column means for numeric columns"""
    print(f"\n{'='*50}")
    print(f"Processing: {dataset_name}")
    print(f"{'='*50}")
    print("Original data shape:", df.shape)
    
    # Check which columns have zero values (excluding Country Name and Country Code)
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    zero_counts = {}
    
    for col in numeric_columns:
        zero_count = (df[col] == 0).sum()
        if zero_count > 0:
            zero_counts[col] = zero_count
    
    print(f"Columns with zero values: {len(zero_counts)}")
    if zero_counts:
        print("Zero counts per column:")
        for col, count in zero_counts.items():
            print(f"  {col}: {count} zeros")
    
    # Create a copy of the dataframe to preserve original
    df_cleaned = df.copy()
    
    # Replace zeros with column means for numeric columns only
    for col in numeric_columns:
        if col in zero_counts:
            # Calculate mean excluding zeros and NaN values
            non_zero_mean = df_cleaned[df_cleaned[col] != 0][col].mean()
            
            # Replace zeros with the mean
            df_cleaned.loc[df_cleaned[col] == 0, col] = non_zero_mean
            
            print(f"Replaced {zero_counts[col]} zeros in '{col}' with mean: {non_zero_mean:.6f}")
    
    # Verify no zeros remain in numeric columns
    remaining_zeros = {}
    for col in numeric_columns:
        zero_count = (df_cleaned[col] == 0).sum()
        if zero_count > 0:
            remaining_zeros[col] = zero_count
    
    if remaining_zeros:
        print("\nRemaining zeros:")
        for col, count in remaining_zeros.items():
            print(f"  {col}: {count} zeros")
    else:
        print("✓ All zeros successfully replaced!")
    
    return df_cleaned

# Define all datasets to process
datasets = [
    {
        'path': './agricultural land(%)/Agriculture_land_percentage.csv',
        'name': 'Agricultural Land Percentage'
    },
    {
        'path': './CO2 emission per capita/CO2 Emission Per Country.csv',
        'name': 'CO2 Emission Per Capita'
    },
    {
        'path': './electic power consumption per capita/Electric_Power_Consumption.csv',
        'name': 'Electric Power Consumption'
    },
    {
        'path': './Renewable electricity output (% of total electricity output)/Renewable_electricity.csv',
        'name': 'Renewable Electricity Output'
    },
    {
        'path': './Total greenhouse gas emissions (kt of CO2 equivalent)/Total_Greenhouse_gas.csv',
        'name': 'Total Greenhouse Gas Emissions'
    }
]

print("Starting preprocessing of all datasets...")
print(f"Total datasets to process: {len(datasets)}")

# Process each dataset
for dataset in datasets:
    try:
        # Load the dataset
        df = pd.read_csv(dataset['path'])
        
        # Process the dataset
        df_cleaned = replace_zeros_with_mean(df, dataset['name'])
        
        # Generate output filename with preprocess tag
        directory = os.path.dirname(dataset['path'])
        filename = os.path.basename(dataset['path'])
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_preprocess{ext}"
        output_path = os.path.join(directory, output_filename)
        
        # Save the cleaned dataset
        df_cleaned.to_csv(output_path, index=False)
        print(f"✓ Saved preprocessed data to: {output_path}")
        
    except Exception as e:
        print(f"✗ Error processing {dataset['name']}: {str(e)}")

print(f"\n{'='*60}")
print("PREPROCESSING COMPLETE!")
print(f"{'='*60}")
print("All datasets have been processed and saved with '_preprocess' suffix.")
