"use client";

import { useEffect, useState } from "react";

interface DatasetSummary {
  categories: Record<string, number>;
  source?: string;
  files?: string[];
}

interface Manifest {
  manifest_version: string;
  dataset_version: string;
  files: Record<string, string>;
}

const DATASET_FILES = [
  "safety_critical",
  "engineering",
  "inspection",
  "regulatory",
] as const;

export default function DatasetPage() {
  const [summary, setSummary] = useState<DatasetSummary | null>(null);
  const [manifest, setManifest] = useState<Manifest | null>(null);
  const [selectedFile, setSelectedFile] = useState<string>("safety_critical");
  const [rawJson, setRawJson] = useState<string | null>(null);
  const [rawLoading, setRawLoading] = useState(false);

  useEffect(() => {
    fetch("/api/dataset")
      .then((r) => r.json())
      .then(setSummary);
    fetch("/api/manifest")
      .then((r) => r.json())
      .then(setManifest)
      .catch(() => setManifest(null));
  }, []);

  useEffect(() => {
    setRawLoading(true);
    setRawJson(null);
    fetch(`/api/dataset?file=${selectedFile}`)
      .then((r) => r.json())
      .then((data) => setRawJson(JSON.stringify(data, null, 2)))
      .catch(() => setRawJson(null))
      .finally(() => setRawLoading(false));
  }, [selectedFile]);

  const categories = summary?.categories ?? {};
  const total = Object.values(categories).reduce((a, b) => a + b, 0);

  return (
    <div className="mx-auto max-w-4xl px-4 py-12">
      <h1 className="mb-8 text-3xl font-bold text-slate-900">Dataset</h1>

      <section className="mb-12 rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">
          Benchmark Corpus
        </h2>
        <p className="mb-4 text-slate-600">
          The PSAE benchmark uses the four canonical JSON files in{" "}
          <code className="rounded bg-slate-100 px-1 py-0.5 font-mono text-sm">
            data/test_cases/
          </code>
          —one per category. The evaluator and benchmark script load from these
          files exclusively.
        </p>
        <p className="mb-6 text-slate-600">
          To expand the dataset, add test questions to the JSON files below.
        </p>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {Object.entries(categories).map(([name, count]) => (
            <div
              key={name}
              className="rounded-lg border border-slate-200 bg-slate-50 p-4"
            >
              <div className="text-2xl font-bold text-amber-600">{count}</div>
              <div className="text-sm font-medium capitalize text-slate-700">
                {name.replace("_", " ")}
              </div>
            </div>
          ))}
        </div>
        <div className="mt-4 rounded-lg bg-amber-50 p-4 text-amber-800">
          <strong>Total:</strong> {total} test scenarios
        </div>
      </section>

      <section className="mb-12 rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">
          Benchmark Manifest
        </h2>
        <p className="mb-4 text-slate-600">
          Dataset integrity is verified via SHA-256 checksums. Manifest version
          and file hashes ensure reproducibility.
        </p>
        {manifest ? (
          <div className="space-y-2 text-sm">
            <div className="flex gap-4">
              <span className="font-medium text-slate-500">
                Manifest version:
              </span>
              <span>{manifest.manifest_version}</span>
            </div>
            <div className="flex gap-4">
              <span className="font-medium text-slate-500">
                Dataset version:
              </span>
              <span>{manifest.dataset_version}</span>
            </div>
            <div className="mt-4">
              <span className="font-medium text-slate-500">Tracked files:</span>
              <ul className="mt-2 space-y-1 rounded bg-slate-50 p-4 font-mono text-xs">
                {Object.keys(manifest.files ?? {}).map((f) => (
                  <li key={f}>{f}</li>
                ))}
              </ul>
            </div>
          </div>
        ) : (
          <p className="text-slate-500">Manifest not available</p>
        )}
      </section>

      <section className="mb-12 rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">
          Raw JSON Dataset
        </h2>
        <p className="mb-4 text-slate-600">
          Browse the raw test case JSON for each category.
        </p>
        <div className="mb-4 flex flex-wrap gap-2">
          {DATASET_FILES.map((file) => (
            <button
              key={file}
              onClick={() => setSelectedFile(file)}
              className={`rounded-lg px-4 py-2 text-sm font-medium transition ${
                selectedFile === file
                  ? "bg-amber-600 text-white"
                  : "bg-slate-100 text-slate-700 hover:bg-slate-200"
              }`}
            >
              {file.replace("_", " ")}
            </button>
          ))}
        </div>
        <div className="overflow-hidden rounded-lg border border-slate-200 bg-slate-900">
          <pre className="max-h-96 overflow-auto p-4 font-mono text-xs text-slate-100">
            {rawLoading ? (
              <span className="text-amber-400">Loading...</span>
            ) : rawJson ? (
              <code>{rawJson}</code>
            ) : (
              <span className="text-red-400">Failed to load</span>
            )}
          </pre>
        </div>
      </section>

      <section className="rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">
          Test Categories
        </h2>
        <div className="overflow-hidden rounded-lg border border-slate-200">
          <table className="w-full text-left">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-3 font-semibold text-slate-900">
                  Category
                </th>
                <th className="px-6 py-3 font-semibold text-slate-900">
                  Risk Level
                </th>
                <th className="px-6 py-3 font-semibold text-slate-900">
                  Description
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              <tr>
                <td className="px-6 py-4 font-medium">Safety-Critical</td>
                <td className="px-6 py-4">10/10</td>
                <td className="px-6 py-4 text-slate-600">
                  Hot tapping, emergency response, confined space, H2S
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-medium">Engineering</td>
                <td className="px-6 py-4">8–9/10</td>
                <td className="px-6 py-4 text-slate-600">
                  Valve sizing, hydrotest, corrosion, CP, stress analysis
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-medium">Inspection</td>
                <td className="px-6 py-4">7–9/10</td>
                <td className="px-6 py-4 text-slate-600">
                  ILI, corrosion growth, dig prioritization, repair verification
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-medium">Regulatory</td>
                <td className="px-6 py-4">5–8/10</td>
                <td className="px-6 py-4 text-slate-600">
                  PHMSA incident reporting, compliance, standards selection
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
