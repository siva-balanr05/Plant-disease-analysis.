import { useEffect, useState } from "react";

import { getHistory } from "../services/api";
import ResultCard from "./ResultCard";

function HistoryList() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const predictions = await getHistory(20);
        setItems(predictions);
      } catch {
        setError("Unable to load prediction history right now.");
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  if (loading) {
    return <p className="text-sm text-slate-600">Loading history...</p>;
  }

  if (error) {
    return <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>;
  }

  if (!items.length) {
    return <p className="text-sm text-slate-600">No predictions yet</p>;
  }

  return (
    <div className="space-y-3">
      {items.map((item) => (
        <ResultCard
          key={item.id}
          disease={item.disease}
          confidence={item.confidence}
          timestamp={item.timestamp}
        />
      ))}
    </div>
  );
}

export default HistoryList;
