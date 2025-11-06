import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def forecast_demand(df, forecast_days=30):
    print(f"\n[3/6] Forecasting demand for next {forecast_days} days using Holt-Winters...")

    forecasts = {}
    
    # Aggregate daily consumption by bar and item
    daily_consumption = df.groupby(['Day', 'Bar Name', 'Item'])['Consumed (ml)'].sum().reset_index()
    
    # Get unique combinations
    combinations = df.groupby(['Bar Name', 'Item']).size().reset_index()[['Bar Name', 'Item']]
    
    print(f"   → Forecasting for {len(combinations)} bar-item combinations...")
    
    for idx, row in combinations.iterrows():
        bar = row['Bar Name']
        item = row['Item']
        
        # Get historical data for this combination
        item_data = daily_consumption[
            (daily_consumption['Bar Name'] == bar) & 
            (daily_consumption['Item'] == item)
        ].copy()
        
        if len(item_data) < 3:  # Need minimum data points
            continue
        
        # Create time index
        item_data = item_data.sort_values('Day')
        item_data.set_index('Day', inplace=True)
        
        # Fit Holt-Winters model
        model = ExponentialSmoothing(item_data['Consumed (ml)'], 
                                      trend='add', 
                                      seasonal='add', 
                                      seasonal_periods=7)
        model_fit = model.fit()
        
        # Forecast for the specified number of days
        forecast = model_fit.forecast(steps=forecast_days)
        
        # Store forecast
        forecasts[(bar, item)] = {
            'forecast_daily': forecast.mean(),
            'forecast_total': forecast.sum(),
            'historical_days': len(item_data)
        }
    
    print(f"   ✓ Generated forecasts for {len(forecasts)} combinations")
    return forecasts