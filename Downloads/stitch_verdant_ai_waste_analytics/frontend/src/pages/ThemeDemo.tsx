import React from 'react';
import { useTheme } from '../components/theme';
import { useResponsive } from '../hooks/useResponsive';

/**
 * ThemeDemo Component
 * 
 * Demonstrates the Obsidian Moss theme system with various UI components
 * Showcases responsive design and dark mode functionality
 */
const ThemeDemo: React.FC = () => {
  const { theme, isDarkMode, toggleDarkMode } = useTheme();
  const { width, height, isMobile, isTablet, isDesktop, breakpoint } = useResponsive();

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-outline-variant bg-surface-container">
        <div className="responsive-container py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-headline-lg text-on-surface">
                Obsidian Moss Theme System
              </h1>
              <p className="text-body-md text-muted mt-2">
                Quiet Luxury for Technical Environments
              </p>
            </div>
            <button
              onClick={toggleDarkMode}
              className="btn-secondary"
              aria-label="Toggle dark mode"
            >
              {isDarkMode ? '🌙 Dark' : '☀️ Light'}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="responsive-container section-spacing">
        {/* Responsive Info Card */}
        <section className="mb-12">
          <h2 className="text-title-md text-on-surface mb-4">
            Responsive Design Information
          </h2>
          <div className="card">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-label-sm text-muted uppercase mb-2">Viewport</p>
                <p className="text-body-lg text-on-surface">
                  {width}px × {height}px
                </p>
              </div>
              <div>
                <p className="text-label-sm text-muted uppercase mb-2">Breakpoint</p>
                <p className="text-body-lg text-on-surface capitalize">
                  {breakpoint}
                </p>
              </div>
              <div>
                <p className="text-label-sm text-muted uppercase mb-2">Device Type</p>
                <div className="flex gap-2 mt-2">
                  {isMobile && <span className="badge">Mobile</span>}
                  {isTablet && <span className="badge">Tablet</span>}
                  {isDesktop && <span className="badge">Desktop</span>}
                </div>
              </div>
              <div>
                <p className="text-label-sm text-muted uppercase mb-2">Theme Mode</p>
                <p className="text-body-lg text-on-surface">
                  {isDarkMode ? 'Dark Mode' : 'Light Mode'}
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Color Palette */}
        <section className="mb-12">
          <h2 className="text-title-md text-on-surface mb-4">
            Color Palette
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <ColorSwatch name="Primary" color={theme.colors.primary} />
            <ColorSwatch name="Secondary" color={theme.colors.secondary} />
            <ColorSwatch name="Tertiary" color={theme.colors.tertiary} />
            <ColorSwatch name="Error" color={theme.colors.error} />
            <ColorSwatch name="Surface" color={theme.colors.surface} />
            <ColorSwatch name="Surface Container" color={theme.colors.surfaceContainer} />
            <ColorSwatch name="Outline" color={theme.colors.outline} />
            <ColorSwatch name="On Surface" color={theme.colors.onSurface} />
          </div>
        </section>

        {/* Typography */}
        <section className="mb-12">
          <h2 className="text-title-md text-on-surface mb-4">
            Typography
          </h2>
          <div className="card space-y-6">
            <div>
              <p className="text-label-sm text-muted uppercase mb-2">Display Large</p>
              <p className="text-display-lg text-on-surface">
                The Sophisticated Architect
              </p>
            </div>
            <div>
              <p className="text-label-sm text-muted uppercase mb-2">Headline Large</p>
              <p className="text-headline-lg text-on-surface">
                Quiet Luxury for Technical Environments
              </p>
            </div>
            <div>
              <p className="text-label-sm text-muted uppercase mb-2">Title Medium</p>
              <p className="text-title-md text-on-surface">
                Verdant AI Integrated Dashboard
              </p>
            </div>
            <div>
              <p className="text-label-sm text-muted uppercase mb-2">Body Large</p>
              <p className="text-body-lg text-on-surface">
                This design system is built upon the philosophy of Quiet Luxury for technical 
                environments. It rejects the hyper-stimulated aesthetic of typical AI dashboards 
                in favor of a serene, focused interface.
              </p>
            </div>
            <div>
              <p className="text-label-sm text-muted uppercase mb-2">Monospace Label</p>
              <p className="text-mono text-on-surface">
                const theme = useTheme();
              </p>
            </div>
          </div>
        </section>

        {/* Buttons */}
        <section className="mb-12">
          <h2 className="text-title-md text-on-surface mb-4">
            Buttons
          </h2>
          <div className="card">
            <div className="flex flex-wrap gap-4">
              <button className="btn-primary">
                Primary Button
              </button>
              <button className="btn-secondary">
                Secondary Button
              </button>
              <button className="btn-primary" disabled>
                Disabled Button
              </button>
            </div>
          </div>
        </section>

        {/* Input Fields */}
        <section className="mb-12">
          <h2 className="text-title-md text-on-surface mb-4">
            Input Fields
          </h2>
          <div className="card space-y-4">
            <input
              type="text"
              placeholder="Enter text..."
              className="input-field w-full"
            />
            <input
              type="email"
              placeholder="Email address"
              className="input-field w-full"
            />
            <textarea
              placeholder="Message..."
              rows={4}
              className="input-field w-full resize-none"
            />
          </div>
        </section>

        {/* Badges */}
        <section className="mb-12">
          <h2 className="text-title-md text-on-surface mb-4">
            Badges & Status Indicators
          </h2>
          <div className="card">
            <div className="flex flex-wrap gap-3 mb-6">
              <span className="badge">Active</span>
              <span className="badge-secondary">Pending</span>
              <span className="badge-error">Error</span>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <span className="status-active"></span>
                <span className="text-body-md text-on-surface">Active</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="status-idle"></span>
                <span className="text-body-md text-on-surface">Idle</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="status-error"></span>
                <span className="text-body-md text-on-surface">Error</span>
              </div>
            </div>
          </div>
        </section>

        {/* Cards */}
        <section className="mb-12">
          <h2 className="text-title-md text-on-surface mb-4">
            Cards
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="card">
              <h3 className="text-title-md text-on-surface mb-2">
                Standard Card
              </h3>
              <p className="text-body-md text-muted">
                Basic card with border and no shadow
              </p>
            </div>
            <div className="card-elevated">
              <h3 className="text-title-md text-on-surface mb-2">
                Elevated Card
              </h3>
              <p className="text-body-md text-muted">
                Card with ambient shadow
              </p>
            </div>
            <div className="card-interactive">
              <h3 className="text-title-md text-on-surface mb-2">
                Interactive Card
              </h3>
              <p className="text-body-md text-muted">
                Hover to see interaction
              </p>
            </div>
          </div>
        </section>

        {/* Glass Morphism */}
        <section className="mb-12">
          <h2 className="text-title-md text-on-surface mb-4">
            Glass Morphism
          </h2>
          <div className="relative h-64 bg-gradient-to-br from-primary/20 to-secondary/20 rounded-lg overflow-hidden">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="glass rounded-lg p-8 max-w-md">
                <h3 className="text-title-md text-on-surface mb-2">
                  Glass Effect
                </h3>
                <p className="text-body-md text-muted">
                  Backdrop blur with transparent background for overlays and modals
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* List */}
        <section className="mb-12">
          <h2 className="text-title-md text-on-surface mb-4">
            Lists
          </h2>
          <div className="card">
            <div className="list-item">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-body-lg text-on-surface">Fleet Unit UX-9012A</p>
                  <p className="text-body-md text-muted">Collection Vehicle</p>
                </div>
                <span className="badge">Active</span>
              </div>
            </div>
            <div className="list-item">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-body-lg text-on-surface">Fleet Unit UX-9013B</p>
                  <p className="text-body-md text-muted">Transport Vehicle</p>
                </div>
                <span className="badge-secondary">Idle</span>
              </div>
            </div>
            <div className="list-item">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-body-lg text-on-surface">Fleet Unit UX-9014C</p>
                  <p className="text-body-md text-muted">Processing Unit</p>
                </div>
                <span className="badge-error">Maintenance</span>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-outline-variant bg-surface-container">
        <div className="responsive-container py-8">
          <p className="text-body-md text-muted text-center">
            Obsidian Moss Design System • Verdant AI Integrated Dashboard
          </p>
        </div>
      </footer>
    </div>
  );
};

/**
 * ColorSwatch Component
 * Displays a color swatch with name and hex value
 */
interface ColorSwatchProps {
  name: string;
  color: string;
}

const ColorSwatch: React.FC<ColorSwatchProps> = ({ name, color }) => {
  return (
    <div className="card">
      <div
        className="w-full h-20 rounded-lg mb-3"
        style={{ backgroundColor: color }}
      />
      <p className="text-body-md text-on-surface font-medium mb-1">{name}</p>
      <p className="text-mono text-muted uppercase">{color}</p>
    </div>
  );
};

export default ThemeDemo;
