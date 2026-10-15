---
name: terraform-iac
description: >
  Architect, author, validate, and manage Infrastructure as Code using Terraform and OpenTofu.
  Use when designing HCL root and reusable child modules, configuring remote state backends
  with S3/DynamoDB or GCS state locking, establishing plan/apply safety workflows, managing
  configuration drift, configuring lifecycle rules, preventing secret exposure, or running
  tflint and checkov security audits.
compatibility: >
  Agent Skills-compatible coding agents with access to terraform, opentofu, tflint, or checkov tooling. Tooling is required only for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "terraform, iac, hcl, modules, state-locking, tflint, checkov, opentofu, devops"
  topics: "devops"
---

# Terraform Infrastructure as Code (IaC) Engineering

Terraform and OpenTofu provide declarative state-managed infrastructure provisioning. Production infrastructure workflows demand disciplined module decomposition, reliable remote state locking, deterministic provider pinning, defense against resource destruction accidents, and automated static security checks to prevent credential leaks and configuration drift.

## Purpose & Overview

This skill establishes standard architectures and operational procedures for writing, validating, and applying Terraform code. Adhering to these patterns ensures:
- Safe, non-destructive execution workflows with guaranteed state concurrency locking.
- Modular codebases separating reusable child modules from environment-specific root configurations.
- Zero secret storage in version control or plain text output variables.
- Rigorous linting, validation, and security scanning with `tflint` and `checkov`.

---

## Core Principles & Rules

1. **Mandatory Remote State with Concurrency Locking**:
   - Never store state locally or in version control.
   - Use S3 with DynamoDB table locking (or GCS with native object locking / Terraform Cloud / Spacelift).
   - Enable S3 server-side encryption with KMS, bucket versioning, and TLS enforcement (`aws:SecureTransport`).

2. **Decouple Root Modules from Child Modules**:
   - **Child Modules**: Reusable, agnostic of backend/environment, define inputs via `variables.tf`, declare outputs via `outputs.tf`, avoid inline providers.
   - **Root Modules**: Define environment configurations (e.g. `envs/prod/`), backend configurations, provider declarations, and wire child modules together.

3. **Strict Version Pinning for Providers and Modules**:
   - In `versions.tf`, pin `required_version` and all `required_providers` with semantic pessimistic constraints (`~> 5.30`) to prevent uncoordinated breaking upgrades.
   - Pin external module sources to immutable git tags or specific registry versions.

4. **Deterministic Two-Phase Plan & Apply Workflows**:
   - Never execute raw `terraform apply` interactively in automated environments.
   - Generate an execution plan to an artifact: `terraform plan -out=tfplan`.
   - Apply exclusively using the pre-generated plan: `terraform apply tfplan`.

5. **Guard Critical Resources with Lifecycle Blocks**:
   - Apply `lifecycle { prevent_destroy = true }` on production databases, KMS keys, S3 buckets, and state storage.
   - Use `lifecycle { create_before_destroy = true }` on zero-downtime updates (e.g., launch templates, security groups).
   - Use `ignore_changes` judiciously only for attributes modified externally by runtime autoscalers or tags managed by external controllers.

6. **Zero Plaintext Secrets**:
   - Mark input variables and outputs holding secrets as `sensitive = true`.
   - Never pass credentials via `.tfvars` checked into Git. Use ambient OIDC credentials, environment variables (`TF_VAR_`), or reference dynamic secret management engines (HashiCorp Vault, AWS Secrets Manager).

---

## Standard Workflows & Procedures

### Workflow: Production Module Engineering

1. **Standard File Structure Layout**:
   ```text
   modules/vpc/
   ├── versions.tf      # Terraform binary and required provider constraints
   ├── main.tf          # Primary resource definitions
   ├── variables.tf     # Typed, validated input variable declarations
   ├── outputs.tf       # Structured output definitions with sensitivity tags
   └── README.md        # Generated documentation (terraform-docs)
   ```
2. **Formatting & Validation**:
   - Run `terraform fmt -recursive` to enforce canonical formatting.
   - Run `terraform validate` to verify internal consistency and type correctness.
3. **Static Analysis & Security Audit**:
   - Run `tflint` to catch provider-specific bugs and unrecommended patterns.
   - Run `checkov -d .` or `tfsec .` to detect misconfigurations before provisioning.
4. **Plan Execution & Review**:
   - Run `terraform plan -out=tfplan -detailed-exitcode` in CI.
   - Review additions, modifications, and unexpected destructions.
5. **Apply & State Verification**:
   - Execute `terraform apply tfplan`.
   - Verify state consistency via `terraform state list`.

---

## Real-World Examples & Patterns

### 1. Hardened Remote Backend Configuration (`versions.tf`)

```hcl
terraform {
  required_version = ">= 1.7.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  backend "s3" {
    bucket         = "corp-infra-terraform-state-prod"
    key            = "networking/vpc/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "corp-infra-state-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Repository  = "github.com/org/infra-core"
    }
  }
}
```

### 2. Validated Input Variables and Sensitive Outputs

```hcl
# variables.tf
variable "environment" {
  type        = string
  description = "Target deployment environment tier."
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: 'dev', 'staging', or 'prod'."
  }
}

variable "cidr_block" {
  type        = string
  description = "Primary IPv4 CIDR block for the VPC."
  validation {
    condition     = can(cidrnetmask(var.cidr_block))
    error_message = "Variable cidr_block must be a valid CIDR notation (e.g. 10.0.0.0/16)."
  }
}

variable "db_master_password" {
  type        = string
  description = "Administrator password for the database cluster."
  sensitive   = true
}

# outputs.tf
output "vpc_id" {
  type        = string
  description = "Identifier of the provisioned VPC."
  value       = aws_vpc.main.id
}

output "database_connection_string" {
  type        = string
  description = "Connection URI for database clients."
  value       = "postgres://${aws_db_instance.db.username}:${var.db_master_password}@${aws_db_instance.db.endpoint}/${aws_db_instance.db.db_name}"
  sensitive   = true
}
```

### 3. Production Resource with Lifecycle Safeguards (`main.tf`)

```hcl
resource "aws_kms_key" "database_key" {
  description             = "KMS CMK for RDS database volume encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_db_instance" "db" {
  identifier_prefix     = "${var.environment}-postgres-"
  engine                = "postgres"
  engine_version        = "16.2"
  instance_class        = "db.r6g.xlarge"
  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_encrypted     = true
  kms_key_id            = aws_kms_key.database_key.arn

  username = "dbadmin"
  password = var.db_master_password

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.db.name
  publicly_accessible    = false
  skip_final_snapshot    = var.environment != "prod"
  final_snapshot_identifier = var.environment == "prod" ? "${var.environment}-postgres-final-snap" : null

  lifecycle {
    prevent_destroy       = true
    create_before_destroy = false
    ignore_changes = [
      latest_restorable_time
    ]
  }
}
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Operational Failure | Production Resolution |
| :--- | :--- | :--- |
| **Local state file (`terraform.tfstate`)** | Multiple operators overwrite state concurrently, resulting in state corruption and orphaned cloud resources. | Mandate remote backends (S3 + DynamoDB locking or GCS state locking) in every root module. |
| **Executing raw `terraform apply`** | Changes inspected in planning differ from what actually executes if upstream cloud state changes during delay. | Run `terraform plan -out=tfplan` followed directly by `terraform apply tfplan`. |
| **Unpinned Provider Versions** | `terraform init` pulls new major provider release with breaking schema changes, breaking CI pipelines. | Explicitly define `required_providers` with semantic pessimistic operators (`~> x.y`). |
| **Secrets committed to `terraform.tfvars`** | API tokens, DB passwords, and SSH keys leak into Git history. | Add `*.tfvars` to `.gitignore`. Inject secrets via environment variables (`TF_VAR_name`) or KMS/SSM. |
| **Hardcoding Environment Variables inside Child Modules** | Reusable modules become non-portable and tightly coupled to specific accounts or regions. | Extract all environment differences into `variables.tf`; supply values only in the calling root module. |
| **Ignoring Configuration Drift** | Out-of-band console changes cause unexpected replacements during emergency deployments. | Run scheduled `terraform plan -detailed-exitcode` in CI to detect drift automatically. |

---

## Verification Checklist

When authoring, reviewing, or applying Terraform configurations, verify each item:

- [ ] **Formatting & Validation**: `terraform fmt -check -recursive` and `terraform validate` pass with zero errors.
- [ ] **Remote Backend**: S3 bucket or GCS backend is configured with encryption enabled and state locking active.
- [ ] **Locking Verification**: DynamoDB table or equivalent locking mechanism is verified in the backend block.
- [ ] **Provider Constraints**: `required_version` and all `required_providers` in `versions.tf` have strict version constraints.
- [ ] **Sensitive Variables**: All variables and outputs holding credentials or keys specify `sensitive = true`.
- [ ] **Lifecycle Guards**: State storage, KMS keys, and production databases declare `lifecycle { prevent_destroy = true }`.
- [ ] **Static Security Scanning**: `tflint` and `checkov -d .` complete with zero critical or high severity violations.
- [ ] **Plan Safety**: Execution plan is created with `-out=tfplan` and reviewed for unexpected destructions (`destroy: 0`).
- [ ] **Drift Detection**: Any existing resources have been refreshed (`terraform plan -refresh-only`) prior to modifying infrastructure.

---

## Tooling & Reference Guides

- **Validation & Formatting Commands**:
  ```bash
  terraform fmt -check -diff -recursive
  terraform validate
  ```
- **Execution Plan Workflow**:
  ```bash
  terraform plan -out=tfplan -detailed-exitcode
  terraform apply tfplan
  ```
- **Static Analysis & Linters**:
  ```bash
  tflint --init && tflint --recursive
  checkov -d . --framework terraform --quiet
  tfsec .
  ```
- **State Inspection Commands**:
  ```bash
  terraform state list
  terraform state show <resource_address>
  ```
- **Official Documentation**:
  - [Terraform Language Documentation](https://developer.hashicorp.com/terraform/language)
  - [Terraform Standard Module Structure](https://developer.hashicorp.com/terraform/language/modules/develop/structure)
  - [OpenTofu Documentation](https://opentofu.org/docs/)
