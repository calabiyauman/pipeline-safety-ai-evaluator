
const docs = [
  {
    title: "Paper Criteria Alignment",
    href: "/documentation/paper-criteria",
    desc: "Implementation status against PipelineAIEvalPaper2026 recommendations",
  },
  {
    title: "Category-Based Scoring",
    href: "/documentation/category-scoring",
    desc: "Per-category grades and combined final score methodology",
  },
  {
    title: "Benchmark Grading Methodology",
    href: "/documentation/benchmark-grading",
    desc: "How the benchmark scores AI responses: metrics, risk multipliers, penalties, pass/fail",
  },
  {
    title: "Benchmark Immutability Controls",
    href: "/documentation/benchmark-immutability",
    desc: "Signed manifest workflow for dataset integrity",
  },
  {
    title: "Industry Standards Compliance",
    href: "/documentation/industry-standards",
    desc: "Alignment with NIST AI RMF, METR, and safety-critical standards",
  },
  {
    title: "Implementation Progress",
    href: "/documentation/implementation",
    desc: "Feature development status and roadmap",
  },
];

export default function DocumentationPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12">
      <h1 className="mb-8 text-3xl font-bold text-slate-900">Documentation</h1>

      <section className="mb-12 rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">
          Methodology Overview
        </h2>
        <p className="mb-4 text-slate-600">
          PSAE evaluates AI systems using the STAR-R framework (Situation, Task,
          Action, Result, Risk). Each test case follows peer-reviewed
          methodologies from NIST AI RMF, METR autonomy evaluation guidelines,
          and ACM AIware safety taxonomy.
        </p>
        <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
          <h3 className="font-medium text-slate-900">Statistical Requirements</h3>
          <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-slate-600">
            <li>Confidence level: 95%</li>
            <li>Minimum runs per scenario: 5</li>
            <li>Inter-rater reliability: Cohen&apos;s κ ≥ 0.8</li>
            <li>Effect size: Cohen&apos;s d for model comparison</li>
          </ul>
        </div>
      </section>

      <section>
        <h2 className="mb-6 text-xl font-semibold text-slate-900">
          Documentation Index
        </h2>
        <div className="space-y-4">
          {docs.map((doc) => (
            <a
              key={doc.href}
              href={doc.href}
              className="block rounded-xl border border-slate-200 bg-white p-6 shadow-sm transition hover:border-amber-300 hover:shadow-md"
            >
              <h3 className="font-semibold text-slate-900">{doc.title}</h3>
              <p className="mt-2 text-sm text-slate-500">{doc.desc}</p>
            </a>
          ))}
        </div>
      </section>
    </div>
  );
}
