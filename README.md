# Resize

> Brings an image to a target width and height: stretched, fitted inside, fitted with padding, or filled and cropped from the centre.

**Category:** Preprocessing

**Status:** Beta

**Last Updated:** 06.11.2026

---

## 1. Overview

Resize sets an image to a fixed `Width` x `Height`. The task decides what happens to the aspect ratio: `Stretch` ignores it, `FitWithin` keeps it and leaves the output smaller on one side, `Letterbox` keeps it and pads the rest with a colour, `CenterCrop` keeps it and cuts what overflows. Choose it over Scaling when the target is a fixed size rather than a percentage of the original.

**Typical use cases:**

- Preparing a dataset version for training at a fixed input size (dataset version "Resize" step).
- Giving a model the same input size in a deployed flow as it was trained with.
- Producing uniform thumbnails for a screen or dashboard.

---

## 2. Inputs

| Field Name | Kind/Type | Required | Default | Description |
|---|---|---|---|---|
| `inputImage` | `Image` or list of `Image` | Yes | — | Frame to resize |

> Derived from the package `Inputs` / `Input` classes. A field that accepts a single object or a list is shown explicitly.

---

## 3. Configuration Parameters

| Parameter | Type | Field Type (UI control) | Allowed Values / Range | Default | Description |
|---|---|---|---|---|---|
| `Width` | number | textInput | 1–8192 | 640 | Target width in pixels |
| `Height` | number | textInput | 1–8192 | 640 | Target height in pixels |
| `PadColor` | string | textInput | `#RRGGBB` | `#000000` | Padding colour (Letterbox task only) |

Tasks: `Stretch` (Width, Height), `FitWithin` (Width, Height), `Letterbox` — shown as "Fit (Padded)" (Width, Height, PadColor), `CenterCrop` — shown as "Fill (Center Crop)" (Width, Height).

> Derived from the package `Configs` classes, including validation bounds and dropdown option labels where present. `ConfigExecutor` is not included.

---

## 4. Outputs

| Field Name | Kind/Type | Description |
|---|---|---|
| `outputImage` | `Image` | The resized frame (stored in Redis; `value` is empty) |

> Derived from the package `Outputs` classes.

---

## 5. Use Case Examples

**Use case 1: Training data at a fixed size**

A dataset version asks for 640x640 with black edges. The augment flow feeds each image through Resize (`Letterbox`, 640, 640, `#000000`) and saves the result; the training archive is built from the saved frames.

**Use case 2: Same input size in production**

A camera source feeds Resize (`Stretch`, 640, 640) before the detector, matching how the model was trained.

---

## 6. Limitations and Notes

- Detections are not carried. Boxes computed on the original frame do not match the resized one. `src/utils/resize.py` returns the transform for each task (`x_new = x * scale_x + offset_x`, same for y) so they can be moved; `CenterCrop` can push boxes partly outside the frame.
- `FitWithin` output can be smaller than the target on one side; use `Letterbox` for an exact size with the ratio kept.
- Shrinking uses `INTER_AREA`, enlarging `INTER_LINEAR`.

---

## 7. Development

**Setup (once per clone):**

```bash
pip install pre-commit
pre-commit install
```

From then on, each commit runs the same checks as CI:

- **Spec check:** `PackageModel.py` and the executors follow the package development specification.
- **Lint and format:** ruff fixes and formats `src/` automatically. Stage the changes and commit again.
- **Commit message:** must follow [Conventional Commits](https://www.conventionalcommits.org).

To run all checks at any time, use `pre-commit run --all-files`.

**Workflow:**

1. Branch off `develop` and open a PR back into `develop`. CI must pass.
2. Write commit messages as `<type>[(scope)]: <description>`, for example `feat: add threshold config` or `fix(executor): handle empty input`. The type sets the next version:

   | Type | Version bump |
   |---|---|
   | `fix`, `perf` | patch |
   | `feat` | minor |
   | `feat!` or a `BREAKING CHANGE:` footer | major |
   | `refactor`, `docs`, `style`, `test`, `build`, `ci`, `chore` | none |

3. Merge `develop` into `main` to release. A release PR is then opened that bumps the version in `setup.py` and updates `CHANGELOG.md`. Merging it creates the tag and the GitHub Release. Don't edit the version yourself.

- Schema: `python apps/export.py` writes `data.json`. Try against a running host: `python apps/client.py`.
