import pandas as pd
import numpy as np

def clean_air_pollution_data():
    """
    Transform the global_air_pollution_data.csv file into a cleaner, more readable format.
    """
    print("Loading air pollution data...")
    
    # Read the original CSV file
    df = pd.read_csv('global_air_pollution_data.csv')
    
    print(f"Original data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Clean column names - remove tabs and extra spaces
    df.columns = df.columns.str.strip().str.replace('\t', '')
    
    # Clean up country names - remove formal titles and extra text
    df['country_name'] = df['country_name'].str.replace('United States of America', 'United States')
    df['country_name'] = df['country_name'].str.replace('United Kingdom of Great Britain and Northern Ireland', 'United Kingdom')
    df['country_name'] = df['country_name'].str.replace('Russian Federation', 'Russia')
    df['country_name'] = df['country_name'].str.replace('Republic of North Macedonia', 'North Macedonia')
    df['country_name'] = df['country_name'].str.replace('United Republic of Tanzania', 'Tanzania')
    
    # Create a cleaner main dataset
    df_clean = df.copy()
    
    # Save the cleaned wide format
    df_clean.to_csv('global_air_pollution_clean.csv', index=False)
    print("Cleaned wide format saved as: global_air_pollution_clean.csv")
    
    # Transform to long format for better analysis
    print("Converting to long format...")
    
    # Define pollutant mappings
    pollutants = {
        'Overall AQI': ('aqi_value', 'aqi_category'),
        'Carbon Monoxide': ('co_aqi_value', 'co_aqi_category'),
        'Ozone': ('ozone_aqi_value', 'ozone_aqi_category'),
        'Nitrogen Dioxide': ('no2_aqi_value', 'no2_aqi_category'),
        'PM2.5': ('pm2.5_aqi_value', 'pm2.5_aqi_category')
    }
    
    # Create long format dataset
    long_data = []
    
    for pollutant_name, (value_col, category_col) in pollutants.items():
        temp_df = df_clean[['country_name', 'city_name', value_col, category_col]].copy()
        temp_df['pollutant'] = pollutant_name
        temp_df['aqi_value'] = temp_df[value_col]
        temp_df['aqi_category'] = temp_df[category_col]
        temp_df = temp_df[['country_name', 'city_name', 'pollutant', 'aqi_value', 'aqi_category']]
        long_data.append(temp_df)
    
    df_long = pd.concat(long_data, ignore_index=True)
    
    # Sort the data logically
    df_long = df_long.sort_values(['country_name', 'city_name', 'pollutant']).reset_index(drop=True)
    
    # Save long format
    df_long.to_csv('global_air_pollution_long.csv', index=False)
    print("Long format saved as: global_air_pollution_long.csv")
    
    # Create country-level summaries
    print("Creating country-level summaries...")
    
    country_summary = df_clean.groupby('country_name').agg({
        'city_name': 'count',
        'aqi_value': ['mean', 'min', 'max', 'std'],
        'co_aqi_value': 'mean',
        'ozone_aqi_value': 'mean',
        'no2_aqi_value': 'mean',
        'pm2.5_aqi_value': 'mean'
    }).round(2)
    
    # Flatten column names
    country_summary.columns = [
        'cities_count', 'avg_aqi', 'min_aqi', 'max_aqi', 'std_aqi',
        'avg_co_aqi', 'avg_ozone_aqi', 'avg_no2_aqi', 'avg_pm25_aqi'
    ]
    
    country_summary = country_summary.reset_index()
    country_summary.to_csv('country_air_pollution_summary.csv', index=False)
    print("Country summary saved as: country_air_pollution_summary.csv")
    
    # Create AQI category analysis
    print("Creating AQI category analysis...")
    
    category_analysis = []
    
    for pollutant_name, (value_col, category_col) in pollutants.items():
        category_counts = df_clean[category_col].value_counts()
        for category, count in category_counts.items():
            category_analysis.append({
                'pollutant': pollutant_name,
                'aqi_category': category,
                'city_count': count,
                'percentage': round(count / len(df_clean) * 100, 2)
            })
    
    category_df = pd.DataFrame(category_analysis)
    category_df.to_csv('aqi_category_analysis.csv', index=False)
    print("AQI category analysis saved as: aqi_category_analysis.csv")
    
    # Create worst air quality cities report
    print("Creating worst air quality cities report...")
    
    worst_cities = df_clean.nlargest(50, 'aqi_value')[
        ['country_name', 'city_name', 'aqi_value', 'aqi_category', 
         'pm2.5_aqi_value', 'ozone_aqi_value', 'no2_aqi_value', 'co_aqi_value']
    ].copy()
    
    worst_cities.to_csv('worst_air_quality_cities.csv', index=False)
    print("Worst air quality cities saved as: worst_air_quality_cities.csv")
    
    # Create best air quality cities report
    best_cities = df_clean.nsmallest(50, 'aqi_value')[
        ['country_name', 'city_name', 'aqi_value', 'aqi_category',
         'pm2.5_aqi_value', 'ozone_aqi_value', 'no2_aqi_value', 'co_aqi_value']
    ].copy()
    
    best_cities.to_csv('best_air_quality_cities.csv', index=False)
    print("Best air quality cities saved as: best_air_quality_cities.csv")
    
    # Create overall statistics summary
    print("Creating overall statistics...")
    
    stats_summary = {
        'Total Cities': len(df_clean),
        'Total Countries': df_clean['country_name'].nunique(),
        'Average Overall AQI': df_clean['aqi_value'].mean().round(2),
        'Median Overall AQI': df_clean['aqi_value'].median(),
        'Cities with Good Air Quality': len(df_clean[df_clean['aqi_category'] == 'Good']),
        'Cities with Moderate Air Quality': len(df_clean[df_clean['aqi_category'] == 'Moderate']),
        'Cities with Unhealthy Air Quality': len(df_clean[df_clean['aqi_category'].str.contains('Unhealthy', na=False)]),
        'Worst AQI Value': df_clean['aqi_value'].max(),
        'Best AQI Value': df_clean['aqi_value'].min(),
        'Most Polluted City': df_clean.loc[df_clean['aqi_value'].idxmax(), 'city_name'],
        'Cleanest City': df_clean.loc[df_clean['aqi_value'].idxmin(), 'city_name']
    }
    
    stats_df = pd.DataFrame(list(stats_summary.items()), columns=['Metric', 'Value'])
    stats_df.to_csv('air_pollution_statistics.csv', index=False)
    print("Overall statistics saved as: air_pollution_statistics.csv")
    
    return df_clean, df_long, country_summary, stats_df

if __name__ == "__main__":
    clean_data, long_data, country_data, stats = clean_air_pollution_data()
    print("\nAir pollution data transformation completed successfully!")
    print("\nFiles created:")
    print("1. global_air_pollution_clean.csv - Main cleaned dataset (wide format)")
    print("2. global_air_pollution_long.csv - Long format for analysis")
    print("3. country_air_pollution_summary.csv - Country-level statistics")
    print("4. aqi_category_analysis.csv - AQI category breakdown")
    print("5. worst_air_quality_cities.csv - Top 50 most polluted cities")
    print("6. best_air_quality_cities.csv - Top 50 cleanest cities")
    print("7. air_pollution_statistics.csv - Overall dataset statistics")
