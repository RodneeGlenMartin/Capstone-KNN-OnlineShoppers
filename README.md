# Capstone — KNN on Online Shoppers Intention

A capstone project applying K-Nearest Neighbors (KNN) classification to the
[Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset)
to predict whether a session ends in a purchase.

## Pipeline

1. **`data_inspect.py`** — initial dataset inspection
2. **`eda.py`** — exploratory data analysis (figures 1–6)
3. **`preprocessing.py`** — encoding + scaling, produces `X_features.npy` / `y_target.npy`
4. **`train_test_split.py`** — stratified split, produces `X_{train,test}_scaled.npy` / `y_{train,test}.npy`
5. **`knn_tune_k.py`** — sweep k, write `k_tuning_results.csv` and `fig7_k_tuning.png`
6. **`knn_model.py`** — fit final KNN
7. **`final_evaluation.py`** — confusion matrix and metrics on the held-out test set (`fig8_final_confusion_matrix.png`)

## Reports

- `Capstone_Report.docx` — full report
- `Capstone_Presentation.pptx` — slide deck
- `Findings.docx` / `Findings(1)Draft.pdf` — findings write-up

## Data

- `online_shoppers_intention.csv` — raw dataset (12,330 sessions, 18 features)
- `feature_names.txt` — column names after preprocessing
- `summary_statistics.csv` — descriptive stats
- `*.npy` — cached preprocessed arrays
