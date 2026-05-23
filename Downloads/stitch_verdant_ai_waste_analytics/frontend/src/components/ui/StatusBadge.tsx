import React from 'react';

/**
 * StatusBadge Component
 *
 * Displays a status badge for fleet units or other entities.
 * Supports: active, idle, maintenance, offline statuses.
 */

export type StatusType = 'active' | 'idle' | 'maintenance' | 'offline';

export interface StatusBadgeProps {
  status: StatusType;
  /** Show a pulsing dot indicator alongside the label */
  showDot?: boolean;
  className?: string;
}

const statusConfig: Record<StatusType, { label: string; dotClass: string; badgeClass: string }> = {
  active: {
    label: 'Active',
    dotClass: 'bg-primary animate-pulse',
    badgeClass: 'bg-primary/15 text-primary',
  },
  idle: {
    label: 'Idle',
    dotClass: 'bg-secondary',
    badgeClass: 'bg-secondary/15 text-secondary',
  },
  maintenance: {
    label: 'Maintenance',
    dotClass: 'bg-error animate-pulse',
    badgeClass: 'bg-error/15 text-error',
  },
  offline: {
    label: 'Offline',
    dotClass: 'bg-outline',
    badgeClass: 'bg-outline/15 text-on-surface-variant',
  },
};

const StatusBadge: React.FC<StatusBadgeProps> = ({ status, showDot = true, className = '' }) => {
  const config = statusConfig[status];

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-label-sm font-medium ${config.badgeClass} ${className}`}
      aria-label={`Status: ${config.label}`}
    >
      {showDot && (
        <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${config.dotClass}`} />
      )}
      {config.label}
    </span>
  );
};

export default StatusBadge;
