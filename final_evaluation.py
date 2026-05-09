import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

X_full = np.load('X_features.npy').astype(float)
y_full = np.load('y_target.npy').astype(int)

X_train = np.load('X_train_scaled.npy')
X_test = np.load('X_test_scaled.npy')
y_train = np.load('y_train.npy')
y_test = np.load('y_test.npy')

print(f"Full dataset: {X_full.shape}")
print(f"Train: {X_train.shape}  |  Test: {X_test.shape}")

def knn_predict(X_train, y_train, X_test, k=7):
    predictions = np.zeros(len(X_test), dtype=int)
    for i, test_point in enumerate(X_test):
        distances = np.sqrt(np.sum((X_train - test_point) ** 2, axis=1))
        k_nearest_indices = np.argsort(distances)[:k]
        k_nearest_labels = y_train[k_nearest_indices]
        values, counts = np.unique(k_nearest_labels, return_counts=True)
        predictions[i] = values[np.argmax(counts)]
    return predictions

def standardize(X_train, X_test):
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)
    std[std == 0] = 1
    return (X_train - mean) / std, (X_test - mean) / std

def evaluate(y_true, y_pred):
    TP = int(np.sum((y_true == 1) & (y_pred == 1)))
    TN = int(np.sum((y_true == 0) & (y_pred == 0)))
    FP = int(np.sum((y_true == 0) & (y_pred == 1)))
    FN = int(np.sum((y_true == 1) & (y_pred == 0)))
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1,
            'TP': TP, 'TN': TN, 'FP': FP, 'FN': FN}

print("\n" + "=" * 70)
print("PART 1: 5-FOLD STRATIFIED CROSS-VALIDATION (k=7)")
print("=" * 70)
print("Splitting data into 5 folds and validating on each one in turn...")
print("This will take about 15-20 seconds.\n")

def stratified_kfold_indices(y, n_splits=5, random_state=42):
    """Return list of (train_idx, test_idx) for each of n_splits folds, stratified."""
    np.random.seed(random_state)
    class_0 = np.where(y == 0)[0]
    class_1 = np.where(y == 1)[0]
    np.random.shuffle(class_0)
    np.random.shuffle(class_1)

    folds_0 = np.array_split(class_0, n_splits)
    folds_1 = np.array_split(class_1, n_splits)

    splits = []
    for i in range(n_splits):
        test_idx = np.concatenate([folds_0[i], folds_1[i]])
        train_idx = np.concatenate([
            np.concatenate([folds_0[j] for j in range(n_splits) if j != i]),
            np.concatenate([folds_1[j] for j in range(n_splits) if j != i])
        ])
        splits.append((train_idx, test_idx))
    return splits

splits = stratified_kfold_indices(y_full, n_splits=5)

cv_scores = {'accuracy': [], 'precision': [], 'recall': [], 'f1': []}

print(f"{'Fold':>5} | {'Accuracy':>10} | {'Precision':>10} | {'Recall':>10} | {'F1':>10} | {'Time':>6}")
print("-" * 70)

for fold_num, (train_idx, test_idx) in enumerate(splits, 1):
    start = time.time()

    X_tr_raw, X_te_raw = X_full[train_idx], X_full[test_idx]
    y_tr, y_te = y_full[train_idx], y_full[test_idx]

    X_tr, X_te = standardize(X_tr_raw, X_te_raw)

    y_pr = knn_predict(X_tr, y_tr, X_te, k=7)
    m = evaluate(y_te, y_pr)

    cv_scores['accuracy'].append(m['accuracy'])
    cv_scores['precision'].append(m['precision'])
    cv_scores['recall'].append(m['recall'])
    cv_scores['f1'].append(m['f1'])

    elapsed = time.time() - start
    print(f"{fold_num:>5} | {m['accuracy']:>10.4f} | {m['precision']:>10.4f} | "
          f"{m['recall']:>10.4f} | {m['f1']:>10.4f} | {elapsed:>5.1f}s")

print("-" * 70)
print(f"{'MEAN':>5} | "
      f"{np.mean(cv_scores['accuracy']):>10.4f} | "
      f"{np.mean(cv_scores['precision']):>10.4f} | "
      f"{np.mean(cv_scores['recall']):>10.4f} | "
      f"{np.mean(cv_scores['f1']):>10.4f}")
print(f"{'STD':>5} | "
      f"{np.std(cv_scores['accuracy']):>10.4f} | "
      f"{np.std(cv_scores['precision']):>10.4f} | "
      f"{np.std(cv_scores['recall']):>10.4f} | "
      f"{np.std(cv_scores['f1']):>10.4f}")

print("\n" + "=" * 70)
print("PART 2: BASELINE COMPARISONS")
print("=" * 70)
print("Comparing kNN against simpler baselines on the same test set...\n")

y_pred_majority = np.zeros(len(y_test), dtype=int)
m_majority = evaluate(y_test, y_pred_majority)

with open('feature_names.txt') as f:
    feature_names = [line.strip() for line in f]
page_values_idx = feature_names.index('PageValues')

train_indices_rule = []
test_indices_rule = []

X_test_raw_pv = np.load('X_features.npy')[:, page_values_idx]

mean_pv = X_train[:, page_values_idx].mean()

y_pred_rule = (X_test[:, page_values_idx] > 0).astype(int)
m_rule = evaluate(y_test, y_pred_rule)

y_pred_knn = knn_predict(X_train, y_train, X_test, k=7)
m_knn = evaluate(y_test, y_pred_knn)

print(f"{'Model':<35} | {'Accuracy':>10} | {'Precision':>10} | {'Recall':>10} | {'F1':>10}")
print("-" * 85)
print(f"{'Baseline 1: Always No-Purchase':<35} | "
      f"{m_majority['accuracy']:>10.4f} | "
      f"{m_majority['precision']:>10.4f} | "
      f"{m_majority['recall']:>10.4f} | "
      f"{m_majority['f1']:>10.4f}")
print(f"{'Baseline 2: Rule (high PageValues)':<35} | "
      f"{m_rule['accuracy']:>10.4f} | "
      f"{m_rule['precision']:>10.4f} | "
      f"{m_rule['recall']:>10.4f} | "
      f"{m_rule['f1']:>10.4f}")
print(f"{'Our Model: kNN (k=7)':<35} | "
      f"{m_knn['accuracy']:>10.4f} | "
      f"{m_knn['precision']:>10.4f} | "
      f"{m_knn['recall']:>10.4f} | "
      f"{m_knn['f1']:>10.4f}")

print("\n" + "=" * 70)
print("PART 3: GENERATING FINAL CONFUSION MATRIX")
print("=" * 70)

cm = np.array([[m_knn['TN'], m_knn['FP']],
               [m_knn['FN'], m_knn['TP']]])

cm_pct = cm / cm.sum(axis=1, keepdims=True) * 100

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Predicted No-Purchase', 'Predicted Purchase'],
            yticklabels=['Actual No-Purchase', 'Actual Purchase'],
            cbar=False, ax=axes[0], annot_kws={'size': 14, 'weight': 'bold'})
axes[0].set_title('Confusion Matrix (Counts)\nkNN, k=7', fontsize=13)

sns.heatmap(cm_pct, annot=True, fmt='.1f', cmap='Blues',
            xticklabels=['Predicted No-Purchase', 'Predicted Purchase'],
            yticklabels=['Actual No-Purchase', 'Actual Purchase'],
            cbar=False, ax=axes[1], annot_kws={'size': 14, 'weight': 'bold'},
            vmin=0, vmax=100)
axes[1].set_title('Confusion Matrix (% by row)\nkNN, k=7', fontsize=13)

for t in axes[1].texts:
    t.set_text(t.get_text() + '%')

plt.tight_layout()
plt.savefig('fig8_final_confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)
print(f"\nModel:   kNN, k=7, Euclidean distance, standardized features")
print(f"Dataset: Online Shoppers Purchasing Intention (UCI), 12,330 sessions")
print(f"Split:   80% train (9,865) / 20% test (2,465), stratified, random_state=42")
print(f"\nFinal test set performance:")
print(f"  Accuracy : {m_knn['accuracy']:.4f}")
print(f"  Precision: {m_knn['precision']:.4f}")
print(f"  Recall   : {m_knn['recall']:.4f}")
print(f"  F1 Score : {m_knn['f1']:.4f}")
print(f"\n5-Fold cross-validation results (mean ± std):")
print(f"  Accuracy : {np.mean(cv_scores['accuracy']):.4f} ± {np.std(cv_scores['accuracy']):.4f}")
print(f"  Precision: {np.mean(cv_scores['precision']):.4f} ± {np.std(cv_scores['precision']):.4f}")
print(f"  Recall   : {np.mean(cv_scores['recall']):.4f} ± {np.std(cv_scores['recall']):.4f}")
print(f"  F1 Score : {np.mean(cv_scores['f1']):.4f} ± {np.std(cv_scores['f1']):.4f}")
print(f"\n✅ Saved final confusion matrix as fig8_final_confusion_matrix.png")
print("=" * 70)
