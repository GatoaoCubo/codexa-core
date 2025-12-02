# /curso_package | Package for Hotmart

## Purpose
Package all generated content for Hotmart deployment with DRM, metadata, and checklist.

## Usage
```
/curso_package
```

## Prerequisites
Before packaging, ensure you have:
- Video scripts generated (/curso_script)
- Workbooks generated (/curso_workbook)
- Sales materials generated (/curso_sales)
- All content validated (/curso_validate --all)

## Workflow

### Step 1: Execute Builder
```bash
python builders/05_hotmart_package_builder.py --input outputs/ --verbose
```

### Step 2: Validate Compliance
```bash
python validators/05_hotmart_compliance_validator.py --file outputs/hotmart_package/HOTMART_MANIFEST.json
```

### Step 3: Review Checklist
Generated deployment checklist:
1. Upload videos (MP4, H.264, 1080p)
2. Configure DRM (anti-download, watermark)
3. Set up gotejamento (drip schedule)
4. Configure checkout page
5. Test purchase flow
6. Launch

## Output
In outputs/hotmart_package/:
- HOTMART_MANIFEST.json (inventory + specs)
- README_DEPLOY.md (deployment guide)

## Technical Specs (Hotmart)
- **Video**: MP4, H.264 codec, 1080p (720p min)
- **DRM**: Hotmart Player built-in
- **LGPD**: Privacy policy required
- **Garantia**: 7-30 days explicitly stated

## Example
```
User: /curso_package

Agent: Scanning outputs directory...
  - Video scripts: 6 files
  - Workbooks: 6 files
  - Sales materials: 1 file

Agent: Generating Hotmart package...
Agent: [OK] HOTMART_MANIFEST.json created
Agent: [OK] README_DEPLOY.md created
Agent: [OK] Compliance validation: 9.0/10.0 PASSED

Agent: Package ready! Follow README_DEPLOY.md for deployment steps.
```

## Compliance Threshold
- Hotmart Compliance: ≥8.0/10.0 (legal requirements)

---
**Version**: 2.0.0 | **Builder**: 05_hotmart_package_builder.py | **Validator**: 05_hotmart_compliance_validator.py
