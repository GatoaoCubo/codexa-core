#!/usr/bin/env node
/**
 * Test script to verify browser launch with fallback mechanism
 *
 * Usage: node test-browser.js
 */

import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';

puppeteer.use(StealthPlugin());

async function testBrowserLaunch() {
  console.log('Starting browser launch test...\n');

  let browser = null;
  let success = false;

  try {
    // Test 1: Default launch (bundled Chromium)
    console.log('[Test 1] Launching with bundled Chromium...');
    const launchOptions = {
      headless: 'new',
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
      ],
    };

    if (process.env.CHROME_PATH) {
      console.log(`[Test 1] Using CHROME_PATH: ${process.env.CHROME_PATH}`);
      launchOptions.executablePath = process.env.CHROME_PATH;
    } else {
      console.log('[Test 1] No CHROME_PATH set, using bundled Chromium');
    }

    browser = await puppeteer.launch(launchOptions);
    console.log('[Test 1] ✓ Browser launched successfully!');

    // Test 2: Create a page
    console.log('\n[Test 2] Creating new page...');
    const page = await browser.newPage();
    console.log('[Test 2] ✓ Page created successfully!');

    // Test 3: Navigate to a simple page
    console.log('\n[Test 3] Navigating to example.com...');
    await page.goto('https://example.com', { waitUntil: 'networkidle2', timeout: 10000 });
    const title = await page.title();
    console.log(`[Test 3] ✓ Page loaded: "${title}"`);

    await page.close();
    success = true;

  } catch (error) {
    console.error('\n[ERROR] Browser test failed:', error.message);
    console.error('\nTroubleshooting:');
    console.error('1. Run: npm install puppeteer');
    console.error('2. Check if Chromium was downloaded: ls node_modules/@puppeteer/browsers/');
    console.error('3. Set CHROME_PATH to your Chrome installation');
    console.error('4. Ensure sufficient disk space (~200MB) and permissions');

  } finally {
    if (browser) {
      await browser.close();
      console.log('\n[Cleanup] Browser closed');
    }
  }

  if (success) {
    console.log('\n✓ All tests passed! Browser is working correctly.');
  } else {
    console.log('\n✗ Tests failed. See errors above.');
    process.exit(1);
  }
}

testBrowserLaunch().catch(console.error);
