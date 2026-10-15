# C++ Core Guidelines & Exception Safety

The C++ Core Guidelines (edited by Bjarne Stroustrup and Herb Sutter) define modern engineering practices for C++.

## 1. Exception Safety Guarantees

Every function that can throw must provide one of these four guarantees:
1. **No-throw (nothrow) guarantee**: The function is guaranteed not to throw exceptions. Indicated with `noexcept`. Destructors and move operations MUST be `noexcept`.
2. **Strong guarantee (commit-or-rollback)**: If an exception is thrown, state remains exactly as it was before the function call.
3. **Basic guarantee**: If an exception is thrown, no resources are leaked and objects remain in a valid, destructible state.
4. **No guarantee**: Leaks or corrupted state on exception. **Unacceptable in production C++**.

---

## 2. Key Rules from Core Guidelines

- **F.16**: For "in" parameters, pass cheaply-copied types by value and others by reference to `const`.
- **F.18**: For "will-move-from" parameters, pass by rvalue reference (`X&&`) or by value (`X`) and `std::move`.
- **C.21**: If you define or `=delete` any copy, move, or destructor function, define or `=delete` them all.
- **ES.20**: Always initialize an object (avoid uninitialized primitive types).
- **R.1**: Manage resources automatically using resource handles and RAII.
- **I.11**: Never transfer ownership by a raw pointer (`T*`) or reference (`T&`).
