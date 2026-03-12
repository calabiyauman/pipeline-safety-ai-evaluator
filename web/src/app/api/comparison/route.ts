import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const PROJECT_ROOT = path.resolve(process.cwd(), "..");

export async function GET() {
  try {
    const filePath = path.join(PROJECT_ROOT, "results", "comparison_summary.json");
    const data = fs.readFileSync(filePath, "utf-8");
    const json = JSON.parse(data);
    return NextResponse.json(json);
  } catch (err) {
    return NextResponse.json(
      { error: "Comparison summary not found" },
      { status: 404 }
    );
  }
}
