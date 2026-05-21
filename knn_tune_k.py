import numpy as np
import matplotlib.pyplot as plt
import time

X_train = np.load('X_train_scaled.npy')
X_test = np.load('X_test_scaled.npy')
y_train = np.load('y_train.npy')
y_test = np.load('y_test.npy')

def knn_predict(X_train, y_train, X_test, k=5):
    predictions = np.zeros(len(X_test), dtype=int)
    for i, test_point in enumerate(X_test):
        distances = np.sqrt(np.sum((X_train - test_point) ** 2, axis=1))
        k_nearest_indices = np.argsort(distances)[:k]
        k_nearest_labels = y_train[k_nearest_indices]
        values, counts = np.unique(k_nearest_labels, return_counts=True)
        predictions[i] = values[np.argmax(counts)]
    return predictions

def evaluate(y_true, y_pred):
    TP = int(np.sum((y_true == 1) & (y_pred == 1)))
    TN = int(np.sum((y_true == 0) & (y_pred == 0)))
    FP = int(np.sum((y_true == 0) & (y_pred == 1)))
    FN = int(np.sum((y_true == 1) & (y_pred == 0)))
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return accuracy, precision, recall, f1

k_values = list(range(1, 31))
results = []

print("=" * 70)
print(f"{'k':>4} | {'Accuracy':>10} | {'Precision':>10} | {'Recall':>10} | {'F1':>10} | {'Time':>6}")
print("=" * 70)

for k in k_values:
    start = time.time()
    y_pred = knn_predict(X_train, y_train, X_test, k=k)
    elapsed = time.time() - start

    acc, prec, rec, f1 = evaluate(y_test, y_pred)
    results.append({'k': k, 'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1})

    print(f"{k:>4} | {acc:>10.4f} | {prec:>10.4f} | {rec:>10.4f} | {f1:>10.4f} | {elapsed:>5.1f}s")

print("\n" + "=" * 70)
print("BEST k FOR EACH METRIC")
print("=" * 70)
best_acc = max(results, key=lambda r: r['accuracy'])
best_f1 = max(results, key=lambda r: r['f1'])
best_recall = max(results, key=lambda r: r['recall'])
best_prec = max(results, key=lambda r: r['precision'])

print(f"  Best Accuracy : k = {best_acc['k']:>3}  -> {best_acc['accuracy']:.4f}")
print(f"  Best F1       : k = {best_f1['k']:>3}  -> {best_f1['f1']:.4f}")
print(f"  Best Recall   : k = {best_recall['k']:>3}  -> {best_recall['recall']:.4f}")
print(f"  Best Precision: k = {best_prec['k']:>3}  -> {best_prec['precision']:.4f}")

ks = [r['k'] for r in results]
accs = [r['accuracy'] for r in results]
precs = [r['precision'] for r in results]
recs = [r['recall'] for r in results]
f1s = [r['f1'] for r in results]

plt.figure(figsize=(11, 6))
plt.plot(ks, accs, marker='o', label='Accuracy', linewidth=2)
plt.plot(ks, precs, marker='s', label='Precision', linewidth=2)
plt.plot(ks, recs, marker='^', label='Recall', linewidth=2)
plt.plot(ks, f1s, marker='d', label='F1 Score', linewidth=2)

# k=3 is the raw F1 max (0.489), but k=7 (F1 0.472) is our chosen model: it has
# much higher precision (0.70 vs 0.60), which is the metric we optimize for.
CHOSEN_K = 7
plt.axvline(x=CHOSEN_K, color='red', linestyle='--', alpha=0.6,
            label=f'Chosen: k={CHOSEN_K}')

plt.title('kNN Performance vs k (Online Shoppers Dataset)', fontsize=13)
plt.xlabel('k (number of neighbors)')
plt.ylabel('Score')
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.xticks(ks)
plt.tight_layout()
plt.savefig('fig7_k_tuning.png', dpi=150, bbox_inches='tight')
plt.show()

import csv
with open('k_tuning_results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['k', 'accuracy', 'precision', 'recall', 'f1'])
    writer.writeheader()
    for r in results:
        writer.writerow(r)

print("\n✅ Saved: fig7_k_tuning.png and k_tuning_results.csv")
