import React from 'react';

/**
 * MetricCard Component
 *
 * Displays a single metric with title, value, optional unit, and optional trend indicator.
 * Uses the Obsidian Moss theme.
 */

export type TrendDirection = 'up' | 'down' | 'stable';

export interface MetricCardProps {
  title: string;
  value: string | number;
  unit?: string;
  trend?: TrendDirection;
  trendValue?: string;
  /** Optional icon element rendered in the top-right corner */
  icon?: React.ReactNode;
  /** Optional additional CSS classes */
  className?: string;
}

const TrendIcon: React.FC<{ direction: TrendDirection }> = ({ direction }) => {
  if (direction === 'up') {
    return (
      <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M5 15l7-7 7 7" />
      </svg>
    );
  }
  if (direction === 'down') {
    return (
      <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
      </svg>
    );
  }
  return (
    <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14" />
    </svg>
  );
};

const trendColorClass = (direction: TrendDirection): string => {
  switch (direction) {
    case 'up':
      return 'text-primary';
    case 'down':
      return 'text-error';
    case 'stable':
    default:
      return 'text-on-surface-variant';
  }
};

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  unit,
  trend,
  trendValue,
  icon,
  className = '',
}) => {
  return (
    <div className={`card flex flex-col gap-3 ${className}`}>
      {/* Header row */}
      <div className="flex items-start justify-between">
        <p className="text-label-sm text-muted uppercase tracking-wide">{title}</p>
        {icon && (
          <div className="text-on-surface-variant opacity-60">{icon}</div>
        )}
      </div>

      {/* Value row */}
      <div className="flex items-end gap-2">
        <span className="text-display-lg text-on-surface leading-none">{value}</span>
        {unit && (
          <span className="text-body-md text-muted mb-1">{unit}</span>
        )}
      </div>

      {/* Trend row */}
      {trend && (
        <div className={`flex items-center gap-1 text-body-md ${trendColorClass(trend)}`}>
          <TrendIcon direction={trend} />
          {trendValue && <span>{trendValue}</span>}
        </div>
      )}
    </div>
  );
};

export default MetricCard;
