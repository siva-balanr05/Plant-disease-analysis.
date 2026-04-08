function ResultCard({ disease, confidence, timestamp }) {
  const confidencePercent = Math.round((confidence || 0) * 100);
  const isHealthy = disease.toLowerCase().includes("healthy");

  return (
    <article className="rounded-2xl border border-emerald-100 bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className={`text-lg font-bold ${isHealthy ? "text-emerald-700" : "text-red-600"}`}>
            {disease}
          </h3>
          <p className="mt-1 text-xs text-slate-500">
            {new Date(timestamp).toLocaleString(undefined, {
              dateStyle: "medium",
              timeStyle: "short",
            })}
          </p>
        </div>
        <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-800">
          {confidencePercent}%
        </span>
      </div>

      <div className="mt-4 h-2 w-full overflow-hidden rounded-full bg-slate-100">
        <progress
          className="h-2 w-full overflow-hidden rounded-full accent-emerald-500"
          max="100"
          value={confidencePercent}
        />
      </div>
    </article>
  );
}

export default ResultCard;
