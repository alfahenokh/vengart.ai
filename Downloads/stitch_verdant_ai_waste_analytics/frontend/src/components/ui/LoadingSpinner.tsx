import React from 'react';

/**
 * LoadingSpinner Component
 *
 * A simple animated loading indicator using the Obsidian Moss theme.
 */

export type SpinnerSize = 'sm' | 'md' | 'lg';

export interface LoadingSpinnerProps {
  size?: SpinnerSize;
  /** Optional label shown below the spinner */
  label?: string;
  /** Center the spinner in its container */
  centered?: boolean;
  className?: string;
}

const sizeClasses: Record<SpinnerSize, string> = {
  sm: 'w-5 h-5 border-2',
  md: 'w-8 h-8 border-2',
  lg: 'w-12 h-12 border-[3px]',
};

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  label,
  centered = false,
  className = '',
}) => {
  const spinner = (
    <div
      className={`inline-block rounded-full border-outline-variant border-t-primary animate-spin ${sizeClasses[size]} ${className}`}
      role="status"
      aria-label={label ?? 'Loading'}
    />
  );

  if (centered) {
    return (
      <div className="flex flex-col items-center justify-center gap-3 py-12">
        {spinner}
        {label && <p className="text-body-md text-muted">{label}</p>}
      </div>
    );
  }

  return (
    <div className="inline-flex flex-col items-center gap-2">
      {spinner}
      {label && <p className="text-body-md text-muted">{label}</p>}
    </div>
  );
};

export default LoadingSpinner;
