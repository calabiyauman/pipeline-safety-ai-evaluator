
export default function WhitepaperPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12">
      <h1 className="mb-8 text-3xl font-bold text-slate-900">
        Pipeline Safety AI Evaluator: Research Framework
      </h1>

      <section className="mb-12 rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">Abstract</h2>
        <p className="leading-relaxed text-slate-600">
          The Pipeline Safety AI Evaluator (PSAE) provides a rigorous,
          scientifically-validated framework for evaluating AI systems in
          pipeline safety-critical applications. Built on peer-reviewed
          methodologies from NIST AI RMF, METR autonomy evaluation guidelines,
          and ACM AIware safety taxonomy, PSAE addresses the unique challenges
          of assessing AI in environments where incorrect recommendations can
          result in catastrophic failures, environmental disasters, or loss of
          life.
        </p>
      </section>

      <section className="mb-12 rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">
          STAR-R Framework
        </h2>
        <p className="mb-4 text-slate-600">
          Each test case follows the STAR-R framework:
        </p>
        <div className="grid gap-4 sm:grid-cols-2">
          {[
            {
              letter: "S",
              term: "Situation",
              desc: "Contextual background from real operations",
            },
            {
              letter: "T",
              term: "Task",
              desc: "Specific objective AI must accomplish",
            },
            {
              letter: "A",
              term: "Action",
              desc: "Expected correct procedure",
            },
            {
              letter: "R",
              term: "Result",
              desc: "Desired outcome metrics",
            },
            {
              letter: "R",
              term: "Risk",
              desc: "Consequences of AI failure",
            },
          ].map((item) => (
            <div
              key={item.letter}
              className="rounded-lg border border-slate-200 bg-slate-50 p-4"
            >
              <span className="text-2xl font-bold text-amber-600">
                {item.letter}
              </span>
              <span className="ml-2 font-semibold">{item.term}</span>
              <p className="mt-2 text-sm text-slate-500">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mb-12 rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">
          Safety-Critical Multipliers
        </h2>
        <div className="overflow-hidden rounded-lg border border-slate-200">
          <table className="w-full text-left">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-3 font-semibold text-slate-900">
                  Test Category
                </th>
                <th className="px-6 py-3 font-semibold text-slate-900">
                  Risk Level
                </th>
                <th className="px-6 py-3 font-semibold text-slate-900">
                  Score Multiplier
                </th>
                <th className="px-6 py-3 font-semibold text-slate-900">
                  Penalty Weight
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              <tr>
                <td className="px-6 py-4 font-medium">Safety-Critical</td>
                <td className="px-6 py-4">10/10</td>
                <td className="px-6 py-4">1.3x</td>
                <td className="px-6 py-4">2.0x</td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-medium">High-Risk</td>
                <td className="px-6 py-4">8–9/10</td>
                <td className="px-6 py-4">1.2x</td>
                <td className="px-6 py-4">1.5x</td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-medium">Standard</td>
                <td className="px-6 py-4">5–7/10</td>
                <td className="px-6 py-4">1.0x</td>
                <td className="px-6 py-4">1.0x</td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-medium">Informational</td>
                <td className="px-6 py-4">1–4/10</td>
                <td className="px-6 py-4">0.9x</td>
                <td className="px-6 py-4">0.5x</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section className="mb-12 rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">
          Research Foundations
        </h2>
        <p className="mb-4 text-slate-600">
          PSAE is built on peer-reviewed methodologies from:
        </p>
        <ul className="list-inside list-disc space-y-2 text-slate-600">
          <li>NIST AI Risk Management Framework (AI RMF 1.0)</li>
          <li>METR Autonomy Evaluation Guidelines</li>
          <li>ACM AIware 2024 Safety Taxonomy</li>
          <li>PHMSA OQ Guidelines</li>
          <li>Leveson&apos;s STAMP Framework</li>
        </ul>
      </section>

      <section className="mb-12 rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">
          Paper Readiness
        </h2>
        <p className="mb-4 text-slate-600">
          The PSAE framework aligns with PipelineAIEvalPaper2026 criteria. A
          readiness gate script verifies statistical configuration, minimum runs,
          and corpus coverage before publication.
        </p>
        <a
          href="/documentation/paper-criteria"
          className="inline-block rounded-lg bg-amber-600 px-4 py-2 text-sm font-medium text-white hover:bg-amber-700"
        >
          View Paper Criteria Alignment →
        </a>
      </section>

      <section className="rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">
          Citation
        </h2>
        <pre className="overflow-x-auto rounded-lg bg-slate-50 p-4 text-sm font-mono text-slate-700">
{`@software{psae2026,
  title = {Pipeline Safety AI Evaluator: A Framework for Safety-Critical AI Evaluation},
  author = {Carnahan, Doug and et al.},
  year = {2026},
  url = {https://github.com/calabiyauman/pipeline-safety-ai-evaluator},
  version = {0.1.0}
}`}
        </pre>
      </section>
    </div>
  );
}
