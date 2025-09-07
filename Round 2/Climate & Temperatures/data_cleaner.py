import pandas as pd
import numpy as np
from datetime import datetime
import re
import os

def parse_date_to_year(date_str):
    """
    Parse various date formats to extract year
    Handles: yyyy-mm-dd, dd-mm-yyyy, yyyy formats
    """
    if pd.isna(date_str) or date_str == '':
        return np.nan
    
    date_str = str(date_str).strip()
    
    # If already just a year (4 digits)
    if re.match(r'^\d{4}$', date_str):
        return int(date_str)
    
    # Try yyyy-mm-dd format
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return int(date_str.split('-')[0])
    
    # Try dd-mm-yyyy format
    if re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
        return int(date_str.split('-')[2])
    
    # Try other common formats
    try:
        # Try parsing with pandas
        parsed_date = pd.to_datetime(date_str, errors='coerce')
        if not pd.isna(parsed_date):
            return parsed_date.year
    except:
        pass
    
    return np.nan

def clean_csv_files():
    """
    Clean all CSV files in the Cleaned folder
    """
    cleaned_folder = r"c:\Users\vinay\projects\climate-o-metric\Round 2\Climate & Temperatures\Cleaned"
    preprocessed_folder = r"c:\Users\vinay\projects\climate-o-metric\Round 2\Climate & Temperatures\Preprocessed"
    
    # Create preprocessed folder if it doesn't exist
    os.makedirs(preprocessed_folder, exist_ok=True)
    
    csv_files = [
        "Climate_Indicators_Annual_Mean_Global_Surface_Temperature_Cleaned.csv",
        "GlobalLandTemperaturesByCountry_cleaned.csv", 
        "GlobalTemperatures_Cleaned.csv"
    ]
    
    for filename in csv_files:
        print(f"\n=== Processing {filename} ===")
        file_path = os.path.join(cleaned_folder, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        print(f"Original shape: {df.shape}")
        
        # Check for null values
        null_counts = df.isnull().sum()
        print(f"Null values per column:\n{null_counts[null_counts > 0]}")
        
        # Handle date columns
        date_columns = []
        for col in df.columns:
            if 'date' in col.lower() or col.lower() == 'date':
                date_columns.append(col)
        
        if date_columns:
            print(f"Found date columns: {date_columns}")
            for date_col in date_columns:
                print(f"Converting {date_col} to year...")
                df[date_col] = df[date_col].apply(parse_date_to_year)
        
        # Fill null values with column means for numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if df[col].isnull().sum() > 0:
                mean_val = df[col].mean()
                df[col].fillna(mean_val, inplace=True)
                print(f"Filled {null_counts[col]} null values in {col} with mean: {mean_val:.4f}")
        
        # For files with date columns, group by year and calculate averages
        if date_columns and len(date_columns) > 0:
            date_col = date_columns[0]  # Use first date column
            print(f"Grouping by year and calculating averages...")
            
            # Group by year and other non-numeric columns, then average numeric columns
            non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
            if date_col in non_numeric_cols:
                non_numeric_cols.remove(date_col)
            
            if non_numeric_cols:
                # Group by year and other categorical columns
                group_cols = [date_col] + non_numeric_cols
                df_grouped = df.groupby(group_cols, as_index=False)[numeric_columns].mean()
            else:
                # Group by year only
                df_grouped = df.groupby(date_col, as_index=False)[numeric_columns].mean()
            
            df = df_grouped
            print(f"After grouping by year, shape: {df.shape}")
        
        # Save the processed file
        output_path = os.path.join(preprocessed_folder, filename.replace('_Cleaned', '_Preprocessed'))
        df.to_csv(output_path, index=False)
        print(f"Saved processed file: {output_path}")
        
        # Show final statistics
        print(f"Final shape: {df.shape}")
        final_nulls = df.isnull().sum().sum()
        print(f"Total null values remaining: {final_nulls}")

if __name__ == "__main__":
    clean_csv_files()
