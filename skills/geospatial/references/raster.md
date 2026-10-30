# Raster & Imagery

## I/O Strategy
- **Size it decompressed:** `width * height * count * dtype bytes`, not file size. A 100MB compressed COG can expand to several GB.
- **Under ~10-20% of available memory** (on SLURM, the job's `--mem`): `rasterio.open().read()` is fine. Float casts and NumPy temporaries push peak use to 5-10x the raw array. Unsure: measure peak RSS on one scene (`/usr/bin/time -v`, `seff`).
- **Above:** **MANDATORY** windowed reading (`rasterio.windows`) or `rioxarray.open_rasterio(..., chunks=...)` with Dask.

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
- Integer rasters need a sentinel outside the dtype's valid data range (`0` is valid data in many products; `-9999` does not fit `uint8`/`uint16`). Record it in the profile's `nodata`. Float rasters use `NaN`.
- Mask nodata before resampling, or fill values bleed into valid pixels.

## Stacking & Alignment
- Before stacking, layers must share `crs`, `transform`, `width`, `height`. Use `rioxarray`'s `reproject_match()`.
- Use VRTs (`gdalbuildvrt`) to mosaic or stack files without duplicating data.
