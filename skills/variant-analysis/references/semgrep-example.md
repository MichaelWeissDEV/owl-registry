# Tested variant rule: request-derived path to open()

Verified with Semgrep CLI 1.174.0: `semgrep --validate --config .` valid; `semgrep --test --metrics=off .` all tests passed (3/3 annotated lines). Rule file `join-request-path-no-containment.yaml`, test file `join-request-path-no-containment.py`.

```yaml
rules:
  - id: join-request-path-no-containment
    mode: taint
    languages: [python]
    severity: MEDIUM
    message: >-
      Request-derived value is joined onto a base directory and opened without
      a containment check. Resolve with realpath and verify the result stays
      under the base (CWE-22).
    metadata:
      cwe: "CWE-22: Improper Limitation of a Pathname to a Restricted Directory"
    pattern-sources:
      - pattern: flask.request.args.get(...)
      - pattern: flask.request.view_args[...]
    pattern-sinks:
      - patterns:
          - pattern: open($P, ...)
          - focus-metavariable: $P
    pattern-sanitizers:
      - pattern: werkzeug.utils.secure_filename(...)
```

```python
import os
import flask
from werkzeug.utils import secure_filename

BASE = "/srv/files"


def download():
    name = flask.request.args.get("name")
    # ruleid: join-request-path-no-containment
    return open(os.path.join(BASE, name), "rb").read()


def export():
    name = flask.request.args.get("report")
    path = os.path.join(BASE, "exports", name)
    # ruleid: join-request-path-no-containment
    return open(path).read()


def fixed():
    name = secure_filename(flask.request.args.get("name"))
    # ok: join-request-path-no-containment
    return open(os.path.join(BASE, name), "rb").read()
```

Limits to state when sharing the rule:

- Only `open(...)` is a sink. Add `send_file`, `send_from_directory`, archive extraction, and your own wrappers as additional sinks.
- A `realpath`-plus-prefix containment check is not modeled, so a correctly fixed handler written that way will be reported (false positive); add it as a `todook:` case or model it with a sanitizer function you control.
- Flows through other files or helper functions defined elsewhere are not followed in the Community engine.
- `secure_filename` is accepted as a sanitizer because it strips path separators; confirm that matches your fix.
