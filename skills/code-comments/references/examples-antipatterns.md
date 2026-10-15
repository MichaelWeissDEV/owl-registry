# Positive & Negative Code Comment Examples

## 1. Redundant / Parrot Comments

### Bad (Paraphrasing the syntax)
```python
# Check if user is None
if user is None:
    # Return false
    return False

# Loop through numbers from 0 to 9
for i in range(10):
    # Print the number
    print(i)
```

### Good (Explaining business logic & non-obvious constraints)
```python
# A null user here indicates an anonymous session. Anonymous users are permitted
# to view preview pages, but must be redirected to SSO before initiating checkout.
if user is None:
    return self._redirect_to_login(target_url=request.url)
```

---

## 2. Inaccurate / Drifting Comments

### Bad (Code changed, comment was forgotten)
```python
# Multiply price by tax rate of 1.19
total = price * 1.21  # Comment claims 1.19, code uses 1.21!
```

### Good (Eliminate comment by making code self-explanatory)
```python
STANDARD_TAX_RATE = 1.21
total = price * STANDARD_TAX_RATE
```

---

## 3. Commented-Out Zombie Code

### Bad (Polluting the file with dead code)
```javascript
function calculateDiscount(user) {
  // const legacyDiscount = user.years * 0.05;
  // if (legacyDiscount > 0.25) legacyDiscount = 0.25;
  // return user.cartTotal * (1 - legacyDiscount);
  return user.cartTotal * 0.90;
}
```

### Good (Clean, rely on Git)
```javascript
function calculateDiscount(user) {
  // Tiered loyalty discount replaced by flat promotional rate (RFC-104)
  return user.cartTotal * 0.90;
}
```

---

## 4. Cryptic Workarounds

### Bad (Mysterious sleep without explanation)
```python
time.sleep(2)
sock.connect((host, port))
```

### Good (Clear explanation of external hardware timing)
```python
# The legacy firmware on the IoT controller requires at least 1800ms
# after a hardware reset before the TCP listening stack becomes responsive.
# Connecting earlier results in a TCP RST and hardware lockout.
time.sleep(2.0)
sock.connect((host, port))
```
