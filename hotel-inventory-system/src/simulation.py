# filepath: /hotel-inventory-system/hotel-inventory-system/src/simulation.py
import pandas as pd

def simulate_inventory_system(df, forecasts, par_levels, simulation_days=30):
    """
    Simulate the inventory management system
    Shows how the system would perform with recommended par levels
    """
    print(f"\n[5/6] Running simulation for {simulation_days} days...")

    # Use last 30 days for simulation
    df_sorted = df.sort_values('Day')
    unique_days = sorted(df_sorted['Day'].unique())

    if len(unique_days) < simulation_days:
        simulation_days = len(unique_days)
        print(f"   → Adjusted simulation period to {simulation_days} days (available data)")

    simulation_start = unique_days[-simulation_days]
    simulation_data = df_sorted[df_sorted['Day'] >= simulation_start].copy()

    # Initialize metrics
    stockout_count = 0
    total_transactions = 0
    overstock_value = 0

    results = []

    # Simulate for each bar-item combination
    for (bar, item), par_info in par_levels.items():
        # Get actual consumption during simulation period
        actual_data = simulation_data[
            (simulation_data['Bar Name'] == bar) & 
            (simulation_data['Item'] == item)
        ]

        if len(actual_data) == 0:
            continue

        # Initialize inventory at par level
        current_inventory = par_info['par_level_ml']
        par_level = par_info['par_level_ml']
        reorder_point = par_info['reorder_point_ml']

        daily_actual = actual_data.groupby('Day')['Consumed (ml)'].sum()

        stockouts = 0
        days_simulated = 0

        for day, consumption in daily_actual.items():
            days_simulated += 1

            # Check if we can fulfill demand
            if current_inventory >= consumption:
                current_inventory -= consumption
            else:
                # Stockout occurred
                stockouts += 1
                current_inventory = 0

            # Reorder if below reorder point
            if current_inventory <= reorder_point:
                current_inventory = par_level  # Replenish to par level

            total_transactions += 1

        stockout_count += stockouts

        # Calculate overstock (excess inventory holding cost)
        avg_inventory = current_inventory
        if avg_inventory > par_level * 1.5:
            overstock_value += (avg_inventory - par_level)

        results.append({
            'Bar Name': bar,
            'Item': item,
            'Days Simulated': days_simulated,
            'Stockouts': stockouts,
            'Stockout Rate': stockouts / days_simulated if days_simulated > 0 else 0,
            'Final Inventory': round(current_inventory, 2),
            'Par Level': round(par_level, 2)
        })

    results_df = pd.DataFrame(results)

    # Calculate overall metrics
    service_level_achieved = 1 - (stockout_count / total_transactions) if total_transactions > 0 else 1

    print(f"\n   Simulation Results:")
    print(f"   → Total transactions simulated: {total_transactions}")
    print(f"   → Stockouts occurred: {stockout_count}")
    print(f"   → Service level achieved: {service_level_achieved*100:.2f}%")
    print(f"   → Items with stockouts: {(results_df['Stockouts'] > 0).sum()}")
    print(f"   ✓ Simulation complete")

    return results_df, service_level_achieved