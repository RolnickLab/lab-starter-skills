# Domain Pitfalls

Domain-specific traps only. Splits, metrics and statistics: `evaluation.md`.

## Biodiversity Monitoring (Camera Traps, Insect Traps)
*   **Train/deploy gap:** Curated GBIF/iNaturalist images differ from trap images (blur, angle, lighting, background). Validate on labelled deployment images, never only on a held-out slice of the training source.
*   **Pipelines:** Detect, crop, classify. Evaluate each stage and the end-to-end result; detector misses cap what the classifier can recover.
*   **Taxonomy:** Pin the taxonomy version (e.g. GBIF backbone keys), resolve synonyms, and allow a coarser rank (genus, family) when species-level confidence is low.
*   **Regional species lists:** Restricting outputs to locally plausible species helps, but hides range shifts and novel species. Pair with open-set detection.
*   **Counts:** Consecutive frames show the same individual. Track or deduplicate before reporting abundance.

## Bioacoustics
*   **Spectrogram parameters:** Sample rate, window, hop and mel bins belong in the config and the model card. Resample all audio the same way.
*   **Baseline:** Embeddings from a pretrained model (Perch, BirdNET) plus a linear probe.
*   **Splits:** By recorder or site and date; background noise is site-specific.

## Species Distribution Modelling
*   **Absence is not observed:** With presence-only data, the pseudo-absence or background choice drives results. Report it. Missing from an incomplete checklist does not mean absent.
*   **Sampling bias:** Citizen-science effort follows roads, cities and popular spots. Correct for it (target-group background, effort covariates) or results map observers, not species.
*   **Covariates:** Match environmental covariates to the observation period. Spatial autocorrelation inflates AUC under random splits.

## Climate and Scientific ML
*   **Physical constraints:** Hard (architecture, e.g. downscaled mean equals the coarse value) or soft (loss penalty). Report the violation rate either way.
*   **Units and calendars:** Check units (K vs °C, kg m⁻² s⁻¹ vs mm/day) and calendars (`noleap`, `360_day` via `cftime`) when mixing models or datasets.
*   **Skewed variables:** Precipitation is zero-inflated and heavy-tailed; transform it and evaluate extremes separately.
*   **Grids:** Lat-lon cells are not equal area: weight losses and metrics by `cos(lat)`. On global grids longitude wraps: use circular padding (not on regional domains).
*   **Shift is the task:** Split by years and, for transfer, by region. For emulators, hold out whole scenarios (e.g. an SSP).
*   **Storage:** Chunk zarr along the axis the training loop reads.

## Remote Sensing
*   **Chipping:** 256 or 512 px chips (TorchGeo samplers or rasterio windows). Overlapping chips never straddle a split boundary.
*   **Normalization:** Per-band stats from the training set or published sensor stats, computed on reflectance. Never ImageNet RGB stats for multispectral input.
*   **Start pretrained:** Fine-tune a remote sensing backbone (TorchGeo weights, SSL4EO) or a foundation model (Prithvi-EO-2.0, Clay, DOFA) before training from scratch.
*   **Match pretraining inputs:** Bands, resolution (GSD), normalization and sequence length. Mismatches degrade results silently.
*   **Fair comparison:** Linear probe, fine-tune and from-scratch at the same budget, with label-efficiency curves (e.g. 1%, 10%, 100% of labels).
*   **Overlap:** Check geographic and temporal overlap between the pretraining corpus and the evaluation set.
*   **Architectures:** U-Net or DeepLabV3+ (`segmentation_models_pytorch`) for segmentation; YOLO or Faster R-CNN for detection (rotated boxes for ships, planes); Siamese encoders or bi-temporal transformers for change detection.
*   **Class imbalance:** Weighted, focal or Dice loss, or oversampling. Report per-class IoU or F1.
*   **Augmentation:** Flips and 90° rotations are safe for nadir imagery. Add spectral jitter and CutMix cautiously when outputs are physical quantities.
*   **Fusion and synthetic data:** Sentinel-1 + Sentinel-2 helps in cloudy regions. Validate synthetic data (cloud removal, rare events) on real data only.

## GNNs for Materials and Molecules
*   **Symmetry tests:** Unit-test invariance and equivariance: rotate, translate and permute inputs, check outputs transform as expected.
*   **Splits:** Use the benchmark's OOD splits (e.g. OC20 ID/OOD); random structure splits overstate generalization.
