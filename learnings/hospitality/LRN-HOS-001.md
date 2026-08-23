# LRN-HOS-001: Hotel Industry Website Structure & Content Model

## Metadata
- **Date:** 2026-08-23
- **Category:** hospitality
- **Subcategory:** hotel-consulting, content-architecture, industry-knowledge
- **Source Project:** TES-Krishna (TES Hospitality — hotel consultants in Mangalore)
- **Confidence:** High
- **Reusability:** Domain-Specific (hospitality/hotel/tourism sector)

## Context
Built website for TES Hospitality — a hotel management consulting firm. The content structure revealed a consistent pattern for hospitality B2B service websites.

## Learning

### Hotel Consulting Website Content Model

```
Homepage Structure (B2B Hotel Services)
├── Hero
│   ├── Value proposition (revenue/growth focused)
│   ├── Years of experience (trust signal)
│   └── CTA: "Explore Services" / "Contact"
│
├── Brand Introduction
│   ├── Company meaning/acronym expansion
│   ├── Brief mission statement
│   └── Service philosophy
│
├── About / Expertise
│   ├── Specific geographic focus (e.g., "Mangalore")
│   ├── Approach description ("align owners' vision")
│   └── Differentiation from competitors
│
├── Strengths / Why Choose Us
│   ├── Years of experience
│   ├── Collaboration philosophy
│   ├── Profit/service balance
│   ├── Market understanding
│   └── Sales & marketing expertise
│
├── Services (Revenue-focused)
│   ├── Dynamic Rate Management
│   ├── Booking Engine / OTA Distribution
│   ├── Comp Set Analysis
│   ├── Promotional Offers
│   ├── Field Sales
│   └── Performance Analytics
│
├── Process / How It Works
│   ├── Step-by-step methodology
│   ├── Key metrics tracked (ARR, RevPAR, Occupancy)
│   └── Competitive positioning approach
│
├── Department Benefits (operational)
│   ├── Front Office & HR (SOPs, training, reporting)
│   ├── Sales & Marketing (budgets, market generation)
│   ├── Housekeeping (hygiene, scheduling, SOPs)
│   ├── F&B Service (training, upselling, revenue)
│   ├── Stores & Purchase (quality, cost control)
│   └── Engineering (maintenance, AMC, servicing)
│
├── Contact
│   ├── Director/founder name and title
│   ├── Phone (with click-to-call)
│   ├── Email
│   ├── Physical address
│   └── Contact form
│
└── Footer
    ├── Quick links
    ├── Service list
    ├── Contact info
    └── Copyright
```

### Industry-Specific Design Considerations

| Element | Hotel Industry Standard |
|---------|----------------------|
| **Colors** | Gold/amber (luxury, warmth), Teal (trust, professionalism), Red (energy, brand accent) |
| **Imagery** | Hotel exteriors, luxury rooms, lobbies, swimming pools, restaurants |
| **Typography** | Mix of elegant serif (headings) + clean sans-serif (body) + script (accents) |
| **Trust signals** | Years experience, hotels managed, revenue growth % |
| **Language** | Revenue-focused: "RevPAR," "ARR," "occupancy," "comp set," "OTA distribution" |
| **CTA style** | Warm, inviting: "Partner With Us" not "Buy Now" |

### Key Industry Terms (for accurate content)
- **OTA** — Online Travel Agency (Booking.com, MakeMyTrip, etc.)
- **RevPAR** — Revenue Per Available Room
- **ARR** — Average Room Rate
- **Comp Set** — Competitive Set (comparable hotels in same market)
- **SOP** — Standard Operating Procedure
- **AMC** — Annual Maintenance Contract
- **F&B** — Food & Beverage
- **Dynamic Pricing** — Adjusting rates based on demand/supply

## Evidence
TES Hospitality PDF contained exactly this structure — validating it as an industry-standard content architecture. The 6-department breakdown (HR, Sales, Housekeeping, F&B, Stores, Engineering) appears to be universal for hotel management services.

## Application Rules
**Apply when:**
- Building website for hotel consulting firm
- Building website for hotel management company
- Building hospitality B2B service site
- Client is in tourism/hotel sector

**Do NOT apply when:**
- Building a hotel booking platform (B2C — different structure)
- Building a restaurant website (simpler, menu-focused)
- Client is pure digital marketing (different terminology)

## Related
- LRN-AI-001 (PDF extraction pipeline used to discover this model)
- LRN-DES-002 (Color extraction from hospitality brochure)
