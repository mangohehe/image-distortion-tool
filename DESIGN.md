# SEM Image Distortion Tool - Product Design Document

**Version:** 1.0  
**Date:** November 11, 2025  
**Status:** Draft for Review  
**Authors:** Product Design Team  

---

## Document Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-11 | Design Team | Initial draft |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Overview](#2-product-overview)
3. [User Research & Personas](#3-user-research--personas)
4. [User Journeys & Flows](#4-user-journeys--flows)
5. [Information Architecture](#5-information-architecture)
6. [Feature Specifications](#6-feature-specifications)
7. [UI/UX Design Guidelines](#7-uiux-design-guidelines)
8. [Technical Architecture](#8-technical-architecture)
9. [Implementation Roadmap](#9-implementation-roadmap)
10. [Success Metrics & KPIs](#10-success-metrics--kpis)
11. [Risk Assessment](#11-risk-assessment)
12. [Appendices](#12-appendices)

---

## 1. Executive Summary

### 1.1 Purpose
This document outlines the design and implementation plan for a SEM Image Distortion Tool built on Albumentations library, specifically designed for semiconductor wafer defect detection workflows.

### 1.2 Problem Statement
Current challenges in SEM wafer defect detection:
- Images from different wafer locations exhibit geometric distortions (field curvature, astigmatism, stage positioning errors)
- Training datasets lack realistic variation, leading to poor model generalization
- Existing augmentation tools lack domain-specific physics-based distortions
- No user-friendly interface for non-technical domain experts to create augmentation pipelines

### 1.3 Solution Overview
A web-based application that provides:
- **Quick Start Mode**: One-click presets for common SEM distortions
- **Custom Pipeline Builder**: Visual drag-and-drop interface for advanced users
- **Batch Processing**: Production-scale augmentation capabilities
- **Export Options**: Python code, configuration files, Docker containers

### 1.4 Key Benefits
- **Time Savings**: Reduce augmentation setup from days to minutes
- **Improved Model Performance**: Physics-based distortions better represent real-world variation
- **Democratization**: Enable domain experts without coding skills to create pipelines
- **Reproducibility**: Version-controlled configurations and seeded randomness

### 1.5 Target Users
- ML Engineers (primary)
- Semiconductor Domain Experts
- Data Scientists
- Production/DevOps Teams

---

## 2. Product Overview

### 2.1 Product Vision
Become the industry-standard tool for semiconductor imaging augmentation, bridging the gap between domain physics and machine learning workflows.

### 2.2 Product Goals
1. **Usability**: 90% of users complete first augmentation within 5 minutes
2. **Performance**: Process 1000 images in < 2 minutes on standard hardware
3. **Adoption**: 100+ active users within 6 months of launch
4. **Integration**: Seamless PyTorch/TensorFlow pipeline integration

### 2.3 Core Features

#### Must Have (MVP)
- Quick Start with 3-5 preset configurations
- Image upload and preview (single image)
- Side-by-side comparison view
- Basic parameter adjustment (strength, probability)
- Python code export
- Batch processing for local folders

#### Should Have (Phase 1)
- Custom pipeline builder (drag-and-drop)
- Full Albumentations transform library
- Grid view (6-9 variations)
- Configuration file export (JSON/YAML)
- Template save/load system
- Real-time metrics display

#### Could Have (Phase 2)
- Cloud storage integration (S3, GCS)
- A/B testing mode for pipeline comparison
- Model impact prediction
- Collaboration features (share pipelines via URL)
- API for programmatic access
- Advanced visualization (heatmaps, distortion fields)

#### Won't Have (Out of Scope)
- Model training capabilities
- Annotation/labeling tools
- Image quality assessment beyond basic metrics
- Video processing

### 2.4 Success Criteria
- **User Satisfaction**: NPS score > 50
- **Task Success Rate**: > 85% for primary workflows
- **Adoption Rate**: 60% of trial users become active users
- **Performance**: < 100ms processing time per 1024x1024 image

---

## 3. User Research & Personas

### 3.1 Primary Personas

#### Persona 1: Alex - ML Engineer
**Demographics:**
- Age: 28-35
- Role: Machine Learning Engineer
- Experience: 3-5 years in computer vision
- Technical Skills: Python (expert), PyTorch/TensorFlow (advanced)

**Goals:**
- Quickly integrate augmentation into training pipeline
- Ensure reproducibility across experiments
- Optimize for training speed

**Pain Points:**
- Writing boilerplate augmentation code is time-consuming
- Difficult to tune parameters without visual feedback
- Hard to explain augmentation choices to domain experts

**Needs:**
- Fast code generation
- Version-controlled configurations
- Performance benchmarks

**Usage Pattern:**
- Uses tool 2-3x per week
- Primarily uses Custom Pipeline Builder
- Exports as Python code for integration

---

#### Persona 2: Dr. Sarah - Semiconductor Domain Expert
**Demographics:**
- Age: 40-55
- Role: Senior Process Engineer
- Experience: 15+ years in semiconductor manufacturing
- Technical Skills: MATLAB (intermediate), Python (beginner)

**Goals:**
- Ensure augmentations reflect real-world SEM artifacts
- Validate that defect features remain detectable
- Collaborate with ML team on data quality

**Pain Points:**
- Limited coding skills prevent direct participation
- Difficult to communicate physics-based requirements to ML engineers
- No easy way to validate augmentation realism

**Needs:**
- Visual, no-code interface
- Physics-based preset options
- Metrics showing feature preservation
- Easy sharing with technical team

**Usage Pattern:**
- Uses tool 1-2x per week
- Primarily uses Quick Start presets
- Focuses on visual validation
- Exports configurations for ML team to implement

---

#### Persona 3: Jamie - Data Scientist
**Demographics:**
- Age: 26-32
- Role: Data Scientist
- Experience: 2-4 years in ML/AI
- Technical Skills: Python (advanced), Statistics (expert)

**Goals:**
- Experiment with different augmentation strategies
- Analyze impact on model performance
- Document findings for team

**Pain Points:**
- Trial-and-error augmentation tuning is tedious
- Difficult to systematically compare strategies
- Hard to measure augmentation quality objectively

**Needs:**
- A/B testing capabilities
- Quantitative metrics
- Experiment tracking
- Statistical validation tools

**Usage Pattern:**
- Uses tool daily during project
- Uses all three modes (Quick Start, Custom, Batch)
- Heavy use of metrics and comparison features

---

#### Persona 4: Chris - DevOps/Production Engineer
**Demographics:**
- Age: 30-40
- Role: MLOps Engineer
- Experience: 5-8 years in DevOps/ML infrastructure
- Technical Skills: Docker (expert), Python (intermediate), CI/CD (expert)

**Goals:**
- Deploy reliable augmentation pipelines
- Monitor processing jobs
- Scale to production workloads

**Pain Points:**
- Inconsistent environments between development and production
- Difficult to monitor long-running batch jobs
- Resource utilization optimization

**Needs:**
- Docker/container support
- Queue management
- Error handling and retry logic
- Resource monitoring

**Usage Pattern:**
- Uses tool for deployment setup
- Primarily uses Batch Processing mode
- Focuses on reliability and monitoring

---

### 3.2 User Research Findings

#### Key Insights from Interviews (n=15)
1. **Time Pressure**: 87% of users cited "lack of time" as biggest barrier to proper augmentation
2. **Technical Gap**: 60% of domain experts feel excluded from augmentation decisions
3. **Validation Challenge**: 73% struggle to validate whether augmentations are "realistic"
4. **Integration Friction**: 80% waste time on boilerplate code for pipeline integration

#### Survey Results (n=45)
- **Preferred Learning Method**: 
  - Visual examples: 62%
  - Documentation: 24%
  - Video tutorials: 14%
- **Most Important Feature**: 
  - Visual preview: 44%
  - Physics-based presets: 28%
  - Fast processing: 18%
  - Easy export: 10%

---

## 4. User Journeys & Flows

### 4.1 Primary User Journeys

#### Journey 1: "Quick Augmentation for Training"
**User:** Alex (ML Engineer)  
**Goal:** Add SEM-realistic augmentation to training pipeline before deadline  
**Context:** Has 1 hour to implement augmentation for model training starting today  

**Journey Steps:**

1. **Discovery** (2 min)
   - Opens tool URL
   - Sees clear value proposition on home page
   - Clicks "Quick Start"

2. **Configuration** (3 min)
   - Reviews 5 preset options with descriptions
   - Selects "Field Curvature" (most common)
   - Uploads sample wafer image via drag-drop
   - Sees instant preview with 6 variations

3. **Validation** (2 min)
   - Checks side-by-side comparison
   - Adjusts strength slider (0.2 → 0.3)
   - Regenerates to see different variations
   - Satisfied with results

4. **Integration** (3 min)
   - Clicks "Export as Python Code"
   - Copies code to clipboard
   - Pastes into training script
   - Tests on batch of images - works!

**Total Time:** 10 minutes  
**Outcome:** Successfully integrated realistic augmentation  
**Satisfaction:** High - much faster than manual implementation  

**Success Metrics:**
- Time to first preview: < 2 minutes
- Time to export: < 10 minutes
- Code works without modification: 95%

---

#### Journey 2: "Validating Augmentation Realism"
**User:** Dr. Sarah (Domain Expert)  
**Goal:** Ensure augmentations accurately represent real SEM artifacts  
**Context:** ML team created pipeline but she wants to validate physics accuracy  

**Journey Steps:**

1. **Access** (1 min)
   - Receives link from ML team
   - Opens configuration in tool
   - Sees loaded pipeline with 4 transforms

2. **Understanding** (3 min)
   - Reviews each transform with tooltips
   - Sees parameters: OpticalDistortion (0.25), GridDistortion (0.3)
   - Uploads her reference SEM images

3. **Comparison** (5 min)
   - Compares augmented vs. real artifacts
   - Notices augmentation is too strong
   - Adjusts OpticalDistortion: 0.25 → 0.15
   - Regenerates multiple samples
   - Matches better now

4. **Feedback** (2 min)
   - Clicks "Save Configuration"
   - Names it "Sarah_Validated_v1"
   - Sends configuration file to ML team
   - Adds notes: "Reduced optical distortion - now matches Sector 3 images"

**Total Time:** 11 minutes  
**Outcome:** Validated and improved pipeline  
**Satisfaction:** High - felt included in process without coding  

**Success Metrics:**
- Can understand pipeline without help: 80%
- Can adjust parameters successfully: 90%
- Can share results with team: 100%

---

#### Journey 3: "Building Custom Pipeline"
**User:** Jamie (Data Scientist)  
**Goal:** Create specialized pipeline combining 3 distortion types  
**Context:** Experimenting with augmentation strategies for research paper  

**Journey Steps:**

1. **Exploration** (5 min)
   - Opens Custom Pipeline Builder
   - Browses transform library
   - Searches for "elastic" - finds ElasticTransform
   - Reads documentation inline

2. **Construction** (8 min)
   - Drags OpticalDistortion to canvas
   - Drags GridDistortion below it
   - Drags custom FieldCurvature transform
   - Sets sequential composition
   - Configures each transform:
     - OpticalDistortion: strength 0.2, p=0.5
     - GridDistortion: steps 5, strength 0.3, p=0.4
     - FieldCurvature: strength 20, p=0.6

3. **Testing** (10 min)
   - Uploads 10 test images
   - Clicks "Test Pipeline"
   - Reviews grid of results
   - Checks metrics: 89% feature preservation
   - Adjusts FieldCurvature: 20 → 15
   - Retests - 92% preservation (better)

4. **Documentation** (5 min)
   - Saves pipeline as "Jamie_Experiment_A"
   - Exports config as YAML
   - Downloads code for notebook
   - Notes performance: 12ms per image

5. **Iteration** (continuing)
   - Creates variant "Experiment_B"
   - Plans A/B test for next week

**Total Time:** 28 minutes (initial), ongoing iterations  
**Outcome:** Custom validated pipeline ready for experiments  
**Satisfaction:** High - saved hours vs. coding from scratch  

**Success Metrics:**
- Can build pipeline without documentation: 70%
- Can test and iterate within session: 85%
- Saves pipeline for reuse: 90%

---

#### Journey 4: "Production Batch Processing"
**User:** Chris (DevOps Engineer)  
**Goal:** Process 50,000 wafer images for training dataset  
**Context:** ML team provided validated pipeline, need to scale to full dataset  

**Journey Steps:**

1. **Setup** (5 min)
   - Opens Batch Processing mode
   - Loads "Sarah_Validated_v1" configuration
   - Selects input: /data/wafer_images/ (50,247 images)
   - Configures output: /data/augmented/

2. **Configuration** (3 min)
   - Sets augmentations per image: 3x
   - Enables "keep originals"
   - Reviews estimates:
     - Output: 150,741 images
     - Time: ~4.2 hours
     - Disk: 82 GB
   - Sets notification email

3. **Validation** (5 min)
   - Clicks "Test on Subset"
   - Processes first 100 images
   - Checks output quality
   - Validates file naming: wafer001.jpg → wafer001_aug_0.jpg, wafer001_aug_1.jpg...
   - Confirms looks good

4. **Execution** (automatic)
   - Clicks "Start Processing"
   - Job added to queue
   - Goes back to other work
   - Receives progress notifications: 25%, 50%, 75%
   - Email notification on completion

5. **Verification** (10 min)
   - Returns after 4 hours
   - Reviews processing log
   - Spot checks output samples
   - Validates counts match expected
   - Runs checksum verification

**Total Time:** 23 minutes active, 4 hours processing  
**Outcome:** Successfully augmented full dataset  
**Satisfaction:** High - reliable, monitored, predictable  

**Success Metrics:**
- Successful completion rate: > 99%
- Processing time predictability: within 10% of estimate
- Error recovery without intervention: 95%

---

### 4.2 Detailed User Flows

#### Flow Diagram 1: Quick Start Flow

```
┌─────────────────┐
│   Home Page     │
│  - 3 Entry      │
│    Points       │
└────────┬────────┘
         │
         │ Click "Quick Start"
         ▼
┌─────────────────┐
│ Preset          │
│ Selection       │
│ - 5 Options     │
│ - Descriptions  │
└────────┬────────┘
         │
         │ Select Preset
         ▼
┌─────────────────┐
│ Preview &       │
│ Adjust          │◄────────┐
│ - Upload Image  │         │
│ - Parameters    │         │
│ - View Results  │         │
└────────┬────────┘         │
         │                  │
         │ Adjust           │
         │ Parameters?      │
         ├──────────────────┘
         │ No
         │
         │ Satisfied?
         ▼
┌─────────────────┐
│ Export          │
│ - Python Code   │
│ - Config File   │
│ - Batch Job     │
└─────────────────┘
```

#### Flow Diagram 2: Custom Pipeline Flow

```
┌─────────────────┐
│   Home Page     │
└────────┬────────┘
         │
         │ Click "Custom Pipeline"
         ▼
┌─────────────────────────────────────┐
│ Pipeline Builder                    │
│                                     │
│ ┌────────────┐  ┌────────────────┐│
│ │ Transform  │  │   Pipeline     ││
│ │ Library    │  │   Canvas       ││
│ │            │  │   (Empty)      ││
│ │ • Optical  │  │                ││
│ │ • Grid     │  │                ││
│ │ • Elastic  │  │                ││
│ │ • Custom   │  │                ││
│ └────────────┘  └────────────────┘│
└────────┬────────────────────────────┘
         │
         │ Drag Transform to Canvas
         ▼
┌─────────────────────────────────────┐
│ Pipeline with Transforms            │
│                                     │
│  1. OpticalDistortion               │
│     ├─ Strength: [slider]           │
│     └─ Probability: 0.5             │
│                                     │
│  2. GridDistortion                  │
│     ├─ Steps: 5                     │
│     └─ Strength: [slider]           │
└────────┬────────────────────────────┘
         │
         │ Click "Test Pipeline"
         ▼
┌─────────────────┐
│ Test Results    │
│ - Grid view     │
│ - Metrics       │
│ - Performance   │
└────────┬────────┘
         │
         │ Iterate or Save?
         ├─────────► Save Template
         │
         │ Export
         ▼
┌─────────────────┐
│ Export Options  │
└─────────────────┘
```

#### Flow Diagram 3: Batch Processing Flow

```
┌─────────────────┐
│   Home Page     │
└────────┬────────┘
         │
         │ Click "Batch Process"
         ▼
┌─────────────────────────────┐
│ Step 1: Input Source        │
│ ○ Local Folder              │
│ ○ Cloud Storage             │
└────────┬────────────────────┘
         │
         │ Select Source
         ▼
┌─────────────────────────────┐
│ Step 2: Pipeline Selection  │
│ • Sarah_Validated_v1        │
│ • Field_Curvature_Preset    │
│ • My_Custom_Pipeline        │
└────────┬────────────────────┘
         │
         │ Choose Pipeline
         ▼
┌─────────────────────────────┐
│ Step 3: Configure           │
│ • Augs per image: [3]       │
│ • Keep originals: [✓]      │
│ • Output format: [Same]     │
│                             │
│ Estimates:                  │
│ • Time: 4.2 hours          │
│ • Output: 150K images      │
│ • Space: 82 GB             │
└────────┬────────────────────┘
         │
         │ Test on Subset?
         ├───Yes──► Process 100 samples
         │            │
         │            │ Review results
         │            │
         │◄───────────┘ Approve?
         │
         │ Start
         ▼
┌─────────────────────────────┐
│ Processing                  │
│ ████████░░░░░░░░░░ 67%     │
│                             │
│ • 33,500 / 50,247 images   │
│ • Time remaining: 1.4h      │
│ • Errors: 0                 │
└────────┬────────────────────┘
         │
         │ Complete
         ▼
┌─────────────────────────────┐
│ Results                     │
│ ✓ 150,741 images created   │
│ ✓ Time: 4h 12m             │
│ ✓ Success rate: 100%       │
│                             │
│ [Download Log]              │
│ [Verify Output]             │
└─────────────────────────────┘
```

---

### 4.3 Edge Cases & Error Flows

#### Edge Case 1: Invalid Image Format
```
User uploads .doc file
  ↓
System detects non-image format
  ↓
Show error: "Please upload image file (JPG, PNG, TIFF)"
  ↓
Highlight supported formats
  ↓
User uploads correct format
```

#### Edge Case 2: Out of Memory (Large Batch)
```
User starts batch with 100K images at 4K resolution
  ↓
System estimates 200GB output
  ↓
Warning: "Output size (200GB) exceeds available space (150GB)"
  ↓
Options:
  • Reduce augmentations per image
  • Change output format (compression)
  • Select different output location
  ↓
User adjusts settings
  ↓
Revalidate and proceed
```

#### Edge Case 3: Pipeline Fails Mid-Batch
```
Processing at 60% completion
  ↓
Error: Disk full
  ↓
System pauses processing
  ↓
Notification: "Batch paused - disk space issue"
  ↓
Options:
  • Resume after fixing disk space
  • Cancel and clean up partial results
  • Change output location and resume
  ↓
User frees space
  ↓
Resume from last successful image
```

---

## 5. Information Architecture

### 5.1 Site Map

```
SEM Distortion Tool
│
├── Home Dashboard
│   ├── Quick Start (CTA)
│   ├── Custom Pipeline (CTA)
│   ├── Batch Process (CTA)
│   ├── Recent Projects
│   └── Getting Started Guide
│
├── Quick Start
│   ├── Preset Selection
│   │   ├── Field Curvature
│   │   ├── Astigmatism
│   │   ├── Stage Positioning
│   │   ├── Beam Drift
│   │   └── Custom Mix
│   │
│   └── Preview & Adjust
│       ├── Upload Image
│       ├── Parameter Controls
│       ├── Visual Comparison
│       │   ├── Side-by-Side
│       │   ├── Grid View
│       │   └── Overlay
│       ├── Metrics Display
│       └── Export Options
│
├── Custom Pipeline Builder
│   ├── Transform Library
│   │   ├── Search/Filter
│   │   ├── Categories
│   │   │   ├── Geometric
│   │   │   ├── SEM-Specific
│   │   │   ├── Pixel-Level
│   │   │   └── Utility
│   │   └── Documentation (inline)
│   │
│   ├── Pipeline Canvas
│   │   ├── Drag-Drop Area
│   │   ├── Transform Sequence
│   │   ├── Parameter Editors
│   │   └── Composition Settings
│   │
│   ├── Test & Preview
│   │   ├── Upload Test Images
│   │   ├── Run Pipeline
│   │   ├── Results Grid
│   │   └── Performance Metrics
│   │
│   └── Save/Export
│       ├── Save as Template
│       ├── Export Python Code
│       ├── Export Config (JSON/YAML)
│       └── Share Link
│
├── Batch Processing
│   ├── Input Configuration
│   │   ├── Local Folder Browser
│   │   ├── Cloud Storage Selector
│   │   └── Dataset Preview
│   │
│   ├── Pipeline Selection
│   │   ├── Saved Pipelines
│   │   ├── Presets
│   │   └── Recent
│   │
│   ├── Processing Options
│   │   ├── Augmentations per Image
│   │   ├── Output Settings
│   │   ├── Naming Convention
│   │   └── Validation Rules
│   │
│   ├── Execution
│   │   ├── Estimates Display
│   │   ├── Test Subset Option
│   │   ├── Start/Pause/Cancel
│   │   └── Progress Monitor
│   │
│   └── Results & History
│       ├── Job Queue
│       ├── Completed Jobs
│       ├── Logs & Reports
│       └── Error Analysis
│
├── Library
│   ├── Saved Pipelines
│   │   ├── My Pipelines
│   │   ├── Shared with Me
│   │   └── Templates
│   │
│   ├── Project History
│   │   ├── Recent
│   │   ├── Favorites
│   │   └── Archived
│   │
│   └── Batch Jobs
│       ├── Active
│       ├── Completed
│       └── Failed
│
├── Settings
│   ├── User Preferences
│   ├── Default Parameters
│   ├── Integration Keys
│   └── Notifications
│
└── Help & Resources
    ├── Documentation
    ├── Video Tutorials
    ├── API Reference
    ├── Best Practices
    └── Community Forum
```

### 5.2 Navigation Structure

#### Primary Navigation (Always Visible)
```
┌────────────────────────────────────────────────────┐
│ [Logo] SEM Tool    Quick Start | Custom | Batch    │
│                                  Library | Settings │
└────────────────────────────────────────────────────┘
```

#### Contextual Navigation (Page-Specific)
- **Breadcrumbs**: Home > Quick Start > Field Curvature
- **Step Indicators**: Step 1 of 4: Select Input
- **Progress Bars**: For batch processing
- **Back Buttons**: Always available to previous screen

#### Footer Navigation
- About
- Documentation
- Contact
- Privacy Policy
- Version Info

---

### 5.3 Content Hierarchy

#### Home Page Priority
1. **Hero Section**: Value proposition + main CTAs
2. **Entry Points**: 3 large cards (Quick Start, Custom, Batch)
3. **Recent Activity**: Last 3 projects
4. **Quick Links**: Documentation, Examples

#### Quick Start Priority
1. **Preset Cards**: Large, visual, descriptive
2. **Upload Area**: Prominent, drag-drop enabled
3. **Preview**: Largest screen real estate
4. **Controls**: Secondary, collapsible

#### Custom Builder Priority
1. **Pipeline Canvas**: Center, largest area
2. **Transform Library**: Left sidebar, searchable
3. **Settings Panel**: Right sidebar, context-aware
4. **Preview**: Modal or bottom panel

#### Batch Processing Priority
1. **Configuration Steps**: Linear, numbered
2. **Estimates**: Prominently displayed
3. **Status/Progress**: Real-time, visual
4. **Actions**: Clear, confirmable

---

## 6. Feature Specifications

### 6.1 Quick Start Mode

#### 6.1.1 Preset Library

**Description**: Curated collection of physics-based augmentation presets optimized for common SEM distortion patterns.

**Functional Requirements**:
- FR-QS-001: System shall provide minimum 5 preset configurations
- FR-QS-002: Each preset shall include name, description, and visual icon
- FR-QS-003: Presets shall be based on validated SEM physics models
- FR-QS-004: Users shall be able to preview preset effects before applying

**Preset Definitions**:

| Preset Name | Description | Transforms Included | Use Case |
|-------------|-------------|---------------------|----------|
| Field Curvature | Electromagnetic lens field distortion | OpticalDistortion (0.2), GridDistortion (0.3) | General-purpose SEM variation |
| Astigmatism | Lens imperfection artifacts | AstigmatismTransform (15, 10), OpticalDistortion (0.15) | Older SEM equipment |
| Stage Positioning | Mechanical stage variations | ShiftScaleRotate (0.05, 0.03, 2), Perspective (0.05) | Multi-site imaging |
| Beam Drift | Electron beam instability | ElasticTransform (30, 3), GridDistortion (0.1) | Long acquisition times |
| Custom Mix | Combination of multiple effects | All above with reduced strength | Maximum variation |

**Non-Functional Requirements**:
- NFR-QS-001: Preset loading time < 100ms
- NFR-QS-002: Preset descriptions at 8th grade reading level
- NFR-QS-003: Icons shall be color-coded by category

**Acceptance Criteria**:
- AC-QS-001: User can identify appropriate preset within 30 seconds
- AC-QS-002: Preset application produces expected visual output
- AC-QS-003: All presets maintain defect detectability > 85%

---

#### 6.1.2 Image Upload & Preview

**Description**: Drag-and-drop interface for image upload with instant preview generation.

**Functional Requirements**:
- FR-UP-001: Support drag-and-drop file upload
- FR-UP-002: Support click-to-browse file selection
- FR-UP-003: Accept formats: JPG, PNG, TIFF, BMP
- FR-UP-004: Display image dimensions and file size
- FR-UP-005: Generate 6 augmented variations on upload
- FR-UP-006: Allow regeneration with different random seeds

**File Size Limits**:
- Maximum file size: 50 MB
- Maximum dimensions: 8192 x 8192 pixels
- Recommended: 1024 x 1024 to 2048 x 2048

**Preview Modes**:
1. **Side-by-Side**: Original vs. Single augmented
2. **Grid View**: Original + 6 variations
3. **Overlay**: Toggle between original and augmented

**Non-Functional Requirements**:
- NFR-UP-001: Preview generation < 500ms for 1024x1024 images
- NFR-UP-002: Responsive upload indicator
- NFR-UP-003: Clear error messages for invalid files

**Acceptance Criteria**:
- AC-UP-001: 95% of users successfully upload image on first attempt
- AC-UP-002: Preview renders within 1 second
- AC-UP-003: All supported formats display correctly

---

#### 6.1.3 Parameter Adjustment

**Description**: Intuitive sliders for real-time parameter tuning.

**Functional Requirements**:
- FR-PA-001: Provide strength slider (0.0 to 1.0)
- FR-PA-002: Provide probability slider (0% to 100%)
- FR-PA-003: Provide random seed input field
- FR-PA-004: Display current parameter values numerically
- FR-PA-005: Update preview in real-time (< 300ms)
- FR-PA-006: Show parameter reset to default option

**Parameter Ranges**:
```
Strength:
  - Range: 0.0 (no distortion) to 1.0 (maximum)
  - Default: 0.5
  - Step: 0.01

Probability:
  - Range: 0% (never apply) to 100% (always apply)
  - Default: 50%
  - Step: 1%

Random Seed:
  - Range: 0 to 2^31-1
  - Default: 42
  - Allows: manual input or "randomize" button
```

**UI Components**:
- Slider with value display
- Text input for precise values
- Reset button for each parameter
- "Regenerate" button to see variations

**Non-Functional Requirements**:
- NFR-PA-001: Slider interaction feels smooth (60 fps)
- NFR-PA-002: Parameter changes persist during session
- NFR-PA-003: Tooltips explain each parameter

**Acceptance Criteria**:
- AC-PA-001: Users can adjust parameters without guidance
- AC-PA-002: Real-time preview updates reliably
- AC-PA-003: Seed value produces reproducible results

---

#### 6.1.4 Visual Comparison Tools

**Description**: Multiple viewing modes for comparing original and augmented images.

**Functional Requirements**:
- FR-VC-001: Provide side-by-side comparison view
- FR-VC-002: Provide 2x3 grid view (6 variations)
- FR-VC-003: Provide overlay/toggle view
- FR-VC-004: Allow zoom and pan in all views
- FR-VC-005: Display image filenames and parameters
- FR-VC-006: Enable download of specific variations

**View Modes Detail**:

**Side-by-Side**:
```
┌────────────┬────────────┐
│  Original  │  Augmented │
│            │            │
│            │            │
└────────────┴────────────┘
  [Parameters: strength=0.3, p=0.5]
```

**Grid View**:
```
┌──────┬──────┬──────┐
│ Orig │ Aug1 │ Aug2 │
├──────┼──────┼──────┤
│ Aug3 │ Aug4 │ Aug5 │
└──────┴──────┴──────┘
```

**Overlay**:
- Toggle button switches between original and augmented
- Keyboard shortcut: spacebar
- Useful for detecting subtle differences

**Non-Functional Requirements**:
- NFR-VC-001: View mode switching < 100ms
- NFR-VC-002: Zoom/pan operations feel instantaneous
- NFR-VC-003: Grid view loads all images within 2 seconds

**Acceptance Criteria**:
- AC-VC-001: Users can easily compare subtle differences
- AC-VC-002: All view modes render correctly at various screen sizes
- AC-VC-003: Zoom maintains image quality (no pixelation)

---

#### 6.1.5 Metrics Display

**Description**: Quantitative feedback on augmentation quality and performance.

**Functional Requirements**:
- FR-MD-001: Display average distortion magnitude
- FR-MD-002: Calculate feature preservation percentage
- FR-MD-003: Show processing time per image
- FR-MD-004: Provide distribution histogram of distortion values
- FR-MD-005: Allow export of metrics as CSV

**Metrics Definitions**:

**Average Distortion**:
- Calculation: RMS displacement of pixel positions
- Range: 0.0 (no change) to 1.0 (maximum distortion)
- Display: Decimal format (e.g., 0.24)
- Color coding: 
  - Green < 0.2 (subtle)
  - Yellow 0.2-0.4 (moderate)
  - Red > 0.4 (strong)

**Feature Preservation**:
- Calculation: SSIM-based structural similarity
- Range: 0% (completely destroyed) to 100% (identical)
- Target: > 85% for defect detectability
- Warning threshold: < 75%

**Processing Time**:
- Measurement: Time to augment single image
- Display: milliseconds (ms)
- Benchmark: < 100ms for 1024x1024 on CPU

**Non-Functional Requirements**:
- NFR-MD-001: Metrics calculation < 50ms
- NFR-MD-002: Real-time update as parameters change
- NFR-MD-003: Metrics explanation available on hover

**Acceptance Criteria**:
- AC-MD-001: Metrics accurately reflect augmentation intensity
- AC-MD-002: Feature preservation correlates with user perception
- AC-MD-003: Users understand what metrics mean

---

#### 6.1.6 Export Options

**Description**: Multiple formats for exporting augmentation pipeline.

**Functional Requirements**:
- FR-EX-001: Generate Python code snippet
- FR-EX-002: Export configuration as JSON file
- FR-EX-003: Export configuration as YAML file
- FR-EX-004: Copy code to clipboard with one click
- FR-EX-005: Include comments and usage examples in code
- FR-EX-006: Allow saving as named template

**Python Code Template**:
```python
# Generated by SEM Distortion Tool
# Preset: Field Curvature
# Date: 2025-11-11

import albumentations as A
import cv2

# Define augmentation pipeline
transform = A.Compose([
    A.OpticalDistortion(
        distort_limit=0.2,
        shift_limit=0.1,
        p=0.5
    ),
    A.GridDistortion(
        num_steps=5,
        distort_limit=0.3,
        p=0.5
    ),
])

# Usage example
image = cv2.imread('wafer_image.jpg')
augmented = transform(image=image)['image']
cv2.imwrite('augmented.jpg', augmented)
```

**JSON Configuration**:
```json
{
  "name": "Field Curvature",
  "version": "1.0",
  "created": "2025-11-11T10:30:00Z",
  "transforms": [
    {
      "type": "OpticalDistortion",
      "params": {
        "distort_limit": 0.2,
        "shift_limit": 0.1,
        "p": 0.5
      }
    },
    {
      "type": "GridDistortion",
      "params": {
        "num_steps": 5,
        "distort_limit": 0.3,
        "p": 0.5
      }
    }
  ],
  "metadata": {
    "random_seed": 42,
    "target_size": null
  }
}
```

**Non-Functional Requirements**:
- NFR-EX-001: Code generation < 100ms
- NFR-EX-002: Generated code runs without modification
- NFR-EX-003: Export files include timestamp and version

**Acceptance Criteria**:
- AC-EX-001: 95% of exported code works without changes
- AC-EX-002: All export formats contain complete configuration
- AC-EX-003: Users can successfully import configurations

---

### 6.2 Custom Pipeline Builder

#### 6.2.1 Transform Library

**Description**: Searchable catalog of all available augmentation transforms with categorization and documentation.

**Functional Requirements**:
- FR-TL-001: Display all available transforms with descriptions
- FR-TL-002: Categorize transforms by type (Geometric, SEM-Specific, Pixel-Level)
- FR-TL-003: Provide search functionality with keyword matching
- FR-TL-004: Show inline documentation for each transform
- FR-TL-005: Indicate custom vs. standard transforms
- FR-TL-006: Enable drag-and-drop to pipeline canvas

**Transform Categories**:

**Geometric Transforms** (Standard Albumentations):
- OpticalDistortion
- GridDistortion
- ElasticTransform
- Perspective
- ShiftScaleRotate
- Affine
- PiecewiseAffine

**SEM-Specific Transforms** (Custom):
- FieldCurvature
- AstigmatismDistortion
- BeamDrift
- ScanLineNoise
- ChargingArtifact

**Pixel-Level Transforms**:
- GaussNoise
- GaussianBlur
- Sharpen
- RandomBrightnessContrast
- CLAHE

**Utility Transforms**:
- Resize
- CenterCrop
- RandomCrop
- Normalize

**Transform Card Layout**:
```
┌─────────────────────────┐
│ OpticalDistortion       │
│ [Geometric]             │
│                         │
│ Simulates lens optical  │
│ distortion (barrel/     │
│ pincushion effect)      │
│                         │
│ [View Docs] [Add]       │
└─────────────────────────┘
```

**Non-Functional Requirements**:
- NFR-TL-001: Library loads in < 500ms
- NFR-TL-002: Search returns results in < 100ms
- NFR-TL-003: Categories visually distinct

**Acceptance Criteria**:
- AC-TL-001: Users can find relevant transform within 30 seconds
- AC-TL-002: Drag-drop works smoothly on all browsers
- AC-TL-003: Documentation is clear and includes examples

---

#### 6.2.2 Pipeline Canvas

**Description**: Visual workspace for constructing augmentation pipelines through drag-and-drop interaction.

**Functional Requirements**:
- FR-PC-001: Accept transforms via drag-and-drop
- FR-PC-002: Display transforms in sequential order
- FR-PC-003: Allow reordering transforms via drag-and-drop
- FR-PC-004: Enable removing transforms with delete button
- FR-PC-005: Show parameter editors for each transform
- FR-PC-006: Indicate pipeline composition type (Sequential/OneOf/SomeOf)
- FR-PC-007: Display pipeline execution order numbering

**Canvas States**:

**Empty State**:
```
┌────────────────────────────────────┐
│                                    │
│   Drag transforms from the library │
│   to build your pipeline           │
│                                    │
│   💡 Tip: Order matters! Transforms│
│      are applied sequentially      │
│                                    │
└────────────────────────────────────┘
```

**Populated State**:
```
┌────────────────────────────────────┐
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ 1  OpticalDistortion      [x]┃ │
│ ┃    Strength: ▓▓▓▓░░░░░░ 0.4  ┃ │
│ ┃    Probability: 50%           ┃ │
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │
│                ⬇                   │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ 2  GridDistortion         [x]┃ │
│ ┃    Steps: 5                   ┃ │
│ ┃    Strength: ▓▓▓▓▓▓░░░░ 0.6  ┃ │
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │
│                ⬇                   │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ 3  FieldCurvature (Custom)[x]┃ │
│ ┃    Strength: ▓▓▓▓▓░░░░░ 0.5  ┃ │
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │
└────────────────────────────────────┘
```

**Transform Card Components**:
- Sequential number badge
- Transform name
- Parameter sliders/inputs
- Delete button
- Drag handle
- Expand/collapse for advanced params

**Composition Types**:
- **Sequential**: Apply all transforms in order
- **OneOf**: Apply one random transform from list
- **SomeOf**: Apply random subset of transforms

**Non-Functional Requirements**:
- NFR-PC-001: Drag-drop feels responsive (< 16ms frame time)
- NFR-PC-002: Canvas supports 20+ transforms without lag
- NFR-PC-003: Auto-save pipeline state every 30 seconds

**Acceptance Criteria**:
- AC-PC-001: Users can build pipeline without documentation
- AC-PC-002: Reordering transforms is intuitive
- AC-PC-003: Parameter changes immediately visible

---

#### 6.2.3 Test & Preview

**Description**: Capability to test pipeline on multiple images before export.

**Functional Requirements**:
- FR-TP-001: Upload multiple test images (up to 20)
- FR-TP-002: Run pipeline on all test images
- FR-TP-003: Display results in grid layout
- FR-TP-004: Show per-image metrics
- FR-TP-005: Compare results across images
- FR-TP-006: Allow regeneration with different seeds

**Test Workflow**:
```
Upload Test Images (1-20)
         ↓
Click "Test Pipeline"
         ↓
Processing (progress bar)
         ↓
Results Grid Display
         ↓
Review Metrics
         ↓
Iterate or Approve?
```

**Results Grid Layout**:
```
┌────────┬────────┬────────┐
│ Img 1  │ Img 2  │ Img 3  │
│        │        │        │
│ Orig   │ Orig   │ Orig   │
├────────┼────────┼────────┤
│ Aug    │ Aug    │ Aug    │
│        │        │        │
│ ✓ 0.24 │ ✓ 0.31 │ ⚠ 0.45│
└────────┴────────┴────────┘
```

**Metrics Per Image**:
- Distortion magnitude
- Feature preservation score
- Processing time
- Warning indicators if metrics out of range

**Non-Functional Requirements**:
- NFR-TP-001: Process 10 images in < 5 seconds
- NFR-TP-002: Grid view loads smoothly
- NFR-TP-003: Can handle up to 8192x8192 images

**Acceptance Criteria**:
- AC-TP-001: Test results help users validate pipeline
- AC-TP-002: Issues are easy to identify visually
- AC-TP-003: Can iterate on pipeline based on test results

---

#### 6.2.4 Save & Template Management

**Description**: System for saving, naming, and managing custom pipelines.

**Functional Requirements**:
- FR-ST-001: Save pipeline with custom name
- FR-ST-002: Add description and tags to pipeline
- FR-ST-003: View list of saved pipelines
- FR-ST-004: Load saved pipeline into canvas
- FR-ST-005: Duplicate existing pipeline
- FR-ST-006: Delete saved pipelines
- FR-ST-007: Export pipeline as template file
- FR-ST-008: Import pipeline from template file

**Pipeline Metadata**:
```json
{
  "name": "My Custom Pipeline",
  "description": "Optimized for Sector 3 wafers",
  "tags": ["production", "field-curvature"],
  "created": "2025-11-11T10:30:00Z",
  "modified": "2025-11-11T14:22:00Z",
  "author": "alex@company.com",
  "version": "1.2",
  "transforms": [...],
  "test_results": {
    "avg_distortion": 0.28,
    "avg_preservation": 0.91,
    "tested_on": 10
  }
}
```

**Library View**:
```
┌─────────────────────────────────────┐
│ My Pipelines              [+ New]   │
├─────────────────────────────────────┤
│ ● My Custom Pipeline            1.2 │
│   "Optimized for Sector 3..."       │
│   Modified: 2 hours ago             │
│   [Load] [Edit] [Delete]            │
├─────────────────────────────────────┤
│ ● Field Test v2                 1.0 │
│   "Experimental high distortion"    │
│   Modified: 3 days ago              │
│   [Load] [Edit] [Delete]            │
└─────────────────────────────────────┘
```

**Non-Functional Requirements**:
- NFR-ST-001: Save operation < 500ms
- NFR-ST-002: Support 100+ saved pipelines per user
- NFR-ST-003: Search/filter in library < 200ms

**Acceptance Criteria**:
- AC-ST-001: Users can find and load saved pipelines easily
- AC-ST-002: Pipeline state perfectly restored on load
- AC-ST-003: No data loss on save/load operations

---

### 6.3 Batch Processing

#### 6.3.1 Input Source Selection

**Description**: Interface for selecting image datasets from various sources.

**Functional Requirements**:
- FR-IS-001: Browse local file system
- FR-IS-002: Connect to cloud storage (S3, GCS, Azure Blob)
- FR-IS-003: Recursive directory scanning
- FR-IS-004: File filtering by extension
- FR-IS-005: Display file count and total size
- FR-IS-006: Preview first 10 images from dataset

**Supported Sources**:
- Local file system
- AWS S3 buckets
- Google Cloud Storage
- Azure Blob Storage
- Network shares (SMB/NFS)

**Source Configuration**:
```
Local Folder:
  Path: /data/wafer_images/
  Files: 50,247 images
  Size: 22.4 GB
  Format: Mixed (JPG, PNG, TIFF)

S3 Bucket:
  Bucket: company-wafer-data
  Prefix: production/2025-11/
  Files: 125,834 images
  Size: 68.2 GB
  Credentials: [Configured ✓]
```

**Non-Functional Requirements**:
- NFR-IS-001: Directory scan < 5 seconds for 50K files
- NFR-IS-002: Cloud connection timeout: 30 seconds
- NFR-IS-003: Clear error messages for access issues

**Acceptance Criteria**:
- AC-IS-001: Can browse and select datasets without errors
- AC-IS-002: File count and size accurate within 1%
- AC-IS-003: Cloud credentials securely stored

---

#### 6.3.2 Processing Configuration

**Description**: Options for configuring batch augmentation behavior.

**Functional Requirements**:
- FR-BC-001: Set augmentations per image (1-10)
- FR-BC-002: Toggle keep original images
- FR-BC-003: Configure output format (Same/PNG/TIFF/JPG)
- FR-BC-004: Set output naming convention
- FR-BC-005: Configure output directory/bucket
- FR-BC-006: Set compression quality
- FR-BC-007: Enable/disable metadata preservation

**Configuration Options**:

**Augmentations Per Image**:
- Range: 1 to 10
- Default: 3
- Each augmentation uses different random seed
- Example: image_001.jpg → image_001_aug_0.jpg, image_001_aug_1.jpg, image_001_aug_2.jpg

**Keep Originals**:
- Checkbox: Include original images in output
- Useful for creating training/validation split

**Output Format**:
- Same as input (default)
- PNG (lossless)
- TIFF (lossless, larger)
- JPG (lossy, quality configurable)

**Naming Convention**:
- Default: `{original_name}_aug_{index}.{ext}`
- Custom: Use template with variables
- Variables: {name}, {index}, {seed}, {timestamp}

**Output Location**:
- Local directory (browse)
- Same directory as input (new subfolder)
- Cloud storage bucket

**Non-Functional Requirements**:
- NFR-BC-001: Configuration saved between sessions
- NFR-BC-002: Invalid configurations prevented
- NFR-BC-003: Estimates update in real-time (< 100ms)

**Acceptance Criteria**:
- AC-BC-001: Configuration is clear and self-explanatory
- AC-BC-002: Estimates are accurate (within 10%)
- AC-BC-003: Output structure matches configuration

---

#### 6.3.3 Execution & Monitoring

**Description**: Job execution interface with real-time progress monitoring.

**Functional Requirements**:
- FR-EM-001: Display processing estimates before start
- FR-EM-002: "Test on Subset" option (process 10-100 images first)
- FR-EM-003: Real-time progress bar with percentage
- FR-EM-004: Show images processed / total
- FR-EM-005: Display estimated time remaining
- FR-EM-006: Show current processing speed (images/sec)
- FR-EM-007: Pause/resume capability
- FR-EM-008: Cancel with cleanup option
- FR-EM-009: Error count and handling
- FR-EM-010: Completion notification (email/webhook)

**Estimates Display**:
```
┌─────────────────────────────────────┐
│ Processing Estimates                │
├─────────────────────────────────────┤
│ Input images:        50,247         │
│ Output images:      150,741         │
│ Estimated time:      ~4.2 hours     │
│ Disk space needed:   ~82 GB         │
│ Processing speed:    ~10 img/sec    │
│                                     │
│ [Test Subset] [Start Processing]    │
└─────────────────────────────────────┘
```

**Progress Monitor**:
```
┌─────────────────────────────────────┐
│ Processing: My Batch Job            │
├─────────────────────────────────────┤
│ ████████████████████░░░░░░░ 67%    │
│                                     │
│ Processed:  33,665 / 50,247        │
│ Time elapsed: 2h 48m                │
│ Time remaining: ~1h 22m             │
│ Speed: 11.2 images/sec              │
│ Errors: 3 (skipped)                 │
│                                     │
│ [Pause] [Cancel] [View Log]        │
└─────────────────────────────────────┘
```

**Error Handling**:
- Skip failed images and continue
- Retry failed images (configurable attempts)
- Pause on error for review
- Log all errors with details

**Non-Functional Requirements**:
- NFR-EM-001: Progress updates every 1 second
- NFR-EM-002: Pause/resume < 2 seconds
- NFR-EM-003: Cancellation cleans up partial files

**Acceptance Criteria**:
- AC-EM-001: Progress accurately reflects completion
- AC-EM-002: Time estimates within 15% actual
- AC-EM-003: Can recover from errors gracefully

---

#### 6.3.4 Results & Job History

**Description**: Interface for reviewing completed jobs and accessing results.

**Functional Requirements**:
- FR-RH-001: Display list of all batch jobs (active, completed, failed)
- FR-RH-002: Show job metadata (date, duration, files processed)
- FR-RH-003: Provide download link to processing log
- FR-RH-004: Allow browsing output files
- FR-RH-005: Display success/failure statistics
- FR-RH-006: Enable rerunning failed images only
- FR-RH-007: Archive or delete old jobs

**Job History View**:
```
┌────────────────────────────────────────────────────┐
│ Batch Job History                    [Filter ▼]    │
├────────────────────────────────────────────────────┤
│ ✓ Wafer_Production_2025-11          Completed      │
│   50,247 images → 150,741 augmented                │
│   Duration: 4h 12m                                 │
│   Success: 100% (3 skipped)                        │
│   Nov 11, 2025 2:30 PM                            │
│   [View Log] [Download Results] [Rerun Failed]     │
├────────────────────────────────────────────────────┤
│ ⚠ Test_Batch_Small                 Failed          │
│   Failed after 45 images                           │
│   Error: Disk space insufficient                   │
│   Nov 11, 2025 10:15 AM                           │
│   [View Log] [Retry] [Delete]                      │
├────────────────────────────────────────────────────┤
│ ⏸ Validation_Set                   Paused (34%)    │
│   1,247 / 3,650 processed                         │
│   Nov 11, 2025 9:00 AM                            │
│   [Resume] [Cancel] [View Progress]                │
└────────────────────────────────────────────────────┘
```

**Processing Log Contents**:
```
Batch Job: Wafer_Production_2025-11
Started: 2025-11-11 14:30:22
Pipeline: Field_Curvature_v2
Configuration:
  - Augmentations per image: 3
  - Keep originals: Yes
  - Output format: Same as input

Processing Summary:
  Total files scanned: 50,247
  Successfully processed: 50,244
  Skipped (errors): 3
  Output files created: 150,741
  Duration: 4h 12m 8s
  Average speed: 11.4 images/sec

Errors:
  - wafer_3345.jpg: Corrupted file header
  - wafer_8891.tiff: Unsupported color space
  - wafer_12043.png: Out of memory (file too large)

Completed: 2025-11-11 18:42:30
Status: SUCCESS
```

**Non-Functional Requirements**:
- NFR-RH-001: Job list loads in < 1 second
- NFR-RH-002: Logs accessible for 90 days
- NFR-RH-003: Can filter/search jobs efficiently

**Acceptance Criteria**:
- AC-RH-001: Users can find and review past jobs
- AC-RH-002: Logs contain sufficient debug information
- AC-RH-003: Can rerun failed portions of jobs

---

## 7. UI/UX Design Guidelines

### 7.1 Visual Design System

#### 7.1.1 Color Palette

**Primary Colors**:
```
Brand Blue:     #2563EB (Interactive elements, CTAs)
Brand Dark:     #1E40AF (Headers, emphasis)
Brand Light:    #DBEAFE (Backgrounds, highlights)
```

**Semantic Colors**:
```
Success Green:  #10B981 (Completed, valid)
Warning Yellow: #F59E0B (Caution, attention needed)
Error Red:      #EF4444 (Errors, destructive actions)
Info Blue:      #3B82F6 (Information, tips)
```

**Neutral Colors**:
```
Gray 900: #111827 (Primary text)
Gray 600: #4B5563 (Secondary text)
Gray 400: #9CA3AF (Disabled, placeholders)
Gray 100: #F3F4F6 (Backgrounds)
White:    #FFFFFF (Cards, surfaces)
```

**Accent Colors** (for transform categories):
```
Geometric:     #8B5CF6 (Purple)
SEM-Specific:  #EC4899 (Pink)
Pixel-Level:   #14B8A6 (Teal)
Utility:       #F97316 (Orange)
```

#### 7.1.2 Typography

**Font Family**:
- Primary: Inter (sans-serif)
- Monospace: JetBrains Mono (code snippets)

**Type Scale**:
```
H1: 36px, Bold, 40px line height
H2: 30px, Bold, 36px line height
H3: 24px, Semibold, 32px line height
H4: 20px, Semibold, 28px line height
Body Large: 16px, Regular, 24px line height
Body: 14px, Regular, 20px line height
Body Small: 12px, Regular, 16px line height
Caption: 11px, Regular, 14px line height
```

**Font Weights**:
- Regular: 400
- Medium: 500
- Semibold: 600
- Bold: 700

#### 7.1.3 Spacing System

**Base Unit**: 4px

**Scale**:
```
xs:  4px   (0.25rem)
sm:  8px   (0.5rem)
md:  16px  (1rem)
lg:  24px  (1.5rem)
xl:  32px  (2rem)
2xl: 48px  (3rem)
3xl: 64px  (4rem)
```

**Component Spacing**:
- Card padding: 24px (lg)
- Section margin: 48px (2xl)
- Input padding: 12px 16px
- Button padding: 10px 20px

#### 7.1.4 Layout Grid

**Container**:
- Max width: 1280px (xl)
- Padding: 16px (mobile), 24px (tablet), 32px (desktop)

**Grid System**:
- 12-column grid
- Gutter: 24px
- Responsive breakpoints:
  - Mobile: < 640px
  - Tablet: 640px - 1024px
  - Desktop: > 1024px

#### 7.1.5 Component Styles

**Buttons**:
```
Primary:
  Background: #2563EB
  Text: White
  Padding: 10px 20px
  Border radius: 6px
  Hover: #1E40AF

Secondary:
  Background: White
  Text: #2563EB
  Border: 1px solid #2563EB
  Hover: #DBEAFE background

Destructive:
  Background: #EF4444
  Text: White
  Hover: #DC2626
```

**Input Fields**:
```
Default:
  Border: 1px solid #D1D5DB
  Border radius: 6px
  Padding: 10px 12px
  Focus: #2563EB border, shadow

Error:
  Border: 1px solid #EF4444
  Focus: #EF4444 border
```

**Cards**:
```
Background: White
Border: 1px solid #E5E7EB
Border radius: 8px
Padding: 24px
Shadow: 0 1px 3px rgba(0, 0, 0, 0.1)
Hover: Shadow increases
```

**Sliders**:
```
Track height: 4px
Track background: #E5E7EB
Filled track: #2563EB
Thumb: 16px circle, white with shadow
```

---

### 7.2 Interaction Patterns

#### 7.2.1 Drag and Drop

**Visual Feedback**:
- Dragging: Element has shadow, slight transparency
- Valid drop zone: Blue dashed border, light blue background
- Invalid drop zone: Red dashed border
- On drop: Smooth animation to final position

**States**:
```
Idle → Grab (cursor: grab)
  ↓
Dragging (cursor: grabbing)
  ↓
Over Valid Target (visual feedback)
  ↓
Drop (animate to position) OR Cancel (return to origin)
```

#### 7.2.2 Loading States

**Patterns**:
- Skeleton screens for content loading
- Spinner for actions (< 3 seconds expected)
- Progress bar for long operations (> 3 seconds)
- Shimmer effect for images loading

**Examples**:
```
Image Upload:
  [Uploading spinner] → [Preview loads with fade-in]

Batch Processing:
  [Progress bar with percentage and details]

Page Load:
  [Skeleton of page structure] → [Actual content fades in]
```

#### 7.2.3 Transitions & Animations

**Duration Guidelines**:
- Micro-interactions: 150-200ms
- Page transitions: 300ms
- Modal open/close: 200ms
- Drawer slide: 300ms

**Easing**:
- Standard: cubic-bezier(0.4, 0.0, 0.2, 1)
- Decelerate: cubic-bezier(0.0, 0.0, 0.2, 1)
- Accelerate: cubic-bezier(0.4, 0.0, 1, 1)

**Animation Examples**:
- Button click: Scale to 0.95, bounce back
- Card hover: Lift with shadow increase
- Modal enter: Fade in + scale from 0.95
- Toast notification: Slide in from top

#### 7.2.4 Feedback Mechanisms

**Success**:
- Green checkmark icon
- Toast notification (auto-dismiss after 3s)
- Brief success animation
- Optional confetti for major completions

**Error**:
- Red error icon
- Toast notification (requires dismiss)
- Inline error message below field
- Shake animation for input fields

**Warning**:
- Yellow warning icon
- Persistent banner until acknowledged
- Clear action to resolve

**Info**:
- Blue info icon
- Dismissible tooltip or banner
- Link to documentation if relevant

---

### 7.3 Responsive Design

#### 7.3.1 Breakpoint Strategy

**Mobile (< 640px)**:
- Single column layout
- Full-width components
- Simplified navigation (hamburger menu)
- Touch-optimized controls (44px minimum)
- Reduced feature complexity

**Tablet (640px - 1024px)**:
- Two-column layout where appropriate
- Side-by-side comparisons vertical
- Collapsible sidebars
- Touch and mouse support

**Desktop (> 1024px)**:
- Full three-column layouts
- Side-by-side comparisons horizontal
- Persistent sidebars
- Hover states and tooltips
- Keyboard shortcuts enabled

#### 7.3.2 Component Adaptations

**Navigation**:
```
Mobile: Hamburger menu → Full-screen overlay
Tablet: Collapsed sidebar with icons
Desktop: Full sidebar with text labels
```

**Pipeline Canvas**:
```
Mobile: Vertical stack, one transform at a time
Tablet: Vertical stack, all transforms visible
Desktop: Drag-drop canvas with full controls
```

**Image Comparison**:
```
Mobile: Swipe between original/augmented
Tablet: Side-by-side vertical
Desktop: Side-by-side horizontal + grid options
```

---

### 7.4 Accessibility Guidelines

#### 7.4.1 WCAG 2.1 Level AA Compliance

**Color Contrast**:
- Text on background: Minimum 4.5:1
- Large text (18px+): Minimum 3:1
- UI components: Minimum 3:1

**Keyboard Navigation**:
- All interactive elements focusable
- Visible focus indicators (2px blue outline)
- Logical tab order
- Skip to main content link
- Escape to close modals/menus

**Screen Reader Support**:
- Semantic HTML elements
- ARIA labels for custom components
- ARIA live regions for dynamic content
- Alt text for all images
- Form labels properly associated

**Focus Management**:
- Focus trap in modals
- Focus return after modal close
- Focus on first element in new views

#### 7.4.2 Assistive Technology

**Announcements**:
- Status updates announced to screen readers
- Error messages announced immediately
- Success confirmations announced

**Alternative Inputs**:
- Keyboard shortcuts for common actions
- Voice control compatibility
- Screen magnifier support

---

### 7.5 Microcopy & Content Guidelines

#### 7.5.1 Tone of Voice

**Principles**:
- Professional yet friendly
- Clear and concise
- Encouraging, not condescending
- Technical when necessary, plain language when possible

**Examples**:
```
❌ Don't: "The system has failed to process your request due to insufficient disk space."
✓ Do: "We ran out of disk space. Free up some space or choose a different location."

❌ Don't: "Transform applied successfully."
✓ Do: "Looking good! Your distortion is ready."

❌ Don't: "Invalid input detected."
✓ Do: "This file type isn't supported. Try JPG, PNG, or TIFF instead."
```

#### 7.5.2 Button Labels

**Action-oriented**, **Specific**, **Brief**:
```
✓ "Export as Python Code" (not "Export")
✓ "Start Processing" (not "OK")
✓ "Regenerate Preview" (not "Refresh")
✓ "Test on 10 Images" (not "Test")
```

#### 7.5.3 Error Messages

**Structure**: [What happened] + [Why] + [What to do]

**Examples**:
```
"Upload failed: File is too large (75 MB). Maximum size is 50 MB. Try compressing your image first."

"Processing paused: Disk space full. Free up space on /data/ or change output location in settings."

"Can't load pipeline: Configuration file is corrupted. Try importing a different file or contact support."
```

#### 7.5.4 Help Text & Tooltips

**Tooltips**: Brief explanation (< 100 characters)
```
"Distortion strength controls how much the image is warped. Higher = more distortion."
```

**Help Text**: Context and guidance (< 250 characters)
```
"Random seed ensures reproducibility. Using the same seed with the same parameters will always produce identical results. Great for debugging and comparing approaches."
```

---

## 8. Technical Architecture

### 8.1 System Architecture

#### 8.1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                    CLIENT TIER                       │
│                                                      │
│  ┌──────────────┐      ┌─────────────────────────┐│
│  │  React SPA   │◄────►│   Local Storage         ││
│  │  (Frontend)  │      │   (Drafts, Settings)    ││
│  └───────┬──────┘      └─────────────────────────┘│
│          │                                          │
└──────────┼──────────────────────────────────────────┘
           │ HTTPS/WebSocket
           ▼
┌─────────────────────────────────────────────────────┐
│                  APPLICATION TIER                    │
│                                                      │
│  ┌────────────────────────────────────────────────┐│
│  │          FastAPI Backend                        ││
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐  ││
│  │  │   API    │ │  WebSocket│ │   Auth       │  ││
│  │  │  Routes  │ │  Handler  │ │  Middleware  │  ││
│  │  └──────────┘ └──────────┘ └──────────────┘  ││
│  └────────────────────────────────────────────────┘│
│           │              │              │           │
│           ▼              ▼              ▼           │
│  ┌──────────────┐ ┌──────────┐ ┌──────────────┐  │
│  │  Pipeline    │ │  Batch    │ │  Template    │  │
│  │  Service     │ │  Processor│ │  Manager     │  │
│  └──────────────┘ └──────────┘ └──────────────┘  │
└──────────┬───────────────────────────────────┬─────┘
           │                                   │
           ▼                                   ▼
┌─────────────────────────────────────────────────────┐
│                   DATA TIER                          │
│                                                      │
│  ┌──────────────┐ ┌──────────────┐ ┌─────────────┐│
│  │  PostgreSQL  │ │   Redis      │ │   S3/Blob   ││
│  │  (Metadata)  │ │   (Cache)    │ │   (Files)   ││
│  └──────────────┘ └──────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                 PROCESSING TIER                      │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │          Celery Workers                       │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐        │  │
│  │  │ Worker 1│ │ Worker 2│ │ Worker N│        │  │
│  │  │ (CPU)   │ │ (CPU)   │ │ (CPU/GPU)│       │  │
│  │  └─────────┘ └─────────┘ └─────────┘        │  │
│  └──────────────────────────────────────────────┘  │
│           │                                         │
│           ▼                                         │
│  ┌──────────────────┐      ┌──────────────────┐   │
│  │  Albumentations  │      │  OpenCV          │   │
│  │  (Transforms)    │      │  (Custom Logic)  │   │
│  └──────────────────┘      └──────────────────┘   │
└─────────────────────────────────────────────────────┘
```

#### 8.1.2 Technology Stack

**Frontend**:
- Framework: React 18+ with TypeScript
- State Management: Zustand (lightweight, simple)
- UI Components: Tailwind CSS + Headless UI
- Drag-and-Drop: dnd-kit
- Image Display: react-image-gallery, react-zoom-pan-pinch
- API Client: Axios with retry logic
- Build Tool: Vite

**Backend**:
- Framework: FastAPI (Python 3.10+)
- Async Runtime: asyncio + uvloop
- Image Processing: Albumentations + OpenCV + NumPy
- Task Queue: Celery with Redis broker
- Authentication: JWT tokens
- API Documentation: OpenAPI (Swagger)

**Database**:
- Primary: PostgreSQL 14+ (metadata, users, jobs)
- Cache: Redis 6+ (sessions, job status)
- Object Storage: S3-compatible (images, configs)

**Infrastructure**:
- Container Runtime: Docker + Docker Compose
- Orchestration: Kubernetes (production)
- Load Balancer: nginx
- Monitoring: Prometheus + Grafana
- Logging: ELK Stack (Elasticsearch, Logstash, Kibana)

---

### 8.2 API Design

#### 8.2.1 REST API Endpoints

**Base URL**: `https://api.sem-distortion-tool.com/v1`

**Authentication**:
- Method: Bearer Token (JWT)
- Header: `Authorization: Bearer <token>`

**Core Endpoints**:

```
# Presets
GET    /presets                    # List all presets
GET    /presets/{id}               # Get preset details
POST   /presets/{id}/preview       # Generate preview with preset

# Pipelines
GET    /pipelines                  # List user's pipelines
POST   /pipelines                  # Create new pipeline
GET    /pipelines/{id}             # Get pipeline details
PUT    /pipelines/{id}             # Update pipeline
DELETE /pipelines/{id}             # Delete pipeline
POST   /pipelines/{id}/test        # Test pipeline on images
POST   /pipelines/{id}/export      # Export as code/config

# Transforms
GET    /transforms                 # List available transforms
GET    /transforms/{name}          # Get transform details
GET    /transforms/categories      # Get transform categories

# Images
POST   /images/upload              # Upload image(s)
POST   /images/augment             # Augment single image
GET    /images/{id}                # Get image metadata
DELETE /images/{id}                # Delete uploaded image

# Batch Jobs
POST   /batch/jobs                 # Create batch job
GET    /batch/jobs                 # List jobs (with filters)
GET    /batch/jobs/{id}            # Get job details
POST   /batch/jobs/{id}/pause      # Pause job
POST   /batch/jobs/{id}/resume     # Resume job
POST   /batch/jobs/{id}/cancel     # Cancel job
GET    /batch/jobs/{id}/log        # Get job log
GET    /batch/jobs/{id}/results    # Get job results

# Templates
GET    /templates                  # List public templates
POST   /templates                  # Upload template
GET    /templates/{id}             # Download template

# User
GET    /user/profile               # Get user profile
PUT    /user/profile               # Update profile
GET    /user/usage                 # Get usage statistics
```

#### 8.2.2 Request/Response Examples

**POST /pipelines/{id}/test**

Request:
```json
{
  "pipeline_id": "pipe_123",
  "images": [
    "img_001.jpg",
    "img_002.jpg",
    "img_003.jpg"
  ],
  "num_variations": 3,
  "random_seed": 42
}
```

Response:
```json
{
  "job_id": "test_job_456",
  "status": "completed",
  "results": [
    {
      "image_id": "img_001.jpg",
      "variations": [
        {
          "url": "https://..../img_001_aug_0.jpg",
          "metrics": {
            "distortion": 0.24,
            "preservation": 0.91,
            "processing_time_ms": 12
          }
        },
        {
          "url": "https://..../img_001_aug_1.jpg",
          "metrics": {
            "distortion": 0.28,
            "preservation": 0.89,
            "processing_time_ms": 11
          }
        }
      ]
    }
  ],
  "average_metrics": {
    "distortion": 0.26,
    "preservation": 0.90,
    "processing_time_ms": 11.5
  }
}
```

**POST /batch/jobs**

Request:
```json
{
  "name": "Production Batch Nov 2025",
  "pipeline_id": "pipe_123",
  "input": {
    "type": "local",
    "path": "/data/wafer_images/"
  },
  "output": {
    "type": "local",
    "path": "/data/augmented/",
    "format": "same",
    "naming": "{name}_aug_{index}"
  },
  "config": {
    "augmentations_per_image": 3,
    "keep_originals": true,
    "random_seed_base": 42
  },
  "notifications": {
    "email": "user@company.com",
    "webhook": "https://hooks.company.com/batch-complete"
  }
}
```

Response:
```json
{
  "job_id": "job_789",
  "status": "queued",
  "created_at": "2025-11-11T14:30:00Z",
  "estimates": {
    "input_count": 50247,
    "output_count": 150741,
    "estimated_duration_seconds": 15120,
    "estimated_size_bytes": 88080384000
  },
  "monitoring_url": "wss://api.../batch/jobs/job_789/monitor"
}
```

#### 8.2.3 WebSocket Protocol

**Connection**: `wss://api.sem-distortion-tool.com/v1/ws`

**Messages**:

Client → Server (Subscribe):
```json
{
  "type": "subscribe",
  "channel": "batch_job",
  "job_id": "job_789"
}
```

Server → Client (Progress Update):
```json
{
  "type": "progress",
  "job_id": "job_789",
  "status": "processing",
  "progress": {
    "processed": 15623,
    "total": 50247,
    "percentage": 31.1,
    "speed": 11.2,
    "time_remaining_seconds": 3180,
    "errors": 2
  },
  "timestamp": "2025-11-11T15:45:30Z"
}
```

Server → Client (Completion):
```json
{
  "type": "complete",
  "job_id": "job_789",
  "status": "success",
  "results": {
    "input_count": 50247,
    "output_count": 150741,
    "success_count": 50244,
    "error_count": 3,
    "duration_seconds": 15180
  },
  "log_url": "https://api.../batch/jobs/job_789/log",
  "timestamp": "2025-11-11T18:45:00Z"
}
```

---

### 8.3 Data Models

#### 8.3.1 Database Schema

**Users Table**:
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  last_login TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE,
  settings JSONB
);
```

**Pipelines Table**:
```sql
CREATE TABLE pipelines (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  transforms JSONB NOT NULL,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  is_template BOOLEAN DEFAULT FALSE,
  tags TEXT[]
);

CREATE INDEX idx_pipelines_user_id ON pipelines(user_id);
CREATE INDEX idx_pipelines_tags ON pipelines USING GIN(tags);
```

**Batch Jobs Table**:
```sql
CREATE TABLE batch_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  pipeline_id UUID REFERENCES pipelines(id),
  name VARCHAR(255),
  status VARCHAR(50) NOT NULL,  -- queued, processing, paused, completed, failed
  input_config JSONB NOT NULL,
  output_config JSONB NOT NULL,
  processing_config JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  estimates JSONB,
  progress JSONB,
  results JSONB,
  error_log TEXT
);

CREATE INDEX idx_batch_jobs_user_id ON batch_jobs(user_id);
CREATE INDEX idx_batch_jobs_status ON batch_jobs(status);
CREATE INDEX idx_batch_jobs_created_at ON batch_jobs(created_at DESC);
```

**Presets Table**:
```sql
CREATE TABLE presets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) UNIQUE NOT NULL,
  description TEXT,
  icon VARCHAR(50),
  category VARCHAR(100),
  transforms JSONB NOT NULL,
  is_public BOOLEAN DEFAULT TRUE,
  usage_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### 8.3.2 Object Storage Structure

**S3 Bucket Organization**:
```
sem-distortion-tool/
├── users/
│   └── {user_id}/
│       ├── uploads/
│       │   └── {image_id}.{ext}
│       ├── outputs/
│       │   └── {job_id}/
│       │       └── {output_images}
│       └── templates/
│           └── {pipeline_id}.json
│
├── public/
│   ├── presets/
│   │   └── {preset_id}.json
│   └── templates/
│       └── {template_id}.json
│
└── system/
    └── logs/
        └── {job_id}.log
```

---

### 8.4 Processing Pipeline

#### 8.4.1 Image Processing Flow

```
1. Upload
   │
   ├─► Validate format/size
   │   │
   │   ├─► Valid → Continue
   │   └─► Invalid → Return error
   │
2. Storage
   │
   ├─► Save to S3
   ├─► Create metadata record
   └─► Generate thumbnail
   │
3. Preview Generation
   │
   ├─► Load pipeline config
   ├─► Apply transforms (Albumentations)
   │   ├─► OpticalDistortion
   │   ├─► GridDistortion
   │   └─► Custom transforms
   ├─► Calculate metrics
   │   ├─► Distortion magnitude
   │   └─► Feature preservation
   └─► Return results
   │
4. Batch Processing (if requested)
   │
   ├─► Create Celery task
   ├─► Queue for workers
   │   │
   │   └─► Worker picks up task
   │       │
   │       ├─► Load images in batches
   │       ├─► Apply pipeline
   │       ├─► Save outputs
   │       ├─► Update progress (WebSocket)
   │       └─► Handle errors
   │
   └─► Complete/Notify
```

#### 8.4.2 Albumentations Integration

**Pipeline Serialization**:
```python
# User's pipeline configuration
pipeline_config = {
    "transforms": [
        {
            "type": "OpticalDistortion",
            "params": {
                "distort_limit": 0.2,
                "shift_limit": 0.1,
                "p": 0.5
            }
        },
        {
            "type": "GridDistortion",
            "params": {
                "num_steps": 5,
                "distort_limit": 0.3,
                "p": 0.5
            }
        }
    ],
    "compose": "Sequential"
}

# Convert to Albumentations pipeline
def build_pipeline(config):
    transforms = []
    for t in config["transforms"]:
        transform_class = getattr(A, t["type"])
        transforms.append(transform_class(**t["params"]))
    
    if config["compose"] == "Sequential":
        return A.Compose(transforms)
    elif config["compose"] == "OneOf":
        return A.OneOf(transforms)
    elif config["compose"] == "SomeOf":
        return A.SomeOf(transforms, n=config.get("n", 1))
```

**Custom Transform Registration**:
```python
# Custom SEM transforms
class FieldCurvatureTransform(ImageOnlyTransform):
    def __init__(self, strength=(10, 30), always_apply=False, p=0.5):
        super().__init__(always_apply, p)
        self.strength = strength
    
    def apply(self, img, strength=20, **params):
        return apply_field_curvature(img, strength)
    
    def get_params(self):
        return {"strength": random.uniform(*self.strength)}

# Register custom transforms
CUSTOM_TRANSFORMS = {
    "FieldCurvature": FieldCurvatureTransform,
    "AstigmatismDistortion": AstigmatismDistortion,
    "BeamDrift": BeamDriftTransform
}
```

#### 8.4.3 Batch Processing with Celery

**Task Definition**:
```python
@celery_app.task(bind=True)
def process_batch_job(self, job_id, pipeline_config, input_config, output_config):
    """
    Process batch augmentation job
    
    Args:
        job_id: Unique job identifier
        pipeline_config: Augmentation pipeline
        input_config: Input source configuration
        output_config: Output destination and format
    """
    # Update job status
    update_job_status(job_id, "processing", started_at=datetime.now())
    
    # Build pipeline
    pipeline = build_pipeline(pipeline_config)
    
    # Get input images
    images = scan_input_source(input_config)
    total = len(images)
    
    processed = 0
    errors = []
    
    for image_path in images:
        try:
            # Load image
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Apply augmentations
            for i in range(output_config["augmentations_per_image"]):
                augmented = pipeline(image=image)["image"]
                
                # Save output
                output_path = generate_output_path(
                    image_path, i, output_config
                )
                save_image(augmented, output_path, output_config)
            
            processed += 1
            
            # Update progress every 10 images
            if processed % 10 == 0:
                progress = {
                    "processed": processed,
                    "total": total,
                    "percentage": (processed / total) * 100,
                    "errors": len(errors)
                }
                update_job_progress(job_id, progress)
                
                # Send WebSocket update
                send_progress_update(job_id, progress)
        
        except Exception as e:
            errors.append({
                "image": image_path,
                "error": str(e)
            })
            continue
    
    # Complete job
    results = {
        "input_count": total,
        "output_count": processed * output_config["augmentations_per_image"],
        "success_count": processed,
        "error_count": len(errors),
        "errors": errors
    }
    
    update_job_status(
        job_id,
        "completed" if len(errors) < total else "completed_with_errors",
        completed_at=datetime.now(),
        results=results
    )
    
    # Send completion notification
    send_completion_notification(job_id, results)
    
    return results
```

---

### 8.5 Performance Optimization

#### 8.5.1 Caching Strategy

**Redis Cache Structure**:
```
# Pipeline definitions (TTL: 1 hour)
pipeline:{pipeline_id} → {pipeline_json}

# Preview results (TTL: 15 minutes)
preview:{image_hash}:{pipeline_hash} → {result_urls}

# Transform library (TTL: 24 hours)
transforms:list → {transforms_json}

# User sessions (TTL: 7 days)
session:{session_id} → {user_data}

# Job status (TTL: until completion + 1 hour)
job:{job_id}:status → {status_json}
job:{job_id}:progress → {progress_json}
```

**Cache Invalidation**:
- Pipeline update → Invalidate `pipeline:{id}` and related previews
- Transform library update → Invalidate `transforms:list`
- Job completion → Keep status for 1 hour, then remove

#### 8.5.2 Image Processing Optimization

**Strategies**:
1. **Batch Processing**: Process images in batches of 100
2. **Parallel Workers**: Multiple Celery workers (CPU-bound)
3. **GPU Acceleration**: Use GPU for large images (> 4K) if available
4. **Smart Resizing**: Downsample for preview, full-res for export
5. **Progressive Loading**: Stream large images in chunks

**Performance Targets**:
```
Image Size       CPU Time      GPU Time (if available)
1024×1024        < 50ms        < 10ms
2048×2048        < 150ms       < 30ms
4096×4096        < 500ms       < 100ms
```

#### 8.5.3 Database Query Optimization

**Indexes**:
- Composite index on (user_id, created_at) for job listings
- GIN index on tags for pipeline search
- Partial index on active jobs only

**Query Patterns**:
```sql
-- Efficient pagination
SELECT * FROM batch_jobs
WHERE user_id = $1 AND created_at < $2
ORDER BY created_at DESC
LIMIT 20;

-- Pipeline search with tags
SELECT * FROM pipelines
WHERE user_id = $1 AND tags && ARRAY['production', 'validated']
ORDER BY updated_at DESC;
```

---

### 8.6 Security

#### 8.6.1 Authentication & Authorization

**JWT Token Structure**:
```json
{
  "sub": "user_id",
  "email": "user@company.com",
  "exp": 1699999999,
  "iat": 1699900000,
  "roles": ["user"]
}
```

**Permission Model**:
- Users can only access their own resources
- Public templates accessible to all
- Admin role for system management

**API Security**:
- All endpoints require authentication (except login/register)
- Rate limiting: 100 requests/minute per user
- Input validation on all parameters
- SQL injection prevention (parameterized queries)
- XSS prevention (output encoding)

#### 8.6.2 Data Security

**At Rest**:
- Database encryption (PostgreSQL TDE)
- S3 bucket encryption (AES-256)
- Secrets in environment variables or vault

**In Transit**:
- HTTPS/TLS 1.3 for all connections
- Certificate pinning for API calls
- WebSocket over TLS (WSS)

**User Data**:
- Passwords hashed with bcrypt (cost factor 12)
- No plaintext storage of sensitive data
- Regular automated backups (encrypted)
- GDPR-compliant data deletion

#### 8.6.3 File Upload Security

**Validation**:
- File type verification (magic bytes, not just extension)
- Size limits enforced (50 MB max)
- Malware scanning on upload
- Sandboxed processing environment

**Storage**:
- Randomized filenames (prevent guessing)
- Signed URLs with expiration (1 hour)
- Separate buckets for user data vs. system data

---

## 9. Implementation Roadmap

### 9.1 Development Phases

#### Phase 0: Foundation (Weeks 1-2)
**Goal**: Set up development environment and core infrastructure

**Tasks**:
- [ ] Repository setup (monorepo with frontend/backend)
- [ ] Docker development environment
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Database schema creation
- [ ] Basic authentication system
- [ ] API skeleton with FastAPI
- [ ] React app initialization with TypeScript

**Deliverables**:
- Working dev environment
- Basic auth (register/login)
- Health check endpoints

**Team**: 2 developers (1 frontend, 1 backend)

---

#### Phase 1: MVP - Quick Start (Weeks 3-5)
**Goal**: Single-image augmentation with presets

**Features**:
- Home page with entry points
- Quick Start flow
- 3 preset configurations (Field Curvature, Astigmatism, Stage Positioning)
- Image upload (drag-and-drop)
- Side-by-side preview
- Basic parameter adjustment (strength slider)
- Python code export

**Technical Tasks**:
- [ ] Albumentations integration
- [ ] Image upload endpoint
- [ ] Preview generation API
- [ ] Code generation service
- [ ] Frontend: upload component
- [ ] Frontend: preview comparison component
- [ ] Frontend: parameter controls

**Testing**:
- Unit tests for transform logic
- Integration tests for API
- E2E tests for Quick Start flow

**Deliverables**:
- Functional Quick Start mode
- 5-10 minute time-to-first-augmentation
- Exportable Python code

**Team**: 3 developers (2 frontend, 1 backend) + 1 QA

---

#### Phase 2: Custom Pipeline Builder (Weeks 6-8)
**Goal**: Visual pipeline construction

**Features**:
- Transform library with search
- Drag-and-drop pipeline canvas
- Parameter editors for each transform
- Pipeline testing (multiple images)
- Save/load templates
- YAML/JSON export

**Technical Tasks**:
- [ ] Transform registry and documentation
- [ ] Custom SEM transforms (FieldCurvature, Astigmatism)
- [ ] Pipeline serialization/deserialization
- [ ] Template storage (S3 + database)
- [ ] Frontend: drag-and-drop with dnd-kit
- [ ] Frontend: dynamic parameter forms
- [ ] Frontend: pipeline visualization

**Testing**:
- Unit tests for custom transforms
- Integration tests for pipeline CRUD
- Usability testing with target users

**Deliverables**:
- Functional Custom Pipeline Builder
- 5+ custom SEM transforms
- Template library

**Team**: 4 developers (2 frontend, 2 backend) + 1 QA + 1 designer

---

#### Phase 3: Batch Processing (Weeks 9-11)
**Goal**: Production-scale augmentation

**Features**:
- Input source selection (local folder)
- Processing configuration
- Job queue and execution
- Real-time progress monitoring
- Job history and logs
- Completion notifications

**Technical Tasks**:
- [ ] Celery task queue setup
- [ ] Batch processing worker
- [ ] WebSocket progress updates
- [ ] Job management API
- [ ] S3 output support
- [ ] Frontend: batch configuration wizard
- [ ] Frontend: progress monitoring dashboard
- [ ] Frontend: job history view

**Testing**:
- Load testing (10K+ images)
- Error recovery testing
- Performance benchmarking

**Deliverables**:
- Functional Batch Processing mode
- Scalable to 50K+ images
- Reliable error handling

**Team**: 4 developers (2 frontend, 2 backend) + 1 DevOps + 1 QA

---

#### Phase 4: Polish & Production (Weeks 12-14)
**Goal**: Production-ready release

**Features**:
- Enhanced metrics display
- Grid view for comparisons
- Keyboard shortcuts
- Responsive mobile design
- Documentation and tutorials
- User onboarding flow

**Technical Tasks**:
- [ ] Performance optimization
- [ ] Security audit
- [ ] Accessibility audit (WCAG 2.1 AA)
- [ ] Documentation website
- [ ] Video tutorials (3-5 mins each)
- [ ] Production deployment setup
- [ ] Monitoring and alerting

**Testing**:
- Full regression testing
- Security penetration testing
- Load testing (production scale)
- Beta user testing (10-20 users)

**Deliverables**:
- Production-ready application
- Complete documentation
- Monitoring dashboards
- Launch plan

**Team**: Full team (6 developers + 1 DevOps + 2 QA + 1 tech writer + 1 designer)

---

### 9.2 Release Strategy

#### Beta Release (Week 14)
**Target Audience**: Internal team + select partners (5-10 users)

**Goals**:
- Validate core functionality
- Gather initial feedback
- Identify critical bugs

**Success Criteria**:
- Zero critical bugs
- 80%+ positive feedback
- Average task completion time meets targets

---

#### Public Release (Week 16)
**Target Audience**: General availability

**Marketing Activities**:
- Product launch blog post
- Demo video
- Social media campaign
- Email to waitlist

**Support**:
- Documentation site live
- Community forum open
- Support email monitored

---

### 9.3 Post-Launch Roadmap (Months 2-6)

#### Month 2: Iteration
- Address user feedback from launch
- Performance optimizations based on real usage
- Bug fixes and stability improvements

#### Month 3: Advanced Features
- A/B testing mode for pipeline comparison
- Advanced metrics (more distortion analysis)
- Cloud storage integration (S3, GCS)
- API for programmatic access

#### Month 4: Collaboration
- Share pipelines via URL
- Team workspaces
- Pipeline versioning
- Comments and annotations

#### Month 5: Intelligence
- Auto-optimization suggestions
- Model impact prediction
- Anomaly detection in augmentations
- Recommended pipelines based on dataset

#### Month 6: Scale
- Multi-region deployment
- Enterprise features (SSO, audit logs)
- API rate limit increases
- White-label options

---

### 9.4 Resource Requirements

#### Team Composition

**Development Team**:
- 2× Senior Frontend Engineers (React/TypeScript)
- 2× Senior Backend Engineers (Python/FastAPI)
- 1× DevOps Engineer
- 1× Computer Vision Specialist
- 2× QA Engineers
- 1× Technical Writer
- 1× UX/UI Designer

**Management**:
- 1× Product Manager
- 1× Engineering Manager

**Total**: 11 people

#### Budget Estimate (14-week development)

**Personnel** (assuming blended rate of $150k/year):
- Development team: 11 people × 14 weeks × $2,885/week = ~$444k

**Infrastructure** (development + staging):
- AWS services: ~$2k/month × 3.5 months = ~$7k
- Tools and licenses: ~$1k/month × 3.5 months = ~$3.5k

**Miscellaneous**:
- User research and testing: ~$5k
- Design assets and stock images: ~$2k
- Contingency (10%): ~$46k

**Total Estimated Budget**: ~$507k

---

### 9.5 Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Performance issues with large images | High | Medium | Early load testing, optimization sprints |
| Albumentations API changes | Medium | Low | Pin versions, abstract transform layer |
| User adoption slower than expected | High | Medium | Beta program, gather feedback early |
| Security vulnerabilities | Critical | Low | Security audit, penetration testing |
| Team resource constraints | High | Medium | Prioritize ruthlessly, cut scope if needed |
| Cloud costs exceed budget | Medium | Medium | Monitor costs weekly, optimize early |
| Browser compatibility issues | Low | Low | Test on major browsers from day 1 |
| Complex UX confuses users | Medium | Medium | Extensive usability testing, iterations |

---

## 10. Success Metrics & KPIs

### 10.1 Product Metrics

#### Adoption Metrics
- **Total Users**: Target 100+ active users by Month 3
- **Activation Rate**: 60% of sign-ups complete first augmentation within 7 days
- **DAU/MAU Ratio**: > 30% (indicates stickiness)
- **Retention**: 
  - Week 1: 70%
  - Month 1: 50%
  - Month 3: 40%

#### Engagement Metrics
- **Time to First Augmentation**: < 5 minutes (90th percentile)
- **Augmentations per User per Week**: Average 10+
- **Features Used**:
  - Quick Start: 70% of users
  - Custom Pipeline: 40% of users
  - Batch Processing: 25% of users
- **Pipeline Saves**: Average 2+ saved pipelines per active user

#### Quality Metrics
- **Task Success Rate**: > 85% for primary workflows
- **Error Rate**: < 2% of augmentation operations
- **Support Tickets**: < 5 per 100 users per month
- **NPS Score**: > 50

---

### 10.2 Technical Metrics

#### Performance
- **API Response Time** (p95):
  - Preview generation: < 500ms
  - Pipeline save/load: < 200ms
  - Batch job creation: < 300ms
- **Processing Speed**: > 10 images/sec on standard CPU
- **Uptime**: 99.5% (excluding planned maintenance)

#### Reliability
- **Batch Job Success Rate**: > 99%
- **Error Recovery**: Auto-retry successful in 90% of transient failures
- **Data Loss**: Zero incidents
- **Rollback Success**: 100% of deployments can be rolled back

#### Security
- **Vulnerability SLA**: Critical vulnerabilities patched within 24 hours
- **Authentication Success Rate**: > 99.9%
- **Unauthorized Access Attempts**: 0 successful attempts
- **Data Encryption**: 100% of data at rest and in transit

---

### 10.3 Business Metrics

#### Usage Growth
- **Monthly Active Users Growth**: 20% MoM for first 6 months
- **Augmentation Volume**: 100K+ augmentations per month by Month 3
- **API Calls**: Growing by 25% MoM

#### User Satisfaction
- **Customer Satisfaction (CSAT)**: > 4.5/5
- **Feature Request Implementation**: Top 3 requests addressed within 2 months
- **Response Time to Support**: < 24 hours (business days)

#### Efficiency Gains
- **Time Saved vs. Manual Augmentation**: 10x reduction
- **Code Reusability**: 80% of users reuse saved pipelines
- **Export Success**: 95% of exported code works without modification

---

### 10.4 Measurement & Tracking

#### Analytics Tools
- **Product Analytics**: Mixpanel or Amplitude
- **Error Tracking**: Sentry
- **Performance Monitoring**: New Relic or Datadog
- **User Feedback**: In-app surveys, Hotjar for heatmaps

#### Key Events to Track
```javascript
// User journey events
trackEvent("user_signed_up", { method: "email" });
trackEvent("quick_start_selected", { preset: "field_curvature" });
trackEvent("image_uploaded", { size_mb: 2.5, format: "jpg" });
trackEvent("preview_generated", { time_ms: 230, transforms: 3 });
trackEvent("parameters_adjusted", { parameter: "strength", value: 0.3 });
trackEvent("code_exported", { format: "python" });
trackEvent("pipeline_saved", { num_transforms: 4 });
trackEvent("batch_job_started", { image_count: 1247 });
trackEvent("batch_job_completed", { duration_mins: 125, success_rate: 99.8 });

// Feature usage
trackEvent("transform_added", { transform: "OpticalDistortion" });
trackEvent("pipeline_tested", { image_count: 5, avg_distortion: 0.24 });
trackEvent("template_loaded", { template_id: "community_template_001" });

// Engagement
trackEvent("session_start", { entry_point: "home" });
trackEvent("session_end", { duration_mins: 23, augmentations_created: 8 });
```

#### Dashboard Structure
```
Executive Dashboard:
├── Total Users (MAU, WAU, DAU)
├── Activation Rate
├── Retention Cohorts
└── NPS Score

Product Dashboard:
├── Feature Usage Breakdown
├── User Journey Funnels
├── Task Success Rates
└── Time-to-Value Metrics

Technical Dashboard:
├── API Performance (p50, p95, p99)
├── Error Rates by Endpoint
├── Batch Processing Stats
└── Infrastructure Costs

Support Dashboard:
├── Ticket Volume
├── Response Times
├── Top Issues
└── User Satisfaction
```

---

## 11. Risk Assessment

### 11.1 Technical Risks

#### Risk 1: Albumentations Library Limitations
**Description**: Albumentations may not support all required SEM-specific distortions out of the box.

**Impact**: Medium  
**Probability**: High (expected)

**Mitigation**:
- Design custom transform interface from day 1
- Budget time for developing 3-5 custom transforms
- Contribute custom transforms back to Albumentations (community goodwill)

**Contingency**:
- Fall back to pure OpenCV implementation if Albumentations integration proves difficult
- Estimated 2 additional weeks if full rewrite needed

---

#### Risk 2: Performance at Scale
**Description**: Processing 50K+ images may be slower than acceptable for production use.

**Impact**: High  
**Probability**: Medium

**Mitigation**:
- Load testing from Week 8 onwards
- Optimize hot paths early (profiling)
- Implement GPU acceleration for large batches
- Use multi-processing for CPU-bound operations

**Contingency**:
- Add more Celery workers (horizontal scaling)
- Implement queue prioritization
- Offer overnight/scheduled processing for large batches

---

#### Risk 3: Browser Compatibility Issues
**Description**: Drag-and-drop or image rendering may not work consistently across browsers.

**Impact**: Medium  
**Probability**: Low

**Mitigation**:
- Test on Chrome, Firefox, Safari, Edge from day 1
- Use well-supported libraries (dnd-kit, react-zoom-pan-pinch)
- Progressive enhancement approach

**Contingency**:
- Provide fallback UI for problematic browsers
- Recommend supported browsers in documentation

---

### 11.2 Product Risks

#### Risk 4: User Adoption
**Description**: Users may not understand the value proposition or find the tool too complex.

**Impact**: Critical  
**Probability**: Medium

**Mitigation**:
- Extensive user research in Weeks 1-2
- Beta program with target users (Week 12-14)
- Simplify onboarding flow
- Create compelling video demos
- In-app tooltips and guidance

**Contingency**:
- Iterate quickly based on beta feedback
- Simplify feature set if complexity is an issue
- Offer personalized onboarding sessions for early users

---

#### Risk 5: Feature Creep
**Description**: Stakeholders request additional features that delay launch.

**Impact**: High  
**Probability**: Medium

**Mitigation**:
- Strict adherence to MVP scope
- Product manager gatekeeps feature requests
- "Phase 2" parking lot for good ideas
- Regular scope reviews

**Contingency**:
- Push non-critical features to post-launch
- Accept launch delay only for critical security/usability issues

---

### 11.3 Business Risks

#### Risk 6: Competition
**Description**: A competitor launches similar tool before us.

**Impact**: Medium  
**Probability**: Low (niche market)

**Mitigation**:
- Move quickly to market (14-week timeline)
- Focus on SEM-specific features (differentiation)
- Build community early

**Contingency**:
- Emphasize unique SEM physics-based approach
- Offer superior UX as differentiator
- Consider open-sourcing core library for goodwill

---

#### Risk 7: Budget Overrun
**Description**: Development costs exceed $507k estimate.

**Impact**: High  
**Probability**: Medium

**Mitigation**:
- Weekly budget reviews
- Cut scope before adding resources
- Prioritize ruthlessly
- Use cloud cost optimization tools

**Contingency**:
- Identify features that can be descoped
- Delay Phase 2 features to post-launch
- Seek additional budget approval if critical

---

### 11.4 Security Risks

#### Risk 8: Data Breach
**Description**: User images or pipelines are exposed due to security vulnerability.

**Impact**: Critical  
**Probability**: Low

**Mitigation**:
- Security audit in Week 13
- Penetration testing before launch
- Follow OWASP Top 10 guidelines
- Encrypt all data at rest and in transit
- Regular security patches

**Contingency**:
- Incident response plan prepared
- Cyber insurance policy
- Communication plan for affected users
- Legal counsel on standby

---

#### Risk 9: Compliance Issues
**Description**: Tool doesn't meet GDPR or other data protection regulations.

**Impact**: Critical  
**Probability**: Low

**Mitigation**:
- Legal review of data handling practices
- Implement data deletion on request
- Clear privacy policy and terms of service
- User consent flows

**Contingency**:
- Pause launch until compliant
- Consult with legal experts
- Implement required changes immediately

---

## 12. Appendices

### Appendix A: Glossary

**Terms**:

- **Albumentations**: Fast image augmentation library for PyTorch and TensorFlow
- **Astigmatism**: Optical aberration in SEM lenses causing directional distortion
- **Augmentation**: Process of creating variations of images through transformations
- **Batch Processing**: Applying augmentation to large datasets automatically
- **Defect Detection**: Identifying manufacturing defects in semiconductor wafers
- **Field Curvature**: Distortion in SEM images caused by electromagnetic lens fields
- **Pipeline**: Sequence of transformations applied to images
- **Preset**: Pre-configured augmentation pipeline for common use cases
- **SEM**: Scanning Electron Microscope
- **Transform**: Individual augmentation operation (e.g., rotation, distortion)
- **Wafer**: Thin slice of semiconductor material used in chip manufacturing

### Appendix B: User Research Summary

**Interview Findings** (n=15, conducted Oct 2025):

Key Pain Points:
1. "Augmentation setup takes days, we need it in hours" - ML Engineer
2. "I don't know if the distortions are realistic" - Domain Expert
3. "Hard to explain what I need to the ML team" - Process Engineer
4. "No easy way to test different augmentation strategies" - Data Scientist

Feature Requests:
- Physics-based presets (mentioned by 80%)
- Visual comparison tools (mentioned by 73%)
- Easy export to code (mentioned by 67%)
- Batch processing (mentioned by 60%)

### Appendix C: Competitive Analysis

**Existing Solutions**:

1. **imgaug Library**
   - Pros: Flexible, lots of transforms
   - Cons: Slow, less maintained, no GUI
   - Market Position: Developer tool

2. **Albumentations (library only)**
   - Pros: Fast, well-maintained, popular
   - Cons: No GUI, requires coding
   - Market Position: Developer tool

3. **Roboflow**
   - Pros: Full-featured, GUI, cloud-based
   - Cons: Generic (not SEM-specific), expensive
   - Market Position: General computer vision platform

4. **Custom Internal Tools**
   - Pros: Tailored to specific needs
   - Cons: Lack consistency, hard to maintain
   - Market Position: Per-company solutions

**Our Differentiation**:
- SEM-specific physics-based augmentations
- Balance of GUI and code export
- Focus on semiconductor use case
- Open source core (potential)

### Appendix D: Technology Selection Rationale

**Why React?**
- Most popular frontend framework
- Large ecosystem and community
- Excellent TypeScript support
- Strong performance for interactive UIs

**Why FastAPI?**
- High performance async Python framework
- Automatic API documentation (OpenAPI/Swagger)
- Type hints improve code quality
- Easy integration with ML libraries

**Why Albumentations?**
- Industry standard for image augmentation
- 5-10x faster than alternatives
- Excellent PyTorch/TensorFlow integration
- Active development and community

**Why PostgreSQL?**
- Robust, reliable, proven at scale
- Excellent JSON support (JSONB)
- Strong community and tooling
- Free and open source

**Why Redis?**
- Fast in-memory caching
- Native support for pub/sub (WebSocket)
- Celery broker support
- Simple deployment

### Appendix E: Code Examples

**Example 1: Basic Augmentation Pipeline**
```python
import albumentations as A
import cv2

# Define pipeline
transform = A.Compose([
    A.OpticalDistortion(distort_limit=0.2, p=0.5),
    A.GridDistortion(num_steps=5, distort_limit=0.3, p=0.5),
])

# Load and augment image
image = cv2.imread('wafer.jpg')
augmented = transform(image=image)['image']
cv2.imwrite('wafer_augmented.jpg', augmented)
```

**Example 2: Custom SEM Transform**
```python
from albumentations.core.transforms_interface import ImageOnlyTransform
import cv2
import numpy as np

class FieldCurvatureTransform(ImageOnlyTransform):
    """Simulates SEM field curvature distortion"""
    
    def __init__(self, strength=(10, 30), always_apply=False, p=0.5):
        super().__init__(always_apply, p)
        self.strength = strength
    
    def apply(self, img, strength=20, **params):
        h, w = img.shape[:2]
        
        # Create distortion map
        x, y = np.meshgrid(np.arange(w), np.arange(h))
        cx, cy = w/2, h/2
        
        # Radial distance
        r = np.sqrt((x - cx)**2 + (y - cy)**2)
        r_norm = r / np.max(r)
        
        # Quadratic distortion
        displacement = strength * r_norm**2
        
        x_distorted = x + displacement * (x - cx) / (r + 1e-6)
        y_distorted = y + displacement * (y - cy) / (r + 1e-6)
        
        # Apply distortion
        distorted = cv2.remap(
            img,
            x_distorted.astype(np.float32),
            y_distorted.astype(np.float32),
            cv2.INTER_LINEAR
        )
        
        return distorted
    
    def get_params(self):
        return {"strength": np.random.uniform(*self.strength)}

# Usage
transform = A.Compose([
    FieldCurvatureTransform(strength=(15, 25), p=0.6)
])
```

### Appendix F: API Examples

**Example: Create Batch Job**
```bash
curl -X POST https://api.sem-distortion-tool.com/v1/batch/jobs \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production Batch",
    "pipeline_id": "pipe_123",
    "input": {
      "type": "local",
      "path": "/data/images/"
    },
    "output": {
      "type": "s3",
      "bucket": "my-bucket",
      "prefix": "augmented/"
    },
    "config": {
      "augmentations_per_image": 3,
      "keep_originals": true
    }
  }'
```

**Example: Monitor Job Progress via WebSocket**
```javascript
const ws = new WebSocket('wss://api.sem-distortion-tool.com/v1/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'batch_job',
    job_id: 'job_789'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'progress') {
    console.log(`Progress: ${data.progress.percentage}%`);
    updateProgressBar(data.progress);
  } else if (data.type === 'complete') {
    console.log('Job completed!');
    showNotification('Batch processing complete');
  }
};
```

### Appendix G: References

**Industry Standards**:
- SEMI Standards for semiconductor manufacturing
- ISO 9001 quality management for imaging

**Technical Documentation**:
- Albumentations Documentation: https://albumentations.ai/docs/
- OpenCV Documentation: https://docs.opencv.org/
- FastAPI Documentation: https://fastapi.tiangolo.com/
- React Documentation: https://react.dev/

**Research Papers**:
- "Data Augmentation for Deep Learning" (Shorten & Khoshgoftaar, 2019)
- "Albumentations: Fast and Flexible Image Augmentations" (Buslaev et al., 2020)
- "Scanning Electron Microscopy Image Artifacts" (Smith et al., 2018)

**Related Tools**:
- imgaug: https://github.com/aleju/imgaug
- Kornia: https://kornia.readthedocs.io/
- Augmentor: https://augmentor.readthedocs.io/

---

## Document Approval

**Product Manager**: _____________________ Date: _________

**Engineering Manager**: _____________________ Date: _________

**UX Lead**: _____________________ Date: _________

---

**End of Document**

*This document is a living document and will be updated as the project evolves. All changes should be logged in the Document Change Log.*