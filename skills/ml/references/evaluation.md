# Evaluation Under Distribution Shift

## Define the Question First
*   **Deployment target:** Before splitting, write down what the model will face: same sites in future years, new sites, a new region, new species. The test split must mirror it.
*   **Three splits:** Train (fit), validation (selection, thresholds, early stopping), test (touched once, at the end).
*   **Frozen splits:** Save split membership (sample or group IDs) to a versioned file. Do not regenerate splits from a seed on every run.

## Splits
*   **Group splits:** When samples are correlated, split by group with `GroupKFold` / `GroupShuffleSplit`. Groups: trap or camera, trap-night, station, scene, individual, observer.
*   **Temporal:** Train on the past, test on the future, with a gap at least as long as the autocorrelation.
*   **Spatial:** Geographically separated blocks, with a buffer at least as wide as the spatial autocorrelation range. Overlapping chips or tiles never straddle a split boundary.
*   **ID vs OOD:** Report in-distribution and out-of-distribution test sets separately. Never average them into one number.
*   **Duplicates:** Check for exact and near-duplicates across splits (image hashes, embedding similarity). Aggregated sources such as GBIF and iNaturalist contain re-uploads.

## Baselines
*   **Always include a trivial one:** Majority or prior class, climatology, persistence, bicubic interpolation (downscaling), linear probe on frozen features.
*   **Re-run, don't copy:** Re-run published baselines on your exact splits. Numbers from another paper's split are not comparable.
*   **Equal tuning budget:** Same number of trials and compute for every method, logged.

## Seeds and Statistics
*   **Seeds:** At least 3 (5 when differences are small). Vary init and data order; use the same seeds for every method.
*   **Uncertainty:** Report mean ± std across seeds, and/or a bootstrap 95% CI over test samples. With grouped data, resample groups, not samples.
*   **Honest conclusions:** If intervals overlap, report "no clear difference".

## Metrics
*   **Long-tailed classification:** Macro-F1, per-class recall, balanced accuracy, top-k. Report head and tail classes separately. Accuracy only alongside these.
*   **Calibration:** ECE and a reliability diagram whenever outputs are used as probabilities or thresholded. Fit temperature scaling on validation.
*   **Thresholds:** Chosen on validation, reported with the result.
*   **Physical fields:** RMSE plus bias, extremes (upper quantiles), power spectra for downscaling and super-resolution, CRPS for probabilistic outputs, rate of physical constraint violations.

## Open-Set and OOD Detection
*   **Unknowns exist:** Deployed models meet unseen species and conditions. Hold out classes to evaluate this.
*   **Metrics:** AUROC known vs unknown, FPR at 95% TPR, accuracy vs coverage curve when the model can abstain.
*   **Baselines first:** Max softmax probability and energy score before anything fancier.

## Error Analysis
*   **Break down results:** Per class, per site or region, per time period. Inspect worst predictions and top confusions.
*   **Data bugs:** If error analysis reveals a data problem, fix the data and re-run every method, not only yours.
