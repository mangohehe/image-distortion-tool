# Config Fidelity Design Principles

## Core Principle: Respect User Configuration

The Image Distortion Tool applies transforms **exactly as specified** in the user's configuration. The platform does not modify, "fix", or "improve" the output beyond what the config requests.

## What We DO

### ✅ Apply Transforms Faithfully
- Load transform parameters exactly as specified in JSON
- Apply transforms in the exact order provided
- Save output in whatever format/range the transforms produce
- Preserve all parameter values without modification

### ✅ Validation and Error Reporting
- Validate that transforms exist in Albumentations library
- Validate that transform parameters can be instantiated
- **Report errors clearly with config details**
- **Do not auto-fix or modify config**
- If Albumentations rejects parameters, report the exact error to user
- Location: `pipeline_manager.py:113-159` in `validate()` and `build_albumentations_pipeline()`

## What We DON'T DO

### ❌ Do Not Modify Output
- **No denormalization** of normalized images
- **No clipping** of pixel values
- **No color space corrections**
- **No quality adjustments**

### ❌ Do Not Filter Transforms
- Do not skip transforms based on "reasonableness"
- Do not remove transforms like `Normalize` even if they produce unusual output
- Do not reorder transforms

### ❌ Do Not Change Parameters
- Do not adjust parameter ranges
- Do not substitute "better" values
- Do not add default parameters beyond what Albumentations requires

## Responsibility Model

| Aspect | Platform Responsibility | User Responsibility |
|--------|------------------------|---------------------|
| **Transform Execution** | Apply exactly as configured | Provide correct config |
| **Output Format** | Save what transforms produce | Ensure transforms produce desired output |
| **Normalize Transform** | Apply if in config | Remove if not wanted for saved images |
| **Parameter Values** | Use exact values provided | Provide valid parameter ranges |
| **Error Handling** | Report errors clearly | Fix config based on errors |

## Common User Errors (Not Platform Issues)

### Issue: Black Output Images
- **Cause**: Config includes `Normalize` transform
- **Why it happens**: Normalize converts [0, 255] to ~[-2, 2] range for neural network input
- **Who fixes it**: User removes `Normalize` from config
- **Platform's role**: Apply Normalize faithfully if present

### Issue: OpenCV/Albumentations Parameter Type Errors
- **Cause**: Config has parameters in format incompatible with Albumentations (e.g., list instead of tuple)
- **Example**: `blur_limit: [3, 9]` when Albumentations expects tuple
- **Why it happens**: JSON format only supports lists, not tuples; or config was created for different library version
- **Who fixes it**: User adjusts config or uses Albumentations-compatible format
- **Platform's role**: Pass parameters exactly as specified; report error if Albumentations rejects them
- **Error message**: Platform shows the exact parameters and Albumentations error message

## Design Verification Checklist

✅ **Pipeline Import** ([pipeline_manager.py:196-217](src/components/pipeline_manager.py#L196-L217))
- Loads params exactly as specified
- No modification during import
- Stores values exactly as they appear in JSON
- Lists stay as lists, integers stay as integers

✅ **Pipeline Build** ([pipeline_manager.py:219-247](src/components/pipeline_manager.py#L219-L247))
- Passes parameters exactly as stored in config
- **No conversions, no modifications**
- If Albumentations fails, raises clear error with config details
- User responsible for fixing config

✅ **Batch Processing** ([batch_processor.py:241-248](src/components/batch_processor.py#L241-L248))
- No denormalization
- No value clipping
- No output modification
- Saves exactly what transforms produce

✅ **Validation** ([pipeline_manager.py:113-159](src/components/pipeline_manager.py#L113-L159))
- Tests transform instantiation
- Reports errors with details
- **Does not auto-fix anything**

## Philosophy

> **"The platform is a faithful executor, not a smart assistant."**

We trust users to know what transforms they need. If the config produces unexpected results (like black images from Normalize), that's feedback for the user to adjust their config, not for the platform to silently "fix".

## Exception: Display Preview Only

The **only** acceptable modification is for **display purposes only** in the UI preview:
- Adding `clamp=True` to Streamlit image display to handle normalized images
- This affects **preview only**, not saved output
- Location: `config_page.py:598-600`

This is acceptable because:
1. It only affects UI rendering
2. Saved files remain unmodified
3. It prevents UI crashes from displaying float32 images
