# **Hotel Bar Inventory Forecasting and Recommendation System**

## **1. Core Business Problem and Why It Matters**

A growing hotel chain operates multiple bars that frequently face **stockouts of high-demand items** and **overstocking of slow-moving inventory**. These issues lead to:

* Lost sales and lower guest satisfaction during stockouts
* Higher holding and wastage costs for overstocked items

Inventory decisions are currently made manually, based on intuition rather than data. This creates inconsistent ordering patterns and inefficient inventory turnover.

The business problem matters because the **profitability and reputation of the hotel chain depend on reliable bar operations**. A data-driven system can help maintain the right balance of inventory — minimizing waste and ensuring guest satisfaction.

---

## **2. Assumptions and Rationale**

To simulate the system realistically while keeping it computationally practical, several assumptions were made:

* **Historical consumption represents future demand trends**, excluding extraordinary events (festivals, parties, etc.).
* **Each bar operates independently**, with unique consumption behavior based on its clientele.
* **Lead times for restocking remain stable**, allowing fixed reorder points to be effective.
* **Daily consumption data** is reliable after cleaning and outlier removal (99th percentile capping).
* Missing numeric or date values are imputed or ignored when they don’t materially affect analysis.

These assumptions simplify the model and make it feasible to forecast demand with limited data while maintaining logical consistency.

---

## **3. Model Choice and Justification**

Different forecasting approaches were considered:

| Model Type                                    | Advantages                    | Drawbacks                                                      |
| --------------------------------------------- | ----------------------------- | -------------------------------------------------------------- |
| **ARIMA / ETS (classical time series)**       | Handles temporal data well    | Requires long, stationary time series; overfits short datasets |
| **Machine Learning (Random Forest, XGBoost)** | Captures non-linear trends    | Data-hungry; limited interpretability                          |
| **Neural Networks (LSTM)**                    | Can model complex seasonality | Overkill for small-scale or noisy data                         |
| **Rolling Average + Exponential Smoothing**   | Simple, explainable, adaptive | Less sensitive to rapid short-term changes                     |

**Chosen Model:** *Rolling Average with Exponential Smoothing*

* Balances simplicity and accuracy.
* Interpretable by hotel managers.
* Works effectively with limited, irregular data across multiple bars.

It also integrates seamlessly with a rule-based recommendation system for par levels and reorder thresholds.

---

## **4. System Performance and Improvements**

The system was tested on historical data to simulate real operations.

**Performance Overview:**

* Forecast accuracy within ±10–15% for stable consumption items.
* Volatile items (seasonal liquors, premium labels) show larger deviations.
* Stockouts predicted correctly in most high-volume categories.

**Strengths:**

* Fully explainable recommendations
* Quick visual insights for top bars and high-consumption items
* Flexible thresholds for par and reorder points

**Areas for Improvement:**

* Incorporate **external features** like occupancy rate, day-of-week, and local events
* Introduce **dynamic reorder points** that adapt to trends and supplier lead times
* Implement **monthly model retraining** for evolving consumption patterns
* Integrate with a **real-time dashboard** for actionable insights

---

## **5. Real-World Implementation in a Hotel**

In an operational setup, the system would function as follows:

1. **Daily Data Ingestion**: Inventory and sales data automatically pulled from POS systems.
2. **Forecast Generation**: Short-term demand forecast for each (Bar, Item) pair.
3. **Recommendation Engine**: Calculates:

   * Par Level (target inventory)
   * Reorder Point (minimum threshold)
   * Suggested Order Quantity
4. **Dashboard for Managers**:

   * Visual indicators: `ORDER NOW`, `MONITOR`, or `OK`
   * Drill-down by bar or item for actionable insights.
5. **Feedback Loop**: Manager overrides and actual outcomes feed back to retrain the model.

This setup would make procurement proactive instead of reactive — ensuring stock continuity without waste.

---

## **6. Scalability and Production Considerations (Optional)**

At larger scale:

* **Data consistency** across multiple hotel branches becomes critical.
* **API integration** with suppliers and POS systems is needed for automation.
* **Central monitoring** of performance metrics:

  * Forecast Accuracy (MAPE)
  * Stockout and Overstock Rates
  * Cost Savings vs. Manual Process
  * Manager Overrides and Compliance

Monitoring these ensures the system remains reliable, interpretable, and trusted as it grows.

---

## **7. Summary**

The designed system transforms hotel bar inventory management from an intuition-based approach to a data-driven, predictive framework.
It enables each location to:

* Maintain optimal stock levels
* Prevent losses due to unavailability
* Reduce carrying costs
* Improve guest satisfaction
