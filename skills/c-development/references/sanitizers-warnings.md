# C Compiler Warnings and LLVM/GCC Sanitizers

## 1. Compiler Warning Flags
Never compile C code with default warnings. Use this baseline set in CMake or Makefiles:

```make
CFLAGS += -std=c17
CFLAGS += -Wall -Wextra -Wpedantic
CFLAGS += -Wformat=2 -Wformat-security
CFLAGS += -Wnull-dereference
CFLAGS += -Wconversion -Wsign-conversion
CFLAGS += -Wstrict-prototypes
CFLAGS += -Wmissing-prototypes
CFLAGS += -Wshadow
CFLAGS += -Werror
```

---

## 2. Dynamic Analysis: Sanitizers

Modern compilers provide built-in runtime instrumentation that detects memory and behavior flaws with low overhead (approx 2x slowdown):

### AddressSanitizer (ASan)
Detects buffer overflows (stack, heap, global), use-after-free, double-free, and memory leaks:
```bash
clang -fsanitize=address -g -O1 -fno-omit-frame-pointer main.c -o app
./app # If a memory error occurs, ASan outputs a detailed trace with line numbers!
```

### UndefinedBehaviorSanitizer (UBSan)
Detects signed integer overflow, null pointer dereferences, alignment errors, and shift overflows:
```bash
clang -fsanitize=undefined -g -O1 main.c -o app
./app
```

### LeakSanitizer (LSan)
Detects memory leaks at process exit (automatically enabled by default with ASan on Linux):
```bash
clang -fsanitize=leak -g main.c -o app
```
