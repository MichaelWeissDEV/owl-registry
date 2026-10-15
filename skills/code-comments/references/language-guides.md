# Language-Specific Commenting Guides

Detailed conventions, tags, and formatting rules across supported programming languages.

---

## 1. Python: PEP 257 & Sphinx/Google Style

Use triple double quotes `"""` for docstrings. Google Style is widely preferred:

```python
def calculate_compound_interest(principal: float, rate: float, periods: int) -> float:
    """Calculate the total accumulated value under compound interest.

    Args:
        principal: Initial invested capital (must be > 0).
        rate: Annual nominal interest rate expressed as a decimal (e.g., 0.05 for 5%).
        periods: Number of compounding periods (must be >= 1).

    Returns:
        The total accumulated future value rounded to two decimal places.

    Raises:
        ValueError: If principal is non-positive or periods is less than 1.
    """
```

---

## 2. Rust: Rustdoc (`///` and `//!`)

Rust documentation comments support full Markdown and run automatically as **doc-tests** during `cargo test`:

```rust
//! Module-level documentation explaining crate subsystem.

/// Validates and parses a cryptographic token.
///
/// # Arguments
///
/// * `raw_token` - The base64-encoded bearer token.
///
/// # Errors
///
/// Returns [`AuthError::Expired`] if token timestamp is in the past.
/// Returns [`AuthError::InvalidSignature`] if HMAC verification fails.
///
/// # Examples
///
/// ```
/// use auth::validate_token;
/// assert!(validate_token("valid_token_sample").is_ok());
/// ```
pub fn validate_token(raw_token: &str) -> Result<Claims, AuthError> { ... }
```

---

## 3. C & C++: Doxygen Style

```cpp
/**
 * @brief Thread-safe circular queue for inter-thread messaging.
 * 
 * @tparam T Type of elements stored in the queue. Must be MoveConstructible.
 * @param capacity Maximum number of elements before push operations block.
 * @note Allocates buffer on heap during construction; subsequent operations are non-allocating.
 */
template <typename T>
class BoundedQueue { ... };
```

---

## 4. Java: Javadoc

```java
/**
 * Manages transactional database sessions for customer billing records.
 *
 * @author Billing Team
 * @see InvoiceService
 */
public class BillingManager {

    /**
     * Charges customer credit card on file.
     *
     * @param customerId unique UUID of the account
     * @param amountInCents transaction amount in integer cents
     * @return PaymentConfirmation with processor transaction ID
     * @throws InsufficientFundsException if card balance is insufficient
     * @throws PaymentGatewayException if external gateway times out
     */
    public PaymentConfirmation charge(UUID customerId, long amountInCents) throws PaymentGatewayException { ... }
}
```

---

## 5. Kotlin: KDoc

KDoc uses Markdown inside `/** ... */`:

```kotlin
/**
 * Fetches user profile asynchronously from remote repository.
 *
 * @param userId Unique identifier for account lookup.
 * @return [UserProfile] or null if account does not exist.
 * @throws NetworkException on socket timeout.
 */
suspend fun fetchProfile(userId: String): UserProfile? { ... }
```

---

## 6. TypeScript / JavaScript: TSDoc / JSDoc

```typescript
/**
 * Transforms an array of raw sensor readings into smoothed moving averages.
 *
 * @param readings - Time-ordered sequence of sensor measurement objects.
 * @param windowSize - Number of adjacent samples to include in the average (default: 5).
 * @returns Array of smoothed points; length will be `readings.length - windowSize + 1`.
 * @throws {@link RangeError} If windowSize is less than 1 or greater than readings length.
 */
export function calculateMovingAverage(
  readings: readonly SensorReading[],
  windowSize = 5
): readonly SmoothedReading[] { ... }
```

---

## 7. Go: GoDoc

GoDoc comments are plain sentences starting with the name of the exported symbol:

```go
// Package cache implements an in-memory, thread-safe LRU cache.
package cache

// Cache is a concurrency-safe in-memory key-value store.
// The zero value of Cache is not usable; use New() to initialize.
type Cache struct { ... }

// Get retrieves an item by key. It returns the value and true if found,
// or a zero-value and false if the key does not exist or has expired.
func (c *Cache) Get(key string) (any, bool) { ... }
```

---

## 8. Swift: DocC

```swift
/// Calculates the geodesic distance between two GPS coordinates.
///
/// - Parameters:
///   - start: Starting coordinate containing latitude and longitude.
///   - end: Destination coordinate containing latitude and longitude.
/// - Returns: Distance in meters according to the WGS-84 reference ellipsoid.
/// - Throws: `LocationError.invalidCoordinate` if latitude exceeds ±90 degrees.
func distance(from start: Coordinate, to end: Coordinate) throws -> Double { ... }
```

---

## 9. Bash: Script Headers & Functions

```bash
# ==============================================================================
# Synchronizes static assets to S3 and invalidates CloudFront cache.
#
# Arguments:
#   $1 - Environment name ('staging' | 'production')
#   $2 - S3 Bucket URI (e.g. s3://my-assets-bucket)
# Returns:
#   0 on successful sync and cache invalidation; non-zero on failure.
# ==============================================================================
sync_assets() { ... }
```

---

## 10. SQL: Migrations & Schema Objects

```sql
-- Migration: 20261015_add_account_status_index.sql
-- Rationale: Speeds up active subscriber queries on the billing batch run.
-- Index is created CONCURRENTLY to avoid locking table during peak hours.
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_accounts_active_status
ON accounts (status, renewal_date)
WHERE status = 'ACTIVE';
```
