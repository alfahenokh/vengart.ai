import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { ThemeProvider, useTheme } from '../../src/components/theme';

// Test component that uses the theme
const TestComponent = () => {
  const { theme, isDarkMode, toggleDarkMode } = useTheme();

  return (
    <div>
      <div data-testid="dark-mode">{isDarkMode ? 'dark' : 'light'}</div>
      <div data-testid="primary-color">{theme.colors.primary}</div>
      <button onClick={toggleDarkMode} data-testid="toggle-button">
        Toggle
      </button>
    </div>
  );
};

describe('ThemeProvider', () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove('dark');
  });

  it('should provide theme context to children', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(screen.getByTestId('primary-color')).toHaveTextContent('#bbcbb6');
  });

  it('should initialize with dark mode by default', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(screen.getByTestId('dark-mode')).toHaveTextContent('dark');
    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });

  it('should toggle dark mode when toggleDarkMode is called', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    const toggleButton = screen.getByTestId('toggle-button');
    
    // Initially dark
    expect(screen.getByTestId('dark-mode')).toHaveTextContent('dark');

    // Toggle to light
    act(() => {
      toggleButton.click();
    });

    expect(screen.getByTestId('dark-mode')).toHaveTextContent('light');
    expect(document.documentElement.classList.contains('dark')).toBe(false);

    // Toggle back to dark
    act(() => {
      toggleButton.click();
    });

    expect(screen.getByTestId('dark-mode')).toHaveTextContent('dark');
    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });

  it('should persist dark mode preference to localStorage', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    const toggleButton = screen.getByTestId('toggle-button');

    // Toggle to light mode
    act(() => {
      toggleButton.click();
    });

    expect(localStorage.getItem('obsidian-moss-dark-mode')).toBe('false');

    // Toggle back to dark mode
    act(() => {
      toggleButton.click();
    });

    expect(localStorage.getItem('obsidian-moss-dark-mode')).toBe('true');
  });

  it('should load dark mode preference from localStorage', () => {
    localStorage.setItem('obsidian-moss-dark-mode', 'false');

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(screen.getByTestId('dark-mode')).toHaveTextContent('light');
    expect(document.documentElement.classList.contains('dark')).toBe(false);
  });

  it('should use initialDarkMode prop when no localStorage value exists', () => {
    render(
      <ThemeProvider initialDarkMode={false}>
        <TestComponent />
      </ThemeProvider>
    );

    expect(screen.getByTestId('dark-mode')).toHaveTextContent('light');
  });

  it('should throw error when useTheme is used outside ThemeProvider', () => {
    // Suppress console.error for this test
    const originalError = console.error;
    console.error = () => {};

    expect(() => {
      render(<TestComponent />);
    }).toThrow('useTheme must be used within a ThemeProvider');

    console.error = originalError;
  });

  it('should provide all Obsidian Moss colors', () => {
    const ColorTest = () => {
      const { theme } = useTheme();
      return (
        <div>
          <div data-testid="surface">{theme.colors.surface}</div>
          <div data-testid="primary">{theme.colors.primary}</div>
          <div data-testid="secondary">{theme.colors.secondary}</div>
          <div data-testid="error">{theme.colors.error}</div>
          <div data-testid="outline">{theme.colors.outline}</div>
        </div>
      );
    };

    render(
      <ThemeProvider>
        <ColorTest />
      </ThemeProvider>
    );

    expect(screen.getByTestId('surface')).toHaveTextContent('#101416');
    expect(screen.getByTestId('primary')).toHaveTextContent('#bbcbb6');
    expect(screen.getByTestId('secondary')).toHaveTextContent('#c5c7c8');
    expect(screen.getByTestId('error')).toHaveTextContent('#ffb4ab');
    expect(screen.getByTestId('outline')).toHaveTextContent('#8e928b');
  });
});
