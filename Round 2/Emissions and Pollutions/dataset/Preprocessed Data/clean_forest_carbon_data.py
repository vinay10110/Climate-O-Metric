import pandas as pd
import numpy as np

def clean_forest_carbon_data():
    """
    Transform the Forest_and_Carbon.csv file into a cleaner, more readable format.
    """
    print("Loading original data...")
    
    # Read the original CSV file
    df = pd.read_csv('Forest_and_Carbon.csv')
    
    print(f"Original data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Remove redundant columns that add clutter
    columns_to_remove = ['ObjectId', 'CTS_Code', 'CTS_Name', 'CTS_Full_Descriptor', 'Source']
    df_clean = df.drop(columns=[col for col in columns_to_remove if col in df.columns])
    
    # Clean up country names - remove formal titles and extra text
    df_clean['Country'] = df_clean['Country'].str.replace(r', Kingdom of.*', '', regex=True)
    df_clean['Country'] = df_clean['Country'].str.replace(r', Republic of.*', '', regex=True)
    df_clean['Country'] = df_clean['Country'].str.replace(r', Islamic Rep\. of', '', regex=True)
    df_clean['Country'] = df_clean['Country'].str.replace(r', Principality of', '', regex=True)
    df_clean['Country'] = df_clean['Country'].str.replace(r', Fed\. Sts\.', '', regex=True)
    df_clean['Country'] = df_clean['Country'].str.replace(r', People\'s Rep\. of', '', regex=True)
    
    # Get year columns (F1992 to F2022)
    year_columns = [col for col in df_clean.columns if col.startswith('F')]
    
    # Melt the dataframe to convert from wide to long format
    print("Converting from wide to long format...")
    df_long = pd.melt(
        df_clean,
        id_vars=['Country', 'ISO2', 'ISO3', 'Indicator', 'Unit'],
        value_vars=year_columns,
        var_name='Year',
        value_name='Value'
    )
    
    # Clean up the Year column - remove 'F' prefix and convert to integer
    df_long['Year'] = df_long['Year'].str.replace('F', '').astype(int)
    
    # Remove rows with missing values
    df_long = df_long.dropna(subset=['Value'])
    
    # Sort the data logically
    df_long = df_long.sort_values(['Country', 'Indicator', 'Year']).reset_index(drop=True)
    
    print(f"Cleaned data shape: {df_long.shape}")
    
    # Create separate datasets for different indicators for better organization
    indicators = df_long['Indicator'].unique()
    print(f"Available indicators: {indicators}")
    
    # Save the main cleaned dataset
    output_file = 'Forest_and_Carbon_Clean.csv'
    df_long.to_csv(output_file, index=False)
    print(f"Main cleaned dataset saved as: {output_file}")
    
    # Create separate files for each indicator type for easier analysis
    for indicator in indicators:
        indicator_data = df_long[df_long['Indicator'] == indicator].copy()
        
        # Create a more readable filename
        filename = indicator.lower().replace(' ', '_').replace(',', '').replace('(', '').replace(')', '')
        filename = f"{filename}_data.csv"
        
        # For area and carbon stock data, add some calculated columns
        if 'area' in indicator.lower() or 'carbon' in indicator.lower():
            # Pivot to have years as columns for easier comparison
            pivot_data = indicator_data.pivot_table(
                index=['Country', 'ISO2', 'ISO3', 'Unit'],
                columns='Year',
                values='Value',
                fill_value=np.nan
            )
            
            # Calculate change from first to last available year
            first_year = pivot_data.columns.min()
            last_year = pivot_data.columns.max()
            
            if first_year in pivot_data.columns and last_year in pivot_data.columns:
                pivot_data['Change_Absolute'] = pivot_data[last_year] - pivot_data[first_year]
                pivot_data['Change_Percent'] = ((pivot_data[last_year] - pivot_data[first_year]) / pivot_data[first_year] * 100).round(2)
            
            # Reset index to make it a regular dataframe
            pivot_data = pivot_data.reset_index()
            
            pivot_data.to_csv(f"pivot_{filename}", index=False)
            print(f"Pivot table for {indicator} saved as: pivot_{filename}")
        
        # Save the long format version
        indicator_data.to_csv(filename, index=False)
        print(f"Data for '{indicator}' saved as: {filename}")
    
    # Create a summary statistics file
    print("Creating summary statistics...")
    summary_stats = []
    
    for indicator in indicators:
        indicator_data = df_long[df_long['Indicator'] == indicator]
        
        stats = {
            'Indicator': indicator,
            'Unit': indicator_data['Unit'].iloc[0],
            'Countries_Count': indicator_data['Country'].nunique(),
            'Years_Available': f"{indicator_data['Year'].min()}-{indicator_data['Year'].max()}",
            'Total_Records': len(indicator_data),
            'Missing_Values': indicator_data['Value'].isna().sum(),
            'Min_Value': indicator_data['Value'].min(),
            'Max_Value': indicator_data['Value'].max(),
            'Mean_Value': indicator_data['Value'].mean().round(2)
        }
        summary_stats.append(stats)
    
    summary_df = pd.DataFrame(summary_stats)
    summary_df.to_csv('Forest_Carbon_Summary.csv', index=False)
    print("Summary statistics saved as: Forest_Carbon_Summary.csv")
    
    return df_long, summary_df

if __name__ == "__main__":
    cleaned_data, summary = clean_forest_carbon_data()
    print("\nData transformation completed successfully!")
    print("\nFiles created:")
    print("1. Forest_and_Carbon_Clean.csv - Main cleaned dataset (long format)")
    print("2. Individual indicator files - Separate CSV for each indicator")
    print("3. Pivot tables - Wide format with calculated changes")
    print("4. Forest_Carbon_Summary.csv - Summary statistics")
