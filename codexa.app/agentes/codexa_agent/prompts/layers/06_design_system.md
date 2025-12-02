# 06_design_system | CODEXA Design System Standards

**Layer Version**: 1.0.0 | **Created**: 2025-11-24
**Purpose**: Define design tokens, semantic naming, UI conventions, and component patterns
**Category**: Standards Layer | **Composable**: Yes
**Integration**: UI component generation, frontend agents, design-related workflows

---

## OVERVIEW

CODEXA generates consistent, accessible, maintainable UI code following design system principles from Lovable, v0, Vercel, Shadcn, Radix, and other leading design systems.

**Core Philosophy** (from Lovable):
- **Semantic Tokens**: Colors, spacing, typography referenced by purpose, not value
- **HSL Color System**: Human-readable, easy to manipulate
- **Component-Driven**: Reusable, composable building blocks
- **Accessibility-First**: WCAG AA minimum, AAA preferred
- **Responsive by Default**: Mobile-first, progressive enhancement

---

## COLOR SYSTEM

### HSL Format (Lovable Pattern)

**Why HSL**: Human-readable, easy to create variants (lighter, darker, opacity)

```css
/* Base HSL definition */
:root {
  /* Primary colors */
  --color-primary-hsl: 221, 83%, 53%;  /* Blue */
  --color-primary: hsl(var(--color-primary-hsl));

  /* Variants */
  --color-primary-light: hsl(var(--color-primary-hsl) / 0.1);  /* 10% opacity */
  --color-primary-dark: hsl(221, 83%, 43%);  /* Darker variant */
  --color-primary-hover: hsl(221, 83%, 63%);  /* Lighter variant */
}
```

---

### Semantic Color Tokens

**Don't use**: `--color-blue-500`, `--color-red-600`
**Do use**: `--color-primary`, `--color-error`, `--color-surface`

```css
:root {
  /* Semantic tokens - light mode */
  --color-primary: hsl(221, 83%, 53%);
  --color-secondary: hsl(142, 71%, 45%);
  --color-accent: hsl(280, 100%, 70%);

  --color-background: hsl(0, 0%, 100%);
  --color-surface: hsl(0, 0%, 98%);
  --color-surface-hover: hsl(0, 0%, 95%);

  --color-text: hsl(222, 47%, 11%);
  --color-text-secondary: hsl(215, 16%, 47%);
  --color-text-tertiary: hsl(215, 14%, 70%);

  --color-border: hsl(214, 32%, 91%);
  --color-border-hover: hsl(214, 32%, 81%);

  --color-success: hsl(142, 71%, 45%);
  --color-warning: hsl(38, 92%, 50%);
  --color-error: hsl(0, 72%, 51%);
  --color-info: hsl(199, 89%, 48%);
}

/* Dark mode overrides */
[data-theme="dark"] {
  --color-background: hsl(222, 47%, 11%);
  --color-surface: hsl(222, 47%, 15%);
  --color-surface-hover: hsl(222, 47%, 18%);

  --color-text: hsl(0, 0%, 100%);
  --color-text-secondary: hsl(215, 16%, 70%);
  --color-text-tertiary: hsl(215, 14%, 47%);

  --color-border: hsl(215, 28%, 17%);
  --color-border-hover: hsl(215, 28%, 27%);
}
```

---

### Color Palette Structure

**Base colors** (5 semantic groups):
1. **Primary**: Main brand color (buttons, links, highlights)
2. **Secondary**: Supporting brand color
3. **Accent**: Call-to-action, special elements
4. **Neutral**: Background, surfaces, text
5. **Semantic**: Success, warning, error, info

**Usage**:
```css
/* ✅ Good: Semantic usage */
.button-primary {
  background-color: var(--color-primary);
  color: var(--color-text-inverse);
}

.alert-error {
  background-color: hsl(var(--color-error-hsl) / 0.1);
  color: var(--color-error);
  border-color: var(--color-error);
}

/* ❌ Bad: Direct color values */
.button {
  background-color: #3b82f6;
  color: #ffffff;
}
```

---

## SPACING SYSTEM

### Scale (8px base)

```css
:root {
  /* Base unit: 0.25rem = 4px */
  --spacing-0: 0;
  --spacing-1: 0.25rem;  /* 4px */
  --spacing-2: 0.5rem;   /* 8px */
  --spacing-3: 0.75rem;  /* 12px */
  --spacing-4: 1rem;     /* 16px */
  --spacing-5: 1.25rem;  /* 20px */
  --spacing-6: 1.5rem;   /* 24px */
  --spacing-8: 2rem;     /* 32px */
  --spacing-10: 2.5rem;  /* 40px */
  --spacing-12: 3rem;    /* 48px */
  --spacing-16: 4rem;    /* 64px */
  --spacing-20: 5rem;    /* 80px */
  --spacing-24: 6rem;    /* 96px */
}
```

**Usage**:
```css
/* ✅ Good: Using spacing tokens */
.card {
  padding: var(--spacing-6);
  margin-bottom: var(--spacing-4);
  gap: var(--spacing-3);
}

/* ❌ Bad: Arbitrary values */
.card {
  padding: 23px;
  margin-bottom: 17px;
  gap: 13px;
}
```

**Mapping to use cases**:
- `spacing-1` (4px): Icon spacing, tight gaps
- `spacing-2` (8px): Compact spacing (chip padding)
- `spacing-3` (12px): Default small gaps
- `spacing-4` (16px): Default padding/gap (most common)
- `spacing-6` (24px): Card/section padding
- `spacing-8` (32px): Large spacing between sections
- `spacing-12+`: Page-level spacing, hero sections

---

## TYPOGRAPHY SYSTEM

### Type Scale

```css
:root {
  /* Font families */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-serif: Georgia, Cambria, "Times New Roman", Times, serif;
  --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;

  /* Font sizes (1rem = 16px base) */
  --text-xs: 0.75rem;     /* 12px */
  --text-sm: 0.875rem;    /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  --text-4xl: 2.25rem;    /* 36px */
  --text-5xl: 3rem;       /* 48px */
  --text-6xl: 3.75rem;    /* 60px */

  /* Font weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Line heights */
  --leading-none: 1;
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;
}
```

---

### Semantic Text Styles

```css
/* Headings */
.text-h1 {
  font-size: var(--text-5xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  letter-spacing: -0.02em;
}

.text-h2 {
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
}

.text-h3 {
  font-size: var(--text-3xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-snug);
}

/* Body text */
.text-body {
  font-size: var(--text-base);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
}

.text-body-sm {
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
}

/* UI text */
.text-label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  line-height: var(--leading-tight);
}

.text-caption {
  font-size: var(--text-xs);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
  color: var(--color-text-secondary);
}
```

---

## COMPONENT PATTERNS

### Button Variants

```typescript
// Button component with variants
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost' | 'danger';
  size: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
}

function Button({ variant, size, children, onClick }: ButtonProps) {
  const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none';

  const variantClasses = {
    primary: 'bg-primary text-white hover:bg-primary-hover',
    secondary: 'bg-secondary text-white hover:bg-secondary-hover',
    ghost: 'bg-transparent hover:bg-surface',
    danger: 'bg-error text-white hover:bg-error-hover'
  };

  const sizeClasses = {
    sm: 'h-9 px-3 text-sm',
    md: 'h-10 px-4 text-base',
    lg: 'h-11 px-6 text-lg'
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

---

### Card Pattern

```typescript
interface CardProps {
  children: React.ReactNode;
  padding?: 'sm' | 'md' | 'lg';
  hoverable?: boolean;
}

function Card({ children, padding = 'md', hoverable = false }: CardProps) {
  const paddingClasses = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  };

  const hoverClass = hoverable ? 'hover:shadow-lg hover:border-border-hover transition-all' : '';

  return (
    <div className={`bg-surface border border-border rounded-lg ${paddingClasses[padding]} ${hoverClass}`}>
      {children}
    </div>
  );
}
```

---

### Form Input Pattern

```typescript
interface InputProps {
  label: string;
  type?: 'text' | 'email' | 'password' | 'number';
  placeholder?: string;
  error?: string;
  value: string;
  onChange: (value: string) => void;
}

function Input({ label, type = 'text', placeholder, error, value, onChange }: InputProps) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-sm font-medium text-text">
        {label}
      </label>
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className={`
          h-10 px-3 py-2 rounded-md border bg-background text-text
          placeholder:text-text-tertiary
          focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent
          disabled:cursor-not-allowed disabled:opacity-50
          ${error ? 'border-error focus:ring-error' : 'border-border'}
        `}
      />
      {error && (
        <span className="text-sm text-error">{error}</span>
      )}
    </div>
  );
}
```

---

## RESPONSIVE DESIGN

### Breakpoints

```css
:root {
  --breakpoint-sm: 640px;   /* Mobile landscape */
  --breakpoint-md: 768px;   /* Tablet */
  --breakpoint-lg: 1024px;  /* Desktop */
  --breakpoint-xl: 1280px;  /* Large desktop */
  --breakpoint-2xl: 1536px; /* Extra large */
}
```

**Tailwind-style media queries**:
```css
/* Mobile first (default) */
.container {
  padding: var(--spacing-4);
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: var(--spacing-6);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    padding: var(--spacing-8);
  }
}
```

---

### Container Patterns

```css
.container-fluid {
  width: 100%;
  padding-left: var(--spacing-4);
  padding-right: var(--spacing-4);
}

.container {
  width: 100%;
  max-width: 1280px;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--spacing-4);
  padding-right: var(--spacing-4);
}

.container-narrow {
  width: 100%;
  max-width: 768px;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--spacing-4);
  padding-right: var(--spacing-4);
}
```

---

## ACCESSIBILITY

### Focus States

```css
/* Always provide visible focus indicators */
.button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Or using ring utility */
.input:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-primary);
}
```

---

### Color Contrast

**Minimum contrast ratios (WCAG AA)**:
- Normal text (16px): 4.5:1
- Large text (24px): 3:1
- UI components: 3:1

```css
/* ✅ Good: High contrast */
.text-on-background {
  color: var(--color-text);  /* #1a1a1a on #ffffff = 16:1 */
  background-color: var(--color-background);
}

/* ⚠️ Check: Ensure sufficient contrast */
.text-secondary {
  color: var(--color-text-secondary);  /* Should be ≥4.5:1 */
}
```

---

### Semantic HTML

```tsx
// ✅ Good: Semantic HTML
function ArticleCard({ title, excerpt, author }: ArticleProps) {
  return (
    <article>
      <h2>{title}</h2>
      <p>{excerpt}</p>
      <footer>
        <address>By {author}</address>
      </footer>
    </article>
  );
}

// ❌ Bad: Non-semantic divs
function ArticleCard({ title, excerpt, author }: ArticleProps) {
  return (
    <div>
      <div>{title}</div>
      <div>{excerpt}</div>
      <div>By {author}</div>
    </div>
  );
}
```

---

### ARIA Attributes

```tsx
// Button with icon (needs aria-label)
function CloseButton({ onClick }: { onClick: () => void }) {
  return (
    <button onClick={onClick} aria-label="Close dialog">
      <XIcon />
    </button>
  );
}

// Loading state
function LoadingButton({ isLoading, children }: LoadingButtonProps) {
  return (
    <button disabled={isLoading} aria-busy={isLoading}>
      {isLoading ? <Spinner /> : children}
    </button>
  );
}

// Form validation
function Input({ error, ...props }: InputProps) {
  return (
    <>
      <input
        aria-invalid={!!error}
        aria-describedby={error ? 'error-message' : undefined}
        {...props}
      />
      {error && <span id="error-message" role="alert">{error}</span>}
    </>
  );
}
```

---

## ANIMATION & TRANSITIONS

### Timing Functions

```css
:root {
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

  --duration-fast: 150ms;
  --duration-base: 200ms;
  --duration-slow: 300ms;
}
```

**Usage**:
```css
.button {
  transition: background-color var(--duration-base) var(--ease-in-out);
}

.modal {
  transition: opacity var(--duration-slow) var(--ease-out),
              transform var(--duration-slow) var(--ease-out);
}
```

---

### Respect User Preferences

```css
/* Disable animations for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## SHADOWS & ELEVATION

```css
:root {
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-base: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}

.card {
  box-shadow: var(--shadow-base);
}

.modal {
  box-shadow: var(--shadow-xl);
}
```

---

## BORDER RADIUS

```css
:root {
  --radius-none: 0;
  --radius-sm: 0.25rem;   /* 4px */
  --radius-base: 0.375rem; /* 6px */
  --radius-md: 0.5rem;    /* 8px */
  --radius-lg: 0.75rem;   /* 12px */
  --radius-xl: 1rem;      /* 16px */
  --radius-full: 9999px;  /* Pill shape */
}

.button {
  border-radius: var(--radius-md);
}

.card {
  border-radius: var(--radius-lg);
}

.avatar {
  border-radius: var(--radius-full);
}
```

---

## COMPONENT LIBRARY INTEGRATION

### Shadcn/Radix Pattern

```typescript
// Base primitive from Radix
import * as DialogPrimitive from '@radix-ui/react-dialog';

// Styled wrapper following design system
const Dialog = DialogPrimitive.Root;
const DialogTrigger = DialogPrimitive.Trigger;

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPrimitive.Portal>
    <DialogPrimitive.Overlay className="fixed inset-0 bg-black/50" />
    <DialogPrimitive.Content
      ref={ref}
      className={`
        fixed left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%]
        bg-surface rounded-lg shadow-xl
        w-full max-w-lg p-6
        ${className}
      `}
      {...props}
    >
      {children}
    </DialogPrimitive.Content>
  </DialogPrimitive.Portal>
));
```

---

## FILE ORGANIZATION

```
src/
├── styles/
│   ├── tokens/
│   │   ├── colors.css          # Color tokens
│   │   ├── spacing.css         # Spacing scale
│   │   ├── typography.css      # Type scale
│   │   └── shadows.css         # Shadow tokens
│   ├── globals.css             # Global styles + reset
│   └── utilities.css           # Utility classes
│
├── components/
│   ├── ui/                     # Base UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   └── dialog.tsx
│   └── [feature]/              # Feature-specific components
│
└── lib/
    └── utils.ts                # cn() helper, etc.
```

---

## UTILITY FUNCTIONS

### Class Name Helper (cn)

```typescript
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge Tailwind CSS classes with proper specificity.
 * Combines clsx for conditional classes + twMerge for conflict resolution.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage
<button
  className={cn(
    'px-4 py-2 rounded-md',
    isPrimary && 'bg-primary text-white',
    isDisabled && 'opacity-50 cursor-not-allowed'
  )}
>
```

---

## DARK MODE IMPLEMENTATION

### CSS Variables Approach

```tsx
// ThemeProvider component
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    // Apply theme to document
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Usage in component
function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      {theme === 'light' ? <MoonIcon /> : <SunIcon />}
    </button>
  );
}
```

---

## INTEGRATION

This layer defines design standards for:
- All UI component generation
- Frontend execution agents
- Design-focused workflows
- Component library creation

**Composition**:
```yaml
prompt_layers:
  - 01_identity_layer.md
  - 02_operating_modes.md
  - 05_code_conventions.md
  - 06_design_system.md  ← YOU ARE HERE
```

---

**Layer Maintained By**: CODEXA Team
**Last Updated**: 2025-11-24
**Related Layers**: 05_code_conventions.md, 08_workflows.md
**Influenced By**: Lovable, v0, Vercel, Shadcn, Radix, Tailwind, Material Design, Ant Design, Chakra UI
