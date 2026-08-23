# LRN-AI-001: PDF Content Extraction for Website Generation

## Metadata
- **Date:** 2026-08-23
- **Category:** ai-patterns
- **Subcategory:** content-extraction, source-analysis, automation
- **Source Project:** TES-Krishna (TES Hospitality website)
- **Confidence:** High
- **Reusability:** Universal

## Context
Client shared a Google Drive PDF (36.5MB, 11 pages) containing all website content — text, images, branding, and layout design. Needed to extract structured data suitable for code generation.

## Learning
A complete AI-assisted pipeline for converting PDF brochures into website code:

### Phase 1: Acquisition
```bash
# Download from Google Drive (public link)
curl -L "https://drive.google.com/uc?export=download&id={FILE_ID}" -o file.pdf

# For large files (>25MB), Google may require confirmation:
# The direct download URL pattern bypasses the confirmation page
```

### Phase 2: Content Extraction (parallel)

**Text extraction (pdfminer.six):**
```python
from pdfminer.high_level import extract_text
text = extract_text('file.pdf', maxpages=20)
# Returns structured text with rough layout preservation
```

**Visual extraction (pdftoppm + PIL):**
```bash
pdftoppm -png -r 150 file.pdf pages/page  # 150 DPI for analysis
```
```python
from PIL import Image
# Quantize to extract dominant colors
img.quantize(colors=8, method=2).getpalette()
```

### Phase 3: Content Structuring
From raw extracted text, identify:
1. **Headings:** ALL CAPS lines, short isolated phrases
2. **Sections:** Group by heading → body text blocks
3. **Lists:** Lines starting with bullets (•, -, →)
4. **Contact info:** Phone patterns, email patterns, addresses
5. **CTAs:** "Know More", "Contact Us", "Join Us" phrases

### Phase 4: Design Analysis
From page images, identify:
1. **Color palette:** Top 3-5 saturated colors across pages
2. **Layout style:** Split screens, full-width, card-based
3. **Typography:** Serif/sans/script combinations
4. **Decorative elements:** Shapes, patterns, borders
5. **Image style:** Photography treatment, overlay styles

### Phase 5: Code Generation
Map structured content → component tree:
```
PDF Section → React Component
Heading → <h2> with brand styling
Body text → <p> with proper spacing
Contact → Contact card component
List items → Icon + text cards
```

## Evidence
TES-Krishna: 36.5MB PDF → 11 pages extracted → 10 React components → deployed website in single session. Content fidelity: 100% (all text, contact info, section structure preserved).

## Application Rules
**Apply when:**
- Client provides PDF/brochure as content source
- No CMS or content API exists
- Building first version of a website from print materials
- Client can't provide content in other formats

**Limitations:**
- Complex table layouts may not extract cleanly
- Embedded images in PDF can't be easily extracted (use external image sources)
- PDF text extraction is fragile — always verify against visual pages
- Very design-heavy PDFs (all images, no text) need manual transcription

## Related
- LRN-DES-002 (Color extraction pipeline)
- LRN-AI-002 (Iterative redesign feedback loop)
- LRN-HOS-001 (Hotel industry content model)
