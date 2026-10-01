Filesystem path resolution audit
================================

Copyright 2026 Qore Technologies, s.r.o.

Scope: POSIX efsw realpath error handling, its regression tests and documentation.
Method: /home/david/.codex/skills/audit-changes/SKILL.md (all 62 checks).
Validation: five Python-driven native tests pass, including a Valgrind run with
all leak kinds treated as errors. The probe compiles the production helper.
The Windows implementation is outside this POSIX change and was not exercised.

.. list-table:: Complete review checklist
   :header-rows: 1
   :widths: 48 8 44

   * - Check
     - Status
     - Evidence

   * - Entry exists in `doxygen/lang/120_modules.dox.tmpl` (for modules in the Qore repo; N/A for external module repos)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Entry exists in `doxygen/lang/900_release_notes.dox.tmpl` (for modules in the Qore repo; external modules have release notes in their .qm)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - `qore_user_module()` or `qore_external_user_module()` call in `CMakeLists.txt`
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Module added to QMOD list in `CMakeLists.txt`
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - `.qm` file has `@section <lowercasemodname>intro` as first doc section — must be all lowercase (e.g., `avrodataproviderintro`, not `AvroDataProviderintro`)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - `%modern` in `.qm` file — no redundant `%new-style`, `%require-types`, `%strict-args`, `%enable-all-warnings`
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - No parse directives (`%requires`, `%modern`, `%new-style`) in separated `.qc` files (check OUTSIDE of `@code` blocks only)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - No `%include` usage (deprecated for modules)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Copyright 2026 on all new files
     - Pass
     - New C++ probe and Python regression tests carry 2026 notices.

   * - Directory layout: `.qm` inside `qlib/<ModuleName>/` directory (not at `qlib/<ModuleName>.qm` for multi-file modules)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - No second `.qm` for the same module at `qlib/<ModuleName>.qm`
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - `ns=Qore::XX` matches the QoreNamespace constructor path
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - `%modern` directive present
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Executable permission set (`chmod +x`)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Uses %prepend-module-path  before %requires for in-repo modules (Qore and Qore modules only; not Qorus)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - External module dependencies use `%try-module` — except modules delivered with the project itself (Qore ex: DataProvider, ConnectionProvider, QUnit, etc.) which use hard `%requires`
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - No filesystem operations (fopen, open, creat, unlink, remove, rename, mkdir, rmdir, stat, chmod) without sandbox checks
     - Pass
     - The existing realpath call is unchanged; its failure is now checked before reading output. Qore sandbox boundaries are unchanged. Test fixtures are private temporary paths.

   * - No network operations (connect, bind, socket, getaddrinfo, gethostbyname) without sandbox checks
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - If filesystem/network ops exist, verify `QoreSandboxManagerHelper` usage
     - Pass
     - The existing realpath call is unchanged; its failure is now checked before reading output. Qore sandbox boundaries are unchanged. Test fixtures are private temporary paths.

   * - No `File::`, `Dir::`, `Socket::`, `HTTPClient::` usage without justification
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - All `for`/`while` loops that could iterate >100 times have `qore_check_cancel()` checks
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Uses `qore_check_cancel()` (NOT deprecated `qore_check_io_interrupt()`)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Check frequency: every 100 iterations for tight loops, every 10 for expensive iterations
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - No blocking operations without cancellation support
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Every action has `display_name`, `short_desc` (plain text, <80 chars), `desc` (markdown)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Every action has `options` populated via `getActionOptionFromFields()` — without this, the action shows an empty, unusable form
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Every action has `output_type` set to a typed data type constant (e.g., `MyResponseDataType`) — not omitted
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - DPAT_API actions: provider has `"supports_request": True` and implements `doRequestImpl()`
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - DPAT_FIND actions: every option exists in `SearchOptions`, `getRecordTypeImpl()` returns `*hash<string, AbstractDataField>`
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Scheme-based apps (with `"scheme"` in registerApp): actions use `"path"` and do NOT use `"cls"` — having both `scheme` and `cls` causes a runtime error
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Single-key hash slices use trailing comma: `Fields{"key",}` (without trailing comma, `Fields{"key"}` returns the value, not a hash)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Typed data type classes exist for request and response types — inherit `HashDataType`, have `const Fields` hash, call `addQoreFields(Fields)` in constructor, export public constant at bottom (e.g., `public const MyDataType = new MyDataType();`)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Request/input types use `public` Fields (enables `ClassName::Fields` in action registration)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Response/output types use `private` Fields
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Each field in data types has `display_name`, `type`, and `desc` (markdown-formatted)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Input fields have `example_value` where useful (string fields, endpoint URIs, SQL queries, etc.)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Fields with finite allowed values use `allowed_values` with `AllowedValueInfo` containing both `value` and `display_name` (Title Case, human-readable) — never bare values, never described only in text
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Password/secret fields have `"sensitive": True`
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - `groups` uses `AppGroup` enum values from `qlib/DataProvider/AppGroup.qc`
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - App `logo` stored as separate file, loaded at module level in `Priv` namespace
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - App `desc` uses markdown: bullet list of capabilities, links to project website, business-language explanation of value
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - `display_name` is user-friendly ("Apache Avro" not "avro")
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - `short_desc` is plain text, under 80 chars, single sentence — no markdown
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - `desc` uses markdown: backticks for code/field refs (`` `field_name` ``, `` `True` ``, `` `pdf` ``), `\n\n` for paragraphs, `- ` bullet lists for enumerations, `bold` for caveats
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Descriptions use plain business language relating to common challenges — not just technical "what" but "why" and "when to use"
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - No bare `True`/`False`/`NOTHING` — must be backtick-wrapped in `desc`
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - No bare field/option names in prose — must use backticks
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Long descriptions (>500 chars) use bold section headers and bullet lists
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Factory registration in Qore repo: every factory name registered in `qlib/DataProvider/DataProvider.qc` → `FactoryMap` (without this, module loads but doesn't appear in Qorus apps)
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - `getRecordTypeImpl()` signature: must be `private *hash<string, AbstractDataField> getRecordTypeImpl(*hash<auto> search_options)` — NOT returning `*AbstractDataProviderType`
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Dependency JARs committed (for JNI modules): JAR files in `qlib/*/jar/` may be gitignored — use `git add -f` to ensure they're tracked, otherwise CI compilation fails
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - JAR install rules in CMakeLists.txt for all dependency JARs
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - No workarounds: No TODOs, FIXMEs, stubs, or partially-implemented features
     - Pass
     - Fixes the unchecked realpath result directly; no warning suppression or fallback path is added.

   * - Exception safety: C++ uses `ReferenceHolder` for Qore allocations, `std::unique_ptr` for C++ allocations, `*xsink` checked after every fallible operation
     - Pass
     - No allocation ownership changes. Returning std::string preserves RAII; the native test probe catches std::exception and the Python fixture registers cleanup before compilation.

   * - Thread safety: All mutable shared state protected by `std::lock_guard<std::mutex>` or documented as immutable-after-construction
     - Pass
     - Only automatic local state is used. No shared state changes.

   * - Type safety: Strongly-typed `code<return(args)>` instead of untyped `code`; `static_cast` instead of C casts; typed hashdecls for results; enums where appropriate
     - Pass
     - The return value is checked directly; no casts or untyped Qore values are introduced.

   * - Performance: No O(n²) where O(n) is possible; no unnecessary copies; coordinate descent uses incremental residuals not full matrix multiply
     - Pass
     - Constant-time error check; no added system call or loop.

   * - Error handling: All inputs validated (dimensions, empty data, unfitted models); C++ I/O handles EAGAIN/EINTR if applicable
     - Pass
     - Missing and empty paths, nonexistent parents, broken and looping symlinks, and overlong paths all return an empty result without reading indeterminate bytes.

   * - Documentation: Doxygen `@param`, `@return`, `@throw` on all public methods; `@par Example` with realistic business scenarios; `@note` for important caveats
     - Pass
     - Header documents the POSIX failure contract, release notes explain the fix, and the delayed-poller option reference names its real hash declaration.

   * - QPP flags: `[flags=CONSTANT]` on methods that never throw; `[flags=RET_VALUE_ONLY]` on methods that throw but have no side effects
     - N/A
     - No new module, DataProvider, QPP interface or Qore test in this focused path-error fix.

   * - Security: No user-controlled format strings; no buffer overflows; bounds checking on array indices; no credentials in code
     - Pass
     - A failed filesystem resolution no longer exposes uninitialized stack data. No credentials or user-controlled formats are introduced.

   * - Correctness: Algorithms verified against reference implementations; edge cases tested (empty data, single sample, all-zero features)
     - Pass
     - Five real-filesystem regression tests pass normally and under Valgrind, covering canonical existing paths and all recorded failure classes.
