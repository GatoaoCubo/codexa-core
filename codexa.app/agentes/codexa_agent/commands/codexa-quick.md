# CODEXA Quick - Optimized HOP Meta-Agent

Execute the optimized CODEXA system with reduced initialization time and lazy loading.

## Quick Start

First, show the system status:

```bash
cd codexa && python codexa_launcher.py status
```

## Common Operations

### 1. Status Check (Fast)
```bash
cd codexa && python cli_optimized.py status
```

### 2. List Documents
```bash
cd codexa && python cli_optimized.py --quiet crud list --type document
```

### 3. Scan Repository
```bash
cd codexa && python cli_optimized.py --quiet scout scan
```

### 4. Read File
```bash
cd codexa && python cli_optimized.py --quiet crud read <path>
```

### 5. Product Management
```bash
cd codexa && python cli_optimized.py --quiet ecom products list
```

## Quick Menu

Show available operations:
```bash
cd codexa && python codexa_launcher.py help
```

## Optimizations Applied

- **Lazy Loading**: Modules loaded only when needed
- **Quiet Mode**: Reduced logging output
- **Fast Status**: Quick system check without full initialization
- **Cached Operations**: Reuses loaded modules
- **Minimal Dependencies**: Only loads required components

## Performance Improvements

- **Original**: 6+ seconds to initialize all modules
- **Optimized**: < 1 second for status check
- **Module Load**: Only when actually used

## Usage Tips

1. Use `--quiet` flag to suppress initialization messages
2. Use `quick` command for common operations
3. Modules are cached after first load in the same session

## Fallback to Full System

If you need all features:
```bash
cd codexa && python cli.py status
```

This will load all modules with full functionality but slower initialization.