import { useMemo, useState } from "react";
import { Search, Activity, ShieldCheck, Zap, Database, CircleDot } from "lucide-react";

const logSamples = [
  {
    id: 1,
    timestamp: "2026-07-24 12:18:43",
    level: "INFO",
    service: "auth-service",
    message: "User login succeeded for user@example.com",
  },
  {
    id: 2,
    timestamp: "2026-07-24 12:18:44",
    level: "WARN",
    service: "processor-service",
    message: "Event batch delayed by 120ms due to queue throttling.",
  },
  {
    id: 3,
    timestamp: "2026-07-24 12:18:46",
    level: "ERROR",
    service: "auth-service",
    message: "Failed JWT validation for token request from /api/v1/auth/refresh.",
  },
  {
    id: 4,
    timestamp: "2026-07-24 12:18:49",
    level: "INFO",
    service: "processor-service",
    message: "Log normalization pipeline completed for incoming payload.",
  },
  {
    id: 5,
    timestamp: "2026-07-24 12:18:52",
    level: "INFO",
    service: "auth-service",
    message: "New user registered and verification email queued.",
  },
];

const levelVariants = {
  INFO: "bg-emerald-500/10 text-emerald-300 border border-emerald-500/30",
  WARN: "bg-amber-500/10 text-amber-300 border border-amber-500/30",
  ERROR: "bg-rose-500/10 text-rose-300 border border-rose-500/30",
};

function LogPulseDashboard() {
  const [query, setQuery] = useState("");

  const filteredLogs = useMemo(
    () =>
      logSamples.filter((log) => {
        const keyword = query.toLowerCase();
        return (
          log.message.toLowerCase().includes(keyword) ||
          log.service.toLowerCase().includes(keyword) ||
          log.level.toLowerCase().includes(keyword)
        );
      }),
    [query]
  );

  return (
    <div className="app-shell">
      <div className="app-container">
        <header className="card card-hero p-6">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div className="space-y-3">
              <div className="flex items-center gap-3 text-slate-300">
                <span className="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-slate-800 text-indigo-300 shadow-inner shadow-indigo-500/20">
                  <CircleDot className="h-5 w-5" />
                </span>
                <div>
                  <p className="text-sm uppercase tracking-[0.25em] text-indigo-300/80">LogPulse Engine</p>
                  <h1 className="text-3xl font-semibold text-slate-50 sm:text-4xl">Cloud-Native Log Analytics</h1>
                </div>
              </div>
              <p className="max-w-2xl text-slate-400">
                A modern observability console for Kubernetes log ingestion, microservice health, and live event streaming.
              </p>
            </div>

            <div className="inline-flex items-center gap-3 rounded-3xl border border-slate-800/90 bg-slate-950 px-4 py-3 text-slate-100 shadow-sm shadow-slate-950/20">
              <span className="flex h-3.5 w-3.5 animate-pulse rounded-full bg-emerald-400 shadow-xl shadow-emerald-500/30"></span>
              <span className="text-sm font-medium text-emerald-300">K8s Cluster: Healthy</span>
            </div>
          </div>
        </header>

        <section className="grid gap-4 xl:grid-cols-4">
          <MetricCard
            icon={<Activity className="h-5 w-5 text-indigo-300" />}
            title="Active Microservices"
            value="2 Online"
            description="Auth & Processor"
          />
          <MetricCard
            icon={<Zap className="h-5 w-5 text-emerald-300" />}
            title="Log Ingestion Rate"
            value="1,420 /sec"
            description="Sustained throughput over the last minute"
          />
          <MetricCard
            icon={<ShieldCheck className="h-5 w-5 text-amber-300" />}
            title="Error Rate"
            value="0.02%"
            description="Very low error volume across the cluster"
          />
          <MetricCard
            icon={<Database className="h-5 w-5 text-sky-300" />}
            title="Storage Utilization"
            value="1.2 GB / 5 GB PVC"
            description="Current log persistence consumption"
          />
        </section>

        <main className="card card-panel">
          <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Live Event Stream</p>
              <h2 className="mt-2 text-2xl font-semibold text-slate-50">Terminal-style log feed</h2>
            </div>
            <div className="relative w-full max-w-md">
              <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
              <input
                type="search"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search logs, services, or levels"
                className="search-input"
              />
            </div>
          </div>

          <div className="overflow-hidden rounded-3xl border border-slate-800 bg-slate-950/80 shadow-inner shadow-slate-950/20">
            <div className="log-table-header">
              <span className="text-xs uppercase tracking-[0.24em]">Timestamp</span>
              <span className="text-xs uppercase tracking-[0.24em]">Service</span>
              <span className="text-xs uppercase tracking-[0.24em]">Message</span>
            </div>
            <div className="max-h-[520px] space-y-2 overflow-y-auto px-6 py-5">
              {filteredLogs.map((log) => (
                <div
                  key={log.id}
                  className="log-row"
                >
                  <div className="text-slate-400">{log.timestamp}</div>
                  <div className="flex flex-wrap items-center gap-2">
                    <span className={`status-pill ${levelVariants[log.level]}`}>
                      {log.level}
                    </span>
                    <span className="rounded-full bg-slate-950/80 px-2 py-1 text-xs text-slate-300">{log.service}</span>
                  </div>
                  <div className="text-slate-300">{log.message}</div>
                </div>
              ))}
              {filteredLogs.length === 0 && (
                <div className="rounded-3xl border border-dashed border-slate-700 bg-slate-900/80 px-6 py-10 text-center text-slate-500">
                  No logs match your search filter.
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

function MetricCard({ icon, title, value, description }) {
  return (
    <div className="metric-card">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-950 text-indigo-300 shadow-inner shadow-indigo-500/10">
            {icon}
          </div>
          <div>
            <p className="text-sm font-medium text-slate-400">{title}</p>
            <p className="mt-2 text-2xl font-semibold text-slate-50">{value}</p>
          </div>
        </div>
      </div>
      <p className="mt-4 text-sm leading-6 text-slate-400">{description}</p>
    </div>
  );
}

export default LogPulseDashboard;
