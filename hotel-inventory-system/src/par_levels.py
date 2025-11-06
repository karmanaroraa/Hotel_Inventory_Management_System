import pandas as pd
import numpy as np

def calculate_par_levels(forecasts, lead_time_days=3, service_level=0.95):
    """
    Calculate optimal inventory par levels.

    Par Level = (Average Daily Demand × Lead Time) + Safety Stock
    Safety Stock = Z-score × Std Dev × sqrt(Lead Time)

    This implementation is defensive about forecast dict keys:
    - Tries common names for avg/std/forecast values
    - Falls back to computing mean/std from a 'history' or 'actuals' series if provided
    """
    print(f"\nCalculating par levels...")
    print(f"   → Lead time: {lead_time_days} days")
    print(f"   → Service level: {service_level*100}%")

    # Z-score for service level
    z_scores = {0.90: 1.28, 0.95: 1.65, 0.99: 2.33}
    z_score = z_scores.get(service_level, 1.65)

    par_levels = {}

    for (bar, item), forecast in forecasts.items():
        # defensive retrieval of average daily consumption
        avg_keys = ['avg_daily_consumption', 'avg_daily', 'avg_consumption', 'mean_daily', 'mean_consumption']
        std_keys = ['std_consumption', 'std_daily', 'std', 'stddev']
        forecast_keys = ['forecast_daily', 'forecast_mean', 'forecast', 'forecast_values']

        avg_daily = None
        for k in avg_keys:
            if k in forecast:
                avg_daily = forecast[k]
                break

        std_daily = None
        for k in std_keys:
            if k in forecast:
                std_daily = forecast[k]
                break

        forecast_daily = None
        for k in forecast_keys:
            if k in forecast:
                forecast_daily = forecast[k]
                break

        # If not present, try to compute from history/actuals/series
        history = forecast.get('history') or forecast.get('actuals') or forecast.get('series') or forecast.get('y')
        if avg_daily is None and history is not None:
            try:
                arr = np.array(history, dtype=float)
                avg_daily = float(np.nanmean(arr))
            except Exception:
                avg_daily = 0.0

        if std_daily is None and history is not None:
            try:
                arr = np.array(history, dtype=float)
                std_daily = float(np.nanstd(arr, ddof=1))
            except Exception:
                std_daily = 0.0

        # If still missing, set reasonable defaults
        try:
            avg_daily = float(avg_daily) if avg_daily is not None else 0.0
        except Exception:
            avg_daily = 0.0

        try:
            std_daily = float(std_daily) if std_daily is not None else 0.0
        except Exception:
            std_daily = max(avg_daily * 0.2, 1e-6)

        # Guard against zero std
        if std_daily == 0 or pd.isna(std_daily):
            std_daily = max(avg_daily * 0.2, 1e-6)

        # Cycle stock: expected demand during lead time
        cycle_stock = avg_daily * lead_time_days

        # Safety stock: buffer for demand variability
        safety_stock = z_score * std_daily * np.sqrt(lead_time_days)

        # Par level
        par_level = cycle_stock + safety_stock

        # Reorder point (when to order) = expected demand during lead time + safety stock
        reorder_point = cycle_stock + safety_stock

        # Forecast daily (single value) - try to reduce array to mean if needed
        if isinstance(forecast_daily, (list, tuple, np.ndarray)):
            try:
                forecast_daily_val = float(np.nanmean(np.array(forecast_daily, dtype=float)))
            except Exception:
                forecast_daily_val = round(avg_daily, 2)
        else:
            forecast_daily_val = float(forecast_daily) if forecast_daily is not None else round(avg_daily, 2)

        par_levels[(bar, item)] = {
            'par_level_ml': round(par_level, 2),
            'cycle_stock_ml': round(cycle_stock, 2),
            'safety_stock_ml': round(safety_stock, 2),
            'reorder_point_ml': round(reorder_point, 2),
            'avg_daily_demand': round(avg_daily, 2),
            'std_daily': round(std_daily, 2),
            'forecast_daily': round(forecast_daily_val, 2)
        }

    print(f"   ✓ Calculated par levels for {len(par_levels)} combinations")
    return par_levels