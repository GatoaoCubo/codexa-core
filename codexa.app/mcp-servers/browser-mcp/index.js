#!/usr/bin/env node
/**
 * Browser MCP Server - Market Research Visual Intelligence
 *
 * Capabilities:
 * - screenshot: Capture visible viewport
 * - screenshot_full: Capture full scrollable page
 * - extract_html: Get rendered HTML (after JS execution)
 * - extract_text: Get visible text content
 * - search_marketplace: Pre-configured marketplace searches
 *
 * Anti-detection:
 * - Puppeteer Stealth plugin
 * - Rotating user agents
 * - Human-like delays
 * - Viewport randomization
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

// Setup stealth
puppeteer.use(StealthPlugin());

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SCREENSHOTS_DIR = path.join(__dirname, 'screenshots');

// User agents pool - realistic and recent
const USER_AGENTS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
];

// Viewport sizes - common resolutions
const VIEWPORTS = [
  { width: 1920, height: 1080 },
  { width: 1366, height: 768 },
  { width: 1536, height: 864 },
  { width: 1440, height: 900 },
];

// Brazilian marketplace configs
const MARKETPLACES = {
  mercadolivre: {
    searchUrl: 'https://lista.mercadolivre.com.br/{query}',
    name: 'Mercado Livre'
  },
  amazon: {
    searchUrl: 'https://www.amazon.com.br/s?k={query}',
    name: 'Amazon BR'
  },
  shopee: {
    searchUrl: 'https://shopee.com.br/search?keyword={query}',
    name: 'Shopee'
  },
  magazineluiza: {
    searchUrl: 'https://www.magazineluiza.com.br/busca/{query}/',
    name: 'Magazine Luiza'
  },
  americanas: {
    searchUrl: 'https://www.americanas.com.br/busca/{query}',
    name: 'Americanas'
  },
  casasbahia: {
    searchUrl: 'https://www.casasbahia.com.br/busca/{query}',
    name: 'Casas Bahia'
  },
  submarino: {
    searchUrl: 'https://www.submarino.com.br/busca/{query}',
    name: 'Submarino'
  }
};

// Helper functions
function getRandomUserAgent() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function getRandomViewport() {
  return VIEWPORTS[Math.floor(Math.random() * VIEWPORTS.length)];
}

function humanDelay(min = 1000, max = 3000) {
  return new Promise(resolve =>
    setTimeout(resolve, Math.floor(Math.random() * (max - min) + min))
  );
}

function sanitizeFilename(url) {
  return url
    .replace(/https?:\/\//, '')
    .replace(/[^a-zA-Z0-9]/g, '_')
    .substring(0, 100);
}

async function ensureScreenshotsDir() {
  try {
    await fs.mkdir(SCREENSHOTS_DIR, { recursive: true });
  } catch (e) {
    // Directory exists
  }
}

// Browser instance management
let browserInstance = null;
let browserLaunchAttempts = 0;
const MAX_LAUNCH_ATTEMPTS = 3;

/**
 * Get or create browser instance with smart fallback strategy:
 * 1. Try system Chrome (if CHROME_PATH env var set)
 * 2. Try bundled Chromium (auto-downloaded by Puppeteer)
 * 3. Retry with alternative args if launch fails
 *
 * Chromium bundling: Puppeteer automatically downloads Chromium on `npm install`
 * Location: node_modules/puppeteer/.local-chromium/
 */
async function getBrowser() {
  if (browserInstance && browserInstance.isConnected()) {
    return browserInstance;
  }

  if (browserLaunchAttempts >= MAX_LAUNCH_ATTEMPTS) {
    throw new Error(
      'Failed to launch browser after multiple attempts. ' +
      'Ensure Chrome/Chromium is available or run: npm install puppeteer'
    );
  }

  browserLaunchAttempts++;

  try {
    // Base launch options
    const launchOptions = {
      headless: 'new',
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--disable-gpu',
        '--window-size=1920,1080',
        '--disable-web-security',
        '--disable-features=IsolateOrigins,site-per-process',
        '--lang=pt-BR,pt',
      ],
    };

    // Strategy 1: Use system Chrome if CHROME_PATH env var is set
    if (process.env.CHROME_PATH) {
      console.error(`[Browser] Attempting to use Chrome at: ${process.env.CHROME_PATH}`);
      launchOptions.executablePath = process.env.CHROME_PATH;
    } else {
      // Strategy 2: Use bundled Chromium (default Puppeteer behavior)
      console.error('[Browser] Using bundled Chromium (auto-downloaded by Puppeteer)');
      // executablePath is omitted - Puppeteer uses bundled Chromium
    }

    browserInstance = await puppeteer.launch(launchOptions);
    browserLaunchAttempts = 0; // Reset on success

    console.error(`[Browser] Successfully launched (attempt ${browserLaunchAttempts})`);

    // Set up disconnect handler
    browserInstance.on('disconnected', () => {
      console.error('[Browser] Browser disconnected, will reconnect on next request');
      browserInstance = null;
    });

    return browserInstance;

  } catch (error) {
    console.error(`[Browser] Launch failed (attempt ${browserLaunchAttempts}/${MAX_LAUNCH_ATTEMPTS}):`, error.message);

    // Strategy 3: Retry with minimal args if first attempt failed
    if (browserLaunchAttempts === 1) {
      console.error('[Browser] Retrying with minimal arguments...');
      try {
        const minimalOptions = {
          headless: 'new',
          args: ['--no-sandbox', '--disable-setuid-sandbox'],
        };

        if (process.env.CHROME_PATH) {
          minimalOptions.executablePath = process.env.CHROME_PATH;
        }

        browserInstance = await puppeteer.launch(minimalOptions);
        browserLaunchAttempts = 0;
        console.error('[Browser] Successfully launched with minimal config');
        return browserInstance;
      } catch (retryError) {
        console.error('[Browser] Minimal config also failed:', retryError.message);
      }
    }

    // If all strategies fail, provide helpful error message
    const errorMessage = [
      'Browser launch failed. Troubleshooting steps:',
      '1. Run: npm install puppeteer (downloads bundled Chromium)',
      '2. Set CHROME_PATH env var to your Chrome installation:',
      '   - Windows: C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
      '   - Linux: /usr/bin/google-chrome or /usr/bin/chromium',
      '   - macOS: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      '3. Check permissions and available disk space',
      `Original error: ${error.message}`
    ].join('\n   ');

    throw new Error(errorMessage);
  }
}

async function createPage() {
  try {
    const browser = await getBrowser();
    const page = await browser.newPage();

    const viewport = getRandomViewport();
    const userAgent = getRandomUserAgent();

    await page.setViewport(viewport);
    await page.setUserAgent(userAgent);

    // Set Brazilian locale
    await page.setExtraHTTPHeaders({
      'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
    });

    // Bypass some detection
    await page.evaluateOnNewDocument(() => {
      Object.defineProperty(navigator, 'webdriver', { get: () => false });
      Object.defineProperty(navigator, 'languages', { get: () => ['pt-BR', 'pt', 'en-US', 'en'] });
      Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
    });

    return page;
  } catch (error) {
    console.error('[Browser] Failed to create page:', error.message);
    // Reset browser instance to force reconnection on next attempt
    if (browserInstance) {
      try {
        await browserInstance.close();
      } catch (e) {
        // Ignore close errors
      }
      browserInstance = null;
    }
    throw new Error(`Failed to create browser page: ${error.message}`);
  }
}

// Core functions
async function takeScreenshot(url, fullPage = false) {
  await ensureScreenshotsDir();
  const page = await createPage();

  try {
    await humanDelay(500, 1500);

    await page.goto(url, {
      waitUntil: 'networkidle2',
      timeout: 30000
    });

    await humanDelay(1000, 2000);

    // Scroll to trigger lazy loading if full page
    if (fullPage) {
      await autoScroll(page);
      await humanDelay(500, 1000);
    }

    const timestamp = Date.now();
    const filename = `${sanitizeFilename(url)}_${timestamp}.png`;
    const filepath = path.join(SCREENSHOTS_DIR, filename);

    await page.screenshot({
      path: filepath,
      fullPage: fullPage,
      type: 'png'
    });

    return {
      success: true,
      filepath: filepath,
      filename: filename,
      url: url,
      fullPage: fullPage,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
      url: url
    };
  } finally {
    await page.close();
  }
}

async function autoScroll(page) {
  await page.evaluate(async () => {
    await new Promise((resolve) => {
      let totalHeight = 0;
      const distance = 400;
      const timer = setInterval(() => {
        const scrollHeight = document.body.scrollHeight;
        window.scrollBy(0, distance);
        totalHeight += distance;

        if (totalHeight >= scrollHeight || totalHeight > 10000) {
          clearInterval(timer);
          window.scrollTo(0, 0);
          resolve();
        }
      }, 100);
    });
  });
}

async function extractContent(url, type = 'html') {
  const page = await createPage();

  try {
    await humanDelay(500, 1500);

    await page.goto(url, {
      waitUntil: 'networkidle2',
      timeout: 30000
    });

    await humanDelay(1000, 2000);

    let content;
    if (type === 'html') {
      content = await page.content();
    } else if (type === 'text') {
      content = await page.evaluate(() => document.body.innerText);
    }

    return {
      success: true,
      content: content,
      url: url,
      type: type,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
      url: url
    };
  } finally {
    await page.close();
  }
}

async function searchMarketplace(marketplace, query) {
  const config = MARKETPLACES[marketplace.toLowerCase()];
  if (!config) {
    return {
      success: false,
      error: `Marketplace not found: ${marketplace}. Available: ${Object.keys(MARKETPLACES).join(', ')}`
    };
  }

  const encodedQuery = encodeURIComponent(query);
  const searchUrl = config.searchUrl.replace('{query}', encodedQuery);

  // Take screenshot of search results
  const screenshot = await takeScreenshot(searchUrl, true);

  // Also extract text for analysis
  const textContent = await extractContent(searchUrl, 'text');

  return {
    success: true,
    marketplace: config.name,
    query: query,
    searchUrl: searchUrl,
    screenshot: screenshot,
    textContent: textContent.success ? textContent.content.substring(0, 10000) : null,
    timestamp: new Date().toISOString()
  };
}

async function multiMarketplaceSearch(query, marketplaces = null) {
  const targets = marketplaces || Object.keys(MARKETPLACES);
  const results = [];

  for (const mp of targets) {
    await humanDelay(2000, 4000); // Longer delay between marketplaces
    const result = await searchMarketplace(mp, query);
    results.push(result);
  }

  return {
    success: true,
    query: query,
    results: results,
    totalMarketplaces: results.length,
    successfulSearches: results.filter(r => r.success).length,
    timestamp: new Date().toISOString()
  };
}

// MCP Server setup
const server = new Server(
  {
    name: 'browser-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'screenshot',
        description: 'Take a screenshot of a webpage (visible viewport). Returns filepath to PNG image. Use Read tool to analyze the image.',
        inputSchema: {
          type: 'object',
          properties: {
            url: {
              type: 'string',
              description: 'URL to screenshot'
            }
          },
          required: ['url']
        }
      },
      {
        name: 'screenshot_full',
        description: 'Take a full-page screenshot (scrolls entire page). Good for product listings and search results. Returns filepath to PNG image.',
        inputSchema: {
          type: 'object',
          properties: {
            url: {
              type: 'string',
              description: 'URL to capture full page'
            }
          },
          required: ['url']
        }
      },
      {
        name: 'extract_html',
        description: 'Extract rendered HTML from a page (after JavaScript execution). Useful for scraping dynamic content.',
        inputSchema: {
          type: 'object',
          properties: {
            url: {
              type: 'string',
              description: 'URL to extract HTML from'
            }
          },
          required: ['url']
        }
      },
      {
        name: 'extract_text',
        description: 'Extract visible text content from a page. Clean text without HTML tags.',
        inputSchema: {
          type: 'object',
          properties: {
            url: {
              type: 'string',
              description: 'URL to extract text from'
            }
          },
          required: ['url']
        }
      },
      {
        name: 'search_marketplace',
        description: 'Search a Brazilian marketplace and capture results. Takes screenshot + extracts text. Marketplaces: mercadolivre, amazon, shopee, magazineluiza, americanas, casasbahia, submarino',
        inputSchema: {
          type: 'object',
          properties: {
            marketplace: {
              type: 'string',
              description: 'Marketplace ID: mercadolivre, amazon, shopee, magazineluiza, americanas, casasbahia, submarino'
            },
            query: {
              type: 'string',
              description: 'Search query (product name, keywords)'
            }
          },
          required: ['marketplace', 'query']
        }
      },
      {
        name: 'multi_search',
        description: 'Search multiple marketplaces at once. Captures screenshots and text from all specified marketplaces.',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Search query to run on all marketplaces'
            },
            marketplaces: {
              type: 'array',
              items: { type: 'string' },
              description: 'Optional: specific marketplaces to search. Default: all 7 BR marketplaces'
            }
          },
          required: ['query']
        }
      },
      {
        name: 'list_screenshots',
        description: 'List all captured screenshots in the screenshots folder.',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      }
    ]
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'screenshot': {
        const result = await takeScreenshot(args.url, false);
        return {
          content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
        };
      }

      case 'screenshot_full': {
        const result = await takeScreenshot(args.url, true);
        return {
          content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
        };
      }

      case 'extract_html': {
        const result = await extractContent(args.url, 'html');
        return {
          content: [{ type: 'text', text: JSON.stringify({
            ...result,
            content: result.content ? result.content.substring(0, 50000) : null // Limit size
          }, null, 2) }]
        };
      }

      case 'extract_text': {
        const result = await extractContent(args.url, 'text');
        return {
          content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
        };
      }

      case 'search_marketplace': {
        const result = await searchMarketplace(args.marketplace, args.query);
        return {
          content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
        };
      }

      case 'multi_search': {
        const result = await multiMarketplaceSearch(args.query, args.marketplaces);
        return {
          content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
        };
      }

      case 'list_screenshots': {
        await ensureScreenshotsDir();
        const files = await fs.readdir(SCREENSHOTS_DIR);
        const screenshots = files.filter(f => f.endsWith('.png'));
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              directory: SCREENSHOTS_DIR,
              count: screenshots.length,
              files: screenshots.slice(-20) // Last 20
            }, null, 2)
          }]
        };
      }

      default:
        return {
          content: [{ type: 'text', text: `Unknown tool: ${name}` }],
          isError: true
        };
    }
  } catch (error) {
    return {
      content: [{ type: 'text', text: `Error: ${error.message}` }],
      isError: true
    };
  }
});

// Cleanup on exit
process.on('SIGINT', async () => {
  if (browserInstance) {
    await browserInstance.close();
  }
  process.exit(0);
});

process.on('SIGTERM', async () => {
  if (browserInstance) {
    await browserInstance.close();
  }
  process.exit(0);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Browser MCP Server running on stdio');
}

main().catch(console.error);
