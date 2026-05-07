---
name: Precision & Clarity
colors:
  surface: '#10131b'
  surface-dim: '#10131b'
  surface-bright: '#363942'
  surface-container-lowest: '#0b0e15'
  surface-container-low: '#181b23'
  surface-container: '#1c1f27'
  surface-container-high: '#272a32'
  surface-container-highest: '#32353d'
  on-surface: '#e0e2ed'
  on-surface-variant: '#c1c6d7'
  inverse-surface: '#e0e2ed'
  inverse-on-surface: '#2d3039'
  outline: '#8b90a0'
  outline-variant: '#414754'
  surface-tint: '#aec6ff'
  primary: '#aec6ff'
  on-primary: '#002e6b'
  primary-container: '#0070f3'
  on-primary-container: '#ffffff'
  inverse-primary: '#0059c5'
  secondary: '#dbb8ff'
  on-secondary: '#470083'
  secondary-container: '#6807ba'
  on-secondary-container: '#d0a6ff'
  tertiary: '#ffb596'
  on-tertiary: '#581e00'
  tertiary-container: '#ca4e00'
  on-tertiary-container: '#fffeff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#aec6ff'
  on-primary-fixed: '#001a43'
  on-primary-fixed-variant: '#004397'
  secondary-fixed: '#efdbff'
  secondary-fixed-dim: '#dbb8ff'
  on-secondary-fixed: '#2b0052'
  on-secondary-fixed-variant: '#6600b7'
  tertiary-fixed: '#ffdbcd'
  tertiary-fixed-dim: '#ffb596'
  on-tertiary-fixed: '#360f00'
  on-tertiary-fixed-variant: '#7d2d00'
  background: '#10131b'
  on-background: '#e0e2ed'
  surface-variant: '#32353d'
typography:
  h1:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  h2:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  h3:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: -0.01em
  body-base:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: 0em
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  code:
    fontFamily: monospace
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.4'
    letterSpacing: 0em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
---

## Brand & Style

The design system is engineered for high-performance productivity, targeting students, career services, and HR professionals. It prioritizes information density without sacrificing legibility. The brand personality is professional, systematic, and utilitarian, evoking an emotional response of organized control and progress.

The design style is **Minimalist-Pro**, drawing inspiration from modern engineering tools. It utilizes a monochromatic foundation to allow user-generated content (certificates, internship logos) and status-driven data to remain the focal point. The interface avoids unnecessary decoration, relying instead on structural integrity, refined typography, and purposeful motion.

## Colors

The color architecture is built on a high-contrast dark-mode scale to ensure a "pro-tool" feel, focusing on readability and reduced eye strain during long sessions.

- **Primary Actions:** "Action Blue" (#0070F3) is reserved exclusively for primary calls-to-action, active states, and focus indicators.
- **Secondary/Status:** "Vibrant Purple" (#7928CA) is utilized for secondary milestones, achievements, and "complete" states.
- **Neutrals:** The palette is anchored in a deep black canvas. #111 acts as the base background with #1A1A1A providing surface elevation. Borders and dividers use low-light grays to maintain structure without creating visual noise.
- **Semantic Logic:** Success, Warning, and Error states use low-saturation variants of Green, Amber, and Red respectively, ensuring they remain legible against dark backgrounds without competing with the primary Brand colors.

## Typography

This design system utilizes **Inter** for all UI elements to maintain a systematic, neutral appearance. 

The typographic hierarchy is established through a mix of weight and letter spacing. Headings use semi-bold weights with negative tracking to appear tight and cohesive. Body text utilizes a generous 1.6 line-height to ensure readability during long-form data entry or review. Small labels use uppercase with increased letter spacing to distinguish them from interactive text.

## Layout & Spacing

This design system employs a strict **4px/8px grid system**. All padding, margins, and component heights must be multiples of 4px. 

The dashboard uses a **Fixed-Fluid Hybrid Grid**:
- **Sidebar:** Fixed width (240px) for navigation.
- **Main Content:** Fluid container with a max-width of 1440px to ensure line lengths remain optimal on ultra-wide monitors.
- **Gutter Logic:** 24px gutters between major layout sections and 16px gutters between cards within a section.

Consistent whitespace is prioritized to prevent the density of internship tracking data from feeling overwhelming.

## Elevation & Depth

Hierarchy is established through **tonal layering** and **low-contrast outlines** rather than heavy shadows. In this dark mode environment, depth is signaled by elements becoming lighter as they "rise" toward the user.

1.  **Level 0 (Base):** The main background (#111111).
2.  **Level 1 (Cards/Containers):** Slightly offset surface (#1A1A1A) with a 1px border (#333333).
3.  **Level 2 (Dropdowns/Modals):** A lighter surface (#242424) with a soft, diffused ambient shadow (25% opacity black) and a slightly more prominent border.

Shadows should never feel "heavy." They act as subtle depth cues to indicate that an element is floating above the primary workspace.

## Shapes

The shape language is balanced and professional. A **Rounded** profile is used throughout the design system to soften the technical UI.

- **Standard Components:** Buttons, input fields, and small cards use an **8px** radius.
- **Large Containers:** Dashboard widgets and main content blocks use a **16px** radius.
- **Inner Elements:** Elements nested inside containers (like progress bars inside a card) use a **4px** radius to maintain visual harmony.

This geometric approach ensures the UI feels modern and approachable while maintaining the precision of a professional tool.

## Components

- **Buttons:** Primary buttons use a solid Action Blue or Vibrant Purple background with white text. Secondary buttons use a transparent background with a 1px neutral border (#444). Padding is strictly 8px (vertical) and 16px (horizontal). Corner radius is 8px.
- **Chips/Badges:** Used for status tracking. In dark mode, use a low-saturation background (15% opacity of the status color) with high-contrast text in the same hue.
- **Input Fields:** 1px border (#333) with **8px** radius. On focus, the border transitions to Action Blue with a subtle 2px glow.
- **Lists:** Data-heavy lists should use subtle 1px dividers (#222). Hover states for list items use a #1F1F1F background tint.
- **Cards:** No shadows for standard dashboard cards; depth is communicated solely via tonal shifts and a 1px border (#333). Large containers use a **16px** radius.
- **Progress Bars:** Thin (4px-6px height) with a **4px** rounded track. Use Action Blue for standard progress and Vibrant Purple for "Milestone Completion."