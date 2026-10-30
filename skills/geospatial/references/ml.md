# Machine Learning in Remote Sensing

## Data Preparation
- **Chipping:** Tile into 256 or 512px chips (TorchGeo samplers, or rasterio windows).
- **Inference:** Overlapping tiles with blended or center-cropped predictions to avoid edge artifacts.
- **Normalization:** Per-band stats from the training set or published sensor stats, computed on reflectance. Never ImageNet RGB stats for multispectral input.

## Models
- **Start pretrained:** Fine-tune a remote sensing backbone (TorchGeo weights, SSL4EO) or a geospatial foundation model (Prithvi-EO-2.0, Clay, DOFA) before training from scratch.
- **Segmentation:** U-Net, DeepLabV3+ (`segmentation_models_pytorch`).
- **Detection:** YOLO, Faster R-CNN; rotated boxes for ships/planes.
- **Change detection:** Siamese encoders, bi-temporal transformers.

## Evaluation and Leakage
- **Spatial folds:** Geographically separated train/val/test blocks, with a buffer at least as wide as the spatial autocorrelation range.
- **Overlapping chips** must never straddle a split boundary.
- **Class imbalance:** Weighted or focal/Dice loss, or oversampling; report per-class IoU/F1.
- **Multi-modal fusion:** Sentinel-1 + Sentinel-2 helps in cloudy regions.

## Augmentation
- Flips and 90° rotations are safe for nadir imagery. Add spectral jitter and CutMix cautiously when outputs are physical quantities.
- Synthetic data (GAN/diffusion cloud removal, rare events): validate on real data only.
