import numpy as np
import time

X_train = np.load('X_train_scaled.npy')
X_test = np.load('X_test_scaled.npy')
y_train = np.load('y_train.npy')
y_test = np.load('y_test.npy')

print(f"Loaded training set: {X_train.shape}")
print(f"Loaded test set:     {X_test.shape}")

def knn_predict(X_train, y_train, X_test, k=5):

    predictions = np.zeros(len(X_test), dtype=int)

    for i, test_point in enumerate(X_test):

        distances = np.sqrt(np.sum((X_train - test_point) ** 2, axis=1))

        k_nearest_indices = np.argsort(distances)[:k]

        k_nearest_labels = y_train[k_nearest_indices]

        values, counts = np.unique(k_nearest_labels, return_counts=True)
        predictions[i] = values[np.argmax(counts)]

        if (i + 1) % 500 == 0:
            print(f"  Predicted {i + 1} / {len(X_test)} test points...")

    return predictions

def confusion_matrix_manual(y_true, y_pred):

    TP = int(np.sum((y_true == 1) & (y_pred == 1)))
    TN = int(np.sum((y_true == 0) & (y_pred == 0)))
    FP = int(np.sum((y_true == 0) & (y_pred == 1)))
    FN = int(np.sum((y_true == 1) & (y_pred == 0)))
    return TP, TN, FP, FN

def evaluate(y_true, y_pred):

    TP, TN, FP, FN = confusion_matrix_manual(y_true, y_pred)

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    specificity = TN / (TN + FP) if (TN + FP) > 0 else 0

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'specificity': specificity,
        'TP': TP, 'TN': TN, 'FP': FP, 'FN': FN
    }

def print_results(metrics, k):

    print("\n" + "=" * 60)
    print(f"RESULTS WITH k = {k}")
    print("=" * 60)
    print(f"  Accuracy   : {metrics['accuracy']:.4f}  ({metrics['accuracy']*100:.2f}%)")
    print(f"  Precision  : {metrics['precision']:.4f}  (when we predict purchase, how often we're right)")
    print(f"  Recall     : {metrics['recall']:.4f}  (of actual buyers, how many we caught)")
    print(f"  F1 Score   : {metrics['f1']:.4f}  (balance of precision & recall)")
    print(f"  Specificity: {metrics['specificity']:.4f}  (of non-buyers, how many we correctly excluded)")
    print("\n  Confusion Matrix:")
    print(f"                  Predicted")
    print(f"                  No-Buy    Buy")
    print(f"    Actual No-Buy   {metrics['TN']:>5}   {metrics['FP']:>5}")
    print(f"    Actual Buy      {metrics['FN']:>5}   {metrics['TP']:>5}")
    print()
    print(f"  TP = {metrics['TP']}  (correctly predicted buyers)")
    print(f"  TN = {metrics['TN']}  (correctly predicted non-buyers)")
    print(f"  FP = {metrics['FP']}  (predicted buy, but didn't)")
    print(f"  FN = {metrics['FN']}  (predicted no-buy, but did)")

print("\n" + "=" * 60)
print("RUNNING kNN WITH k = 5 (BASELINE)")
print("=" * 60)
print("This may take 1-3 minutes...\n")

start = time.time()
y_pred_5 = knn_predict(X_train, y_train, X_test, k=5)
elapsed = time.time() - start
print(f"\nPrediction completed in {elapsed:.1f} seconds.")

metrics_5 = evaluate(y_test, y_pred_5)
print_results(metrics_5, k=5)

np.save('y_pred_k5.npy', y_pred_5)
print("\n✅ Predictions saved to y_pred_k5.npy")

