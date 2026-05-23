# Capstone — KNN on Online Shoppers Purchasing Intention

**Group 14**

**Authors:**
- Rodnee Glen A. Martin
- Renier P. Apal
- Earl Lenser B. Bolansoy

---

## Project Overview

This capstone project applies **K-Nearest Neighbors (KNN)** classification to predict whether an e-commerce session will end in a purchase (i.e., whether the `Revenue` attribute is true or false). The entire machine learning pipeline—encompassing exploratory data analysis (EDA), data preprocessing, stratified dataset splitting, hyperparameter tuning (k-tuning), model training, and comprehensive evaluation—has been built from the ground up. Notably, the KNN classifier and supporting evaluation utilities are implemented completely from scratch utilizing NumPy, demonstrating a deep understanding of the algorithm's inner workings.

**Dataset:** [Online Shoppers Purchasing Intention Dataset (UCI)](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset).

---

## Headline Results

The final model performance was evaluated using a testing set and validated through 5-fold Stratified Cross-Validation.

| Metric        | Test set (k=7) | 5-fold CV (mean ± std)      |
|---------------|----------------|-----------------------------|
| Accuracy      | **0.8767**     | 0.8740 ± 0.0033 |
| Precision     | 0.6974         | 0.6865 ± 0.0235 |
| Recall        | 0.3570         | 0.3417 ± 0.0124 |
| F1 Score      | 0.4722         | 0.4562 ± 0.0149 |

- **Best k by F1 Score:** k = 3 (F1 = 0.4892). We **selected k = 7** (F1 = 0.4722) instead, trading a negligible amount of F1 for substantially higher precision (0.6974 vs 0.5962); see [k_tuning_results.csv](k_tuning_results.csv).
- **Best k by Accuracy:** k = 21 (Favors the majority class)
- **Baseline Comparison:** kNN decisively beats the majority-class baseline (always "no-purchase", 0.0 F1). However, a single-feature rule — predict "purchase" when `PageValues` exceeds the training mean — **outperforms our kNN on F1 (0.6819 vs 0.4722) and recall (0.7428 vs 0.3570)**, losing only on precision. This is one of our key findings; see Key Takeaways and [final_evaluation.py](final_evaluation.py).

---

## Dataset at a Glance

The dataset consists of feature vectors belonging to **12,330** user sessions over a 12-month period.
- **Features:** Originally 17 features + 1 target variable (`Revenue`).
- **Preprocessed Features:** Expanded to **28** features after one-hot encoding categorical variables (`Month`, `VisitorType`).
- **Class Imbalance:** Significant skew towards the negative class (~84.5% no-purchase vs. ~15.5% purchase). This equates to an approximate ratio of 5.46 : 1.

### Data Dictionary

The preprocessed dataset features include:
- **Administrative / Administrative_Duration:** Number of administrative pages visited and total time spent on them.
- **Informational / Informational_Duration:** Number of informational pages visited and total time spent on them.
- **ProductRelated / ProductRelated_Duration:** Number of product-related pages visited and total time spent on them.
- **BounceRates:** Percentage of visitors who enter the site from that page and then leave without triggering any other requests to the analytics server.
- **ExitRates:** Percentage of pageviews on the website that end at that specific page.
- **PageValues:** Average value for a web page that a user visited before completing an e-commerce transaction.
- **SpecialDay:** Closeness of the site visiting time to a specific special day (e.g., Mother’s Day, Valentine's Day) reflecting the probability of a transaction.
- **OperatingSystems, Browser, Region, TrafficType:** Categorical IDs representing the user's environment and traffic source.
- **Weekend:** A binary indicator of whether the session was on a weekend.
- **Month (One-Hot Encoded):** Binary indicators for the months of the year (Aug, Dec, Feb, Jul, June, Mar, May, Nov, Oct, Sep).
- **VisitorType (One-Hot Encoded):** Binary indicators distinguishing between `New_Visitor`, `Returning_Visitor`, and `Other`.
- **Target (`Revenue`):** Binary integer indicating if a purchase was made (1) or not (0).

---

## Repository Layout

```text
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
├── fig9_sample_prediction.png        Worked example: one session classified by its 7 neighbors
│
├── Capstone_Report.docx / .pdf       Full written report
├── Capstone_Presentation.pptx / .pdf Slide deck (editable + exported)
├── Findings.docx                     Detailed findings write-up
└── Findings(1)Draft.pdf              Earlier draft of findings
```

---

## Complete Execution Pipeline

The pipeline is modular. Each script reads/writes `.npy` artifacts, ensuring steps are independently re-runnable.

| # | Script | Inputs | Outputs | Description |
|---|--------|--------|---------|-------------|
| 1 | [`data_inspect.py`](data_inspect.py) | `online_shoppers_intention.csv` | Console output | Basic sanity check, shape analysis, data types, and initial class balance. |
| 2 | [`eda.py`](eda.py) | `online_shoppers_intention.csv` | `fig1`–`fig6` PNGs | Generates visual exploratory data analysis plots to understand distributions and correlations. |
| 3 | [`preprocessing.py`](preprocessing.py) | `online_shoppers_intention.csv` | `X_features.npy`, `y_target.npy`, `feature_names.txt` | Handles one-hot encoding for categorical text variables and converts boolean values to integers. |
| 4 | [`train_test_split.py`](train_test_split.py) | `X_features.npy`, `y_target.npy` | `X_train_scaled.npy`, `X_test_scaled.npy`, `y_train.npy`, `y_test.npy` | Performs a stratified 80/20 train/test split to preserve class imbalance, followed by Z-score standardization. |
| 5 | [`knn_tune_k.py`](knn_tune_k.py) | Scaled train/test arrays | `k_tuning_results.csv`, `fig7_k_tuning.png` | Sweeps hyperparameters to find the optimal 'k' value by recording precision, recall, and F1 scores. |
| 6 | [`knn_model.py`](knn_model.py) | Scaled train/test arrays | `y_pred_k5.npy`, console metrics | Runs the standard model using a baseline k=5 to verify basic predictive capabilities. |
| 7 | [`final_evaluation.py`](final_evaluation.py) | Full feature/target + scaled splits | `fig8_final_confusion_matrix.png` | Evaluates the optimized k=7 model using 5-fold cross-validation and tests against standard baselines. |

---

## In-Depth Methodology

### 1. Preprocessing ([preprocessing.py](preprocessing.py))
- **Categorical Handling:** One-hot encoding was applied to `Month` and `VisitorType`. We retained all dummy variables (no drop-first) for complete representation.
- **Type Conversion:** Binary columns such as `Weekend` and the target `Revenue` were explicitly cast to integers to ensure mathematical compatibility with the NumPy routines.
- **Caching:** Output arrays (`X` and `y`) are saved as `.npy` binaries. This allows downstream scripts to load data instantly without redundant parsing.

### 2. Stratified Train/Test Split ([train_test_split.py](train_test_split.py))
- **Stratification:** A custom stratified 80/20 split algorithm was implemented. Indices for each class were shuffled independently, and exactly 20% of each class was held out for testing. This guarantees the test set accurately mirrors the real-world 84.5% / 15.5% class distribution.
- **Data Standardization (Z-score Scaling):** Features have different scales (e.g., milliseconds vs. percentages). We computed the mean and standard deviation exclusively on the training data. The test data was subsequently scaled using these training parameters, completely preventing data leakage.

### 3. Custom KNN Classifier ([knn_model.py](knn_model.py), [knn_tune_k.py](knn_tune_k.py), [final_evaluation.py](final_evaluation.py))
- **Distance Calculation:** The classifier calculates the Euclidean distance from every test data point to every single training data point.
- **Majority Voting:** The algorithm selects the `k` closest training instances and applies a majority vote to determine the final predicted class.
- **Evaluation Metrics:** We implemented custom logic to compute Confusion Matrix components (True Positives, True Negatives, False Positives, False Negatives). From these, we derived comprehensive metrics: Accuracy, Precision, Recall, F1-Score, and Specificity.

### 4. Hyperparameter Tuning ([knn_tune_k.py](knn_tune_k.py))
- We conducted a systematic sweep over `k` values from 1 to 30.
- Logging the performance across Accuracy, Precision, Recall, and F1 allowed us to visually and quantitatively determine the optimal decision boundary. 
- Results are stored in [k_tuning_results.csv](k_tuning_results.csv) and visualized in [fig7_k_tuning.png](fig7_k_tuning.png).

### 5. Final Evaluation & Baselines ([final_evaluation.py](final_evaluation.py))
- **5-Fold Stratified Cross-Validation:** To validate the robustness of our selected `k = 7`, we implemented a 5-fold CV algorithm. Each fold maintains the exact class balance of the original dataset.
- **Baseline Comparisons:**
  - *Majority-Class Baseline:* Always predicts "no-purchase". Yields high accuracy but 0% recall and an undefined/zero F1-score.
  - *Rule-Based Baseline:* Predicts "purchase" when a session's `PageValues` exceeds the **training mean** (coded as `PageValues > 0` on standardized features). This single-feature heuristic is remarkably strong — it **outperforms the full kNN on F1 and recall** (0.6819 / 0.7428 vs 0.4722 / 0.3570). See Key Takeaways for why.
- The confusion matrix for our optimal test set predictions is visualized in [fig8_final_confusion_matrix.png](fig8_final_confusion_matrix.png).

---

## Getting Started

### Requirements
Ensure you are running an updated Python environment.
- Python 3.9+
- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`

Install all dependencies via pip:

```bash
pip install numpy pandas matplotlib seaborn
```

### Running the Project

To execute the entire project from data inspection to final evaluation, run the following commands sequentially from the repository root:

```bash
python data_inspect.py
python eda.py
python preprocessing.py
python train_test_split.py
python knn_tune_k.py
python knn_model.py
python final_evaluation.py
```

Because intermediate steps are cached as `.npy` binaries, you can safely skip the preprocessing and split scripts (Steps 3 and 4) if you just want to experiment with tuning or evaluation.

> **Runtime Note:** K-Nearest Neighbors prediction is computationally intensive, scaling at $O(n_{train} \times n_{test} \times d)$ for each test phase, as there is no initial "training" phase. On a standard machine, the comprehensive 30-step k-sweep takes roughly 1–2 minutes (about 3–4 seconds per value of `k`). Individual cross-validation folds run in a few seconds each.

---

## Figures and Visualizations

Visualizing the data and model performance was a core component of our project. All generated figures are saved in the repository:

| File | What it shows |
|------|---------------|
| [fig1_class_distribution.png](fig1_class_distribution.png) | The extreme imbalance between purchase and no-purchase sessions. |
| [fig2_correlation_heatmap.png](fig2_correlation_heatmap.png) | Pearson correlations among numeric features, highlighting multicollinearity (e.g., between BounceRates and ExitRates). |
| [fig3_pagevalues_boxplot.png](fig3_pagevalues_boxplot.png) | `PageValues` distribution split by outcome, showing its strong predictive power. |
| [fig4_bouncerates_boxplot.png](fig4_bouncerates_boxplot.png) | `BounceRates` distribution split by outcome, showing buyers tend to have lower bounce rates. |
| [fig5_purchases_by_month.png](fig5_purchases_by_month.png) | Total sessions and conversion rates broken down by month. |
| [fig6_visitor_type.png](fig6_visitor_type.png) | Sessions and conversion rates comparing Returning vs. New Visitors. |
| [fig7_k_tuning.png](fig7_k_tuning.png) | Line plots tracking Accuracy, Precision, Recall, and F1 across `k = 1..30`. |
| [fig8_final_confusion_matrix.png](fig8_final_confusion_matrix.png) | Heatmap of the Test-set confusion matrix for the final deployed model (k=7). |
| [fig9_sample_prediction.png](fig9_sample_prediction.png) | A worked example classifying one new session by its 7 nearest neighbors (5 buyers vs. 2 non-buyers → Purchase), shown on the two most predictive features. |

---

## Project Deliverables

- [Capstone_Report.pdf](Capstone_Report.pdf) / [Capstone_Report.docx](Capstone_Report.docx) — The full written report detailing our approach, literature review, and comprehensive findings.
- [Capstone_Presentation.pptx](Capstone_Presentation.pptx) / [Capstone_Presentation.pdf](Capstone_Presentation.pdf) — Slide deck for the final project defense (editable PowerPoint and exported PDF).
- [Findings.docx](Findings.docx) — An extended, detailed write-up of specific analytical findings.
- [Findings(1)Draft.pdf](Findings(1)Draft.pdf) — Earlier draft version of the findings document.

---

## Key Takeaways & Future Work

- **A Single-Feature Rule Beats Our kNN:** A one-line heuristic — predict "purchase" when `PageValues` exceeds the training mean — scores **F1 0.6819**, beating our full kNN's **0.4722** (and winning on recall, 0.7428 vs 0.3570). The likely cause: kNN spreads its distance calculation across all 28 standardized features — including redundant pairs (BounceRates/ExitRates) and noisy one-hot columns — which *dilutes* the dominant `PageValues` signal instead of amplifying it. kNN's only edge is marginally higher precision (0.6974 vs 0.6303). This is a humbling but instructive result: when one feature carries most of the signal, a distance-based model over many features can underperform a simple threshold.
- **Tuning `k` Manages the Precision/Recall Trade-off:** 
  - Small values of `k` (e.g., k = 1) maximize Recall but yield low Precision (overfitting to individual training points). 
  - Large values of `k` (≥20) maximize Accuracy and Precision, but the model becomes too conservative, causing Recall to collapse. 
  - F1 actually peaks at **k = 3** (0.4892); we selected **k = 7** (F1 0.4722) because it delivers far higher Precision (0.6974 vs 0.5962) at only a marginal F1 cost — the right call for a precision-oriented model.
- **The Challenge of Class Imbalance:** Because only ~15.5% of the data represents actual buyers, the model naturally biases towards "no-purchase". Even at optimal settings, it correctly identifies only ~36% of actual buyers. 
- **Future Enhancements:** Future iterations of this project could address this recall bottleneck by implementing explicit class weighting within the distance metric, applying synthetic data generation (e.g., SMOTE), or moving to a threshold-tuned probabilistic classification model.

---

## Citation

Dataset Source: Sakar, C.O., Polat, S.O., Katircioglu, M. *et al.* "Real-time prediction of online shoppers' purchasing intention using multilayer perceptron and LSTM recurrent neural networks." *Neural Comput & Applic* **31**, 6893–6908 (2019). 

UCI Machine Learning Repository Link: <https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset>
