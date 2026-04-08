import { useRef, useState } from "react";

function ImageUploader({ onFileSelect, accept = "image/jpeg,image/png", maxSizeMB = 5 }) {
  const inputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState("");

  const validateFile = (file) => {
    if (!file) {
      return false;
    }

    if (!["image/jpeg", "image/png"].includes(file.type)) {
      setError("Only JPEG and PNG images are allowed.");
      return false;
    }

    if (file.size > maxSizeMB * 1024 * 1024) {
      setError(`File exceeds ${maxSizeMB}MB limit.`);
      return false;
    }

    setError("");
    return true;
  };

  const handleFile = (file) => {
    if (validateFile(file)) {
      onFileSelect(file);
    }
  };

  const onDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);
    const file = event.dataTransfer.files?.[0];
    handleFile(file);
  };

  return (
    <div className="space-y-3">
      <div
        className={`rounded-2xl border-2 border-dashed p-8 text-center transition ${
          isDragging
            ? "border-emerald-500 bg-emerald-50"
            : "border-emerald-200 bg-white hover:border-emerald-400"
        }`}
        onDragOver={(event) => {
          event.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={onDrop}
      >
        <p className="text-lg font-semibold text-emerald-900">Drag and drop your plant image</p>
        <p className="mt-2 text-sm text-slate-600">JPG or PNG, up to {maxSizeMB}MB</p>
        <button
          type="button"
          className="mt-5 rounded-full bg-emerald-600 px-5 py-2 text-sm font-semibold text-white hover:bg-emerald-700"
          onClick={() => inputRef.current?.click()}
        >
          Select File
        </button>
        <input
          ref={inputRef}
          type="file"
          accept={accept}
          className="hidden"
          onChange={(event) => handleFile(event.target.files?.[0])}
        />
      </div>

      {error && <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
    </div>
  );
}

export default ImageUploader;
