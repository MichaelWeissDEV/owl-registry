# C Memory Safety & Allocation Patterns

Memory corruption bugs (buffer overflows, use-after-free, double-free) account for approximately 70% of all critical software vulnerabilities.

## 1. Ownership & Lifetime Conventions

Adopt explicit ownership contracts:
- **Caller-allocated**: The caller passes a buffer and its capacity; the callee fills it up to capacity and returns the number of bytes written.
- **Callee-allocated**: The callee allocates with `malloc` and returns ownership to the caller. The documentation must clearly declare: `"Caller owns the returned pointer and must free it via free_func()"`

### Safe Buffer Pattern
```c
int get_hostname(char* buffer, size_t buffer_size) {
    if (!buffer || buffer_size == 0) {
        return -1;
    }
    // Safely copy bounded string with guaranteed null-terminator
    const char* host = "localhost";
    size_t len = strlen(host);
    if (len >= buffer_size) {
        return -2; /* Buffer too small */
    }
    memcpy(buffer, host, len + 1);
    return 0;
}
```

---

## 2. Safe Dynamic Reallocation (`realloc`)

The standard `realloc` function has a notorious leak trap: if `realloc` fails, it returns `NULL`, but the original memory block remains allocated. If you assign the return value directly back to the original pointer, you leak the old block!

```c
/* BUG: Memory leak if realloc fails */
/* ptr = realloc(ptr, new_size); */

/* CORRECT PATTERN: */
void* tmp = realloc(ptr, new_size);
if (tmp == NULL) {
    /* Handle error: ptr is STILL VALID and must be freed or handled */
    free(ptr);
    ptr = NULL;
    return -1;
}
ptr = tmp;
```
