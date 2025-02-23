import pandas as pd

# Load the dataset
input_file = "LargeData-Fuel-Consumption.csv"  # Replace with your input file name
df = pd.read_csv(input_file)

# Debugging: Print column names to verify
print("Original column names:")
print(df.columns.tolist())

# Clean column names (remove extra spaces and convert to uppercase)
df.columns = df.columns.str.strip().str.upper()

# Debugging: Print cleaned column names
print("\nCleaned column names:")
print(df.columns.tolist())

# Step 1: Check for missing values
print("\nStep 1: Checking for missing values...")
print(df.isnull().sum())

# Drop rows with missing values
df_cleaned = df.dropna()
print("\nRows with missing values have been dropped.")

# Step 2: Check for duplicates
print("\nStep 2: Checking for duplicates...")
duplicates = df_cleaned.duplicated().sum()
print(f"Number of duplicate rows: {duplicates}")

# Drop duplicates
df_cleaned = df_cleaned.drop_duplicates()
print("Duplicate rows have been dropped.")

# Step 3: Check data types
print("\nStep 3: Checking data types...")
print(df_cleaned.dtypes)

# Convert columns to appropriate data types if needed
df_cleaned['ENGINE SIZE'] = df_cleaned['ENGINE SIZE'].astype(float)
df_cleaned['CYLINDERS'] = df_cleaned['CYLINDERS'].astype(int)
df_cleaned['FUEL CONSUMPTION'] = df_cleaned['FUEL CONSUMPTION'].astype(float)
df_cleaned['COEMISSIONS'] = df_cleaned['COEMISSIONS'].astype(int)  # Ensure this matches the cleaned column name
print("\nData types have been corrected.")

# Step 4: Handle outliers
print("\nStep 4: Handling outliers...")

# Function to detect and handle outliers using IQR
def handle_outliers(column):
    Q1 = column.quantile(0.25)
    Q3 = column.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return column[(column >= lower_bound) & (column <= upper_bound)]

# Apply outlier handling to numerical columns
df_cleaned['FUEL CONSUMPTION'] = handle_outliers(df_cleaned['FUEL CONSUMPTION'])
df_cleaned['COEMISSIONS'] = handle_outliers(df_cleaned['COEMISSIONS'])  # Ensure this matches the cleaned column name
print("Outliers have been handled.")

# Save the cleaned dataset to a new file
output_file = "cleaned_fuel_consumption.csv"  # Replace with your desired output file name
df_cleaned.to_csv(output_file, index=False)

# Confirm completion
print(f"\nCleaned dataset saved to '{output_file}'.")
print(f"Number of rows in cleaned dataset: {len(df_cleaned)}")