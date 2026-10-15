# Modern C++ Features (C++17, C++20, C++23)

## 1. C++17 Key Highlights
- **`std::string_view`**: Zero-allocation non-owning reference to character sequences. Use in function parameters instead of `const std::string&` when no ownership transfer is required.
- **`std::optional<T>`**: Explicit representation of nullable value types without heap allocation.
- **`std::variant<Ts...>`**: Type-safe tagged union (replaces C unions and void*).
- **Structured bindings**: `auto [key, val] = map_entry;`
- **`if constexpr`**: Compile-time branch evaluation in templates.
- **Filesystem library (`std::filesystem`)**: Cross-platform path and directory manipulation.

---

## 2. C++20 Key Highlights
- **Concepts**: Constrained template specifications (`template <std::integral T>`).
- **Ranges (`std::ranges`)**: Composable pipelines (`views::filter`, `views::transform`).
- **Coroutines**: Language support for cooperative multitasking and generators (`co_await`, `co_yield`).
- **Three-way comparison (`<=>`)**: Default spaceship operator generates all 6 comparison operators (`auto operator<=>(const Point&) const = default;`).
- **`std::span<T>`**: Non-owning view over contiguous sequences of objects (replaces pointer + length pairs).
- **`std::format`**: Fast, type-safe Python-style string formatting.

---

## 3. C++23 Highlights
- **`std::expected<T, E>`**: Value-or-error monad (similar to Rust `Result<T, E>`).
- **`std::print`**: Modern, formatted standard I/O replacing `std::cout` and `printf`.
- **Deducing `this`**: Explicit object parameters simplifying member function templates.
