# Browser MCP - Chrome/Chromium Fallback Implementation

**Date**: 2025-12-04
**Version**: 1.1.0
**Status**: Complete

## Problem

The browser-mcp server required Chrome to be pre-installed on the system. Puppeteer can download a bundled Chromium automatically, but the original implementation didn't handle cases where Chrome wasn't available or the bundled Chromium wasn't properly configured.

## Solution

Implemented a robust 3-tier fallback strategy with enhanced error handling to ensure the browser works in all environments.

---

## Changes Made

### 1. Enhanced `getBrowser()` Function (index.js)

**Location**: Lines 116-223

**New Features**:
- **Connection Check**: Verifies browser is connected before reusing instance
- **Retry Logic**: 3 attempts with progressive fallback
- **Strategy 1**: Use system Chrome if `CHROME_PATH` env var is set
- **Strategy 2**: Use bundled Chromium (Puppeteer default)
- **Strategy 3**: Retry with minimal arguments on failure
- **Error Recovery**: Auto-reconnect on browser disconnect
- **Helpful Errors**: Clear troubleshooting messages with platform-specific paths

**Key Code**:
```javascript
async function getBrowser() {
  if (browserInstance && browserInstance.isConnected()) {
    return browserInstance;
  }

  // Strategy 1: System Chrome (optional)
  if (process.env.CHROME_PATH) {
    launchOptions.executablePath = process.env.CHROME_PATH;
  }
  // Strategy 2: Bundled Chromium (default)
  // executablePath omitted = Puppeteer uses auto-downloaded Chromium

  // Strategy 3: Retry with minimal args
  if (browserLaunchAttempts === 1) {
    // Fallback to minimal config
  }
}
```

### 2. Enhanced `createPage()` Function (index.js)

**Location**: Lines 225-262

**New Features**:
- Try-catch wrapper for page creation
- Browser reset on failure (forces reconnection)
- Clear error messages

**Benefits**:
- Handles browser crashes gracefully
- Prevents stale browser instances
- Enables automatic recovery

### 3. Updated package.json

**Changes**:
- Version bumped to 1.1.0
- Added `puppeteer.skipDownload: false` to ensure Chromium download
- Added `test-browser` script for validation
- Added Node.js engine requirement (>=18.0.0)
- Enhanced keywords with "chromium"

**Key Configuration**:
```json
"puppeteer": {
  "skipDownload": false
}
```

### 4. Enhanced README.md

**New Sections**:

#### Chrome/Chromium Setup
- Explains bundled Chromium (default behavior)
- Documents CHROME_PATH environment variable for all platforms
- Shows fallback architecture

#### Troubleshooting
- Common error scenarios with solutions
- Platform-specific Chrome paths
- Manual Chromium download instructions

#### Arquitetura de Fallback
- Visual diagram of 3-tier fallback
- Benefits of the approach
- Code examples

### 5. New Test Script (test-browser.js)

**Purpose**: Validate browser launch and basic operations

**Tests**:
1. Browser launch (with fallback)
2. Page creation
3. Navigation to example.com

**Usage**:
```bash
npm run test-browser
# or
node test-browser.js
```

---

## Environment Variable Support

### Setting CHROME_PATH (Optional)

**Windows**:
```cmd
set CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
```

**Linux**:
```bash
export CHROME_PATH=/usr/bin/google-chrome
# or
export CHROME_PATH=/usr/bin/chromium
```

**macOS**:
```bash
export CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

---

## How It Works

### Fallback Hierarchy

```
┌─────────────────────────────────────┐
│  1. System Chrome (CHROME_PATH)     │ ← Fastest, if available
├─────────────────────────────────────┤
│  2. Bundled Chromium (default)      │ ← Works everywhere
├─────────────────────────────────────┤
│  3. Minimal Config Retry            │ ← Last resort
├─────────────────────────────────────┤
│  4. Clear Error + Troubleshooting   │ ← Helpful guidance
└─────────────────────────────────────┘
```

### Chromium Auto-Download

Puppeteer automatically downloads Chromium (~150MB) during `npm install`:

**Location**:
- `$HOME/.cache/puppeteer/` (Linux/macOS)
- `%USERPROFILE%\.cache\puppeteer\` (Windows)
- Or: `node_modules/puppeteer/.local-chromium/` (older versions)

**Verification**:
```bash
npm run test-browser
```

---

## Benefits

1. **Zero Configuration**: Works out of the box with bundled Chromium
2. **System Chrome Support**: Can use existing Chrome for better performance
3. **Automatic Recovery**: Handles browser crashes and disconnects
4. **Clear Errors**: Provides actionable troubleshooting steps
5. **Platform Agnostic**: Works on Windows, Linux, macOS
6. **Resilient**: Multiple fallback strategies prevent failures

---

## Testing

### Manual Test
```bash
cd codexa.app/mcp-servers/browser-mcp
npm run test-browser
```

**Expected Output**:
```
[Test 1] ✓ Browser launched successfully!
[Test 2] ✓ Page created successfully!
[Test 3] ✓ Page loaded: "Example Domain"
✓ All tests passed!
```

### Integration Test
The browser-mcp server will now handle these scenarios automatically:
- Chrome not installed → Uses bundled Chromium
- Chromium not downloaded → Error with download instructions
- Browser crashes → Auto-reconnect on next request
- Launch fails → Retry with minimal config

---

## Files Modified

1. **index.js** (lines 116-262)
   - Enhanced `getBrowser()` with 3-tier fallback
   - Enhanced `createPage()` with error recovery

2. **package.json**
   - Version: 1.0.0 → 1.1.0
   - Added puppeteer config
   - Added test-browser script
   - Added engines requirement

3. **README.md**
   - Added Chrome/Chromium Setup section
   - Added Troubleshooting section
   - Added Arquitetura de Fallback section
   - Updated version to 1.1.0

4. **test-browser.js** (NEW)
   - Browser launch validation script
   - 3 automated tests
   - Clear error messages

5. **BROWSER_FALLBACK_CHANGES.md** (NEW)
   - This document

---

## Rollback Instructions

If issues occur, revert to v1.0.0:

```bash
git checkout HEAD~1 -- index.js package.json README.md
git rm test-browser.js BROWSER_FALLBACK_CHANGES.md
npm install
```

---

## Future Improvements

1. **Auto-download Chromium**: Add script to force download if missing
2. **Browser Pool**: Support multiple browser instances for parallel operations
3. **Health Check**: Periodic browser health validation
4. **Metrics**: Log browser launch times and failure rates

---

## Summary

The browser-mcp server now works **without requiring Chrome pre-installed**:

- ✓ Uses bundled Chromium by default (auto-downloaded)
- ✓ Falls back to system Chrome if available (via CHROME_PATH)
- ✓ Retries with minimal config on launch failure
- ✓ Provides clear error messages with troubleshooting steps
- ✓ Handles browser crashes and disconnects gracefully
- ✓ Includes test script for validation

**No action required from users** - the server will work out of the box after `npm install`.
