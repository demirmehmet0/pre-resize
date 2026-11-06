# [Package Name]

> One-sentence summary of what this package does (e.g., "Rotates an image by a specified angle.")

**Category:** Utility / Capsule / Classical Computer Vision / Preprocessing / Auxiliary / Sources / Widget

**Status:** Stable / Beta / Experimental

**Last Updated:** DD.MM.YYYY

---

## 1. Overview

Describe in 2–3 sentences/paragraphs what this package does, what problem it solves, and typical use cases. Mention when a user should choose this package over a similar one, if relevant.

**Typical use cases:**

- [Use case 1]
- [Use case 2]
- [Use case 3]

---

## 2. Inputs

| Field Name | Kind/Type | Required | Default | Description |
|---|---|---|---|---|
| `[inputFieldName]` | `[Image / string / number / list / object ...]` | Yes/No | `[default or —]` | [What this input represents] |

> Derived from the package `Inputs` / `Input` classes. A field that accepts a single object or a list is shown explicitly.

---

## 3. Configuration Parameters

| Parameter | Type | Field Type (UI control) | Allowed Values / Range | Default | Description |
|---|---|---|---|---|---|
| `[ParamName]` | `[number/bool/string/object]` | `[textInput/dropdownlist/...]` | `[range or options]` | `[default]` | [What this parameter controls, and how it affects behavior] |

> Derived from the package `Configs` classes, including validation bounds and dropdown option labels where present. `ConfigExecutor` is not included.

---

## 4. Outputs

| Field Name | Kind/Type | Description |
|---|---|---|
| `[outputFieldName]` | `[Image / string / number / list / object ...]` | [What this output represents] |

> Derived from the package `Outputs` classes.

---

## 5. Use Case Examples

**Use case 1: [Short title]**

[Describe the scenario — what pipeline is being built, what package(s) come before this one and provide its input, what this package does in that context, and what package(s) come after it to consume its output.]

**Use case 2: [Short title]**

[Same structure as above, for a different context.]

**Use case 3: [Short title, optional]**

[Same structure as above, for a different context.]

---

## 6. Limitations and Notes

- [Known constraints, e.g. value ranges, unsupported formats, size limits]
- [Performance notes, e.g. GPU requirement, expected latency]
- [Common pitfalls or things to watch out for]

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
