# Classical Machine Learning (Tabular)

## Data Leakage Prevention
*   **The Golden Rule:** Transformations are learned ONLY from the training set.
*   **Pipelines:** **MANDATORY**. Use `sklearn.pipeline.Pipeline`, so preprocessing is refit inside every CV fold.
    *   *Bad:* `scaler.fit_transform(X); X_train, X_test = split(X)` (Leakage!)
    *   *Good:* `pipe = Pipeline([('scaler', StandardScaler()), ('clf', Model())]); pipe.fit(X_train, y_train)`
*   **Inside the pipeline too:** Imputation, target encoding, feature selection, resampling (`imblearn.pipeline.Pipeline` for SMOTE and similar).

## Cross-Validation
*   **IID data:** `StratifiedKFold`.
*   **Grouped data:** `GroupKFold` or `StratifiedGroupKFold` (sites, individuals, stations). See `evaluation.md`.
*   **Time series:** `TimeSeriesSplit` with `gap`. **NEVER** shuffled K-Fold; it leaks the future into the past.
*   **Spatial:** Geographic block splits with a buffer at least as wide as the autocorrelation range. See `evaluation.md`.
*   **Tuning:** Nested CV, or tune with CV on the training set and evaluate once on a held-out test set.

## Models
*   **Order:** Linear or logistic regression, then random forest, then gradient boosting (`LightGBM` / `XGBoost`). Keep the simpler model unless the gain holds across folds.

## Evaluation
*   **Imbalanced data:** PR-AUC, macro-F1, balanced accuracy. Accuracy alone is misleading. See `evaluation.md`.
*   **Calibration:** Check `calibration_curve`; fix with `CalibratedClassifierCV` when probabilities are used downstream.
*   **Feature importance:** SHAP for tree models; permutation importance on held-out data. Correlated features split importance between them, so group or drop them before interpreting.

## Formats
*   **Data:** **Parquet**. Preserves schema (int vs float) and compresses well. CSVs lose type information.
*   **Models:** `joblib` / `pickle` files execute code on load: only load files you created. For partner handoff, export to ONNX (`skl2onnx`, `onnxmltools`). See `operationalization.md`.
