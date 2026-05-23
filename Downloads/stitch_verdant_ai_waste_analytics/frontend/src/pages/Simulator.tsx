import React from 'react';

/**
 * Simulator Page — Placeholder
 *
 * Full implementation coming in a future task.
 */
const Simulator: React.FC = () => {
  return (
    <div className="min-h-screen bg-background">
      <div className="responsive-container py-16">
        <div className="max-w-lg mx-auto text-center">
          {/* Icon */}
          <div className="w-16 h-16 rounded-2xl bg-secondary/15 flex items-center justify-center mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 6.75V15m6-6v8.25m.503 3.498l4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 00-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0z" />
            </svg>
          </div>

          <h1 className="text-headline-lg text-on-surface mb-3">Operational Simulator</h1>
          <p className="text-body-lg text-muted mb-6">
            Interactive route simulation with Leaflet maps and AI-powered optimisation is coming soon.
          </p>

          <div className="card text-left space-y-3">
            <p className="text-label-sm text-muted uppercase tracking-wide">Planned features</p>
            {[
              'Interactive Leaflet.js map interface',
              'Simulation parameter controls',
              'AI route optimisation engine',
              'Real-time execution logging',
            ].map((feature) => (
              <div key={feature} className="flex items-center gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0" />
                <span className="text-body-md text-on-surface-variant">{feature}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Simulator;
