# Pattern: Design System Enforcement

Sources: v0 (Vercel), Lovable

## When to Use

- Agent generates UI code (HTML, React, CSS)
- Visual consistency is required across outputs
- Specific design tokens and component libraries must be used
- Ad-hoc styling should be prohibited

## v0's Implementation

### Color System

```
zinc-based neutral palette:
  --background: oklch(1 0 0)
  --foreground: oklch(0.145 0 0)
  --primary: oklch(0.205 0.006 285.885)
  --secondary: oklch(0.97 0.001 286.375)
```

### Typography

```
Font family: Geist Sans (body), Geist Mono (code)
Base size: 16px (1rem)
Scale: 0.875rem / 1rem / 1.125rem / 1.25rem / 1.5rem / 2rem / 2.5rem / 3rem
```

### Component Library

Enforce specific components: shadcn/ui with Radix primitives. List all available components and their import paths.

### Framework Requirements

```
- Next.js App Router (NO Pages Router)
- Server Components by default
- Tailwind CSS for styling
- Lucide React for icons
- Recharts for data visualization
```

## Lovable's Implementation

### Semantic Token Requirements

```css
:root {
  --background: /* page background */
  --foreground: /* default text */
  --primary: /* buttons, links, accents */
  --primary-foreground: /* text on primary */
  --secondary: /* secondary UI elements */
  --muted: /* disabled, placeholder text */
  --border: /* dividers, input borders */
  --ring: /* focus indicators */
}
```

### Enforcement Rules

- Only use colors defined in the design system
- No inline color values (no `#ff0000`, no `rgb()`)
- All interactive elements must have focus indicators via `--ring`
- Discussion-first workflow: discuss design direction before coding

## Template

```xml
<design_system>
Color palette:
  Primary: [value]
  Secondary: [value]
  Background: [value]
  Foreground: [value]

Typography:
  Heading font: [family]
  Body font: [family]
  Scale: [sm / base / lg / xl / 2xl / 3xl]

Components: Use [library] exclusively.
  Available: Button, Card, Dialog, Input, Select, Table, Tabs, Toast

Icons: [library] only. No inline SVGs.

Rules:
- No ad-hoc colors. All colors via design tokens.
- No inline styles. All styling via [framework].
- All interactive elements need hover + focus states.
</design_system>
```

## Key Principle

Constraint breeds consistency. By prohibiting ad-hoc values and requiring semantic tokens, the agent's output is always visually coherent. The design system is not optional guidance — it is a hard constraint embedded in the system prompt.
