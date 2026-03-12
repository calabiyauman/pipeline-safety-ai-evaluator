"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

const DOCS: Record<string, { title: string }> = {
  "paper-criteria": { title: "Paper Criteria Alignment" },
  "category-scoring": { title: "Category-Based Scoring" },
  "benchmark-grading": { title: "Benchmark Grading Methodology" },
  "benchmark-immutability": { title: "Benchmark Immutability Controls" },
  "industry-standards": { title: "Industry Standards Compliance" },
  implementation: { title: "Implementation Progress" },
};

const SLUG_TO_API: Record<string, string> = {
  "paper-criteria": "paper-criteria-alignment",
  "category-scoring": "category-based-scoring",
  "benchmark-grading": "benchmark-grading",
  "benchmark-immutability": "benchmark-immutability-controls",
  "industry-standards": "industry-standards-compliance",
  implementation: "implementation-progress",
};

export default function DocPage() {
  const params = useParams();
  const slug = params.slug as string;
  const [content, setContent] = useState<string | null>(null);

  const apiName = SLUG_TO_API[slug];
  const meta = DOCS[slug];

  useEffect(() => {
    if (!apiName) return;
    fetch(`/api/doc?name=${apiName}`)
      .then((r) => r.json())
      .then((d) => setContent(d.content ?? null))
      .catch(() => setContent(null));
  }, [apiName]);

  if (!meta) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-12">
        <p className="text-slate-500">Document not found</p>
        <a href="/documentation" className="mt-4 inline-block text-amber-600 hover:underline">
          Back to Documentation
        </a>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-12">
      <a
        href="/documentation"
        className="mb-6 inline-block text-sm text-amber-600 hover:underline"
      >
        ← Documentation
      </a>
      <h1 className="mb-8 text-3xl font-bold text-slate-900">{meta.title}</h1>
      {content ? (
        <article className="prose prose-slate max-w-none rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
          <pre className="whitespace-pre-wrap font-sans text-sm text-slate-700">
            {content}
          </pre>
        </article>
      ) : (
        <p className="text-slate-500">Loading...</p>
      )}
    </div>
  );
}
