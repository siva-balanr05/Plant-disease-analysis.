import { useMemo, useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";

import HistoryList from "../components/HistoryList";
import { getDiseaseSolution } from "../data/diseaseSolutions";

function Result() {
  const navigate = useNavigate();
  const location = useLocation();
  const [showHistory, setShowHistory] = useState(false);

  const resultState = location.state;

  if (!resultState || !resultState.result) {
    return <Navigate to="/upload" replace />;
  }

  const { result, imageUrl } = resultState;
  const disease = result.disease || "Unknown";
  const isHealthy = disease.toLowerCase().includes("healthy");
  const confidencePercent = Math.round((result.confidence || 0) * 100);
  const solution = getDiseaseSolution(disease);

  const topKRows = useMemo(() => {
    const topK = result.top_k || {};
    return Object.entries(topK);
  }, [result.top_k]);

  return (
    <section className="space-y-6">
      <div className="grid gap-6 rounded-3xl border border-emerald-100 bg-white p-6 shadow-sm lg:grid-cols-2">
        <div className="overflow-hidden rounded-2xl border border-emerald-100 bg-emerald-50 p-2">
          <img src={imageUrl} alt="Analysed plant" className="h-full min-h-72 w-full rounded-xl object-cover" />
        </div>

        <div className="space-y-5">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Diagnosis</p>
            <h1 className={`mt-2 text-3xl font-black ${isHealthy ? "text-emerald-700" : "text-red-600"}`}>
              {disease}
            </h1>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm font-medium text-slate-700">
              <span>Confidence</span>
              <span>{confidencePercent}%</span>
            </div>
            <progress
              className="h-3 w-full overflow-hidden rounded-full accent-emerald-500"
              max="100"
              value={confidencePercent}
            />
          </div>

          <p className="text-sm text-slate-600">
            <span className="font-semibold text-slate-700">Timestamp:</span>{" "}
            {new Date(result.timestamp).toLocaleString(undefined, {
              dateStyle: "full",
              timeStyle: "medium",
            })}
          </p>
          <p className="text-sm text-slate-600">
            <span className="font-semibold text-slate-700">Prediction ID:</span> {result.prediction_id}
          </p>

          <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-4">
            <h2 className="text-lg font-bold text-emerald-900">Recommended Solution</h2>
            <p className="mt-1 text-sm font-medium text-emerald-800">{solution.title}</p>
            <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-slate-700">
              {solution.steps.map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ul>
          </div>

          <div>
            <h2 className="mb-3 text-lg font-bold text-emerald-900">Top Predictions</h2>
            <div className="overflow-hidden rounded-xl border border-slate-200">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-50 text-slate-600">
                  <tr>
                    <th className="px-4 py-2">Label</th>
                    <th className="px-4 py-2">Confidence</th>
                  </tr>
                </thead>
                <tbody>
                  {topKRows.map(([label, score]) => (
                    <tr key={label} className="border-t border-slate-100">
                      <td className="px-4 py-2 font-medium text-slate-800">{label}</td>
                      <td className="px-4 py-2 text-slate-700">{Math.round(Number(score) * 100)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="flex flex-wrap gap-3">
            <button
              type="button"
              className="rounded-full bg-emerald-600 px-5 py-2 text-sm font-semibold text-white hover:bg-emerald-700"
              onClick={() => navigate("/upload")}
            >
              Analyse Another
            </button>
            <button
              type="button"
              className="rounded-full border border-emerald-200 px-5 py-2 text-sm font-semibold text-emerald-800 hover:bg-emerald-50"
              onClick={() => setShowHistory((prev) => !prev)}
            >
              View History
            </button>
          </div>
        </div>
      </div>

      {showHistory && (
        <div className="rounded-3xl border border-emerald-100 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-bold text-emerald-900">Prediction History</h2>
          <p className="mt-1 text-sm text-slate-600">Stored in backend logs.</p>
          <div className="mt-4">
            <HistoryList />
          </div>
        </div>
      )}
    </section>
  );
}

export default Result;
