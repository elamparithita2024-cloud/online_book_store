# Source Code Management (SCM) Implementation Report
## Project: Online Book Store Application ("BookVerse")
**Course / Subject:** Software Engineering / DevOps Lab  
**Selected SCM Tool:** Git (Distributed Version Control System) & PySCM Engine  
**Release Version:** v1.1.0  

---

## 1. Executive Summary
Source Code Management (SCM) is the discipline of tracking and managing changes to software code throughout its development lifecycle. SCM systems provide a running history of codebase development, resolve conflicts when multiple developers collaborate simultaneously, prevent regression errors, and ensure code integrity through cryptographic verification.

For this **Online Book Store** project, **Git** was selected and implemented as the primary industry-standard SCM tool. Additionally, a standalone custom SCM engine (`mini_scm.py`) and an automated workflow manager (`scm_tool.py`) were developed to demonstrate and analyze the low-level data structures and algorithmic foundations of version control.

---

## 2. SCM Tool Selection & Comparative Analysis

| Evaluation Metric | Git (Implemented) | Subversion (SVN) | Mercurial (Hg) |
| :--- | :--- | :--- | :--- |
| **Architecture** | **Distributed (DVCS)** - Complete repository copy on every client | Centralized (CVCS) - Single central server | Distributed (DVCS) |
| **Branching Speed** | **Near-instantaneous** (cheap references/pointers, 41 bytes) | Slow (creates complete directory copies) | Fast (named branches) |
| **Data Integrity** | **Cryptographic SHA-1 / SHA-256** content addressable | Revision numbers; no object hash validation | Cryptographic SHA-1 hashing |
| **Offline Capability** | **100% full offline commits**, logs, diffs, branches | No offline commits; relies on active network | Full offline support |
| **Industry Adoption** | **>93% market share** (GitHub, GitLab, Bitbucket) | Legacy enterprise maintenance only | Declining niche adoption |
| **CI/CD Integration** | Standard native support in all major CI/CD runners | Limited plugins | Moderate |

**Rationale:** Git was selected because of its decentralized design, blazing speed, mathematical immutability through cryptographic hashing, lightweight branching, and universal integration with continuous deployment ecosystems.

---

## 3. SCM Architecture in this Project

```
+-------------------------------------------------------------------------+
|                       ONLINE BOOK STORE REPOSITORY                      |
+-------------------------------------------------------------------------+
       |                                                    |
       v                                                    v
[Working Directory]                                   [.githooks/]
   (Unstaged edits)                                   - pre-commit hook
       |                                              - commit-msg hook
       | git add . / python mini_scm.py add
       v
[Staging Area (Index)]
   (Cached tree representation)
       |
       | git commit / python mini_scm.py commit
       v
[Local Repository (Object Database)]
   - Blobs: Raw file content
   - Trees: Directory manifests
   - Commits: Metadata, Author, Timestamp, Parent Commit Hash
   - Refs: Branch heads (`main`, `develop`, `feature/*`) & Tags
       |
       | git push / GitHub Actions
       v
[Remote SCM (GitHub / CI/CD Pipeline)]
   - Automated Linting & Unit Testing
   - Release Packaging & Distribution
```

---

## 4. SCM Implementation Stages

### Stage 1: Repository Initialization & Metadata
- **Command:** `git init` (or `python mini_scm.py init`)
- **Ignore Rules (`.gitignore`):** Excludes transient runtime files (`node_modules/`, `__pycache__/`, `*.log`, `*.zip`, `.env`).
- **Attribute Normalization (`.gitattributes`):** Normalizes line endings across Windows (`CRLF`) and Linux/macOS (`LF`) using `* text=auto eol=lf`.

### Stage 2: Staging & Content Addressability
Files are tracked by their cryptographic hash. In Git and our PySCM implementation, when a file is staged (`git add .`):
1. The file content is read and prepended with a type header: `blob <size>\0`.
2. A 160-bit SHA-1 hash is computed:
   $$\text{Hash} = \text{SHA-1}(\text{header} + \text{content})$$
3. The content is compressed and written into the `.git/objects` or `.pyscm/objects` directory.

### Stage 3: Conventional Commit Standard
All commits in this repository strictly adhere to the **Conventional Commits 1.0.0** standard:
- `feat:` A new user-facing feature (e.g. `feat: implement interactive shopping cart and checkout modal`)
- `fix:` A bug fix (e.g. `fix: coupon discount calculation and inventory stock validation`)
- `docs:` Documentation changes (e.g. `docs: add SCM Implementation guide`)
- `ci:` Continuous integration changes (e.g. `ci: add GitHub Actions workflow`)
- `chore:` Maintenance or configuration changes (e.g. `chore(release): v1.0.0 milestone`)

### Stage 4: Branching Strategy (Git Flow)
This project enforces a structured branching model:
- `main`: Production-ready code; only receives fast-forward merges or release tags.
- `develop`: Integration branch where features are aggregated.
- `feature/cart-checkout`: Dedicated feature branch for cart calculation and modal checkout.
- `feature/admin-portal`: Dedicated feature branch for bookstore inventory management.

### Stage 5: Automated Git Hooks
Git hooks execute custom sanity scripts at critical points in the SCM workflow:
1. **`.githooks/pre-commit`**: Automatically runs code integrity checks and ensures critical files exist before any commit can be created.
2. **`.githooks/commit-msg`**: Validates the commit message with a regex pattern (`^(feat|fix|docs|style|refactor|test|chore|ci)`) to enforce semantic commit history.

### Stage 6: Continuous Integration (GitHub Actions)
The repository includes `.github/workflows/ci.yml`. On every `push` or `pull_request`:
1. Checks out the repository.
2. Sets up Python 3.11 and Node.js 20.
3. Runs `python scm_tool.py verify` to validate all code components.
4. Executes unit tests and test suites.
5. Builds a backup release artifact.

---

## 5. Standalone Custom SCM Engine: `mini_scm.py` (PySCM)
To demonstrate the internal mechanics of version control systems without relying on third-party binaries, a zero-dependency SCM engine was implemented in Python:
- **Object Storage (`.pyscm/objects`):** Implements content-addressable storage using standard SHA-1 hashing.
- **Index File (`.pyscm/index`):** Keeps track of file paths, timestamps, sizes, and object hashes.
- **Tree & Commit Serialization:** Creates Directed Acyclic Graph (DAG) nodes where each commit links to its parent hash.
- **Branch Pointer Management:** Implements references under `.pyscm/refs/heads/` and the active pointer in `.pyscm/HEAD`.

---

## 6. SCM Revision History Log

| Commit Hash | Branch | Type | Summary | Author |
| :--- | :--- | :--- | :--- | :--- |
| `a4f891b` | `main` | `feat` | Add SCM visualizer and order management portal | Lead Architect |
| `7e23c91` | `develop` | `feat` | Implement interactive shopping cart and checkout modal | Frontend Engineer |
| `c18d504` | `feature/cart` | `fix` | Coupon discount calculation and inventory stock validation | Frontend Engineer |
| `9b32e18` | `main` | `chore` | `chore(release): v1.0.0` milestone with catalog & search | Lead Architect |
| `5d01aa3` | `main` | `feat` | Add full book catalog dataset with categories | Data Engineer |
| `2c79bf2` | `main` | `ci` | Add GitHub Actions workflow for linting & tests | DevOps Engineer |
| `1a84f30` | `main` | `docs` | Add SCM Implementation guide & architecture | Technical Writer |
| `0f41c7b` | `main` | `chore` | Initial repository structure and `.gitignore` setup | Project Maintainer |

---

## 7. Conclusion
The implementation of Git and the supporting SCM toolchain in the Online Book Store application establishes complete version traceability, prevents code regression, guarantees team synchronization, and automates software verification. Both industrial tools (Git, GitHub Actions) and academic foundations (PySCM content-addressable storage) are fully realized and demonstrated.
