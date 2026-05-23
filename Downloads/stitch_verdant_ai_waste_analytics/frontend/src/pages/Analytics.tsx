import React from 'react';

/**
 * Analytics Page — Placeholder
 *
 * Full implementation coming in a future task.
 */
const Analytics: React.FC = () => {
  return (
    <div className="min-h-screen bg-background">
      <div className="responsive-container py-16">
        <div className="max-w-lg mx-auto text-center">
          {/* Icon */}
          <div className="w-16 h-16 rounded-2xl bg-primary/15 flex items-center justify-center mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
            </svg>
          </div>

          <h1 className="text-headline-lg text-on-surface mb-3">Analytics Module</h1>
          <p className="text-body-lg text-muted mb-6">
            KPI dashboards, waste volume forecasting, and report generation are coming soon.
          </p>

          <div className="card text-left space-y-3">
            <p className="text-label-sm text-muted uppercase tracking-wide">Planned features</p>
            {[
              'Interactive KPI cards with trend indicators',
              'Waste volume forecast charts',
              'Regional distribution mapping',
              'PDF & Excel report export',
            ].map((feature) => (
              <div key={feature} className="flex items-center gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-primary flex-shrink-0" />
                <span className="text-body-md text-on-surface-variant">{feature}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
