# Load necessary libraries
library(dplyr)
library(ggplot2)
library(randomForest)

# Load the data
data <- read.csv("resultados_eto_ray_kdmile_2024_08_08.csv")

# Inspect the data
head(data)
str(data)

# Convert relevant columns to factors
data$Feature <- factor(data$Feature)
data$SelectionMethod <- factor(data$SelectionMethod)
data$ForecastHorizon <- factor(data$ForecastHorizon)
data$Region <- factor(data$Region)

# Ensure all NumberSelections values are non-negative and finite
data <- data %>%
  filter(NumberSelections >= 0, !is.na(NumberSelections))

# Create contingency tables
feature_selection_method_table <- xtabs(NumberSelections ~ Feature + SelectionMethod, data = data)
feature_forecast_horizon_table <- xtabs(NumberSelections ~ Feature + ForecastHorizon, data = data)
feature_region_table <- xtabs(NumberSelections ~ Feature + Region, data = data)

# Perform Chi-Square Tests
chi2_selection_method <- chisq.test(feature_selection_method_table)
chi2_forecast_horizon <- chisq.test(feature_forecast_horizon_table)
chi2_region <- chisq.test(feature_region_table)

# Output the results
print("Chi-Square Test for Feature and Selection Method:")
print(chi2_selection_method)
print("Chi-Square Test for Feature and Forecast Horizon:")
print(chi2_forecast_horizon)
print("Chi-Square Test for Feature and Region:")
print(chi2_region)

# Validate assumptions: check expected frequencies
print("Expected frequencies for Feature and Selection Method:")
print(chi2_selection_method$expected)
print("Expected frequencies for Feature and Forecast Horizon:")
print(chi2_forecast_horizon$expected)
print("Expected frequencies for Feature and Region:")
print(chi2_region$expected)

