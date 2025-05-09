import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
file_path = 'D:\\test-tasks\\appflame\\Task4.csv'
df = pd.read_csv(file_path)

# Convert 'rd' and 'TD' to datetime format
df['rd'] = pd.to_datetime(df['rd'], format='%d.%m.%Y')
df['TD'] = pd.to_datetime(df['TD'], format='%d.%m.%Y')

# Filter out rows where 'TD' is NaN
df_filtered = df[df['TD'].notna()].copy()

# Calculate months since registration
df_filtered['months_since_registration'] = ((df_filtered['TD'].dt.year - df_filtered['rd'].dt.year) * 12 + df_filtered['TD'].dt.month - df_filtered['rd'].dt.month)

# Group by customer and month, and sum the revenue
df_grouped = df_filtered.groupby(['customer_id', 'months_since_registration'])['revenue_usd'].sum().reset_index()

# Calculate average revenue per user for each month
df_monthly_revenue = df_grouped.groupby('months_since_registration')['revenue_usd'].mean().reset_index()

# Calculate cumulative LTV
df_monthly_revenue['LTV'] = df_monthly_revenue['revenue_usd'].cumsum()

# LTV for the 6th month
ltv_6th_month = df_monthly_revenue[df_monthly_revenue['months_since_registration'] == 6]['LTV'].values[0]
print(f"LTV for the 6th month: {ltv_6th_month:.2f}")

# Plotting the LTV curve using matplotlib
plt.figure(figsize=(10, 6))
plt.plot(df_monthly_revenue['months_since_registration'], df_monthly_revenue['LTV'], marker='o')
plt.title('LTV Curve')
plt.xlabel('Month')
plt.ylabel('Cumulative LTV')
plt.grid(True)
plt.show()