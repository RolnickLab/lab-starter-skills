---
name: geospatial
description: Vector/raster processing, CRS handling, satellite imagery and sensor selection, remote sensing preprocessing, geospatial ML, and scalable geospatial pipelines (geopandas, rasterio, xarray, STAC).
---

# Geospatial & Remote Sensing

## 1. Core Philosophy
- **CRS is Law:** Never assume a coordinate system. Explicitly check, define, and transform it.
- **Lazy Evaluation:** Geospatial data is massive. Prefer lazy loading (Dask, windowed reads) over eager loading.
- **Right Data Model:** Don't rasterize vectors or vectorize rasters unnecessarily.
- **Fit the Sensor to the Phenomenon:** Match spatial, temporal and spectral resolution to the target, and understand the sensor's physics before analyzing its data.

## 2. Engineering Preferences
- **Vector Data:** Prefer GeoParquet over Shapefiles. Use vectorized `geopandas` methods and spatial indexes.
- **Raster Data:** Output Cloud Optimized GeoTIFF (COG). Use windowed reading for rasters > 100MB to avoid OOM.
- **Projections:** Never compute distance/area in a geographic CRS (WGS84); project first (`gdf.estimate_utm_crs()` for local work) or use geodesic methods. Details: `crs.md`.
- **Metadata:** When writing rasters, always copy or define `src.profile` and `transform`.
- **Sensor Selection:** Defaults: Vegetation → Sentinel-2 Red Edge; Deformation/Clouds → Sentinel-1 SAR; Biomass → LiDAR or L/P-band SAR; High-res Infrastructure → Maxar/Planet. Specs: `sensors.md`.
- **Preprocessing:** Prefer L2A Surface Reflectance over L1C TOA. Always mask clouds and shadows. Apply product scale/offset before computing indices (`processing.md`).
- **Machine Learning:** Tile/chip large rasters. Use spatial cross-validation to prevent data leakage. Use IoU/F1-score over global accuracy for imbalanced classes.

## 3. Forbidden Patterns
- ❌ **Eager Loading Massive Data:** Never load multi-GB rasters fully into RAM.
- ❌ **Loops over Geometries:** Iterating over vector rows is slow; use vectorized operations.
- ❌ **Writing Shapefiles:** Use GeoParquet or GeoPackage instead.
- ❌ **Ignoring CRS:** Performing spatial analysis without aligning and verifying CRS.
- ❌ **Random Spatial Splits:** Never use random train/test splits on spatial data; use spatial block splitting.
- ❌ **Using TOA for Multi-temporal Analysis:** Always use Surface Reflectance for time-series comparisons.

## 4. Deep-Dive References
- `crs.md`: CRS handling, EPSG, axis order, area/distance
- `raster.md`: I/O, COG, resampling, nodata, stacking
- `vector.md`: Formats, validity, spatial ops, large data
- `stack.md`: Library choices
- `sensors.md`: Sensor specs (Landsat, Sentinel, SAR, LiDAR, hyperspectral)
- `processing.md`: Surface reflectance, scale factors, indices, cloud masking
- `applications.md`: Application → data → method lookup
- `ml.md`: Chipping, pretrained models, spatial CV, augmentation
