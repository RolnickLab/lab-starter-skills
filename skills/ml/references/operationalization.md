# Operationalization (TRL 6-7)

Goal: a partner can install the model, run it on their own data, integrate it in their pipeline, and know where it fails.
Running the partner's production system is out of scope; handing them something integrable is not.

## Readiness Ladder
| Stage | TRL | Evidence |
| :--- | :--- | :--- |
| **Paper code** | 3-4 | One command reproduces each table from released data and weights. |
| **Reusable** | 5 | Installable package, inference CLI, tests in CI; validated on held-out data matching the deployment setting (e.g. OOD sites or years). |
| **Integrable** | 6 | Validated on the partner's data; stable I/O contract; container. |
| **Piloted** | 7 | Running in the partner's environment on real data, with a feedback loop. |

## Reproducibility
*   **Environment:** Lockfile (`uv.lock`), stated Python, CUDA and driver versions.
*   **Results:** One command per table or figure. Released data and weights get a DOI (Zenodo) or a versioned Hugging Face repo.

## Inference Interface
*   **Separate from training:** An importable `predict` function with no training-only dependencies (tracker, Hydra, Lightning).
*   **Typed contract:** Pydantic models for inputs and outputs. Document units, CRS, dtype, value ranges, band order, expected sensor or product, and class list / taxonomy version.
*   **Validate at the boundary:** Reject wrong shapes, bands, CRS or units with a clear error rather than returning garbage predictions.
*   **One preprocessing path:** Training and inference call the same preprocessing code. Normalization stats ship with the weights.
*   **Batch first:** Partners usually process archives. CLI over a directory, manifest or STAC query; resumable; writes standard formats (COG, GeoParquet, NetCDF, typed CSV). Tiled inference for large rasters: overlapping tiles with blended or center-cropped predictions, to avoid edge artifacts.
*   **Honest outputs:** Include confidence, an abstain or "unknown" option, and the model version in output metadata.
*   **Service only if needed:** A `FastAPI` wrapper is a thin layer over `predict`, built when a partner needs a service, not by default.

## Packaging
*   **Weights:** `safetensors` + config + normalization stats + class list, versioned, never overwritten.
*   **ONNX:** Optional, when the partner's runtime is not Python. Check numerical parity with PyTorch on fixture inputs.
*   **Container:** Multi-stage Docker, non-root user, pinned CUDA base image; a CPU variant if the partner has no GPU. Apptainer for HPC partners.
*   **Licenses:** For code, weights and data. Check upstream data terms (e.g. GBIF records under CC BY-NC).

## Partner Documentation
*   **Model card:** Intended use, training coverage (regions, years, sensors, species), ID and OOD metrics, known failure modes, out-of-scope uses.
*   **Quickstart:** Install, run on the bundled example, see the expected output, in under 10 minutes.
*   **Resources:** Memory and throughput (images/s, km²/h) on stated hardware.

## Validation and Maintenance
*   **Partner data first:** Before handoff, evaluate on a labelled sample from the partner's sites or sensors and report it next to the paper numbers. Expect a drop.
*   **Input drift:** Compare incoming input statistics or embeddings to the training distribution; flag OOD inputs.
*   **Feedback loop:** Partner-flagged errors get labelled, added to the evaluation set, and drive the next versioned release.
*   **CI gates:** CPU tests on small fixtures: I/O schema, preprocessing, and a golden-output test (fixed input, expected predictions within tolerance).
