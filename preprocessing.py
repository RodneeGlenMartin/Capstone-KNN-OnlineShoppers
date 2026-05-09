import pandas as pd
import numpy as np

df = pd.read_csv('online_shoppers_intention.csv')
print("Original shape:", df.shape)
print("Original columns:", list(df.columns))

df_encoded = pd.get_dummies(df, columns=['Month', 'VisitorType'], drop_first=False)

print("\nAfter one-hot encoding:")
print("New shape:", df_encoded.shape)

new_columns = [c for c in df_encoded.columns if c.startswith('Month_') or c.startswith('VisitorType_')]
print("New columns created:", new_columns)

df_encoded['Weekend'] = df_encoded['Weekend'].astype(int)
df_encoded['Revenue'] = df_encoded['Revenue'].astype(int)

for col in new_columns:
    df_encoded[col] = df_encoded[col].astype(int)

print("\nData types after conversion:")
print(df_encoded.dtypes.value_counts())

X = df_encoded.drop('Revenue', axis=1).values
y = df_encoded['Revenue'].values
feature_names = df_encoded.drop('Revenue', axis=1).columns.tolist()

print("\nFinal feature matrix X shape:", X.shape)
print("Final target vector y shape:", y.shape)
print("Number of features used:", len(feature_names))

np.save('X_features.npy', X)
np.save('y_target.npy', y)

with open('feature_names.txt', 'w') as f:
    for name in feature_names:
        f.write(name + '\n')

print("\nPreprocessed data saved:")
print("  X_features.npy   -> the feature matrix")
print("  y_target.npy     -> the target vector")
print("  feature_names.txt -> the feature names in order")

print("\n" + "=" * 60)
print("SANITY CHECKS")
print("=" * 60)
print(f"Total rows: {X.shape[0]}  (should be 12330)")
print(f"Total features: {X.shape[1]}")
print(f"Class 0 (No Purchase) count: {(y == 0).sum()}  (should be 10422)")
print(f"Class 1 (Purchase)   count: {(y == 1).sum()}  (should be 1908)")
print(f"Any NaN values in X? {np.isnan(X.astype(float)).any()}")
print(f"All values numeric? {X.dtype}")

print("\n" + "=" * 60)
print("PREVIEW OF FEATURES (first 3 rows, first 8 columns)")
print("=" * 60)
preview_df = pd.DataFrame(X[:3, :8], columns=feature_names[:8])
print(preview_df)

print("\n✅ Preprocessing complete. Ready for train/test split (Step 4).")
