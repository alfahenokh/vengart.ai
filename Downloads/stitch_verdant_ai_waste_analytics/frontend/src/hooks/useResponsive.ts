import { useState, useEffect } from 'react';

/**
 * Breakpoint definitions based on Obsidian Moss design system
 * Supports screen sizes from 320px to 1920px
 */
export const breakpoints = {
  mobile: 320,
  mobileLg: 480,
  tablet: 768,
  desktop: 1024,
  desktopLg: 1440,
  desktopXl: 1920,
} as const;

export type Breakpoint = keyof typeof breakpoints;

interface ResponsiveState {
  width: number;
  height: number;
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
  isDesktopLg: boolean;
  isDesktopXl: boolean;
  breakpoint: Breakpoint;
}

/**
 * useResponsive Hook
 * 
 * Provides responsive design utilities and breakpoint detection
 * Maintains Obsidian Moss theme consistency across all screen sizes
 * 
 * @returns ResponsiveState with current viewport dimensions and breakpoint flags
 * 
 * @example
 * ```tsx
 * const { isMobile, isDesktop, width } = useResponsive();
 * 
 * return (
 *   <div>
 *     {isMobile ? <MobileNav /> : <DesktopNav />}
 *     <p>Current width: {width}px</p>
 *   </div>
 * );
 * ```
 */
export const useResponsive = (): ResponsiveState => {
  const [state, setState] = useState<ResponsiveState>(() => {
    const width = typeof window !== 'undefined' ? window.innerWidth : breakpoints.desktop;
    const height = typeof window !== 'undefined' ? window.innerHeight : 768;
    
    return {
      width,
      height,
      isMobile: width < breakpoints.tablet,
      isTablet: width >= breakpoints.tablet && width < breakpoints.desktop,
      isDesktop: width >= breakpoints.desktop && width < breakpoints.desktopLg,
      isDesktopLg: width >= breakpoints.desktopLg && width < breakpoints.desktopXl,
      isDesktopXl: width >= breakpoints.desktopXl,
      breakpoint: getBreakpoint(width),
    };
  });

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      const height = window.innerHeight;

      setState({
        width,
        height,
        isMobile: width < breakpoints.tablet,
        isTablet: width >= breakpoints.tablet && width < breakpoints.desktop,
        isDesktop: width >= breakpoints.desktop && width < breakpoints.desktopLg,
        isDesktopLg: width >= breakpoints.desktopLg && width < breakpoints.desktopXl,
        isDesktopXl: width >= breakpoints.desktopXl,
        breakpoint: getBreakpoint(width),
      });
    };

    // Add event listener with debouncing for performance
    let timeoutId: NodeJS.Timeout;
    const debouncedResize = () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(handleResize, 150);
    };

    window.addEventListener('resize', debouncedResize);
    
    // Initial call
    handleResize();

    return () => {
      window.removeEventListener('resize', debouncedResize);
      clearTimeout(timeoutId);
    };
  }, []);

  return state;
};

/**
 * Get the current breakpoint name based on width
 */
function getBreakpoint(width: number): Breakpoint {
  if (width >= breakpoints.desktopXl) return 'desktopXl';
  if (width >= breakpoints.desktopLg) return 'desktopLg';
  if (width >= breakpoints.desktop) return 'desktop';
  if (width >= breakpoints.tablet) return 'tablet';
  if (width >= breakpoints.mobileLg) return 'mobileLg';
  return 'mobile';
}

/**
 * useMediaQuery Hook
 * 
 * Custom hook for media query matching
 * 
 * @param query - CSS media query string
 * @returns boolean indicating if the media query matches
 * 
 * @example
 * ```tsx
 * const isLargeScreen = useMediaQuery('(min-width: 1024px)');
 * ```
 */
export const useMediaQuery = (query: string): boolean => {
  const [matches, setMatches] = useState<boolean>(() => {
    if (typeof window !== 'undefined') {
      return window.matchMedia(query).matches;
    }
    return false;
  });

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);
    
    const handleChange = (event: MediaQueryListEvent) => {
      setMatches(event.matches);
    };

    // Modern browsers
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    } 
    // Legacy browsers
    else {
      mediaQuery.addListener(handleChange);
      return () => mediaQuery.removeListener(handleChange);
    }
  }, [query]);

  return matches;
};

export default useResponsive;
