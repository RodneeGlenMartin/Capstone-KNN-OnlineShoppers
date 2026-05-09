import numpy as np

X = np.load('X_features.npy').astype(float)
y = np.load('y_target.npy').astype(int)
print(f"Loaded X: {X.shape}, y: {y.shape}")

def stratified_train_test_split(X, y, test_size=0.2, random_state=42):

    np.random.seed(random_state)

    class_0_indices = np.where(y == 0)[0]
    class_1_indices = np.where(y == 1)[0]

    np.random.shuffle(class_0_indices)
    np.random.shuffle(class_1_indices)

    n_test_0 = int(len(class_0_indices) * test_size)
    n_test_1 = int(len(class_1_indices) * test_size)

    test_idx = np.concatenate([class_0_indices[:n_test_0],
                                class_1_indices[:n_test_1]])
    train_idx = np.concatenate([class_0_indices[n_test_0:],
                                 class_1_indices[n_test_1:]])

    np.random.shuffle(train_idx)
    np.random.shuffle(test_idx)

    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]

X_train, X_test, y_train, y_test = stratified_train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\n" + "=" * 60)
print("TRAIN/TEST SPLIT RESULTS")
print("=" * 60)
print(f"Training set: {X_train.shape[0]} samples ({X_train.shape[0] / len(X) * 100:.1f}%)")
print(f"Test set:     {X_test.shape[0]} samples ({X_test.shape[0] / len(X) * 100:.1f}%)")

print("\nClass balance check (should be ~84.5% / 15.5% in both):")
print(f"  Train: Class 0 = {(y_train == 0).sum()} ({(y_train == 0).mean()*100:.2f}%)  |  Class 1 = {(y_train == 1).sum()} ({(y_train == 1).mean()*100:.2f}%)")
print(f"  Test:  Class 0 = {(y_test == 0).sum()} ({(y_test == 0).mean()*100:.2f}%)  |  Class 1 = {(y_test == 1).sum()} ({(y_test == 1).mean()*100:.2f}%)")

def standardize(X_train, X_test):

    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)

    std[std == 0] = 1

    X_train_scaled = (X_train - mean) / std
    X_test_scaled = (X_test - mean) / std

    return X_train_scaled, X_test_scaled, mean, std

X_train_scaled, X_test_scaled, train_mean, train_std = standardize(X_train, X_test)

print("\n" + "=" * 60)
print("STANDARDIZATION CHECK")
print("=" * 60)
print("After standardization, training data should have mean ≈ 0 and std ≈ 1 for every feature.")
print(f"  Mean of X_train_scaled (avg across all features): {X_train_scaled.mean():.6f}  (should be ≈ 0)")
print(f"  Std  of X_train_scaled (avg across all features): {X_train_scaled.std():.6f}  (should be ≈ 1)")

print("\nBefore standardization (first 3 features in training set):")
print(f"  PageValues       range: {X_train[:, 8].min():.2f} to {X_train[:, 8].max():.2f}")
print(f"  BounceRates      range: {X_train[:, 6].min():.4f} to {X_train[:, 6].max():.4f}")
print(f"  ProductRelated_Duration range: {X_train[:, 5].min():.2f} to {X_train[:, 5].max():.2f}")

print("\nAfter standardization (same features):")
print(f"  PageValues       range: {X_train_scaled[:, 8].min():.2f} to {X_train_scaled[:, 8].max():.2f}")
print(f"  BounceRates      range: {X_train_scaled[:, 6].min():.2f} to {X_train_scaled[:, 6].max():.2f}")
print(f"  ProductRelated_Duration range: {X_train_scaled[:, 5].min():.2f} to {X_train_scaled[:, 5].max():.2f}")

np.save('X_train_scaled.npy', X_train_scaled)
np.save('X_test_scaled.npy', X_test_scaled)
np.save('y_train.npy', y_train)
np.save('y_test.npy', y_test)

print("\n✅ Saved: X_train_scaled.npy, X_test_scaled.npy, y_train.npy, y_test.npy")

