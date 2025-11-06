import pytest
import pandas as pd
from src.forecasting import forecast_demand
from datetime import timedelta

def test_forecast_demand():
    # Sample data for testing
    data = {
        'Day': pd.date_range(start='2023-01-01', periods=10, freq='D'),
        'Bar Name': ['Bar A'] * 10,
        'Item': ['Item 1'] * 10,
        'Consumed (ml)': [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    }
    df = pd.DataFrame(data)

    # Call the forecast_demand function
    forecasts = forecast_demand(df, forecast_days=5)

    # Check if the forecast contains the expected keys
    assert ('Bar A', 'Item 1') in forecasts
    assert 'forecast_daily' in forecasts[('Bar A', 'Item 1')]
    assert 'forecast_total' in forecasts[('Bar A', 'Item 1')]
    
    # Check if the forecasted daily consumption is a positive number
    assert forecasts[('Bar A', 'Item 1')]['forecast_daily'] > 0

    # Check if the total forecast is calculated correctly
    expected_total_forecast = forecasts[('Bar A', 'Item 1')]['forecast_daily'] * 5
    assert forecasts[('Bar A', 'Item 1')]['forecast_total'] == expected_total_forecast

    # Check if the historical days count is correct
    assert forecasts[('Bar A', 'Item 1')]['historical_days'] == 10

    # Test with insufficient data
    insufficient_data = {
        'Day': pd.date_range(start='2023-01-01', periods=2, freq='D'),
        'Bar Name': ['Bar A'] * 2,
        'Item': ['Item 1'] * 2,
        'Consumed (ml)': [100, 150]
    }
    df_insufficient = pd.DataFrame(insufficient_data)
    forecasts_insufficient = forecast_demand(df_insufficient, forecast_days=5)
    
    # Ensure no forecast is generated for insufficient data
    assert len(forecasts_insufficient) == 0

    # Test with negative consumption values
    negative_data = {
        'Day': pd.date_range(start='2023-01-01', periods=10, freq='D'),
        'Bar Name': ['Bar A'] * 10,
        'Item': ['Item 1'] * 10,
        'Consumed (ml)': [-100, -150, -200, -250, -300, -350, -400, -450, -500, -550]
    }
    df_negative = pd.DataFrame(negative_data)
    forecasts_negative = forecast_demand(df_negative, forecast_days=5)

    # Ensure forecast is not negative
    assert forecasts_negative[('Bar A', 'Item 1')]['forecast_daily'] >= 0
    assert forecasts_negative[('Bar A', 'Item 1')]['forecast_total'] >= 0

    # Test with varying consumption patterns
    varying_data = {
        'Day': pd.date_range(start='2023-01-01', periods=10, freq='D'),
        'Bar Name': ['Bar A'] * 10,
        'Item': ['Item 1'] * 10,
        'Consumed (ml)': [100, 200, 150, 300, 250, 400, 350, 500, 450, 600]
    }
    df_varying = pd.DataFrame(varying_data)
    forecasts_varying = forecast_demand(df_varying, forecast_days=5)

    # Check if the forecasted daily consumption is a positive number
    assert forecasts_varying[('Bar A', 'Item 1')]['forecast_daily'] > 0

    # Check if the total forecast is calculated correctly
    expected_total_forecast_varying = forecasts_varying[('Bar A', 'Item 1')]['forecast_daily'] * 5
    assert forecasts_varying[('Bar A', 'Item 1')]['forecast_total'] == expected_total_forecast_varying