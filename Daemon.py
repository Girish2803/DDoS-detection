import pandas as pd
from sklearn.cluster import Birch
from sklearn.preprocessing import StandardScaler

# Load the data from the CSV file
data = pd.read_csv('output.csv')

# Select the 14 features
selected_features = ['Bwd IAT Min', 'Bwd IAT Mean', 'Src Port', 'Protocol', 'Bwd IAT Tot', 'Flow IAT Max', 'Dst Port', 'Bwd Header Len', 'Flow IAT Min', 'Flow Pkts/s', 'Bwd IAT Max', 'Flow Duration', 'Bwd Pkts/s', 'Flow IAT Std']

# Extract the selected features
features = data[selected_features]

# Standardize the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Create and fit the BIRCH model
birch_model = Birch(threshold=0.5, n_clusters=2)  # You may need to adjust the threshold based on your data
data['cluster'] = birch_model.fit_predict(features_scaled)

# Now, you can analyze the clusters and identify suspicious hosts based on your criteria
# For example, if you determine that cluster 0 is suspicious, you can filter the data
suspicious_hosts = data[data['cluster'] == 0]

# Save the suspicious hosts to a new CSV file named 'suspicious.csv'
suspicious_hosts.to_csv('suspicious.csv', index=False)