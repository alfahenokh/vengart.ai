/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Obsidian Moss Color Palette
        surface: {
          DEFAULT: '#101416',
          dim: '#101416',
          bright: '#353a3c',
          'container-lowest': '#0a0f10',
          'container-low': '#181c1e',
          container: '#1c2022',
          'container-high': '#262b2c',
          'container-highest': '#313537',
        },
        'on-surface': {
          DEFAULT: '#dfe3e5',
          variant: '#c4c8c0',
        },
        'inverse-surface': '#dfe3e5',
        'inverse-on-surface': '#2d3133',
        outline: {
          DEFAULT: '#8e928b',
          variant: '#444842',
        },
        'surface-tint': '#bbcbb6',
        primary: {
          DEFAULT: '#bbcbb6',
          on: '#263425',
          container: '#6b7a68',
          'on-container': '#ffffff',
          inverse: '#546251',
          fixed: '#d7e7d2',
          'fixed-dim': '#bbcbb6',
          'on-fixed': '#121f11',
          'on-fixed-variant': '#3c4a3b',
        },
        secondary: {
          DEFAULT: '#c5c7c8',
          on: '#2e3132',
          container: '#444748',
          'on-container': '#b3b5b6',
          fixed: '#e1e3e4',
          'fixed-dim': '#c5c7c8',
          'on-fixed': '#191c1d',
          'on-fixed-variant': '#444748',
        },
        tertiary: {
          DEFAULT: '#c6c6c7',
          on: '#2f3132',
          container: '#757677',
          'on-container': '#ffffff',
          fixed: '#e2e2e3',
          'fixed-dim': '#c6c6c7',
          'on-fixed': '#1a1c1d',
          'on-fixed-variant': '#454748',
        },
        error: {
          DEFAULT: '#ffb4ab',
          on: '#690005',
          container: '#93000a',
          'on-container': '#ffdad6',
        },
        background: {
          DEFAULT: '#101416',
          on: '#dfe3e5',
        },
        'surface-variant': '#313537',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'Monaco', 'Courier New', 'monospace'],
      },
      fontSize: {
        'display-lg': ['48px', { lineHeight: '56px', letterSpacing: '-0.02em', fontWeight: '300' }],
        'headline-lg': ['32px', { lineHeight: '40px', letterSpacing: '-0.01em', fontWeight: '400' }],
        'headline-lg-mobile': ['24px', { lineHeight: '32px', fontWeight: '500' }],
        'title-md': ['18px', { lineHeight: '24px', fontWeight: '500' }],
        'body-lg': ['16px', { lineHeight: '26px', fontWeight: '400' }],
        'body-md': ['14px', { lineHeight: '22px', fontWeight: '400' }],
        'label-sm': ['12px', { lineHeight: '16px', letterSpacing: '0.05em', fontWeight: '600' }],
        'mono-label': ['13px', { lineHeight: '18px', fontWeight: '400' }],
      },
      borderRadius: {
        sm: '0.25rem',
        DEFAULT: '0.5rem',
        md: '0.75rem',
        lg: '1rem',
        xl: '1.5rem',
        full: '9999px',
      },
      spacing: {
        'gutter': '24px',
        'margin-mobile': '16px',
        'margin-desktop': '48px',
      },
      maxWidth: {
        'container': '1440px',
      },
      backdropBlur: {
        'glass': '12px',
      },
      boxShadow: {
        'ambient': '0px 4px 20px rgba(0, 0, 0, 0.5)',
      },
    },
  },
  plugins: [],
}
