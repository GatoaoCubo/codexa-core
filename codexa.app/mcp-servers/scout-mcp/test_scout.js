#!/usr/bin/env node
/**
 * Scout MCP Server - Test Suite
 * Run: node test_scout.js
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { glob } from 'glob';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(__dirname, '../../..');

console.log('='.repeat(60));
console.log('SCOUT MCP SERVER - TEST SUITE');
console.log('='.repeat(60));
console.log(`Project Root: ${PROJECT_ROOT}\n`);

// ============================================================================
// MOCK IMPLEMENTATIONS (same logic as index.js)
// ============================================================================

const CATEGORIES = {
  prime: { patterns: ['**/PRIME.md'], priority: 1.0 },
  readme: { patterns: ['**/README.md'], priority: 0.9 },
  hop: { patterns: ['**/*_HOP.md'], priority: 0.8 },
  adw: { patterns: ['**/*_ADW*.md', '**/ADW_*.md'], priority: 0.8 },
  config: { patterns: ['**/config/**/*.json'], priority: 0.7 },
  command: { patterns: ['**/.claude/commands/**/*.md'], priority: 0.7 },
};

const IGNORE_PATTERNS = [
  'node_modules/**',
  '.venv/**',
  '__pycache__/**',
  '.git/**',
  '*.pyc',
  '*.log',
  'package-lock.json',
];

function detectCategory(filePath) {
  const relativePath = path.relative(PROJECT_ROOT, filePath).replace(/\\/g, '/');

  for (const [category, config] of Object.entries(CATEGORIES)) {
    for (const pattern of config.patterns) {
      const regex = new RegExp(
        '^' + pattern
          .replace(/\*\*/g, '.*')
          .replace(/\*/g, '[^/]*')
          .replace(/\//g, '[\\\\/]')
        + '$',
        'i'
      );
      if (regex.test(relativePath)) {
        return category;
      }
    }
  }
  return 'other';
}

function detectAgent(filePath) {
  const relativePath = path.relative(PROJECT_ROOT, filePath).replace(/\\/g, '/');
  const agentMatch = relativePath.match(/agentes[\\\/]([^\\\/]+)[\\\/]/);
  if (agentMatch) {
    return agentMatch[1];
  }
  return null;
}

// ============================================================================
// TESTS
// ============================================================================

async function test_indexing() {
  console.log('\n[TEST 1] Indexing Performance');
  console.log('-'.repeat(40));

  const startTime = Date.now();

  const files = await glob('**/*', {
    cwd: PROJECT_ROOT,
    nodir: true,
    ignore: IGNORE_PATTERNS,
    absolute: true,
  });

  const duration = Date.now() - startTime;

  console.log(`Files found: ${files.length}`);
  console.log(`Time: ${duration}ms`);
  console.log(`Rate: ${Math.round(files.length / (duration / 1000))} files/sec`);

  return files;
}

async function test_category_detection(files) {
  console.log('\n[TEST 2] Category Detection');
  console.log('-'.repeat(40));

  const byCategory = {};

  for (const file of files.slice(0, 1000)) { // Sample first 1000
    const category = detectCategory(file);
    byCategory[category] = (byCategory[category] || 0) + 1;
  }

  const sorted = Object.entries(byCategory).sort((a, b) => b[1] - a[1]);
  for (const [cat, count] of sorted.slice(0, 10)) {
    console.log(`  ${cat}: ${count}`);
  }

  return byCategory;
}

async function test_agent_detection(files) {
  console.log('\n[TEST 3] Agent Detection');
  console.log('-'.repeat(40));

  const byAgent = {};

  for (const file of files) {
    const agent = detectAgent(file);
    if (agent) {
      byAgent[agent] = (byAgent[agent] || 0) + 1;
    }
  }

  const sorted = Object.entries(byAgent).sort((a, b) => b[1] - a[1]);
  for (const [agent, count] of sorted) {
    console.log(`  ${agent}: ${count} files`);
  }

  return byAgent;
}

async function test_prime_files(files) {
  console.log('\n[TEST 4] PRIME Files Discovery');
  console.log('-'.repeat(40));

  const primes = files.filter(f => f.endsWith('PRIME.md'));

  console.log(`Found ${primes.length} PRIME.md files:`);
  for (const prime of primes.slice(0, 10)) {
    const rel = path.relative(PROJECT_ROOT, prime);
    console.log(`  - ${rel}`);
  }

  return primes;
}

async function test_hop_files(files) {
  console.log('\n[TEST 5] HOP Files Discovery');
  console.log('-'.repeat(40));

  const hops = files.filter(f => f.includes('_HOP.md') || f.includes('_hop.md'));

  console.log(`Found ${hops.length} HOP files`);

  // Group by agent
  const byAgent = {};
  for (const hop of hops) {
    const agent = detectAgent(hop);
    if (agent) {
      byAgent[agent] = (byAgent[agent] || 0) + 1;
    }
  }

  for (const [agent, count] of Object.entries(byAgent)) {
    console.log(`  ${agent}: ${count} HOPs`);
  }

  return hops;
}

async function test_search_pattern() {
  console.log('\n[TEST 6] Search Pattern: **/config/*.json');
  console.log('-'.repeat(40));

  const files = await glob('**/config/*.json', {
    cwd: PROJECT_ROOT,
    nodir: true,
    ignore: IGNORE_PATTERNS,
  });

  console.log(`Found ${files.length} config JSON files`);
  for (const f of files.slice(0, 5)) {
    console.log(`  - ${f}`);
  }

  return files;
}

async function test_agent_context() {
  console.log('\n[TEST 7] Agent Context: scout_agent');
  console.log('-'.repeat(40));

  const scoutPath = path.join(PROJECT_ROOT, 'codexa.app/agentes/scout_agent');

  try {
    const files = await glob('**/*', {
      cwd: scoutPath,
      nodir: true,
    });

    console.log(`scout_agent has ${files.length} files:`);
    for (const f of files) {
      const category = detectCategory(path.join(scoutPath, f));
      console.log(`  [${category}] ${f}`);
    }
  } catch (e) {
    console.log(`Error: ${e.message}`);
  }
}

// ============================================================================
// RUN TESTS
// ============================================================================

async function main() {
  try {
    const files = await test_indexing();
    await test_category_detection(files);
    await test_agent_detection(files);
    await test_prime_files(files);
    await test_hop_files(files);
    await test_search_pattern();
    await test_agent_context();

    console.log('\n' + '='.repeat(60));
    console.log('ALL TESTS COMPLETED');
    console.log('='.repeat(60));

  } catch (error) {
    console.error('Test failed:', error);
    process.exit(1);
  }
}

main();
