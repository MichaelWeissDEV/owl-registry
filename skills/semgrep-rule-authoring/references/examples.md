# Tested Semgrep examples

Everything below was run with Semgrep CLI 1.174.0 using `semgrep --validate --config .` and `semgrep --test --metrics=off .` in a directory holding each rule beside its test file. Result: configuration valid, all tests passed. Rule and test share a base name, as Semgrep requires.

## Taint rule: request data to shell (`flask-request-to-shell.yaml`)

```yaml
rules:
  - id: flask-request-to-shell
    mode: taint
    languages: [python]
    severity: HIGH
    message: >-
      Request data reaches a shell-executing subprocess call. Pass an argument
      list with shell=False, or validate against an allowlist.
    metadata:
      cwe: "CWE-78: Improper Neutralization of Special Elements used in an OS Command"
      confidence: MEDIUM
    pattern-sources:
      - pattern: flask.request.$ATTR
      - pattern: flask.request.$ATTR.get(...)
    pattern-sinks:
      - patterns:
          - pattern: subprocess.$FUNC($CMD, ..., shell=True, ...)
          - focus-metavariable: $CMD
    pattern-sanitizers:
      - pattern: shlex.quote(...)
```

Test file `flask-request-to-shell.py`:

```python
import shlex
import subprocess
import flask


def bad():
    name = flask.request.args.get("name")
    # ruleid: flask-request-to-shell
    subprocess.run("ls " + name, shell=True)


def bad_attr():
    # ruleid: flask-request-to-shell
    subprocess.call(flask.request.form, shell=True)


def good_quoted():
    name = flask.request.args.get("name")
    # ok: flask-request-to-shell
    subprocess.run("ls " + shlex.quote(name), shell=True)


def good_list():
    name = flask.request.args.get("name")
    # ok: flask-request-to-shell
    subprocess.run(["ls", name], shell=False)


def good_constant():
    # ok: flask-request-to-shell
    subprocess.run("ls -l", shell=True)
```

## Pattern rule: password hashed with a fast hash (`weak-hash-password.yaml`)

```yaml
rules:
  - id: md5-sha1-on-password
    languages: [python]
    severity: MEDIUM
    message: >-
      $FUNC is a fast general-purpose hash and must not protect passwords.
      Use a password KDF (argon2id, scrypt, bcrypt, or PBKDF2 per NIST SP 800-132).
    metadata:
      cwe: "CWE-916: Use of Password Hash With Insufficient Computational Effort"
    patterns:
      - pattern-either:
          - pattern: hashlib.$FUNC($PW, ...)
          - pattern: hashlib.$FUNC($PW.encode(...), ...)
      - metavariable-regex:
          metavariable: $FUNC
          regex: ^(md5|sha1|sha256)$
      - metavariable-regex:
          metavariable: $PW
          regex: (?i).*(passw|pwd|passwd).*
```

Test file `weak-hash-password.py`:

```python
import hashlib

def f(password, data):
    # ruleid: md5-sha1-on-password
    a = hashlib.md5(password.encode())
    # ruleid: md5-sha1-on-password
    b = hashlib.sha256(password)
    # ok: md5-sha1-on-password
    c = hashlib.sha256(data)
    # ok: md5-sha1-on-password
    d = hashlib.pbkdf2_hmac("sha256", password, b"salt", 600000)
    return a, b, c, d
```

Design notes:

- The rule is a name heuristic. A variable called `secret` that holds a password is missed. Acceptable for a low-severity hint, not for a gate.
- Unsalted single-pass SHA-256 is not a password KDF, so `sha256` is listed. `hashlib.pbkdf2_hmac` is deliberately not matched.

## Debugging a rule that does not match

1. Reduce the test to the smallest snippet and run `semgrep --config rule.yaml file.py`.
2. Remove operators one at a time until it matches; the last one removed is the culprit.
3. Check `languages:`. A `python` rule will not scan templates or non-Python files.
4. Check ellipses: `f($X)` does not match `f($X, extra)`; write `f($X, ...)`.
5. In taint mode, confirm the source expression matches as a plain `pattern` first, then the sink.
6. `semgrep --dump-ast -l python file.py` prints how Semgrep parsed the code when syntax assumptions are wrong.
