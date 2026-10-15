# RAII and Smart Pointer Lifetimes

## 1. Smart Pointer Ownership Models

### `std::unique_ptr<T>` (Exclusive Ownership)
- Default smart pointer in modern C++.
- Zero runtime overhead compared to a raw pointer.
- Move-only (cannot be copied). Transfer ownership explicitly using `std::move`.
- Always construct using `std::make_unique<T>(args...)`.

### `std::shared_ptr<T>` (Shared Ownership)
- Manages reference counting via a control block on the heap.
- Atomically thread-safe reference count increments/decrements.
- Overhead: 2 pointers (pointer to object + pointer to control block) + atomic operations.
- Always construct with `std::make_shared<T>(args...)` to allocate the object and control block in a single contiguous memory chunk.

### `std::weak_ptr<T>` (Non-Owning Observer)
- Observes an object managed by a `std::shared_ptr` without incrementing its reference count.
- Breaks cyclic dependency leaks (e.g. parent-child tree nodes, listener lists).
- Must be upgraded to `std::shared_ptr` before access via `.lock()`:
```cpp
if (auto shared = weak_node.lock()) {
    shared->process();
} else {
    // Target object has already been destroyed
}
```

---

## 2. The Rule of Zero, Three, and Five

### The Rule of Zero
If a class does not directly manage a raw resource handle, declare NO destructor, copy, or move operations. The compiler will generate optimal ones:
```cpp
class UserProfile {
    std::string name;
    std::vector<std::string> roles;
    std::unique_ptr<Settings> settings; // Default move/dtor handled automatically!
};
```

### The Rule of Five
If you manage a low-level resource handle directly and must define a custom destructor, you must explicitly declare or delete all five special member functions:
1. Destructor `~MyClass()`
2. Copy constructor `MyClass(const MyClass&)`
3. Copy assignment operator `MyClass& operator=(const MyClass&)`
4. Move constructor `MyClass(MyClass&&) noexcept`
5. Move assignment operator `MyClass& operator=(MyClass&&) noexcept`
