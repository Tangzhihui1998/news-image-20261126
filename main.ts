// Entry point for the news-image-20261126 bounty.
//
// Copies the front-page image (entry.png, drawn by generate.py) into the
// grader's output directory. No network, no clock, no randomness: the same
// input bytes always produce the same output bytes.
import { chmodSync, copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });

const source = join(repoRoot, "entry.png");
const destination = join(outputDir, "entry.png");
copyFileSync(source, destination);
chmodSync(destination, 0o644);

// Fail loudly instead of shipping a truncated copy.
if (statSync(destination).size !== statSync(source).size) {
  throw new Error(`entry.png copy size mismatch: ${destination}`);
}
console.log(`wrote ${destination}`);
