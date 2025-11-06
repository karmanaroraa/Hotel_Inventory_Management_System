import pytest
import pandas as pd
from src.simulation import simulate_inventory_system

def test_simulate_inventory_system():
    # Sample data for testing
    sample_data = {
        'Bar Name': ['Bar A', 'Bar A', 'Bar B', 'Bar B'],
        'Item': ['Item 1', 'Item 2', 'Item 1', 'Item 2'],
        'Day': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-01', '2023-01-02']),
        'Consumed (ml)': [100, 150, 200, 250]
    }
    
    sample_forecasts = {
        ('Bar A', 'Item 1'): {'avg_daily_consumption': 100, 'forecast_daily': 100, 'par_level_ml': 300, 'reorder_point_ml': 150},
        ('Bar A', 'Item 2'): {'avg_daily_consumption': 150, 'forecast_daily': 150, 'par_level_ml': 450, 'reorder_point_ml': 225},
        ('Bar B', 'Item 1'): {'avg_daily_consumption': 200, 'forecast_daily': 200, 'par_level_ml': 600, 'reorder_point_ml': 300},
        ('Bar B', 'Item 2'): {'avg_daily_consumption': 250, 'forecast_daily': 250, 'par_level_ml': 750, 'reorder_point_ml': 375},
    }
    
    sample_par_levels = {
        ('Bar A', 'Item 1'): {'par_level_ml': 300, 'reorder_point_ml': 150},
        ('Bar A', 'Item 2'): {'par_level_ml': 450, 'reorder_point_ml': 225},
        ('Bar B', 'Item 1'): {'par_level_ml': 600, 'reorder_point_ml': 300},
        ('Bar B', 'Item 2'): {'par_level_ml': 750, 'reorder_point_ml': 375},
    }
    
    # Convert sample data to DataFrame
    df = pd.DataFrame(sample_data)
    
    # Run the simulation
    results_df, service_level_achieved = simulate_inventory_system(df, sample_forecasts, sample_par_levels, simulation_days=2)
    
    # Assertions to verify the results
    assert len(results_df) == 4  # Check if results contain all bar-item combinations
    assert service_level_achieved >= 0  # Service level should be a valid percentage
    assert all(results_df['Final Inventory'] >= 0)  # Final inventory should not be negative

    # Check specific values for known inputs
    assert results_df.loc[(results_df['Bar Name'] == 'Bar A') & (results_df['Item'] == 'Item 1'), 'Stockouts'].values[0] == 0
    assert results_df.loc[(results_df['Bar Name'] == 'Bar B') & (results_df['Item'] == 'Item 2'), 'Stockouts'].values[0] == 1  # Expected stockout for Item 2 in Bar B

    # Additional checks can be added as needed for more comprehensive testing