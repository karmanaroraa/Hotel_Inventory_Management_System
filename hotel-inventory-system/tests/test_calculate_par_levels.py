import pytest
from src.par_levels import calculate_par_levels

def test_calculate_par_levels():
    forecasts = {
        ('Bar A', 'Item 1'): {
            'avg_daily_consumption': 100,
            'std_consumption': 20,
            'forecast_daily': 110
        },
        ('Bar B', 'Item 2'): {
            'avg_daily_consumption': 50,
            'std_consumption': 10,
            'forecast_daily': 60
        }
    }
    
    lead_time_days = 3
    service_level = 0.95
    
    expected_par_levels = {
        ('Bar A', 'Item 1'): {
            'par_level_ml': 360.0,
            'cycle_stock_ml': 300.0,
            'safety_stock_ml': 60.0,
            'reorder_point_ml': 180.0,
            'avg_daily_demand': 100.0,
            'forecast_daily': 110.0
        },
        ('Bar B', 'Item 2'): {
            'par_level_ml': 130.0,
            'cycle_stock_ml': 150.0,
            'safety_stock_ml': 20.0,
            'reorder_point_ml': 65.0,
            'avg_daily_demand': 50.0,
            'forecast_daily': 60.0
        }
    }
    
    par_levels = calculate_par_levels(forecasts, lead_time_days, service_level)
    
    for key in expected_par_levels:
        for sub_key in expected_par_levels[key]:
            assert par_levels[key][sub_key] == expected_par_levels[key][sub_key]