# 📬 Boone Envelope Reference Guide

This reference guide is designed to help the Boone Quote Assistant intelligently handle questions, quotes, and upsells related to envelope printing and mailing. It includes technical specs, use cases, conversational triggers, and smart follow-up logic for each envelope type.

---

## ✉️ Envelope Categories

### Personal & Event Envelopes
| Name | Size | Max Insert | Common Use | Flap Type | Notes |
|------|------|-------------|-------------------------------|------------|-------|
| **A1** | 3.625" x 5.125" | 3.5" x 5" | RSVP cards | Tapered | Flap on long edge |
| **A2** | 4.375" x 5.75" | 4.25" x 5.5" | Invitations, greeting cards | Tapered | Flap on long edge |
| **A6** | 4.75" x 6.5" | 4.5" x 6.25" | Save-the-dates | Tapered | Flap on long edge |
| **A7** | 5.25" x 7.25" | 5" x 7" | Wedding invites | Tapered | Flap on long edge |

### Business & Corporate Envelopes
| Name | Size | Max Insert | Use Case | Flap Type | Notes |
|------|------|-------------|--------------------------|------------|-------|
| **#6-3/4 Remittance** | 3.625" x 6.5" | 3.375" x 6.25" | Fundraising | Tapered | Inside flap printable |
| **#9** | 3.875" x 8.875" | 3.625" x 8.625" | Reply/donation | Tapered | Fits inside #10 |
| **#9 Remittance** | 3.875" x 8.875" | 3.625" x 8.625" | Donation return | Tapered | Inside printable flap |
| **#10** | 4.125" x 9.5" | 3.875" x 9.25" | Business mail | V-shape | Most common style |
| **#10 Window** | 4.125" x 9.5" | 3.875" x 9.25" | Address visible | Tapered | Left window |
| **#10 Window Security** | 4.125" x 9.5" | 3.875" x 9.25" | Confidential mail | V-shape | Internal tint |

### Catalog & Booklet Envelopes
| Name | Size | Max Insert | Use Case | Flap Type | Notes |
|------|------|-------------|---------------------------|------------|-------|
| **6x9 Open Side** | 6" x 9" | 5.75" x 8.75" | Folded docs | Tapered | Long edge flap |
| **6x9.5 Open Side** | 6" x 9.5" | 5.75" x 9.25" | Folded docs | Tapered | - |
| **9x12 Open Side** | 9" x 12" | 8.75" x 11.75" | Booklets, flats | Tapered | - |
| **10x13 Open Side** | 10" x 13" | 9.75" x 12.75" | Oversize docs | Tapered | - |

### Coin Envelopes
| Name | Size | Use Case |
|------|------|------------------|
| **#1** | 2.25" x 3.5" | Tiny parts, coins, labels |
| **#3** | 2.5" x 4.25" | Small hardware, keys |
| **#6** | 3.625" x 6" | Internal transfers |
| **Mini-lope** | 3.625" x 2.125" | Tickets, swatches |

---

## 🧠 Conversational Triggers & Follow-ups

### Detectable Terms
If the user says:
- "folded letter into envelope" or mentions #10 window → **Ask if they want to quote envelopes too**
- Mentions reply/donation → **Recommend #6-3/4 or #9 remittance**
- "Security envelope" → **Offer window security w/ tinted interior**
- "Wedding" or "invite" → **Prompt A-series envelopes (A6, A7)**
- Mentions flap printing or branding → **Ask if they need flap printed or two-sided**

### Follow-up Prompts
- Would you like to quote envelopes as a separate item?
- Should the envelopes be printed with your logo or return address?
- Is machine insertion required?
- Should the envelope display the recipient address through a window?

### Inserting Rules
- Insert must be **1/2" narrower** and **1/4" shorter** than envelope
- If not: **hand insertion required → higher cost and longer time**

---

## 🔍 Boone-Specific Practices

- Always offer envelopes as an optional **add-on line item**
- Prompt envelope upsell if quoting:
  - Letters
  - Appeals
  - Kits (MedPrint)
  - Billing docs
  - Statements
  - Donation or membership campaigns

### Envelope Print Types
- Full Color / Black / Spot PMS
- Flap-only print (note special setup)
- Dual-side print (Remittance-specific)

### Envelope Paper Stocks
- **Wove** ✨: Smooth, white, economical and most widely used for standard business mail
- **Recycled** ♻️: Sustainable, earthy feel; made from post-consumer waste
- **Smooth** 🏋️‍♂️: Non-textured, clean appearance
- (Additional options: Kraft, Specialty, Tear-resistant for specific use cases)

### Texture / Finish Options
- **Smooth** (Wove)
- **Linen** (subtle fabric feel)
- **Laid** (lined, vintage look)
- **Felt** (soft textured)
- **Embossed** (raised patterns)
- **Metallic/Foil** (shimmering surface)

### ⛔️ Never Offer These Options
- Glossy stock
- Cover-weight paper

> Envelopes should **never be quoted** using glossy or cover-weight paper. Default to uncoated text or standard envelope stock unless specified otherwise.

### PrintPapa Types
- Envelope types supported: Regular, Window, Security, Self-Seal, Remittance
- Remittance: flaps open for reply/donation forms
- Print on flap means printing full flap surface
- Link: [PrintPapa Envelope Options](https://www.printpapa.com/eshop/pc/Envelopes-c62.htm)

### USPS Considerations
- Smallest mailable size: 3.5" x 5"
- Max mailable size: 6.125" x 11.5"
- Square envelopes require **extra postage**
- Aspect ratio must be between 1.3 and 2.5 or incur extra charges

> ✅ Always verify that quoted envelope size fits the content inside.
