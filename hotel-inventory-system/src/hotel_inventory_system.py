import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
from forecasting import forecast_demand
from par_levels import calculate_par_levels
from simulation import simulate_inventory_system
from utils import load_and_prepare_data, perform_eda, generate_recommendations, create_visualizations

warnings.filterwarnings('ignore')

print("="*80)
print("HOTEL BAR INVENTORY MANAGEMENT SYSTEM")
print("="*80)

# MAIN EXECUTION

def main():
    """Main execution function"""
    
    # Configuration
    DATA_FILE = 'hotel_bar_inventory.csv'  # Update with your file path
    FORECAST_DAYS = 30
    LEAD_TIME_DAYS = 3
    SERVICE_LEVEL = 0.95
    
    try:
        # Step 1: Load data
        df = load_and_prepare_data(DATA_FILE)
        
        # Step 2: EDA
        top_items, bar_consumption = perform_eda(df)
        
        # Step 3: Forecast demand using Holt-Winters or Prophet
        forecasts = forecast_demand(df, forecast_days=FORECAST_DAYS)
        
        # Step 4: Calculate par levels
        par_levels = calculate_par_levels(forecasts, 
                                         lead_time_days=LEAD_TIME_DAYS,
                                         service_level=SERVICE_LEVEL)
        
        # Step 5: Simulate system
        results_df, service_level_achieved = simulate_inventory_system(
            df, forecasts, par_levels, simulation_days=30
        )
        
        # Step 6: Generate recommendations
        rec_df = generate_recommendations(df, forecasts, par_levels, results_df)
        
        # Step 7: Visualizations
        create_visualizations(df, forecasts, par_levels, rec_df)
        
        # Save outputs
        print("\nSaving outputs...")
        rec_df.to_csv('inventory_recommendations.csv', index=False)
        results_df.to_csv('simulation_results.csv', index=False)
        
        # Create par levels export
        par_df = pd.DataFrame([
            {
                'Bar Name': bar,
                'Item': item,
                'Par Level (ml)': info['par_level_ml'],
                'Reorder Point (ml)': info['reorder_point_ml'],
                'Cycle Stock (ml)': info['cycle_stock_ml'],
                'Safety Stock (ml)': info['safety_stock_ml']
            }
            for (bar, item), info in par_levels.items()
        ])
        par_df.to_csv('par_levels.csv', index=False)
        
        print("\n" + "="*80)
        print("EXECUTION COMPLETE")
        print("="*80)
        print("\nOutput files generated:")
        print("  1. inventory_recommendations.csv - Action items for each bar-item")
        print("  2. par_levels.csv - Recommended par levels for all items")
        print("  3. simulation_results.csv - Simulation performance metrics")
        print("  4. inventory_analysis.png - Visual analysis charts")
        print("\nKey Insights:")
        print(f"  • Service Level Achieved: {service_level_achieved*100:.2f}%")
        print(f"  • Items Analyzed: {len(par_levels)}")
        print(f"  • Immediate Actions Needed: {len(rec_df[rec_df['Action'] == 'ORDER NOW'])}")
        
    except FileNotFoundError:
        print(f"\n❌ Error: Could not find '{DATA_FILE}'")
        print("   Please update DATA_FILE variable with correct path")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()