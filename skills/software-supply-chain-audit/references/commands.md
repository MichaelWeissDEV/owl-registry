# Inspection commands by ecosystem

Check each tool's `--help` for your installed version. None of these should be run against untrusted packages in a way that executes their code; the listed forms read metadata or archives only. Run in an empty scratch directory, and pass paths as arguments.

## npm / pnpm / yarn
```bash
npm view <name>@<version> dist.tarball dist.integrity repository maintainers time
npm pack <name>@<version>               # downloads the tarball; does not install
tar -tzf <name>-<version>.tgz            # list files without extracting
npm ci --ignore-scripts                  # install from lockfile, skip lifecycle scripts
npm audit signatures                     # verify registry signatures/attestations of installed packages
grep -n '"hasInstallScript": true' package-lock.json
```

## Python
```bash
pip download --no-deps --only-binary=:all: -d ./scratch <name>==<version>
unzip -l ./scratch/<wheel-file>
pip install --require-hashes -r requirements.txt   # every line must carry --hash=
pip-audit -r requirements.txt                       # advisories (PyPA tool)
uv sync --locked                                    # fail if the lockfile is out of date
```

## Rust
```bash
cargo build --locked
cargo audit                      # RustSec advisories (cargo-audit)
cargo deny check                 # licenses, bans, advisories, sources (cargo-deny)
cargo vet                        # audit records (cargo-vet)
```

## Go
```bash
go mod verify                    # compare module cache with go.sum
govulncheck ./...                # reachable-vulnerability analysis
go list -m all                   # full module list
```

## Containers and artifacts
```bash
cosign verify-attestation ...    # verify Sigstore attestations (see cosign docs for identity flags)
gh attestation verify <file> --owner <org>   # GitHub artifact attestations
slsa-verifier verify-artifact ...            # SLSA provenance verification
```

## Cross-ecosystem
```bash
osv-scanner scan source -r .     # OSV database scan (v2 CLI syntax; older v1 used `osv-scanner -r .`)
scorecard --repo=github.com/<org>/<repo>   # OpenSSF Scorecard
```

## Dependency confusion quick check (read-only)
For each internal package name or scope, query the public registry for existence (`npm view <name>`, `pip index versions <name>` or the PyPI JSON API). A public package that you do not own with an internal name is a finding; reserve the name or scope and configure index routing so internal names resolve only from the private registry.

## SBOM field check
Per component: unique identifier (purl), name, version, supplier or originator, hash, license, relationships. Prefer generation from the built artifact or container image. Validate against the schema of the declared format (SPDX or CycloneDX) with its official tooling before treating it as evidence.
