# LRN-DES-002: PDF-to-Website Color Extraction Pipeline

## Metadata
- **Date:** 2026-08-23
- **Category:** design-systems
- **Subcategory:** color-extraction, automation, design-fidelity
- **Source Project:** TES-Krishna (TES Hospitality website)
- **Confidence:** High
- **Reusability:** Universal

## Context
Client provided a PDF brochure (36.5MB, 11 pages) as the sole design reference. Needed to extract the exact brand colors, understand the visual language, and recreate the feel in code — without Figma, design tokens, or brand guidelines.

## Learning
A reliable pipeline for extracting design intent from PDF documents:

### Step 1: PDF → Images
```bash
# Install poppler-utils for pdftoppm
pdftoppm -png -r 150 input.pdf output_dir/page
```
- Use 150 DPI for color analysis (300 DPI for detail inspection)
- Generates one PNG per page

### Step 2: Color Palette Extraction
```python
from PIL import Image

def get_dominant_colors(image_path, num_colors=8):
    img = Image.open(image_path)
    img = img.resize((150, 150))  # Downsample for speed
    img = img.convert('RGB')
    img_quantized = img.quantize(colors=num_colors, method=2)
    palette = img_quantized.getpalette()
    colors = []
    for i in range(num_colors):
        r, g, b = palette[i*3], palette[i*3+1], palette[i*3+2]
        colors.append(f"#{r:02x}{g:02x}{b:02x}")
    return colors
```

### Step 3: Color Interpretation
Raw extracted colors need interpretation:
- **Filter noise:** Remove near-white (#f8f8f8+) and near-black (#1a1a1a−) unless they dominate
- **Find brand colors:** The 3-5 most saturated non-neutral colors
- **Build palette:** Create 50/100/default/dark variants of each brand color
- **Cross-validate:** Compare colors across multiple pages — consistent ones are brand, unique ones are decorative

### Step 4: Text Content Extraction
```python
from pdfminer.high_level import extract_text
text = extract_text('input.pdf', maxpages=20)
```
- Gives structured text with rough section ordering
- Headings typically appear as ALL CAPS or isolated short lines
- Body text appears as longer paragraphs

### Step 5: Visual Language Analysis
Read the page images to identify:
- Layout patterns (split sections, full-width, cards)
- Decorative elements (shapes, patterns, textures)
- Typography style (serif/sans-serif, script fonts, weight usage)
- Photo treatment (rounded corners, overlays, compositions)

## Evidence
From TES-Krishna PDF:
- Extracted: Gold `#D28911`, Teal `#0D8D93`, Red `#C20202`
- Refined to: Gold `#D4920F`, Teal `#0B7A80`, Red `#B91C1C` (slightly adjusted for screen)
- Identified: torn paper edges, blob shapes, dot patterns, script font accents
- Result: Client recognized the visual identity immediately

## Application Rules
**Apply when:**
- Client provides PDF/print materials as design reference
- No Figma/Sketch files available
- Need to match existing brand without formal guidelines
- Building a website from a brochure or presentation

**Do NOT apply when:**
- Proper design files exist (use those directly)
- Client wants a completely new design (PDF is just content source)
- PDF is text-only with no visual design

## Related
- LRN-DES-001 (Extracted colors need contrast validation)
- LRN-AI-001 (PDF content extraction for structure)
