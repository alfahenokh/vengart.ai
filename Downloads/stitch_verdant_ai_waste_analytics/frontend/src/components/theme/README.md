# Obsidian Moss Theme System

The Obsidian Moss theme system provides a consistent, sophisticated design language for the Verdant AI Integrated Dashboard. Built on the philosophy of "Quiet Luxury" for technical environments, it emphasizes cognitive clarity and professional confidence.

## Features

- **Complete Color Palette**: Full Obsidian Moss color system with surface tiers, primary/secondary/tertiary colors, and semantic colors
- **Dark Mode Support**: Built-in dark mode with localStorage persistence
- **Responsive Design**: Breakpoint utilities for mobile (320px) to desktop XL (1920px)
- **Typography System**: Inter font family with predefined text styles
- **Component Styles**: Pre-built Tailwind classes for buttons, cards, inputs, badges, and more
- **Theme Context**: React Context API for accessing and modifying theme throughout the app

## Usage

### ThemeProvider

Wrap your application with the `ThemeProvider` to enable theme support:

```tsx
import { ThemeProvider } from './components/theme';

function App() {
  return (
    <ThemeProvider initialDarkMode={true}>
      <YourApp />
    </ThemeProvider>
  );
}
```

### useTheme Hook

Access theme values and controls in any component:

```tsx
import { useTheme } from './components/theme';

function MyComponent() {
  const { theme, isDarkMode, toggleDarkMode, updateThemeColors } = useTheme();

  return (
    <div>
      <p style={{ color: theme.colors.primary }}>Primary Color Text</p>
      <button onClick={toggleDarkMode}>
        Toggle {isDarkMode ? 'Light' : 'Dark'} Mode
      </button>
    </div>
  );
}
```

### useResponsive Hook

Get responsive breakpoint information:

```tsx
import { useResponsive } from '../../hooks/useResponsive';

function ResponsiveComponent() {
  const { isMobile, isTablet, isDesktop, width, breakpoint } = useResponsive();

  return (
    <div>
      {isMobile && <MobileView />}
      {isTablet && <TabletView />}
      {isDesktop && <DesktopView />}
      <p>Current width: {width}px</p>
      <p>Breakpoint: {breakpoint}</p>
    </div>
  );
}
```

## Tailwind CSS Classes

### Buttons

```tsx
<button className="btn-primary">Primary Button</button>
<button className="btn-secondary">Secondary Button</button>
```

### Cards

```tsx
<div className="card">Standard Card</div>
<div className="card-elevated">Elevated Card with Shadow</div>
<div className="card-interactive">Interactive Hover Card</div>
```

### Input Fields

```tsx
<input type="text" className="input-field" placeholder="Enter text..." />
<textarea className="input-field" placeholder="Message..." />
```

### Badges

```tsx
<span className="badge">Primary Badge</span>
<span className="badge-secondary">Secondary Badge</span>
<span className="badge-error">Error Badge</span>
```

### Status Indicators

```tsx
<span className="status-active"></span>
<span className="status-idle"></span>
<span className="status-error"></span>
```

### Layout Utilities

```tsx
<div className="responsive-container">
  {/* Max-width container with responsive padding */}
</div>

<section className="section-spacing">
  {/* Vertical spacing for sections */}
</section>

<div className="container-padding">
  {/* Responsive horizontal padding */}
</div>
```

### Typography

```tsx
<h1 className="text-display-lg">Display Large</h1>
<h2 className="text-headline-lg">Headline Large</h2>
<h3 className="text-title-md">Title Medium</h3>
<p className="text-body-lg">Body Large</p>
<p className="text-body-md">Body Medium</p>
<span className="text-label-sm">Label Small</span>
<code className="text-mono">Monospace</code>
```

### Text Utilities

```tsx
<p className="text-muted">Muted text with on-surface-variant color</p>
<code className="text-mono">Monospace text</code>
```

## Color Palette

The Obsidian Moss palette includes:

### Surface Colors
- `surface` - Base surface (#101416)
- `surface-container` - Container surface (#1c2022)
- `surface-container-high` - Elevated container (#262b2c)
- `surface-bright` - Bright surface (#353a3c)

### Primary Colors
- `primary` - Moss green (#bbcbb6)
- `primary-container` - Primary container (#6b7a68)
- `on-primary` - Text on primary (#263425)

### Secondary Colors
- `secondary` - Secondary gray (#c5c7c8)
- `secondary-container` - Secondary container (#444748)

### Semantic Colors
- `error` - Error red (#ffb4ab)
- `outline` - Border outline (#8e928b)
- `outline-variant` - Subtle outline (#444842)

## Responsive Breakpoints

- **mobile**: 320px - Small mobile devices
- **mobileLg**: 480px - Large mobile devices
- **tablet**: 768px - Tablets
- **desktop**: 1024px - Desktop screens
- **desktopLg**: 1440px - Large desktop screens
- **desktopXl**: 1920px - Extra large screens

## Design Philosophy

The Obsidian Moss theme follows these principles:

1. **Quiet Luxury**: Sophisticated, calm interface that prioritizes cognitive clarity
2. **Tonal Layering**: Depth through subtle color variations rather than shadows
3. **Generous Spacing**: Comfortable padding and margins for breathability
4. **Low Contrast**: Soft off-white text on dark backgrounds to reduce eye strain
5. **Organic Accents**: Desaturated moss green for meaningful actions and highlights

## Requirements Validation

This theme system validates:
- **Requirement 1.3**: Consistent Obsidian Moss theme across all modules
- **Requirement 9.1**: Responsive design for all device sizes
- **Requirement 9.4**: Theme consistency across screen sizes from 320px to 1920px
