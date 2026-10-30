# Remote Sensing Preprocessing

## Surface Reflectance
- Use provider Level-2 products (Sentinel-2 L2A, Landsat Collection 2 Level-2, HLS) rather than running atmospheric correction yourself. Sen2Cor (Sentinel-2), LaSRC (Landsat 8-9), LEDAPS (Landsat 4-7) or Py6S only when no L2 product fits.

## Scale Factors (common silent bug)
- **Sentinel-2 L2A, processing baseline >= 04.00 (Jan 2022+):** reflectance = (DN + BOA_ADD_OFFSET) / 10000, offset is -1000. Mixing pre/post-2022 scenes without the offset breaks time series.
- **Landsat C2 L2 SR:** reflectance = DN × 0.0000275 − 0.2. Thermal ST: K = DN × 0.00341802 + 149.0.
- Read scale/offset from metadata when available instead of hardcoding.

## Spectral Indices
Sentinel-2 bands: Green B3, Red B4, Red Edge B5, NIR B8, SWIR1 B11, SWIR2 B12.
- `NDVI = (NIR - Red) / (NIR + Red)`; EVI saturates less in dense canopy; NDRE uses Red Edge.
- `NDWI = (Green - NIR) / (Green + NIR)`; `MNDWI = (Green - SWIR1) / (Green + SWIR1)` handles built-up areas better.
- `NBR = (NIR - SWIR2) / (NIR + SWIR2)`; dNBR for burn severity.
- Compute on reflectance (after scale/offset), as float, with nodata masked.

## Cloud and Shadow Masking
- **Sentinel-2:** SCL band from L2A as baseline; s2cloudless or Cloud Score+ for better accuracy.
- **Landsat:** QA_PIXEL bit flags (CFMask).
- Dilate masks by a few pixels to catch thin cloud edges and shadows.
- **Compositing:** Median or medoid over a time window for cloud-free mosaics.

## Resolution Enhancement
- **Pan-sharpening:** Fuse pan with multispectral (Landsat 15m pan + 30m MS). Visual use; alters spectral values.
- **Super-resolution:** Model-generated detail is a prediction with error, not measured signal. Validate it against higher-resolution reference data before quantitative use.
