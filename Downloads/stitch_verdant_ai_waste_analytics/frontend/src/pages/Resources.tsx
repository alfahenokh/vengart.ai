import React from 'react';

/**
 * Resources Page — Placeholder
 *
 * Full implementation coming in a future task.
 */
const Resources: React.FC = () => {
  return (
    <div className="min-h-screen bg-background">
      <div className="responsive-container py-16">
        <div className="max-w-lg mx-auto text-center">
          {/* Icon */}
          <div className="w-16 h-16 rounded-2xl bg-tertiary/15 flex items-center justify-center mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 text-tertiary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
            </svg>
          </div>

          <h1 className="text-headline-lg text-on-surface mb-3">Resource Manager</h1>
          <p className="text-body-lg text-muted mb-6">
            Fleet tracking, personnel management, and maintenance scheduling are coming soon.
          </p>

          <div className="card text-left space-y-3">
            <p className="text-label-sm text-muted uppercase tracking-wide">Planned features</p>
            {[
              'Real-time fleet status tracking',
              'Personnel roster & shift scheduling',
              'Automated dispatch recommendations',
              'Maintenance scheduling & tracking',
            ].map((feature) => (
              <div key={feature} className="flex items-center gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-tertiary flex-shrink-0" />
                <span className="text-body-md text-on-surface-variant">{feature}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Resources;
