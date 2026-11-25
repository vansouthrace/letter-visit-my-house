// Entry point for the make.fun "Convince the AI Judge to Visit Your House"
// bounty. Copies the pre-rendered letter image (entry.png, produced by
// render.py) into MAKEFUN_OUTPUT_DIR as entry.png, after verifying it is a
// whole 1024x1024 PNG within the 1 MiB gate. Node 22, standard library only.
// Deterministic: running twice writes identical bytes.

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1_048_576;
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;

function fail(message: string): never {
  console.error(`error: ${message}`);
  process.exit(1);
}

function readPngDimensions(buf: Buffer): { width: number; height: number } {
  const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  if (buf.length < 33 || !buf.subarray(0, 8).equals(PNG_SIGNATURE)) {
    fail("entry.png is not a PNG file");
  }
  const chunkType = buf.toString("ascii", 12, 16);
  if (chunkType !== "IHDR") {
    fail("entry.png has no IHDR chunk where one was expected");
  }
  return {
    width: buf.readUInt32BE(16),
    height: buf.readUInt32BE(20),
  };
}

const here = dirname(fileURLToPath(import.meta.url));
const source = resolve(here, "entry.png");
if (!existsSync(source)) {
  fail(`entry.png not found next to main.ts (${source}); run render.py first`);
}

const bytes = readFileSync(source);
if (bytes.length > MAX_BYTES) {
  fail(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
const { width, height } = readPngDimensions(bytes);
if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
  fail(`entry.png is ${width}x${height}, expected 1024x1024`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(source, dest);

const written = statSync(dest).size;
if (written !== bytes.length || !readFileSync(dest).equals(bytes)) {
  fail("copied entry.png does not match the source byte for byte");
}
console.log(`wrote ${dest} (${written} bytes, ${width}x${height} PNG)`);
