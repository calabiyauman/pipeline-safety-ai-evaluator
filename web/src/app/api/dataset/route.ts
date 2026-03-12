import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const PROJECT_ROOT = path.resolve(process.cwd(), "..");
const TEST_CASES = ["safety_critical", "engineering", "inspection", "regulatory"];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const file = searchParams.get("file");

  if (file && TEST_CASES.includes(file)) {
    try {
      const filePath = path.join(PROJECT_ROOT, "data", "test_cases", `${file}.json`);
      const data = fs.readFileSync(filePath, "utf-8");
      const json = JSON.parse(data);
      return NextResponse.json(json);
    } catch (err) {
      return NextResponse.json({ error: "File not found" }, { status: 404 });
    }
  }

  const summary: Record<string, number> = {};
  for (const name of TEST_CASES) {
    try {
      const filePath = path.join(PROJECT_ROOT, "data", "test_cases", `${name}.json`);
      const data = fs.readFileSync(filePath, "utf-8");
      const json = JSON.parse(data);
      const count = Array.isArray(json)
        ? json.length
        : (json.scenarios?.length ?? json.test_cases?.length ?? 0);
      summary[name] = count;
    } catch {
      summary[name] = 0;
    }
  }
  return NextResponse.json({
    categories: summary,
    source: "data/test_cases/",
    files: TEST_CASES.map((n) => `${n}.json`),
  });
}
