# Capstone — KNN on Online Shoppers Purchasing Intention

A capstone project that builds a **K-Nearest Neighbors (KNN) classifier from
scratch in NumPy** to predict whether an e-commerce session will end in a
purchase. The full pipeline — exploratory analysis, preprocessing, stratified
splitting, k-tuning, training, and evaluation — is implemented without
scikit-learn, so every step (distance computation, majority vote, stratified
sampling, standardization, k-fold CV, confusion matrix, precision/recall/F1)
is hand-rolled and inspectable.

Dataset: [Online Shoppers Purchasing Intention Dataset (UCI)](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset).

---

## Headline results

| Metric        | Test set (k=7) | 5-fold CV (mean ± std)      |
|---------------|----------------|-----------------------------|
| Accuracy      | **0.8767**     | reported in `final_evaluation.py` |
| Precision     | 0.6974         | reported in `final_evaluation.py` |
| Recall        | 0.3570         | reported in `final_evaluation.py` |
| F1 Score      | 0.4722         | reported in `final_evaluation.py` |

- **Best k by F1:** k = 7 (see [k_tuning_results.csv](k_tuning_results.csv))
- **Best k by Accuracy:** k = 21
- **Baselines beaten:** majority-class (always "no-purchase") and a simple
  "PageValues > 0" rule (see [final_evaluation.py](final_evaluation.py))

---

## Dataset at a glance

- **12,330** user sessions over a 12-month period
- **17** original features + 1 target (`Revenue`)
- **28** features after one-hot encoding (`Month`, `VisitorType`) — see
  [feature_names.txt](feature_names.txt)
- **Class imbalance:** ~84.5% no-purchase / ~15.5% purchase (~5.46 : 1)

Numeric features include `Administrative`, `Informational`, `ProductRelated`
(plus their `_Duration` counterparts), `BounceRates`, `ExitRates`,
`PageValues`, `SpecialDay`, and several categorical IDs
(`OperatingSystems`, `Browser`, `Region`, `TrafficType`). Categorical columns
`Month` and `VisitorType` are one-hot encoded; `Weekend` and `Revenue` are
cast to integers.

---

## Repository layout

```
.
├── online_shoppers_intention.csv     Raw dataset (12,330 × 18)
│
├── data_inspect.py                   Quick shape / dtypes / class counts
├── eda.py                            Exploratory analysis + figures 1–6
├── preprocessing.py                  One-hot encoding + dtype cleanup
├── train_test_split.py               Stratified 80/20 split + standardization
├── knn_tune_k.py                     Sweep k ∈ [1, 30], record metrics
├── knn_model.py                      Fit baseline KNN (k=5)
├── final_evaluation.py               5-fold CV, baselines, final confusion matrix
│
├── feature_names.txt                 Column order after preprocessing
├── summary_statistics.csv            describe() output for numeric features
├── k_tuning_results.csv              Accuracy/precision/recall/F1 for k=1..30
│
├── X_features.npy / y_target.npy            Cached preprocessed arrays
├── X_train_scaled.npy / X_test_scaled.npy   Cached scaled splits
├── y_train.npy / y_test.npy / y_pred_k5.npy
│
├── fig1_class_distribution.png       Revenue class balance
├── fig2_correlation_heatmap.png      Numeric feature correlations
├── fig3_pagevalues_boxplot.png       PageValues vs Revenue
├── fig4_bouncerates_boxplot.png      BounceRates vs Revenue
├── fig5_purchases_by_month.png       Conversion rate by month
├── fig6_visitor_type.png             Conversion rate by visitor type
├── fig7_k_tuning.png                 Metric curves over k
├── fig8_final_confusion_matrix.png   Final test-set confusion matrix
│
├── Capstone_Report.docx / .pdf       Full written report
├── Capstone_Presentation.pptx        Slide deck
├── Findings.docx                     Detailed findings write-up
└── Findings(1)Draft.pdf              Earlier draft of findings
```

---

## Pipeline (run in this order)

Each script reads/writes `.npy` artifacts so steps are independently
re-runnable. Numbered headings match the order in
[`README.md`](README.md) and the report.

| # | Script | Inputs | Outputs |
|---|--------|--------|---------|
| 1 | [`data_inspect.py`](data_inspect.py) | `online_shoppers_intention.csv` | console-only sanity check |
| 2 | [`eda.py`](eda.py) | `online_shoppers_intention.csv` | `fig1`–`fig6` PNGs, console tables |
| 3 | [`preprocessing.py`](preprocessing.py) | `online_shoppers_intention.csv` | `X_features.npy`, `y_target.npy`, `feature_names.txt` |
| 4 | [`train_test_split.py`](train_test_split.py) | `X_features.npy`, `y_target.npy` | `X_train_scaled.npy`, `X_test_scaled.npy`, `y_train.npy`, `y_test.npy` |
| 5 | [`knn_tune_k.py`](knn_tune_k.py) | scaled train/test arrays | `k_tuning_results.csv`, `fig7_k_tuning.png` |
| 6 | [`knn_model.py`](knn_model.py) | scaled train/test arrays | `y_pred_k5.npy`, console metrics |
| 7 | [`final_evaluation.py`](final_evaluation.py) | full feature/target + scaled splits | `fig8_final_confusion_matrix.png`, CV + baseline tables |

---

## Methodology

### Preprocessing ([preprocessing.py](preprocessing.py))
- One-hot encode `Month` and `VisitorType` (no drop-first; all dummies retained).
- Cast `Weekend` and `Revenue` to `int`.
- Save the resulting `X` and `y` as `.npy` so downstream scripts skip CSV parsing.

### Train/test split ([train_test_split.py](train_test_split.py))
- **Custom stratified 80/20 split** — shuffle each class's indices, take the
  first 20% of each as the test set so class proportions are preserved.
- **Z-score standardization** fit on training data only; the same mean/std are
  applied to the test set to prevent leakage.

### KNN classifier ([knn_model.py](knn_model.py), [knn_tune_k.py](knn_tune_k.py), [final_evaluation.py](final_evaluation.py))
- Pure NumPy implementation: compute Euclidean distances from each test point
  to every training point, take the `k` smallest, majority-vote the labels.
- Confusion-matrix counts (TP, TN, FP, FN) and all metrics (accuracy,
  precision, recall, F1, specificity) are computed by hand.

### Model selection ([knn_tune_k.py](knn_tune_k.py))
- Sweep `k = 1..30`, log accuracy / precision / recall / F1 per `k`.
- Save the results to [k_tuning_results.csv](k_tuning_results.csv) and plot
  metric curves to [fig7_k_tuning.png](fig7_k_tuning.png).

### Final evaluation ([final_evaluation.py](final_evaluation.py))
- **5-fold stratified cross-validation** with `k = 7` — folds are built by
  splitting each class's shuffled indices into 5 parts, so every fold keeps
  the original class balance.
- **Baseline comparisons:** majority-class (always predict "no-purchase") and
  a simple rule (`PageValues > 0 → purchase`).
- Final confusion matrix saved as both counts and row-wise percentages in
  [fig8_final_confusion_matrix.png](fig8_final_confusion_matrix.png).

---

## Getting started

### Requirements
- Python 3.9+
- `numpy`, `pandas`, `matplotlib`, `seaborn`

Install with:

```bash
pip install numpy pandas matplotlib seaborn
```

### Run the full pipeline

From the repository root, in order:

```bash
python data_inspect.py
python eda.py
python preprocessing.py
python train_test_split.py
python knn_tune_k.py
python knn_model.py
python final_evaluation.py
```

The cached `.npy` files are committed, so you can also skip steps 3–4 and
jump straight to tuning or final evaluation.

**Runtime note.** KNN is O(n_train · n_test · d) per prediction, with no
training phase. On a laptop the full k-sweep (`knn_tune_k.py`, 30 values of
`k`) takes roughly 30–60 seconds; `knn_model.py` and each CV fold in
`final_evaluation.py` take a few seconds each.

---

## Figures

| File | What it shows |
|------|---------------|
| [fig1_class_distribution.png](fig1_class_distribution.png) | Imbalance between purchase / no-purchase sessions |
| [fig2_correlation_heatmap.png](fig2_correlation_heatmap.png) | Correlations among numeric features |
| [fig3_pagevalues_boxplot.png](fig3_pagevalues_boxplot.png) | `PageValues` distribution split by outcome |
| [fig4_bouncerates_boxplot.png](fig4_bouncerates_boxplot.png) | `BounceRates` distribution split by outcome |
| [fig5_purchases_by_month.png](fig5_purchases_by_month.png) | Sessions and conversion rate by month |
| [fig6_visitor_type.png](fig6_visitor_type.png) | Sessions and conversion rate by visitor type |
| [fig7_k_tuning.png](fig7_k_tuning.png) | Accuracy / precision / recall / F1 across `k = 1..30` |
| [fig8_final_confusion_matrix.png](fig8_final_confusion_matrix.png) | Test-set confusion matrix for the final model (k=7) |

---

## Deliverables

- [Capstone_Report.pdf](Capstone_Report.pdf) / [Capstone_Report.docx](Capstone_Report.docx) — full written report
- [Capstone_Presentation.pptx](Capstone_Presentation.pptx) — defense slide deck
- [Findings.docx](Findings.docx) — extended findings write-up
- [Findings(1)Draft.pdf](Findings(1)Draft.pdf) — earlier draft

---

## Key takeaways

- **`PageValues` is the dominant signal.** Even a naive `PageValues > 0` rule
  outperforms majority-class on F1; KNN improves further by combining it with
  the rest of the feature space.
- **Tuning `k` is a precision/recall trade-off.** Small `k` (≤3) chases
  recall at the cost of false positives; large `k` (≥20) pushes precision
  upward but recall collapses. `k = 7` sits near the F1 peak.
- **Class imbalance hurts recall.** With ~15.5% positives, the model
  correctly catches only ~36% of actual buyers at k=7 even with standardized
  features — a future iteration could add class weighting, SMOTE, or a
  threshold-tuned probabilistic model.

---

## Citation

Dataset: Sakar, C.O., Polat, S.O., Katircioglu, M. *et al.* "Real-time prediction of online shoppers' purchasing intention using multilayer perceptron and LSTM recurrent neural networks." *Neural Comput & Applic* **31**, 6893–6908 (2019). UCI ML Repository: <https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset>
