# PSAE Web

Informational Next.js frontend for the Pipeline Safety AI Evaluator project.

## Features

- **Overview** – Project vision, mission, and key differentiators
- **Dataset** – Benchmark corpus summary and manifest
- **Documentation** – Methodology and implementation docs
- **Results** – Model benchmarks and comparison tables with charts
- **White Paper** – Research framework and citation

## Run

From the `web` directory:

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Data

The app reads from the parent project's `data/`, `results/`, and `Documentation/` folders via API routes. Run the app from within the pipeline-safety-ai-evaluator repo (with `web/` as a subdirectory) so paths resolve correctly.

## Build

```bash
npm run build
npm start
```
