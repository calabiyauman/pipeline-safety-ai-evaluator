# PSAE Web Frontend

## Overview

A Next.js informational frontend for the Pipeline Safety AI Evaluator project. Displays project vision, dataset, documentation, results, and white paper content.

## Features

- **Overview** – Mission statement, key differentiators, evaluation framework
- **Dataset** – Benchmark corpus summary, manifest, test categories
- **Documentation** – Methodology overview and links to markdown docs
- **Results** – Model benchmark tables, comparison by category, bar visualizations
- **White Paper** – STAR-R framework, safety multipliers, research foundations, citation

## Run

From the project root:

```bash
cd web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Data Sources

The app reads from the parent project via API routes:

- `results/model_benchmark_scores.json` – Quick benchmark scores
- `results/comparison_summary.json` – Model comparison with category scores
- `data/benchmark_manifest.json` – Dataset integrity manifest
- `data/test_cases/*.json` – Test case counts
- `Documentation/*.md` – Doc content (paper-criteria, category-scoring, etc.)

Run the app from within the pipeline-safety-ai-evaluator repo so paths resolve correctly.

## Build

```bash
cd web
npm run build
npm start
```

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Static + API routes for data
