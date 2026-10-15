# Undefined Behavior (UB) in C

Undefined Behavior in C means the C ISO standard places no requirements on the compiler or hardware. Once UB is invoked, the compiler may optimize away checks, corrupt data, or execute arbitrary branches.

## 1. Top Undefined Behavior Traps

### Signed Integer Overflow
In C, signed integer arithmetic overflow is undefined:
```c
int a = INT_MAX;
int b = a + 1; // UNDEFINED BEHAVIOR!
```
The compiler assumes signed arithmetic never overflows, so a safety check like `if (x + 10 < x)` can be completely eliminated by the optimizer!
**Fix**: Use `unsigned int` or explicit bounds checks before adding.

### Strict Aliasing Violations
Accessing an object through a pointer of an incompatible type violates strict aliasing:
```c
float f = 1.0f;
int* i = (int*)&f; // UNDEFINED BEHAVIOR: Violates strict aliasing
```
**Fix**: Use `memcpy` to cast bit patterns safely:
```c
float f = 1.0f;
uint32_t raw_bits;
memcpy(&raw_bits, &f, sizeof(f)); // Perfectly legal and optimized to a no-op
```

### Out-of-Bounds Pointer Arithmetic
Forming a pointer outside array bounds (except exactly one past the end) is undefined behavior, even if not dereferenced!
```c
int arr[5];
int* p = arr - 1; // UNDEFINED BEHAVIOR immediately upon pointer creation
```

### Reading Uninitialized Memory
Variables declared without initialization contain indeterminate garbage values:
```c
int count;
if (count > 0) // UNDEFINED BEHAVIOR: reading uninitialized value
```
**Fix**: Always initialize variables at declaration (`int count = 0;`).
