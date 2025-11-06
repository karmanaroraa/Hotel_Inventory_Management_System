import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ...existing code...
def load_and_prepare_data(file_path):
    """
    Load CSV and normalize expected columns:
    - Ensures Date/Day column exists and is datetime
    - Ensures numeric columns for consumption and closing balance
    """
    df = pd.read_csv(file_path)
    # Normalize column names
    df.columns = [c.strip() for c in df.columns]
    # Detect date column
    date_col = None
    for candidate in ['Date', 'Day', 'date', 'day', 'Date Time Served', 'DateTime']:
        if candidate in df.columns:
            date_col = candidate
            break
    if date_col is None:
        raise ValueError("Could not find a Date/Day column in the dataset")
    df['Date'] = pd.to_datetime(df[date_col], errors='coerce')
    if df['Date'].isna().all():
        raise ValueError("Date column could not be parsed to datetime")
    df['Date'] = df['Date'].dt.normalize()
    df['Day'] = df['Date'].dt.date
    # Ensure key columns exist
    if 'Bar Name' not in df.columns or 'Item' not in df.columns:
        # Try to construct Item if alternative columns exist
        if 'Alcohol Type' in df.columns and 'Brand Name' in df.columns:
            df['Item'] = df['Alcohol Type'].astype(str) + ' - ' + df['Brand Name'].astype(str)
        else:
            raise ValueError("Expected columns 'Bar Name' and 'Item' in dataset")
    # Normalize numeric columns
    if 'Consumed (ml)' in df.columns:
        df['Consumed (ml)'] = pd.to_numeric(df['Consumed (ml)'], errors='coerce').fillna(0)
    else:
        df['Consumed (ml)'] = 0
    if 'Closing Balance (ml)' in df.columns:
        df['Closing Balance (ml)'] = pd.to_numeric(df['Closing Balance (ml)'], errors='coerce').fillna(0)
    else:
        df['Closing Balance (ml)'] = 0
    # Ensure Bar Name is string
    df['Bar Name'] = df['Bar Name'].astype(str)
    return df

# ...existing code...
def perform_eda(df, top_n=10):
    """
    Simple EDA helpers:
    - top_items: list of top N items by total consumption
    - bar_consumption: total consumption per bar (Series)
    """
    item_totals = df.groupby('Item')['Consumed (ml)'].sum().sort_values(ascending=False)
    top_items = item_totals.head(top_n).index.tolist()
    bar_consumption = df.groupby('Bar Name')['Consumed (ml)'].sum().sort_values(ascending=False)
    return top_items, bar_consumption

# ...existing code...
def generate_recommendations(df, forecasts, par_levels, results_df):
    """
    Generate actionable recommendations (same signature used in main).
    Returns DataFrame with actions and order quantities.
    """
    recommendations = []
    for (bar, item), par_info in par_levels.items():
        # get latest closing balance
        rows = df[(df['Bar Name'] == bar) & (df['Item'] == item)].sort_values('Date')
        current_stock = rows['Closing Balance (ml)'].iloc[-1] if len(rows) > 0 else 0
        par_level = par_info['par_level_ml']
        reorder_point = par_info['reorder_point_ml']
        if current_stock < reorder_point:
            action = "ORDER NOW"
            order_quantity = max(par_level - current_stock, 0)
        elif current_stock < par_level:
            action = "Monitor - Below Par"
            order_quantity = max(par_level - current_stock, 0)
        elif current_stock > par_level * 1.5:
            action = "Reduce - Overstock"
            order_quantity = 0
        else:
            action = "OK"
            order_quantity = 0
        avg_daily = par_info.get('avg_daily_demand', 0) or 0
        days_of_stock = round(current_stock / avg_daily, 1) if avg_daily > 0 else np.nan
        recommendations.append({
            'Bar Name': bar,
            'Item': item,
            'Current Stock (ml)': round(current_stock, 2),
            'Par Level (ml)': round(par_level, 2),
            'Reorder Point (ml)': round(reorder_point, 2),
            'Avg Daily Demand (ml)': par_info.get('avg_daily_demand', 0),
            'Forecasted Daily Demand (ml)': par_info.get('forecast_daily', 0),
            'Action': action,
            'Order Quantity (ml)': round(order_quantity, 2),
            'Days of Stock': days_of_stock
        })
    rec_df = pd.DataFrame(recommendations)
    return rec_df

# ...existing code...
def create_visualizations(df, forecasts, par_levels, rec_df):
    """
    Create a couple of quick plots and save as inventory_analysis.png
    """
    plt.figure(figsize=(12, 6))
    # consumption by bar
    if 'Bar Name' in df.columns and 'Consumed (ml)' in df.columns:
        bar_sum = df.groupby('Bar Name')['Consumed (ml)'].sum().sort_values(ascending=False).head(10)
        sns.barplot(x=bar_sum.values, y=bar_sum.index, palette='viridis')
        plt.title('Top 10 Bars by Consumption (ml)')
        plt.tight_layout()
        plt.savefig('inventory_analysis_top_bars.png', dpi=150)
        plt.close()

    # Items with most ORDER NOW
    if rec_df is not None and not rec_df.empty:
        plt.figure(figsize=(8, 6))
        urgent = rec_df[rec_df['Action'] == 'ORDER NOW'].groupby('Item').size().sort_values(ascending=False).head(10)
        if not urgent.empty:
            sns.barplot(x=urgent.values, y=urgent.index, palette='rocket')
            plt.title('Top Items Needing Immediate Orders')
            plt.tight_layout()
            plt.savefig('inventory_analysis_urgent_items.png', dpi=150)
            plt.close()
    return True

# ...existing code...
def clean_data(df):
    """Clean the input DataFrame by handling missing values and outliers."""
    if 'Consumed (ml)' in df.columns:
        df['Consumed (ml)'] = df['Consumed (ml)'].fillna(0)
        # Remove outliers in consumption (values > 99th percentile)
        consumption_99th = df['Consumed (ml)'].quantile(0.99)
        df.loc[df['Consumed (ml)'] > consumption_99th, 'Consumed (ml)'] = consumption_99th
    if 'Purchase (ml)' in df.columns:
        df['Purchase (ml)'] = df['Purchase (ml)'].fillna(0)
    return df

def create_item_identifier(df):
    """Create a unique item identifier in the DataFrame if needed."""
    if 'Item' not in df.columns and 'Alcohol Type' in df.columns and 'Brand Name' in df.columns:
        df['Item'] = df['Alcohol Type'].astype(str) + ' - ' + df['Brand Name'].astype(str)
    return df

def convert_date_columns(df):
    """Convert date columns to datetime format and extract additional date features."""
    # Look for possible date columns
    candidates = ['Date', 'Date Time Served', 'DateTime']
    date_col = next((c for c in candidates if c in df.columns), None)
    if date_col is None:
        return df
    df['Date'] = pd.to_datetime(df[date_col], errors='coerce')
    if df['Date'].isna().all():
        return df
    df['Day'] = df['Date'].dt.date
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['DayName'] = df['Date'].dt.day_name()
    df['Week'] = df['Date'].dt.isocalendar().week
    df['Month'] = df['Date'].dt.month
    return df
# ...existing code...

if __name__ == "__main__":
    file_path = "hotel_bar_inventory.csv"
    df = load_and_prepare_data(file_path)
    df = clean_data(df)
    df = create_item_identifier(df)
    df = convert_date_columns(df)

    top_items, bar_consumption = perform_eda(df)
    print("Top items:", top_items)

    # Mock placeholders for testing
    forecasts = {}
    par_levels = {
        ('Bar A', 'Whisky - Glenfiddich'): {'par_level_ml': 5000, 'reorder_point_ml': 2000, 'avg_daily_demand': 150, 'forecast_daily': 140}
    }
    results_df = pd.DataFrame()

    rec_df = generate_recommendations(df, forecasts, par_levels, results_df)
    create_visualizations(df, forecasts, par_levels, rec_df)
