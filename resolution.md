# Lab Reflection — Resolution

1. Which issues were the easiest to fix, and which were the hardest? Why?

- Easiest: style and lint fixes (naming, blank lines, unused imports, f-strings, context managers). These were mechanical and low-risk.
- Hardest: security and behavior changes (removing eval and handling bare except). They required design decisions about error handling and safer alternatives.

2. Did the static analysis tools report any false positives? If so, describe one example.

- Yes. For example, Bandit flagged the try/except/pass (B110) used to ignore a missing-key scenario; in this case the pattern was intentionally tolerant, so the tool's conservative warning is a false positive unless the code's intention is to silently swallow all exceptions.

3. How would you integrate static analysis tools into your actual software development workflow?

- Run linters and formatters locally via pre-commit hooks.
- Enforce linting and security scans in CI as separate stages; fail builds on high-severity issues.
- Maintain a baseline/allowlist for legacy code and review tool outputs regularly to avoid alert fatigue.

4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- Removed unsafe constructs (no eval, no bare except), added input validation and type hints, used context managers and explicit encodings for file I/O, and improved naming and docstrings — all improving readability, maintainability, and runtime robustness.
