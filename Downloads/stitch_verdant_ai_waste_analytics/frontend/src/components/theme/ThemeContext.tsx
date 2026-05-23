import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';

/**
 * Obsidian Moss Theme Colors
 * Based on the Obsidian Moss design system
 */
export interface ThemeColors {
  surface: string;
  surfaceDim: string;
  surfaceBright: string;
  surfaceContainerLowest: string;
  surfaceContainerLow: string;
  surfaceContainer: string;
  surfaceContainerHigh: string;
  surfaceContainerHighest: string;
  onSurface: string;
  onSurfaceVariant: string;
  inverseSurface: string;
  inverseOnSurface: string;
  outline: string;
  outlineVariant: string;
  surfaceTint: string;
  primary: string;
  onPrimary: string;
  primaryContainer: string;
  onPrimaryContainer: string;
  inversePrimary: string;
  secondary: string;
  onSecondary: string;
  secondaryContainer: string;
  onSecondaryContainer: string;
  tertiary: string;
  onTertiary: string;
  tertiaryContainer: string;
  onTertiaryContainer: string;
  error: string;
  onError: string;
  errorContainer: string;
  onErrorContainer: string;
  background: string;
  onBackground: string;
}

export interface ObsidianMossTheme {
  colors: ThemeColors;
  isDarkMode: boolean;
}

interface ThemeContextValue {
  theme: ObsidianMossTheme;
  isDarkMode: boolean;
  toggleDarkMode: () => void;
  updateThemeColors: (colors: Partial<ThemeColors>) => void;
}

const defaultColors: ThemeColors = {
  surface: '#101416',
  surfaceDim: '#101416',
  surfaceBright: '#353a3c',
  surfaceContainerLowest: '#0a0f10',
  surfaceContainerLow: '#181c1e',
  surfaceContainer: '#1c2022',
  surfaceContainerHigh: '#262b2c',
  surfaceContainerHighest: '#313537',
  onSurface: '#dfe3e5',
  onSurfaceVariant: '#c4c8c0',
  inverseSurface: '#dfe3e5',
  inverseOnSurface: '#2d3133',
  outline: '#8e928b',
  outlineVariant: '#444842',
  surfaceTint: '#bbcbb6',
  primary: '#bbcbb6',
  onPrimary: '#263425',
  primaryContainer: '#6b7a68',
  onPrimaryContainer: '#ffffff',
  inversePrimary: '#546251',
  secondary: '#c5c7c8',
  onSecondary: '#2e3132',
  secondaryContainer: '#444748',
  onSecondaryContainer: '#b3b5b6',
  tertiary: '#c6c6c7',
  onTertiary: '#2f3132',
  tertiaryContainer: '#757677',
  onTertiaryContainer: '#ffffff',
  error: '#ffb4ab',
  onError: '#690005',
  errorContainer: '#93000a',
  onErrorContainer: '#ffdad6',
  background: '#101416',
  onBackground: '#dfe3e5',
};

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

interface ThemeProviderProps {
  children: ReactNode;
  initialDarkMode?: boolean;
}

/**
 * ThemeProvider Component
 * 
 * Provides consistent Obsidian Moss theme across all modules
 * Supports dynamic theme customization and dark mode toggling
 * Manages responsive design breakpoints
 * 
 * @example
 * ```tsx
 * <ThemeProvider>
 *   <App />
 * </ThemeProvider>
 * ```
 */
export const ThemeProvider: React.FC<ThemeProviderProps> = ({ 
  children, 
  initialDarkMode = true 
}) => {
  const [isDarkMode, setIsDarkMode] = useState<boolean>(() => {
    // Check localStorage for saved preference
    const saved = localStorage.getItem('obsidian-moss-dark-mode');
    if (saved !== null) {
      return JSON.parse(saved);
    }
    return initialDarkMode;
  });

  const [colors, setColors] = useState<ThemeColors>(defaultColors);

  // Apply dark mode class to document root
  useEffect(() => {
    const root = document.documentElement;
    if (isDarkMode) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    // Save preference to localStorage
    localStorage.setItem('obsidian-moss-dark-mode', JSON.stringify(isDarkMode));
  }, [isDarkMode]);

  const toggleDarkMode = () => {
    setIsDarkMode(prev => !prev);
  };

  const updateThemeColors = (newColors: Partial<ThemeColors>) => {
    setColors(prev => ({ ...prev, ...newColors }));
  };

  const theme: ObsidianMossTheme = {
    colors,
    isDarkMode,
  };

  const value: ThemeContextValue = {
    theme,
    isDarkMode,
    toggleDarkMode,
    updateThemeColors,
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

/**
 * useTheme Hook
 * 
 * Access the Obsidian Moss theme context
 * 
 * @returns ThemeContextValue with theme, isDarkMode, toggleDarkMode, and updateThemeColors
 * @throws Error if used outside of ThemeProvider
 * 
 * @example
 * ```tsx
 * const { theme, isDarkMode, toggleDarkMode } = useTheme();
 * ```
 */
export const useTheme = (): ThemeContextValue => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export default ThemeProvider;
