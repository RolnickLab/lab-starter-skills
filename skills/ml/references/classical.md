# Classical Machine Learning (Tabular)

## Data Leakage Prevention
*   **The Golden Rule:** Transformations must be learned ONLY from the training set.
*   **Pipelines:** **MANDATORY**. Use `sklearn.pipeline.Pipeline`.
    *   *Bad:* `scaler.fit_transform(X); X_train, X_test = split(X)` (Leakage!)
    *   *Good:* `pipe = Pipeline([('scaler', StandardScaler()), ('clf', Model())]); pipe.fit(X_train, y_train)`
*   **Cross-Validation:**
    *   **IID Data:** Stratified K-Fold (maintains class distribution).
    *   **Time-Series:** `TimeSeriesSplit`. **NEVER** use K-Fold on time-series; it leaks the future into the past.
    *   **Spatial:** Spatial K-Fold (prevent spatial autocorrelation leakage).

## Evaluation
*   **Imbalanced Data:**
    *   **Metric:** Accuracy is useless. Use **F1-Score**, **Precision-Recall AUC**, or **Balanced Accuracy**.
    *   **Calibration:** Check `calibration_curve` if you need probability outputs (e.g., fraud risk).
*   **Feature Importance:**
    *   **Tree Models:** Use SHAP (SHapley Additive exPlanations) values instead of generic "gain". It is more theoretically sound.
    *   **Permutation Importance:** Model-agnostic way to measure feature value.

## Formats
*   **Data:** **Parquet**. It preserves schema (int vs float) and compresses well. CSVs lose type information.
*   **Models:** **ONNX** or **Treelite**. Decouples the model from the Python runtime (useful for C++/Go deployment).
