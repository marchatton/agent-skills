#!/usr/bin/env node

// Firecrawl "Branding Format v2" receipt fetcher.
//
// Usage (dry-run):
//   node --experimental-strip-types ./firecrawl_branding_v2.ts --config path/to/config.json --run-folder path/to/run --dry-run

const fs = require('node:fs');
const path = require('node:path');

const API_ENDPOINT = 'https://api.firecrawl.dev/v2/scrape';

const usage = () => {
  return [
    'Fetch Firecrawl Branding Format v2 receipts (v2 scrape endpoint).',
    '',
    'Required:',
    '  --config <path>        Path to config JSON (must include run_id and urls[])',
    '  --run-folder <path>    Run folder root where .firecrawl/ will be created',
    '',
    'Optional:',
    '  --wait-for <ms>        waitFor ms (default: 10000)',
    '  --concurrency <n>      Max parallel requests (default: 4)',
    '  --dry-run              No network; print planned output file paths + request summary',
    '  --force                Overwrite existing receipts',
    '',
    'Env:',
    '  FIRECRAWL_API_KEY      Required unless --dry-run',
  ].join('\n');
};

const fail = (message) => {
  console.error(`ERROR: ${message}`);
  console.error('');
  console.error(usage());
  process.exit(1);
};

const nowUtc = () => new Date().toISOString();

const sanitizeSlug = (value) => {
  const slug = String(value)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-+/, '')
    .replace(/-+$/, '');
  return slug || 'site';
};

const parseArgs = (argv) => {
  const args = argv.slice(2);
  const out = {
    configPath: null,
    runFolder: null,
    waitForMs: 10000,
    concurrency: 4,
    dryRun: false,
    force: false,
  };

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];

    if (arg === '--dry-run') {
      out.dryRun = true;
      continue;
    }

    if (arg === '--force') {
      out.force = true;
      continue;
    }

    if (arg === '--config') {
      out.configPath = args[i + 1] ?? null;
      i += 1;
      continue;
    }

    if (arg === '--run-folder') {
      out.runFolder = args[i + 1] ?? null;
      i += 1;
      continue;
    }

    if (arg === '--wait-for') {
      const raw = args[i + 1];
      if (raw == null) fail('--wait-for requires a value');
      const n = Number.parseInt(raw, 10);
      if (!Number.isFinite(n) || n < 0) fail(`--wait-for must be an integer >= 0 (got: ${raw})`);
      out.waitForMs = n;
      i += 1;
      continue;
    }

    if (arg === '--concurrency') {
      const raw = args[i + 1];
      if (raw == null) fail('--concurrency requires a value');
      const n = Number.parseInt(raw, 10);
      if (!Number.isFinite(n) || n <= 0) fail(`--concurrency must be an integer >= 1 (got: ${raw})`);
      out.concurrency = n;
      i += 1;
      continue;
    }

    fail(`Unknown argument: ${arg}`);
  }

  if (!out.configPath) fail('Missing required --config');
  if (!out.runFolder) fail('Missing required --run-folder');

  return out;
};

const readJsonFile = (filePath) => {
  const raw = fs.readFileSync(filePath, 'utf8');
  try {
    return JSON.parse(raw);
  } catch (err) {
    const msg = err && err.message ? err.message : String(err);
    fail(`Failed to parse JSON: ${filePath} (${msg})`);
  }
};

const validateConfig = (config) => {
  const runId = config?.run_id;
  const urls = config?.urls;

  if (typeof runId !== 'string' || runId.trim() === '') {
    fail('Config must include non-empty string: run_id');
  }

  if (!Array.isArray(urls) || urls.length === 0 || urls.some((u) => typeof u !== 'string' || u.trim() === '')) {
    fail('Config must include non-empty array of strings: urls');
  }

  return { runId: runId.trim(), urls: urls.map((u) => u.trim()) };
};

const computeSiteSlugs = (urls) => {
  const used = new Map();
  return urls.map((url) => {
    let hostname = null;
    try {
      hostname = new URL(url).hostname;
    } catch {
      hostname = url;
    }

    const base = sanitizeSlug(hostname);
    const count = (used.get(base) ?? 0) + 1;
    used.set(base, count);

    const slug = count === 1 ? base : `${base}-${count}`;
    return slug;
  });
};

const ensureDir = (dirPath) => {
  fs.mkdirSync(dirPath, { recursive: true });
};

const fileExists = (filePath) => {
  try {
    fs.accessSync(filePath, fs.constants.F_OK);
    return true;
  } catch {
    return false;
  }
};

const writeJson = (filePath, value) => {
  fs.writeFileSync(filePath, JSON.stringify(value, null, 2) + '\n', 'utf8');
};

const snippet = (value, maxChars = 2000) => {
  if (value == null) return null;
  const s = String(value);
  if (s.length <= maxChars) return s;
  return s.slice(0, maxChars) + `… [truncated ${s.length - maxChars} chars]`;
};

const runPool = async (items, concurrency, worker) => {
  const results = new Array(items.length);
  let nextIndex = 0;

  const runners = new Array(Math.min(concurrency, items.length)).fill(0).map(async () => {
    // eslint-disable-next-line no-constant-condition
    while (true) {
      const idx = nextIndex;
      nextIndex += 1;
      if (idx >= items.length) return;
      results[idx] = await worker(items[idx], idx);
    }
  });

  await Promise.all(runners);
  return results;
};

const fetchBranding = async ({ apiKey, url, waitForMs }) => {
  const body = {
    url,
    formats: ['branding'],
  };

  if (waitForMs != null) {
    body.waitFor = waitForMs;
  }

  const res = await fetch(API_ENDPOINT, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  const text = await res.text();
  let json = null;
  try {
    json = text ? JSON.parse(text) : null;
  } catch {
    // fall through with json=null; keep text for diagnostics
  }

  return { ok: res.ok, status: res.status, text, json };
};

const main = async () => {
  const args = parseArgs(process.argv);

  const configPathAbs = path.resolve(process.cwd(), args.configPath);
  const runFolderAbs = path.resolve(process.cwd(), args.runFolder);

  const config = readJsonFile(configPathAbs);
  const { runId, urls } = validateConfig(config);

  const outputDir = path.join(runFolderAbs, '.firecrawl', runId, 'branding');
  const slugs = computeSiteSlugs(urls);

  if (args.dryRun) {
    console.log('DRY-RUN: Firecrawl Branding Format v2 receipts');
    console.log(`run_id: ${runId}`);
    console.log(`config: ${configPathAbs}`);
    console.log(`run_folder: ${runFolderAbs}`);
    console.log(`output_dir: ${outputDir}`);
    console.log(`wait_for_ms: ${args.waitForMs}`);
    console.log(`concurrency: ${args.concurrency}`);
    console.log(`urls: ${urls.length}`);
    console.log('');

    for (let i = 0; i < urls.length; i += 1) {
      const outFile = path.join(outputDir, `${slugs[i]}.json`);
      console.log(`PLAN ${urls[i]} -> ${outFile}`);
    }

    return;
  }

  const apiKey = process.env.FIRECRAWL_API_KEY;
  if (!apiKey || apiKey.trim() === '') {
    fail('FIRECRAWL_API_KEY is required unless --dry-run');
  }

  ensureDir(outputDir);

  let failures = 0;
  const tasks = urls.map((url, i) => ({
    url,
    slug: slugs[i],
    outFile: path.join(outputDir, `${slugs[i]}.json`),
    errFile: path.join(outputDir, `${slugs[i]}.error.json`),
  }));

  // Pre-skip existing success receipts to avoid unnecessary calls.
  const toFetch = [];
  for (const task of tasks) {
    if (!args.force && fileExists(task.outFile)) {
      console.log(`SKIP existing ${task.url} -> ${task.outFile}`);
      continue;
    }
    toFetch.push(task);
  }

  await runPool(toFetch, args.concurrency, async (task) => {
    try {
      const res = await fetchBranding({
        apiKey: apiKey.trim(),
        url: task.url,
        waitForMs: args.waitForMs,
      });

      if (!res.ok) {
        writeJson(task.errFile, {
          url: task.url,
          status: res.status,
          bodySnippet: snippet(res.text),
          timestampUtc: nowUtc(),
        });
        console.log(`FAIL ${task.url} -> ${task.errFile} (HTTP ${res.status})`);
        failures += 1;
        return;
      }

      const success = res.json && res.json.success === true && res.json.data != null;
      if (!success) {
        writeJson(task.errFile, {
          url: task.url,
          status: res.status,
          bodySnippet: snippet(res.text),
          timestampUtc: nowUtc(),
        });
        console.log(`FAIL ${task.url} -> ${task.errFile} (unexpected response)`);
        failures += 1;
        return;
      }

      writeJson(task.outFile, res.json);
      console.log(`OK ${task.url} -> ${task.outFile}`);
    } catch (err) {
      const msg = err && err.message ? err.message : String(err);
      writeJson(task.errFile, {
        url: task.url,
        status: null,
        bodySnippet: snippet(msg),
        timestampUtc: nowUtc(),
      });
      console.log(`FAIL ${task.url} -> ${task.errFile} (network/error)`);
      failures += 1;
    }
  });

  if (failures > 0) {
    process.exitCode = 1;
  }
};

main().catch((err) => {
  const msg = err && err.message ? err.message : String(err);
  console.error(`ERROR: ${msg}`);
  process.exit(1);
});

