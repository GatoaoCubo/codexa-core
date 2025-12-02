# 05_code_conventions | CODEXA Code Style Standards

**Layer Version**: 1.0.0 | **Created**: 2025-11-24
**Purpose**: Define code style, naming conventions, and best practices from 30+ AI coding platforms
**Category**: Standards Layer | **Composable**: Yes
**Integration**: All code generation, execution agents

---

## OVERVIEW

CODEXA generates high-quality, maintainable code following best practices synthesized from 30+ leading AI coding platforms including Claude Code, Devin, Cursor, Windsurf, Copilot, v0, Lovable, and others.

**Core Philosophy**:
- **High Verbosity**: Explicit over implicit (Cursor pattern)
- **Self-Documenting**: Code should be readable without comments
- **Type-Safe**: Full type annotations everywhere possible
- **Defensive**: Validate at boundaries, trust internal code
- **Conventional**: Follow language idioms and community standards

---

## UNIVERSAL PRINCIPLES

### 1. Readability First

**Code is read 10x more than written** - optimize for the reader.

```python
❌ Bad (Cryptic):
def p(l, k):
    return [x for x in l if x[k]]

✅ Good (Explicit):
def filter_items_by_key(items: list[dict], key: str) -> list[dict]:
    """Filter list of dictionaries to only items where key exists and is truthy."""
    return [item for item in items if item.get(key)]
```

**Principles**:
- Use full words, not abbreviations (except standard ones: `id`, `url`, `api`)
- Name variables for what they contain, not their type
- Name functions for what they do (verbs)
- Name classes for what they are (nouns)

---

### 2. Explicit Over Implicit (Cursor Pattern)

**High-verbosity code** - make intent crystal clear.

```typescript
❌ Bad (Implicit):
const data = await fetch(url).then(r => r.json());

✅ Good (Explicit):
const response: Response = await fetch(url);
const userData: UserData = await response.json();
```

```python
❌ Bad (Implicit):
result = process(data)

✅ Good (Explicit):
processed_user_records: list[ProcessedUserRecord] = process_user_data(
    raw_user_data=data
)
```

---

### 3. Type Safety Everywhere

**Full type annotations** - no implicit types.

**TypeScript**:
```typescript
// ✅ Good: Full type annotations
interface User {
  id: string;
  email: string;
  createdAt: Date;
}

function createUser(
  email: string,
  password: string
): Promise<User> {
  // Implementation
}

const users: User[] = await fetchUsers();
```

**Python**:
```python
# ✅ Good: Full type hints
from typing import Optional, List, Dict

def calculate_total(
    items: List[Dict[str, float]],
    tax_rate: float,
    discount: Optional[float] = None
) -> float:
    """Calculate total price with tax and optional discount."""
    subtotal: float = sum(item["price"] for item in items)
    taxed_total: float = subtotal * (1 + tax_rate)

    if discount is not None:
        return taxed_total * (1 - discount)

    return taxed_total
```

---

## NAMING CONVENTIONS

### Variables

**Pattern**: `descriptive_noun` or `adjective_noun`

```python
# ✅ Good
user_email = "user@example.com"
is_authenticated = True
total_price = 99.99
filtered_items = [item for item in items if item.active]
max_retry_attempts = 3

# ❌ Bad
email = "user@example.com"  # Too generic
auth = True  # Abbreviated
tot = 99.99  # Abbreviated
result = [item for item in items if item.active]  # Generic
retries = 3  # Unclear what it represents
```

**JavaScript/TypeScript** (camelCase):
```typescript
const userEmail = "user@example.com";
const isAuthenticated = true;
const totalPrice = 99.99;
const maxRetryAttempts = 3;
```

---

### Functions/Methods

**Pattern**: `verb_noun` (Python) or `verbNoun` (JS/TS)

```python
# ✅ Good
def fetch_user_by_id(user_id: str) -> User:
    """Fetch user from database by ID."""
    pass

def calculate_total_price(items: list[Item]) -> float:
    """Calculate total price of items."""
    pass

def validate_email_format(email: str) -> bool:
    """Check if email matches valid format."""
    pass

# ❌ Bad
def get(id):  # Too generic
def calc(items):  # Abbreviated
def check_email(email):  # Unclear what aspect is checked
```

**JavaScript/TypeScript**:
```typescript
function fetchUserById(userId: string): Promise<User> { }
function calculateTotalPrice(items: Item[]): number { }
function validateEmailFormat(email: string): boolean { }
```

---

### Classes

**Pattern**: `PascalCase` noun (all languages)

```python
# ✅ Good
class UserAuthentication:
    """Handles user authentication logic."""
    pass

class EmailNotificationService:
    """Service for sending email notifications."""
    pass

class DatabaseConnectionPool:
    """Manages database connection pooling."""
    pass

# ❌ Bad
class Auth:  # Too abbreviated
class email_service:  # Wrong case
class DBPool:  # Acronym without full word
```

---

### Constants

**Pattern**: `UPPER_SNAKE_CASE`

```python
# ✅ Good
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT_SECONDS = 30
API_BASE_URL = "https://api.example.com"
DATABASE_CONNECTION_STRING = "postgresql://..."

# ❌ Bad
max_retries = 3  # Not uppercase
TIMEOUT = 30  # Missing unit
url = "https://..."  # Not constant-case
```

```typescript
// TypeScript
const MAX_RETRY_ATTEMPTS = 3;
const DEFAULT_TIMEOUT_SECONDS = 30;
const API_BASE_URL = "https://api.example.com";
```

---

### Files and Modules

**Python**: `snake_case.py`
```
user_authentication.py
email_notification_service.py
database_connection_pool.py
```

**JavaScript/TypeScript**: `kebab-case.ts` or `PascalCase.tsx` (React components)
```
user-authentication.ts
email-notification-service.ts
UserProfile.tsx
EmailForm.tsx
```

---

## CODE STRUCTURE

### Function Length

**Target**: 10-30 lines per function
**Maximum**: 50 lines (extract if longer)

```python
# ✅ Good: Focused, single-responsibility
def validate_user_input(email: str, password: str) -> ValidationResult:
    """Validate user registration input."""
    errors: list[str] = []

    if not validate_email_format(email):
        errors.append("Invalid email format")

    if len(password) < 8:
        errors.append("Password must be at least 8 characters")

    return ValidationResult(is_valid=len(errors) == 0, errors=errors)

# ❌ Bad: Too long, multiple responsibilities
def process_user_registration(email, password, name, age, address, ...):
    # 100+ lines of validation, database insertion, email sending, etc.
    pass
```

**If function exceeds 50 lines**: Extract helper functions

---

### File Length

**Target**: 200-400 lines per file
**Maximum**: 600 lines (split if longer)

**When to split**:
- Multiple classes in one file → Separate files per class
- Long file with many functions → Group by domain into modules
- Mix of concerns → Separate by responsibility

---

### Import Organization

**Order**:
1. Standard library
2. Third-party packages
3. Local application imports

```python
# ✅ Good: Organized imports
# Standard library
import os
import sys
from typing import Optional, List

# Third-party
import requests
from fastapi import FastAPI
from pydantic import BaseModel

# Local
from app.models.user import User
from app.services.email import EmailService
from app.utils.validation import validate_email
```

```typescript
// ✅ Good: Organized imports
// Standard library (Node.js built-ins)
import fs from 'fs';
import path from 'path';

// Third-party
import express from 'express';
import { z } from 'zod';

// Local
import { User } from '@/models/User';
import { EmailService } from '@/services/EmailService';
```

---

## DOCUMENTATION

### Docstrings (Python)

**Every public function/class must have docstring.**

```python
def calculate_discount(
    original_price: float,
    discount_percentage: float,
    member_tier: str
) -> float:
    """
    Calculate final price after applying discount.

    Args:
        original_price: Original item price before discount
        discount_percentage: Discount as percentage (0-100)
        member_tier: Membership tier ('bronze', 'silver', 'gold')

    Returns:
        Final price after discount, rounded to 2 decimal places

    Raises:
        ValueError: If discount_percentage not in range 0-100
        ValueError: If member_tier not recognized

    Examples:
        >>> calculate_discount(100.0, 10.0, 'silver')
        90.0
        >>> calculate_discount(50.0, 25.0, 'gold')
        37.5
    """
    if not 0 <= discount_percentage <= 100:
        raise ValueError(f"Invalid discount: {discount_percentage}")

    # Additional member tier discount
    tier_bonuses = {'bronze': 0, 'silver': 5, 'gold': 10}
    if member_tier not in tier_bonuses:
        raise ValueError(f"Unknown tier: {member_tier}")

    total_discount = discount_percentage + tier_bonuses[member_tier]
    final_price = original_price * (1 - total_discount / 100)

    return round(final_price, 2)
```

---

### JSDoc (TypeScript)

```typescript
/**
 * Calculate final price after applying discount.
 *
 * @param originalPrice - Original item price before discount
 * @param discountPercentage - Discount as percentage (0-100)
 * @param memberTier - Membership tier ('bronze', 'silver', 'gold')
 * @returns Final price after discount, rounded to 2 decimal places
 * @throws {Error} If discount percentage not in range 0-100
 * @throws {Error} If member tier not recognized
 *
 * @example
 * ```typescript
 * calculateDiscount(100.0, 10.0, 'silver') // Returns 90.0
 * calculateDiscount(50.0, 25.0, 'gold')   // Returns 37.5
 * ```
 */
function calculateDiscount(
  originalPrice: number,
  discountPercentage: number,
  memberTier: 'bronze' | 'silver' | 'gold'
): number {
  if (discountPercentage < 0 || discountPercentage > 100) {
    throw new Error(`Invalid discount: ${discountPercentage}`);
  }

  const tierBonuses = { bronze: 0, silver: 5, gold: 10 };
  const totalDiscount = discountPercentage + tierBonuses[memberTier];
  const finalPrice = originalPrice * (1 - totalDiscount / 100);

  return Math.round(finalPrice * 100) / 100;
}
```

---

### Inline Comments

**When to comment**:
- Complex algorithms (explain "why", not "what")
- Non-obvious business logic
- Workarounds for bugs/limitations
- TODOs and FIXMEs

**When NOT to comment**:
- Obvious code (comment would just repeat code)
- Code that should be refactored to be self-explanatory

```python
# ❌ Bad: Stating the obvious
# Increment counter by 1
counter += 1

# Loop through users
for user in users:
    # Print user name
    print(user.name)

# ✅ Good: Explaining non-obvious logic
# Use exponential backoff to avoid overwhelming API during high load periods
retry_delay = base_delay * (2 ** attempt_number)

# WORKAROUND: Library bug (issue #1234) - remove when v2.0 released
# The library incorrectly handles timezone offsets, so we normalize to UTC first
normalized_time = timestamp.astimezone(timezone.utc)
```

---

## ERROR HANDLING

### Validate at Boundaries

**Input Validation** - validate user input, API requests, file uploads:

```python
def create_user(email: str, password: str, age: int) -> User:
    """Create new user account."""
    # Validate at boundary (user input)
    if not validate_email_format(email):
        raise ValueError(f"Invalid email format: {email}")

    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")

    if age < 13:
        raise ValueError("User must be at least 13 years old")

    # Internal code can now trust the inputs
    return User(email=email, password=hash_password(password), age=age)
```

**Don't over-validate internal code**:

```python
# ❌ Bad: Over-validation in internal function
def _calculate_hash(password: str) -> str:
    """Internal helper to hash password."""
    # Don't re-validate here - caller already validated
    if not password or len(password) < 8:
        raise ValueError("Invalid password")

    return bcrypt.hash(password)

# ✅ Good: Trust internal caller
def _calculate_hash(password: str) -> str:
    """Internal helper to hash password. Assumes password already validated."""
    return bcrypt.hash(password)
```

---

### Clear Error Messages

```python
# ❌ Bad: Vague error
if user is None:
    raise Exception("Error")

# ❌ Bad: Technical jargon
if user is None:
    raise Exception("NULL pointer exception in user object resolution")

# ✅ Good: Clear, actionable
if user is None:
    raise ValueError(f"User not found with ID: {user_id}")

# ✅ Good: Include context
if balance < amount:
    raise ValueError(
        f"Insufficient balance. Required: ${amount:.2f}, Available: ${balance:.2f}"
    )
```

---

### Try-Catch Scope

**Keep try blocks small** - only wrap code that can fail:

```python
# ❌ Bad: Try block too large
try:
    user = fetch_user(user_id)
    items = fetch_user_items(user)
    total = calculate_total(items)
    discount = calculate_discount(user, total)
    final_price = total - discount
    return final_price
except Exception as e:
    # Which operation failed? Unclear!
    log_error(e)

# ✅ Good: Small, focused try blocks
user = fetch_user(user_id)  # Let this propagate if fails
items = fetch_user_items(user)

try:
    total = calculate_total(items)
except CalculationError as e:
    log_error(f"Failed to calculate total for user {user_id}: {e}")
    return 0.0  # Sensible default
```

---

## TESTING CONVENTIONS

### Test File Names

**Python**: `test_<module_name>.py`
```
test_user_authentication.py
test_email_service.py
test_database_connection.py
```

**JavaScript/TypeScript**: `<module-name>.test.ts` or `<module-name>.spec.ts`
```
user-authentication.test.ts
email-service.test.ts
UserProfile.test.tsx
```

---

### Test Function Names

**Pattern**: `test_<function_name>_<scenario>_<expected_result>`

```python
def test_calculate_discount_with_valid_inputs_returns_correct_price():
    """Test discount calculation with valid inputs."""
    result = calculate_discount(100.0, 10.0, 'silver')
    assert result == 85.0  # 10% + 5% silver bonus

def test_calculate_discount_with_invalid_percentage_raises_value_error():
    """Test that invalid discount percentage raises ValueError."""
    with pytest.raises(ValueError, match="Invalid discount"):
        calculate_discount(100.0, 150.0, 'silver')

def test_calculate_discount_with_unknown_tier_raises_value_error():
    """Test that unknown membership tier raises ValueError."""
    with pytest.raises(ValueError, match="Unknown tier"):
        calculate_discount(100.0, 10.0, 'platinum')
```

---

### Test Structure (AAA Pattern)

**Arrange, Act, Assert**:

```python
def test_user_creation_with_valid_data_succeeds():
    """Test creating user with valid data."""
    # Arrange
    email = "test@example.com"
    password = "secure_password_123"
    age = 25

    # Act
    user = create_user(email=email, password=password, age=age)

    # Assert
    assert user.email == email
    assert user.age == age
    assert user.password != password  # Should be hashed
    assert len(user.id) > 0  # ID should be generated
```

---

## LANGUAGE-SPECIFIC CONVENTIONS

### Python

**Follow PEP 8**:
- 4 spaces for indentation
- Max line length: 88 characters (Black formatter)
- snake_case for variables, functions
- PascalCase for classes
- UPPER_CASE for constants

**Use type hints everywhere** (Python 3.10+):
```python
from typing import Optional

def process_data(
    data: list[dict[str, str | int]],
    filter_key: Optional[str] = None
) -> list[dict[str, str | int]]:
    """Process data with optional filtering."""
    if filter_key is None:
        return data

    return [item for item in data if filter_key in item]
```

**Use dataclasses for data containers**:
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    """User account data."""
    id: str
    email: str
    created_at: datetime
    is_active: bool = True
```

---

### TypeScript

**Strict mode enabled**:
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

**Prefer interfaces over types** (when possible):
```typescript
// ✅ Good: Interface (extendable)
interface User {
  id: string;
  email: string;
  createdAt: Date;
}

// Use type for unions, intersections, utilities
type UserRole = 'admin' | 'user' | 'guest';
type UserWithRole = User & { role: UserRole };
```

**Use const assertions**:
```typescript
// ✅ Good: Const assertion for literal types
const USER_ROLES = ['admin', 'user', 'guest'] as const;
type UserRole = typeof USER_ROLES[number]; // 'admin' | 'user' | 'guest'
```

---

### React/JSX

**Component naming**: PascalCase
```typescript
// ✅ Good
function UserProfile() { }
function EmailNotificationSettings() { }

// ❌ Bad
function userProfile() { }
function email_settings() { }
```

**Props interface naming**: `<ComponentName>Props`
```typescript
interface UserProfileProps {
  userId: string;
  showEmail?: boolean;
  onUpdate?: (user: User) => void;
}

function UserProfile({ userId, showEmail = true, onUpdate }: UserProfileProps) {
  // Component implementation
}
```

**Event handlers**: `handle<Event>` or `on<Event>`
```typescript
function EmailForm() {
  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    // Handle submission
  };

  const handleEmailChange = (event: ChangeEvent<HTMLInputElement>) => {
    setEmail(event.target.value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleEmailChange} />
    </form>
  );
}
```

---

## ANTI-PATTERNS TO AVOID

### 1. Magic Numbers/Strings

```python
# ❌ Bad
if user.age >= 18:
    allow_access()

if status == 2:
    process_complete()

# ✅ Good
MINIMUM_AGE_FOR_ACCESS = 18
STATUS_COMPLETE = 2

if user.age >= MINIMUM_AGE_FOR_ACCESS:
    allow_access()

if status == STATUS_COMPLETE:
    process_complete()
```

---

### 2. Premature Abstraction

```python
# ❌ Bad: Abstraction for 2 uses
def apply_operation(value, operation_type):
    if operation_type == 'double':
        return value * 2
    elif operation_type == 'square':
        return value ** 2

result1 = apply_operation(5, 'double')
result2 = apply_operation(5, 'square')

# ✅ Good: Direct and clear
doubled_value = value * 2
squared_value = value ** 2
```

---

### 3. Mutable Default Arguments (Python)

```python
# ❌ Bad: Mutable default
def add_item(item, items=[]):
    items.append(item)
    return items

# ✅ Good: Immutable default
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

---

### 4. Catching Broad Exceptions

```python
# ❌ Bad: Too broad
try:
    process_data()
except Exception:
    pass  # Silently fails

# ✅ Good: Specific exception
try:
    process_data()
except ValueError as e:
    log_error(f"Invalid data format: {e}")
    raise
```

---

## PLATFORM-SPECIFIC PATTERNS

### From Cursor: High Verbosity Code

```typescript
// Cursor pattern: Explicit everything
interface UserAccountCreationRequest {
  emailAddress: string;
  plaintextPassword: string;
  dateOfBirth: Date;
  agreedToTermsAt: Date;
}

async function createNewUserAccount(
  request: UserAccountCreationRequest
): Promise<CreatedUserAccount> {
  const hashedPassword: string = await hashPasswordSecurely(
    request.plaintextPassword
  );

  const newUserId: string = generateUniqueUserId();

  const createdUserAccount: CreatedUserAccount = await database.users.create({
    id: newUserId,
    email: request.emailAddress,
    password: hashedPassword,
    dateOfBirth: request.dateOfBirth,
    createdAt: new Date(),
  });

  return createdUserAccount;
}
```

---

### From Windsurf: Defensive Programming

```python
# Windsurf pattern: Validate boundaries, trust internals
def process_payment(amount: float, currency: str, user_id: str) -> PaymentResult:
    """Process payment for user."""
    # Validate at boundary
    if amount <= 0:
        raise ValueError(f"Amount must be positive: {amount}")

    if currency not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Unsupported currency: {currency}")

    user = _fetch_user(user_id)  # Internal - assumes valid user_id
    if user.balance < amount:
        return PaymentResult(success=False, reason="insufficient_balance")

    # Internal calls trust their inputs
    transaction = _create_transaction(user, amount, currency)
    _deduct_balance(user, amount)
    _send_receipt(user, transaction)

    return PaymentResult(success=True, transaction_id=transaction.id)
```

---

## INTEGRATION

This layer defines code generation standards for:
- All execution agents generating code
- All builders creating new files
- All validators checking code quality
- All workflows involving code modification

**Composition**:
```yaml
prompt_layers:
  - 01_identity_layer.md
  - 02_operating_modes.md
  - 03_tool_usage_layer.md
  - 04_communication_layer.md
  - 05_code_conventions.md  ← YOU ARE HERE
```

---

**Layer Maintained By**: CODEXA Team
**Last Updated**: 2025-11-24
**Related Layers**: 06_design_system.md, 03_tool_usage_layer.md
**Influenced By**: Cursor, Windsurf, Claude Code, Devin, Copilot, Lovable, v0, and 20+ other platforms
