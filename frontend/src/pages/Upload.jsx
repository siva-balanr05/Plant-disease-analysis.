import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import ImageUploader from "../components/ImageUploader";
import { predictDisease } from "../services/api";

function Upload() {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);
  const [imageUrl, setImageUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    return () => {
      if (imageUrl) {
        URL.revokeObjectURL(imageUrl);
      }
    };
  }, [imageUrl]);

  const handleFileSelect = (file) => {
    setError("");

    if (!file) {
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setError("File size must be under 5MB.");
      return;
    }

    if (imageUrl) {
      URL.revokeObjectURL(imageUrl);
    }

    setSelectedFile(file);
    setImageUrl(URL.createObjectURL(file));
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setError("Please select an image before analysing.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const result = await predictDisease(selectedFile);
      navigate("/result", { state: { result, imageUrl } });
    } catch (submitError) {
      const message =
        submitError?.response?.data?.detail || "Prediction failed. Please check backend connection.";
      setError(String(message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="mx-auto w-full max-w-3xl space-y-6 rounded-3xl border border-emerald-100 bg-white p-6 shadow-sm sm:p-8">
      <div>
        <h1 className="text-3xl font-black text-emerald-900">Upload Plant Image</h1>
        <p className="mt-2 text-sm text-slate-600">Drop a clear leaf photo for disease analysis.</p>
      </div>

      <ImageUploader onFileSelect={handleFileSelect} accept="image/jpeg,image/png" maxSizeMB={5} />

      {imageUrl && (
        <div className="overflow-hidden rounded-2xl border border-emerald-100 bg-emerald-50 p-2">
          <img src={imageUrl} alt="Selected preview" className="h-72 w-full rounded-xl object-cover" />
        </div>
      )}

      {error && <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

      <button
        type="button"
        onClick={handleSubmit}
        disabled={loading}
        className="inline-flex min-w-40 items-center justify-center rounded-full bg-emerald-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-emerald-300"
      >
        {loading ? (
          <span className="inline-flex items-center gap-2">
            <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
            Analysing...
          </span>
        ) : (
          "Analyse Plant"
        )}
      </button>
    </section>
  );
}

export default Upload;
