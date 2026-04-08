import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import HistoryList from "../components/HistoryList";
import { checkHealth } from "../services/api";

function Home() {
  const [health, setHealth] = useState({ loading: true, ok: false, modelLoaded: false, device: "-" });

  useEffect(() => {
    const loadHealth = async () => {
      try {
        const response = await checkHealth();
        setHealth({
          loading: false,
          ok: response.status === "ok",
          modelLoaded: Boolean(response.model_loaded),
          device: response.device || "unknown",
        });
      } catch {
        setHealth({ loading: false, ok: false, modelLoaded: false, device: "unreachable" });
      }
    };

    loadHealth();
  }, []);

  return (
    <div className="space-y-10">
      <section className="rounded-3xl border border-emerald-100 bg-white px-6 py-10 shadow-sm sm:px-10">
        <div className="max-w-3xl space-y-5">
          <span className="inline-flex items-center rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-emerald-800">
            Offline Plant Intelligence
          </span>
          <h1 className="text-4xl font-black tracking-tight text-emerald-900 sm:text-5xl">
            Plant Disease Detection
          </h1>
          <p className="text-lg text-slate-600">AI-powered offline plant health analysis</p>

          <div className="flex flex-wrap gap-3">
            <Link
              to="/upload"
              className="rounded-full bg-emerald-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-emerald-700"
            >
              Upload Image
            </Link>
            <a
              href="#history"
              className="rounded-full border border-emerald-200 bg-white px-6 py-3 text-sm font-semibold text-emerald-800 transition hover:border-emerald-300 hover:bg-emerald-50"
            >
              View History
            </a>
          </div>

          <div className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700">
            <span
              className={`h-2.5 w-2.5 rounded-full ${
                health.loading ? "bg-amber-400" : health.ok && health.modelLoaded ? "bg-emerald-500" : "bg-red-500"
              }`}
            />
            {health.loading
              ? "Checking API health..."
              : `API ${health.ok ? "online" : "offline"} | Model ${
                  health.modelLoaded ? "loaded" : "not loaded"
                } | Device: ${health.device}`}
          </div>
        </div>
      </section>

      <section id="history" className="rounded-3xl border border-emerald-100 bg-white px-6 py-6 shadow-sm sm:px-8">
        <h2 className="text-xl font-bold text-emerald-900">Recent Analyses</h2>
        <p className="mt-1 text-sm text-slate-600">Latest predictions from the local backend.</p>
        <div className="mt-5">
          <HistoryList />
        </div>
      </section>
    </div>
  );
}

export default Home;
