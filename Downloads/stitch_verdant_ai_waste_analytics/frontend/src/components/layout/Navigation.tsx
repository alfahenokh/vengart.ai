import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { useTheme } from '../theme';

/**
 * Navigation Component
 *
 * Top navigation bar for the Verdant AI Integrated Dashboard.
 * Includes module tabs, brand logo, dark mode toggle, and responsive hamburger menu.
 */

interface NavItem {
  label: string;
  path: string;
}

const navItems: NavItem[] = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Analytics', path: '/analytics' },
  { label: 'Simulator', path: '/simulator' },
  { label: 'Resources', path: '/resources' },
];

const Navigation: React.FC = () => {
  const { isDarkMode, toggleDarkMode } = useTheme();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav
      className="bg-surface-container border-b border-outline-variant sticky top-0 z-50"
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="responsive-container">
        <div className="flex items-center justify-between h-16">
          {/* Brand */}
          <div className="flex items-center gap-3 flex-shrink-0">
            {/* Logo mark */}
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
              <span className="text-on-primary font-bold text-sm select-none">V</span>
            </div>
            <div className="hidden sm:block">
              <span className="text-title-md text-on-surface font-semibold">Verdant AI</span>
              <span className="text-body-md text-muted ml-2 hidden md:inline">Integrated Dashboard</span>
            </div>
          </div>

          {/* Desktop nav tabs */}
          <div className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive: active }) =>
                  [
                    'px-4 py-2 rounded-lg text-body-md font-medium transition-colors duration-150',
                    active
                      ? 'bg-primary/15 text-primary'
                      : 'text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface',
                  ].join(' ')
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>

          {/* Right side controls */}
          <div className="flex items-center gap-2">
            {/* Dark mode toggle */}
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-lg text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-colors duration-150"
              aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
              title={isDarkMode ? 'Light mode' : 'Dark mode'}
            >
              {isDarkMode ? (
                /* Sun icon */
                <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1.5M12 19.5V21M4.22 4.22l1.06 1.06M18.72 18.72l1.06 1.06M3 12H1.5M22.5 12H21M4.22 19.78l1.06-1.06M18.72 5.28l1.06-1.06M16.5 12a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0z" />
                </svg>
              ) : (
                /* Moon icon */
                <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
                </svg>
              )}
            </button>

            {/* Hamburger menu (mobile) */}
            <button
              className="md:hidden p-2 rounded-lg text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-colors duration-150"
              onClick={() => setMenuOpen((prev) => !prev)}
              aria-label={menuOpen ? 'Close menu' : 'Open menu'}
              aria-expanded={menuOpen}
            >
              {menuOpen ? (
                /* X icon */
                <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                /* Hamburger icon */
                <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>
        </div>

        {/* Mobile dropdown menu */}
        {menuOpen && (
          <div className="md:hidden border-t border-outline-variant py-2 pb-4">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={() => setMenuOpen(false)}
                className={({ isActive: active }) =>
                  [
                    'block px-4 py-3 rounded-lg text-body-md font-medium transition-colors duration-150 my-0.5',
                    active
                      ? 'bg-primary/15 text-primary'
                      : 'text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface',
                  ].join(' ')
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation;
