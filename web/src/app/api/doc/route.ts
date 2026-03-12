import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const PROJECT_ROOT = path.resolve(process.cwd(), "..");
const ALLOWED = [
  "paper-criteria-alignment",
  "category-based-scoring",
  "benchmark-grading",
  "benchmark-immutability-controls",
  "industry-standards-compliance",
  "implementation-progress",
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const name = searchParams.get("name");

  if (!name || !ALLOWED.includes(name)) {
    return NextResponse.json({ error: "Invalid doc name" }, { status: 400 });
  }

  try {
    const filePath = path.join(
      PROJECT_ROOT,
      "Documentation",
      `${name}.md`
    );
    const content = fs.readFileSync(filePath, "utf-8");
    return NextResponse.json({ content });
  } catch (err) {
    return NextResponse.json({ error: "Doc not found" }, { status: 404 });
  }
}
