# Raster & Imagery

## I/O Strategy
- **Small (<100MB):** `rasterio.open().read()` in memory is fine.
- **Large (>100MB):** **MANDATORY** windowed reading (`rasterio.windows`) or `rioxarray.open_rasterio(..., chunks=...)` with Dask.

## Cloud Optimized GeoTIFF (COG)
- **Create with the GDAL COG driver** (`driver="COG"` in rasterio, `gdal_translate -of COG`, or `rio cogeo create`). A tiled GTiff plus `add_overviews()` afterwards is **not** a valid COG (overviews end up after the data).
- Compression: `deflate` or `zstd` with `predictor=2` (integers) / `predictor=3` (floats); `lzw` for old readers.
- Validate: `rio cogeo validate`.
- COGs stream from S3/GCS via HTTP range requests; read only the windows needed.

## Resampling & Reprojection
- **Categorical data (land cover, masks):** MUST use `nearest` (or `mode` when downsampling).
- **Continuous data (elevation, reflectance):** `bilinear` or `cubic`; `average` when downsampling.
- Always pass `resampling` explicitly to `reproject()`; the default is `nearest`.

## Nodata
- Always check `src.nodata`; it may be unset even when fill values exist.
- Mask on read: `rasterio` `masked=True`, or `rioxarray.open_rasterio(..., masked=True)`.
- Integer rasters need a sentinel value (e.g. 0, -9999); float rasters use `NaN`.
- Mask nodata before resampling, or fill values bleed into valid pixels.

## Stacking & Alignment
- Before stacking, layers must share `crs`, `transform`, `width`, `height`. Use `rioxarray`'s `reproject_match()`.
- Use VRTs (`gdalbuildvrt`) to mosaic or stack files without duplicating data.
