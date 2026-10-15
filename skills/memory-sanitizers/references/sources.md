# Sources and Provenance

## Official sources consulted (2026-10-15)

| URL | Used for |
|---|---|
| https://clang.llvm.org/docs/AddressSanitizer.html | ASan flags, use-after-return/scope options, `ASAN_OPTIONS`, LSan/UBSan options parsed separately, platform support, no static linking, 16+ TB virtual address space. |
| https://clang.llvm.org/docs/MemorySanitizer.html | `-fsanitize=memory`, origin tracking flags and cost, requirement that all code including libc++ be instrumented, Linux/NetBSD/FreeBSD support. The page does not itself discuss combination with other sanitizers. |
| https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html | Which sanitizers GCC cannot combine (address with thread/hwaddress; thread with address/leak). |

## Local verification (Apple clang 21.0.0, arm64 macOS, 2026-10-15)

- `-fsanitize=address,thread` rejected: "not allowed with".
- `-fsanitize=address,memory` rejected: MSan unsupported for the darwin target (so the ASan+MSan rule rests on the design restriction in LLVM community documentation, not on a local test).
- `-fsanitize=address,undefined` with `-fno-sanitize-recover=undefined` builds; the worked-example overflow was reported as heap-buffer-overflow.

## Not verified

- GCC and Linux runtime behavior (LSan ptrace failure in containers, default option values) rely on documentation and general knowledge; not executed.
- TSan/UBSan "ok in practice" statements are experience-based, not documented guarantees.

## Provenance

All text is original. External skill repositories (anthropics/skills, obra/superpowers, trailofbits/skills, vercel-labs/agent-skills, huggingface/skills, supabase/agent-skills) were not consulted; nothing copied.
