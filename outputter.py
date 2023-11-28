import pandas as pd

# Read the input CSV file
df = pd.read_csv('input.csv')

# Rename 'Completed Items' to 'Comments'
df.rename(columns={'Completed Items': 'Comments'}, inplace=True)

# Select only the relevant columns
df = df[['Date', 'Source', 'Comments', 'Replies', 'Time']]

# Melt the DataFrame to long format
df_melt = df.melt(id_vars=['Date', 'Source'], var_name='Type', value_name='Value')

# Create a new column by combining 'Source' and 'Type'
df_melt['Source_Type'] = df_melt['Source'] + ' ' + df_melt['Type']

# Aggregate the data by taking the sum of 'Value' for each 'Date' and 'Source_Type'
df_agg = df_melt.groupby(['Date', 'Source_Type'])['Value'].sum().reset_index()

# Pivot the DataFrame back to wide format
df_pivot = df_agg.pivot(index='Date', columns='Source_Type', values='Value')

# Write the output DataFrame to a CSV file
df_pivot.to_csv('output.csv')
