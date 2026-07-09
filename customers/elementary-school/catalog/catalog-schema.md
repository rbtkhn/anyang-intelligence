# Catalog Schema

This schema is the shared shape for both:

- `khan_academy_main_catalog`
- `khan_kids_curated_catalog`

## Required Fields

- `stable_id`
- `source_product`
- `title`
- `subject_domain`
- `age_grade_band`
- `content_type`
- `evidence_status`
- `import_method`

## Optional Fields

- `standards_tags`
- `source_url`
- `source_note`
- `operator_notes`

At least one provenance field should be present:

- `source_url`
- `source_note`

## Allowed Values

### `source_product`

- `khan_academy_main_catalog`
- `khan_kids_curated_catalog`

### `evidence_status`

- `official-public-web`
- `manual-curated`
- `manual-in-app-capture`
- `operator-note`

### `import_method`

- `public-web-manifest`
- `manual-curated`
- `manual-in-app-capture`

## Interpretation Rules

- `khan_academy_main_catalog` should normally use:
  - `evidence_status: official-public-web`
  - `import_method: public-web-manifest`
- `khan_kids_curated_catalog` should normally use:
  - `evidence_status: manual-curated` or `manual-in-app-capture`
  - `import_method: manual-curated` or `manual-in-app-capture`

## Example Entry

```yaml
catalog_entries:
  - stable_id: khan-main-math-early-math
    source_product: khan_academy_main_catalog
    title: Early math
    subject_domain: Math
    age_grade_band: early elementary
    standards_tags:
      - common-core
    content_type: course-domain
    source_url: https://www.khanacademy.org/math
    source_note: official Khan Academy public web structure
    evidence_status: official-public-web
    import_method: public-web-manifest
    operator_notes: Candidate reinforcement directory for families needing extra math practice.
```
