
export default function HomePage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12">
      <div className="mb-12 text-center">
        <h1 className="mb-4 text-4xl font-bold tracking-tight text-slate-900">
          Pipeline Safety AI Evaluator
        </h1>
        <p className="text-xl text-slate-600">
          A rigorous evaluation framework for AI systems in pipeline
          safety-critical applications
        </p>
        <p className="mt-2 text-sm text-slate-500">Version 0.1.0 | Beta</p>
      </div>

      <section className="mb-12 rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-2xl font-semibold text-slate-900">
          Mission Statement
        </h2>
        <p className="leading-relaxed text-slate-600">
          PSAE provides a scientifically-validated framework for evaluating AI
          systems in pipeline safety-critical applications. Built on
          peer-reviewed methodologies from safety-critical systems research, PSAE
          addresses the unique challenges of assessing AI in environments where
          incorrect recommendations can result in catastrophic failures,
          environmental disasters, or loss of life.
        </p>
      </section>

      <section className="mb-12">
        <h2 className="mb-6 text-2xl font-semibold text-slate-900">
          Key Differentiators
        </h2>
        <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
          <table className="w-full text-left">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-4 font-semibold text-slate-900">
                  Feature
                </th>
                <th className="px-6 py-4 font-semibold text-slate-900">
                  Industry Standard
                </th>
                <th className="px-6 py-4 font-semibold text-slate-900">
                  PSAE Innovation
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              <tr>
                <td className="px-6 py-4 font-medium">Test Coverage</td>
                <td className="px-6 py-4 text-slate-600">
                  Normal operations only
                </td>
                <td className="px-6 py-4 text-slate-600">
                  Normal + abnormal + edge cases
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-medium">Statistical Rigor</td>
                <td className="px-6 py-4 text-slate-600">
                  Basic accuracy metrics
                </td>
                <td className="px-6 py-4 text-slate-600">
                  Confidence intervals, significance testing
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-medium">Human Factors</td>
                <td className="px-6 py-4 text-slate-600">AI-only testing</td>
                <td className="px-6 py-4 text-slate-600">
                  Human-AI collaborative evaluation
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-medium">Real-World Validation</td>
                <td className="px-6 py-4 text-slate-600">
                  Theoretical scenarios
                </td>
                <td className="px-6 py-4 text-slate-600">
                  PHMSA incident-based test cases
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-medium">Safety Weighting</td>
                <td className="px-6 py-4 text-slate-600">
                  Equal weight to all tests
                </td>
                <td className="px-6 py-4 text-slate-600">
                  Risk-adjusted safety multipliers
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-medium">Reproducibility</td>
                <td className="px-6 py-4 text-slate-600">
                  Limited documentation
                </td>
                <td className="px-6 py-4 text-slate-600">
                  Full protocol + code + data
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section className="mb-12 rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-2xl font-semibold text-slate-900">
          Evaluation Framework
        </h2>
        <p className="mb-4 text-slate-600">
          PSAE evaluates AI across six weighted primary metrics:
        </p>
        <div className="grid gap-4 sm:grid-cols-2">
          {[
            { name: "Accuracy", weight: "25%", desc: "Information correctness" },
            { name: "Relevance", weight: "20%", desc: "Domain appropriateness" },
            { name: "Safety", weight: "20%", desc: "Protocol adherence" },
            { name: "Completeness", weight: "15%", desc: "Coverage of aspects" },
            { name: "Technical Depth", weight: "10%", desc: "Engineering calculations" },
            { name: "Sources", weight: "10%", desc: "Reference utilization" },
          ].map((m) => (
            <div
              key={m.name}
              className="rounded-lg border border-slate-200 bg-slate-50 p-4"
            >
              <div className="flex justify-between">
                <span className="font-medium">{m.name}</span>
                <span className="text-amber-600">{m.weight}</span>
              </div>
              <p className="mt-1 text-sm text-slate-500">{m.desc}</p>
            </div>
          ))}
        </div>
        <a
          href="/documentation/benchmark-grading"
          className="mt-4 inline-block text-sm text-amber-600 hover:underline"
        >
          Full grading methodology (risk multipliers, penalties, pass/fail) →
        </a>
      </section>

      <section className="grid gap-6 sm:grid-cols-2">
        <a
          href="/dataset"
          className="block rounded-xl border border-slate-200 bg-white p-6 shadow-sm transition hover:border-amber-300 hover:shadow-md"
        >
          <h3 className="font-semibold text-slate-900">Dataset</h3>
          <p className="mt-2 text-sm text-slate-500">
            Explore test cases, benchmarks, and human baseline data
          </p>
        </a>
        <a
          href="/results"
          className="block rounded-xl border border-slate-200 bg-white p-6 shadow-sm transition hover:border-amber-300 hover:shadow-md"
        >
          <h3 className="font-semibold text-slate-900">Results</h3>
          <p className="mt-2 text-sm text-slate-500">
            View model benchmarks, comparisons, and evaluation reports
          </p>
        </a>
        <a
          href="/documentation"
          className="block rounded-xl border border-slate-200 bg-white p-6 shadow-sm transition hover:border-amber-300 hover:shadow-md"
        >
          <h3 className="font-semibold text-slate-900">Documentation</h3>
          <p className="mt-2 text-sm text-slate-500">
            Methodology, implementation guides, and compliance standards
          </p>
        </a>
        <a
          href="/whitepaper"
          className="block rounded-xl border border-slate-200 bg-white p-6 shadow-sm transition hover:border-amber-300 hover:shadow-md"
        >
          <h3 className="font-semibold text-slate-900">White Paper</h3>
          <p className="mt-2 text-sm text-slate-500">
            Research paper alignment and methodology details
          </p>
        </a>
      </section>
    </div>
  );
}
