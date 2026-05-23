---
name: Obsidian Moss
colors:
  surface: '#101416'
  surface-dim: '#101416'
  surface-bright: '#353a3c'
  surface-container-lowest: '#0a0f10'
  surface-container-low: '#181c1e'
  surface-container: '#1c2022'
  surface-container-high: '#262b2c'
  surface-container-highest: '#313537'
  on-surface: '#dfe3e5'
  on-surface-variant: '#c4c8c0'
  inverse-surface: '#dfe3e5'
  inverse-on-surface: '#2d3133'
  outline: '#8e928b'
  outline-variant: '#444842'
  surface-tint: '#bbcbb6'
  primary: '#bbcbb6'
  on-primary: '#263425'
  primary-container: '#6b7a68'
  on-primary-container: '#ffffff'
  inverse-primary: '#546251'
  secondary: '#c5c7c8'
  on-secondary: '#2e3132'
  secondary-container: '#444748'
  on-secondary-container: '#b3b5b6'
  tertiary: '#c6c6c7'
  on-tertiary: '#2f3132'
  tertiary-container: '#757677'
  on-tertiary-container: '#ffffff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d7e7d2'
  primary-fixed-dim: '#bbcbb6'
  on-primary-fixed: '#121f11'
  on-primary-fixed-variant: '#3c4a3b'
  secondary-fixed: '#e1e3e4'
  secondary-fixed-dim: '#c5c7c8'
  on-secondary-fixed: '#191c1d'
  on-secondary-fixed-variant: '#444748'
  tertiary-fixed: '#e2e2e3'
  tertiary-fixed-dim: '#c6c6c7'
  on-tertiary-fixed: '#1a1c1d'
  on-tertiary-fixed-variant: '#454748'
  background: '#101416'
  on-background: '#dfe3e5'
  surface-variant: '#313537'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '300'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '400'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  title-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-label:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
  container-max-width: 1440px
---

## Brand & Style

This design system is built upon the philosophy of **Quiet Luxury** for technical environments. It rejects the hyper-stimulated aesthetic of typical AI dashboards in favor of a serene, focused interface that prioritizes cognitive clarity. The brand personality is "The Sophisticated Architect"—precise, calm, and effortlessly capable.

The visual style is a blend of **Minimalism** and **Tonal Layering**. It leverages deep, monochromatic foundations with rare, organic accents. By maintaining a low information density and generous negative space, the system ensures that complex AI data feels approachable rather than overwhelming. The emotional response should be one of professional confidence and quiet focus.

## Colors

The palette is anchored in deep charcoal and obsidian tones to minimize eye strain and establish a premium technical feel.

- **Primary (Moss Green):** Used exclusively for meaningful actions, active states, or subtle data highlights. It is desaturated and organic, avoiding the "neon" tropes of tech.
- **Surface Tiers:** Depth is created through a progression of dark grays. The base background is nearly black, with cards and containers using slightly lighter "charcoal" values.
- **Typography Colors:** Primary text uses a soft off-white (#E1E3E4) to reduce high-contrast glare. Secondary and disabled text utilizes a muted "Cloud" gray (#808486) to maintain hierarchy.

## Typography

This design system utilizes **Inter** for its neutral, highly legible characteristics. The hierarchy is established through weight and tracking rather than extreme size differentials.

- **Display & Headlines:** Use lighter weights (300-400) for large titles to maintain an elegant, editorial feel. 
- **Labels:** Small labels use a semi-bold weight with increased letter-spacing and uppercase styling to provide clear structural markers without dominating the visual field.
- **Monospace Integration:** For technical AI outputs (code snippets, parameters), **JetBrains Mono** is used sparingly to denote raw data.
- **Readability:** Line heights are kept generous (1.5x - 1.6x for body text) to support the "breathable" design intent.

## Layout & Spacing

The layout philosophy follows a **Fixed-Fluid Hybrid** model. Content is centered within a max-width container for desktop viewing to prevent excessive line lengths and horizontal scanning fatigue.

- **Grid:** A 12-column grid is used for primary dashboard layouts, transitioning to a single-column stack on mobile.
- **Rhythm:** A 4px baseline unit governs all spacing. Vertical margins between sections are intentionally large (64px - 96px) to enforce the "Quiet Luxury" aesthetic.
- **Density:** Elements are given significant internal padding. A "comfortable" setting is the default, ensuring that no two interactive elements feel crowded.

## Elevation & Depth

In this system, depth is communicated through **Tonal Tiers** and **Low-Contrast Outlines** rather than aggressive shadows.

1.  **Level 0 (Base):** The dark background (#0F1111).
2.  **Level 1 (Containers):** Slightly lighter surface (#161819) with a 1px border of #2A2D2E.
3.  **Level 2 (Interactive):** Elements that are hoverable or active may use a very subtle ambient shadow (0px 4px 20px rgba(0,0,0,0.5)) or a slight moss-green border tint.
4.  **Glassmorphism:** Reserved for overlays (modals, dropdowns). Use a 12px backdrop blur with a 40% transparent surface color to maintain context of the underlying dashboard.

## Shapes

The shape language is consistently **Rounded**. This softens the technical nature of the dashboard, making the AI feel more organic and less "brutal."

- **Standard Radius:** 8px (0.5rem) for cards and input fields.
- **Large Radius:** 16px (1rem) for major containers or featured sections.
- **Circular/Pill:** Reserved for status indicators and specific toggle switches to differentiate them from actionable buttons.
- **Borders:** When borders are used, they are never pure white or high-contrast. They should always be a 1px stroke that is only 5-10% lighter than the surface they sit on.

## Components

- **Buttons:** Primary buttons use a solid Moss Green background with dark charcoal text. Secondary buttons are ghost-style with a subtle gray border and no background fill.
- **Input Fields:** Use a dark, recessed background (#0D0E0E) with no border until focused. Upon focus, the border transitions to a soft Moss Green.
- **Chips/Badges:** Small, pill-shaped elements with low-opacity Moss Green fills (15% opacity) and solid Moss Green text for status indicators.
- **Cards:** Cards should not have shadows by default. Use a 1px solid border (#2A2D2E) to define the boundary against the background.
- **Data Visualizations:** Charts should utilize a monochromatic palette of grays, with the Moss Green reserved only for the "Target" or "Current" data point to draw immediate focus.
- **Lists:** Use generous 16px vertical padding between list items and subtle 1px dividers that do not span the full width of the container.