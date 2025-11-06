# Hotel Inventory Management System

## Overview
The Hotel Inventory Management System is designed to efficiently manage and forecast the inventory of bar items in a hotel setting. This system utilizes advanced forecasting techniques, including Holt-Winters exponential smoothing, to predict demand and optimize inventory levels. The project includes data loading, preparation, exploratory data analysis, demand forecasting, par level calculations, and simulation of inventory management.

## Project Structure
```
hotel-inventory-system
├── src
│   ├── hotel_inventory_system.py      # Main logic for the inventory management system
│   ├── forecasting.py                  # Implements forecasting methods (Holt-Winters/Prophet)
│   ├── simulation.py                   # Handles inventory simulation and performance metrics
│   ├── par_levels.py                   # Calculates optimal inventory par levels
│   └── utils.py                        # Utility functions for data cleaning and preprocessing
├── notebooks
│   └── hotel_inventory_analysis.ipynb   # Jupyter notebook for analysis and reporting
├── tests
│   ├── test_forecast_demand.py         # Unit tests for the forecast_demand function
│   ├── test_calculate_par_levels.py     # Unit tests for the calculate_par_levels function
│   └── test_simulate_inventory_system.py # Unit tests for the simulate_inventory_system function
├── requirements.txt                     # Lists project dependencies
├── pyproject.toml                       # Project configuration and metadata
├── .gitignore                           # Specifies files to ignore in version control
└── README.md                            # Project documentation
```

## Setup Instructions
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd hotel-inventory-system
   ```

2. **Install dependencies**:
   It is recommended to create a virtual environment before installing the dependencies.
   ```
   pip install -r requirements.txt
   ```

3. **Run the main script**:
   Execute the main script to start the inventory management system:
   ```
   python src/hotel_inventory_system.py
   ```

## Usage
- The system will load the inventory data, perform exploratory data analysis, forecast demand, calculate par levels, and simulate inventory management.
- The results will be saved in CSV files and visualizations will be generated for analysis.

## Testing
- Unit tests are provided for the core functions. To run the tests, use:
   ```
   pytest tests/
   ```

## Contributions
Contributions to improve the system are welcome. Please submit a pull request or open an issue for discussion.

## License
This project is licensed under the MIT License. See the LICENSE file for details.