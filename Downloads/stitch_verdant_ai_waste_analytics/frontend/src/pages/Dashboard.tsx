import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
} from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';
import { MetricCard, StatusBadge, LoadingSpinner } from '../components/ui';
import type { StatusType } from '../components/ui';

// Register Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

// ─── Types ────────────────────────────────────────────────────────────────────

interface FleetUnit {
  id: string;
  identifier: string;
  type: string;
  status: StatusType;
  capacity_current: number;
  capacity_maximum: number;
  capacity_unit: string;
  location_zone?: string;
}

interface DashboardOverview {
  total_fleet: number;
  active_units: number;
  capacity_utilization: number;
  efficiency_score: number;
  fleet_units: FleetUnit[];
  status_distribution: {
    active: number;
    idle: number;
    maintenance: number;
    offline: number;
  };
}

// ─── Mock data (fallback when API is unavailable) ─────────────────────────────

const MOCK_DATA: DashboardOverview = {
  total_fleet: 48,
  active_units: 31,
  capacity_utilization: 73.4,
  efficiency_score: 88.2,
  status_distribution: {
    active: 31,
    idle: 10,
    maintenance: 5,
    offline: 2,
  },
  fleet_units: [
    { id: '1', identifier: 'UX-9012A', type: 'Collection', status: 'active', capacity_current: 4.2, capacity_maximum: 6.0, capacity_unit: 'tons', location_zone: 'Zone A' },
    { id: '2', identifier: 'UX-9013B', type: 'Transport', status: 'idle', capacity_current: 0, capacity_maximum: 12.0, capacity_unit: 'tons', location_zone: 'Depot' },
    { id: '3', identifier: 'UX-9014C', type: 'Processing', status: 'maintenance', capacity_current: 0, capacity_maximum: 20.0, capacity_unit: 'tons', location_zone: 'Workshop' },
    { id: '4', identifier: 'UX-9015D', type: 'Collection', status: 'active', capacity_current: 5.1, capacity_maximum: 6.0, capacity_unit: 'tons', location_zone: 'Zone B' },
    { id: '5', identifier: 'UX-9016E', type: 'Transport', status: 'active', capacity_current: 8.3, capacity_maximum: 12.0, capacity_unit: 'tons', location_zone: 'Zone C' },
    { id: '6', identifier: 'UX-9017F', type: 'Collection', status: 'offline', capacity_current: 0, capacity_maximum: 6.0, capacity_unit: 'tons', location_zone: 'Depot' },
    { id: '7', identifier: 'UX-9018G', type: 'Processing', status: 'active', capacity_current: 14.0, capacity_maximum: 20.0, capacity_unit: 'tons', location_zone: 'Zone A' },
    { id: '8', identifier: 'UX-9019H', type: 'Collection', status: 'idle', capacity_current: 0, capacity_maximum: 6.0, capacity_unit: 'tons', location_zone: 'Depot' },
  ],
};

// ─── Chart theme colours ──────────────────────────────────────────────────────

const CHART_COLORS = {
  active: 'rgba(187, 203, 182, 0.85)',      // primary
  idle: 'rgba(197, 199, 200, 0.85)',         // secondary
  maintenance: 'rgba(255, 180, 171, 0.85)', // error
  offline: 'rgba(142, 146, 139, 0.85)',     // outline
};

const CHART_BORDER_COLORS = {
  active: '#bbcbb6',
  idle: '#c5c7c8',
  maintenance: '#ffb4ab',
  offline: '#8e928b',
};

// ─── Sub-components ───────────────────────────────────────────────────────────

const FleetTable: React.FC<{ units: FleetUnit[] }> = ({ units }) => (
  <div className="card overflow-hidden p-0">
    <div className="px-6 py-4 border-b border-outline-variant">
      <h3 className="text-title-md text-on-surface">Fleet Status</h3>
      <p className="text-body-md text-muted mt-0.5">Real-time unit overview</p>
    </div>
    <div className="overflow-x-auto">
      <table className="w-full text-body-md">
        <thead>
          <tr className="border-b border-outline-variant bg-surface-container-low">
            <th className="text-left px-6 py-3 text-label-sm text-muted uppercase tracking-wide">Unit ID</th>
            <th className="text-left px-6 py-3 text-label-sm text-muted uppercase tracking-wide">Type</th>
            <th className="text-left px-6 py-3 text-label-sm text-muted uppercase tracking-wide">Status</th>
            <th className="text-left px-6 py-3 text-label-sm text-muted uppercase tracking-wide">Capacity</th>
            <th className="text-left px-6 py-3 text-label-sm text-muted uppercase tracking-wide">Zone</th>
          </tr>
        </thead>
        <tbody>
          {units.map((unit, idx) => {
            const capacityPct = unit.capacity_maximum > 0
              ? Math.round((unit.capacity_current / unit.capacity_maximum) * 100)
              : 0;
            return (
              <tr
                key={unit.id}
                className={`border-b border-outline-variant/50 hover:bg-surface-container-high transition-colors duration-100 ${idx % 2 === 0 ? '' : 'bg-surface-container-lowest/30'}`}
              >
                <td className="px-6 py-4 text-mono text-on-surface font-medium">{unit.identifier}</td>
                <td className="px-6 py-4 text-on-surface-variant">{unit.type}</td>
                <td className="px-6 py-4">
                  <StatusBadge status={unit.status} />
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className="flex-1 min-w-[80px] bg-surface-container-high rounded-full h-1.5">
                      <div
                        className="h-1.5 rounded-full bg-primary transition-all duration-300"
                        style={{ width: `${capacityPct}%` }}
                      />
                    </div>
                    <span className="text-on-surface-variant text-body-md whitespace-nowrap">
                      {unit.capacity_current}/{unit.capacity_maximum} {unit.capacity_unit}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4 text-on-surface-variant">{unit.location_zone ?? '—'}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  </div>
);

// ─── Main Dashboard Page ──────────────────────────────────────────────────────

const Dashboard: React.FC = () => {
  const [data, setData] = useState<DashboardOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [usingMock, setUsingMock] = useState(false);

  useEffect(() => {
    let cancelled = false;

    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await axios.get<DashboardOverview>('/api/v1/dashboard/overview', {
          timeout: 5000,
        });
        if (!cancelled) {
          setData(response.data);
          setUsingMock(false);
        }
      } catch {
        if (!cancelled) {
          // Graceful fallback to mock data
          setData(MOCK_DATA);
          setUsingMock(true);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    fetchData();

    // Refresh every 30 seconds
    const interval = setInterval(fetchData, 30_000);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  // ── Chart data ──────────────────────────────────────────────────────────────

  const doughnutData = data
    ? {
        labels: ['Active', 'Idle', 'Maintenance', 'Offline'],
        datasets: [
          {
            data: [
              data.status_distribution.active,
              data.status_distribution.idle,
              data.status_distribution.maintenance,
              data.status_distribution.offline,
            ],
            backgroundColor: [
              CHART_COLORS.active,
              CHART_COLORS.idle,
              CHART_COLORS.maintenance,
              CHART_COLORS.offline,
            ],
            borderColor: [
              CHART_BORDER_COLORS.active,
              CHART_BORDER_COLORS.idle,
              CHART_BORDER_COLORS.maintenance,
              CHART_BORDER_COLORS.offline,
            ],
            borderWidth: 1,
          },
        ],
      }
    : null;

  const barData = data
    ? {
        labels: ['Active', 'Idle', 'Maintenance', 'Offline'],
        datasets: [
          {
            label: 'Fleet Units',
            data: [
              data.status_distribution.active,
              data.status_distribution.idle,
              data.status_distribution.maintenance,
              data.status_distribution.offline,
            ],
            backgroundColor: [
              CHART_COLORS.active,
              CHART_COLORS.idle,
              CHART_COLORS.maintenance,
              CHART_COLORS.offline,
            ],
            borderColor: [
              CHART_BORDER_COLORS.active,
              CHART_BORDER_COLORS.idle,
              CHART_BORDER_COLORS.maintenance,
              CHART_BORDER_COLORS.offline,
            ],
            borderWidth: 1,
            borderRadius: 4,
          },
        ],
      }
    : null;

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#c4c8c0',
          font: { family: 'Inter, system-ui, sans-serif', size: 12 },
          padding: 16,
        },
      },
      tooltip: {
        backgroundColor: '#1c2022',
        titleColor: '#dfe3e5',
        bodyColor: '#c4c8c0',
        borderColor: '#444842',
        borderWidth: 1,
      },
    },
  };

  const barOptions = {
    ...chartOptions,
    scales: {
      x: {
        ticks: { color: '#c4c8c0', font: { family: 'Inter, system-ui, sans-serif', size: 12 } },
        grid: { color: 'rgba(68, 72, 66, 0.4)' },
      },
      y: {
        ticks: { color: '#c4c8c0', font: { family: 'Inter, system-ui, sans-serif', size: 12 } },
        grid: { color: 'rgba(68, 72, 66, 0.4)' },
        beginAtZero: true,
      },
    },
  };

  // ── Render ──────────────────────────────────────────────────────────────────

  if (loading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <LoadingSpinner size="lg" label="Loading dashboard data…" centered />
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="text-center">
          <p className="text-title-md text-on-surface mb-2">Unable to load dashboard</p>
          <p className="text-body-md text-muted">Please check your connection and try again.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="responsive-container py-8">
        {/* Page header */}
        <div className="mb-8 flex items-start justify-between flex-wrap gap-4">
          <div>
            <h1 className="text-headline-lg text-on-surface">System Overview</h1>
            <p className="text-body-md text-muted mt-1">
              Real-time fleet operations and performance metrics
            </p>
          </div>
          {usingMock && (
            <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-error/10 border border-error/20">
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 text-error flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
              </svg>
              <span className="text-body-md text-error">Demo data — API offline</span>
            </div>
          )}
        </div>

        {/* Metric cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <MetricCard
            title="Total Fleet"
            value={data.total_fleet}
            unit="units"
            trend="stable"
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
              </svg>
            }
          />
          <MetricCard
            title="Active Units"
            value={data.active_units}
            unit="online"
            trend="up"
            trendValue={`${Math.round((data.active_units / data.total_fleet) * 100)}% of fleet`}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            }
          />
          <MetricCard
            title="Capacity Utilization"
            value={data.capacity_utilization.toFixed(1)}
            unit="%"
            trend={data.capacity_utilization >= 70 ? 'up' : 'down'}
            trendValue={data.capacity_utilization >= 70 ? 'Above target' : 'Below target'}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
              </svg>
            }
          />
          <MetricCard
            title="Efficiency Score"
            value={data.efficiency_score.toFixed(1)}
            unit="%"
            trend={data.efficiency_score >= 85 ? 'up' : 'stable'}
            trendValue={data.efficiency_score >= 85 ? 'Excellent' : 'Good'}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
              </svg>
            }
          />
        </div>

        {/* Charts row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Doughnut chart */}
          <div className="card">
            <div className="mb-4">
              <h3 className="text-title-md text-on-surface">Fleet Status Distribution</h3>
              <p className="text-body-md text-muted mt-0.5">Current operational breakdown</p>
            </div>
            <div className="h-64 flex items-center justify-center">
              {doughnutData && (
                <Doughnut
                  data={doughnutData}
                  options={{
                    ...chartOptions,
                    cutout: '65%',
                  }}
                />
              )}
            </div>
          </div>

          {/* Bar chart */}
          <div className="card">
            <div className="mb-4">
              <h3 className="text-title-md text-on-surface">Units by Status</h3>
              <p className="text-body-md text-muted mt-0.5">Comparative fleet status view</p>
            </div>
            <div className="h-64">
              {barData && (
                <Bar
                  data={barData}
                  options={barOptions}
                />
              )}
            </div>
          </div>
        </div>

        {/* Fleet table */}
        <FleetTable units={data.fleet_units} />
      </div>
    </div>
  );
};

export default Dashboard;
