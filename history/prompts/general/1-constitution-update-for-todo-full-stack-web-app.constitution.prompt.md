---
id: 1
title: "Constitution Update for Todo Full-Stack Web Application"
stage: "constitution"
date: "2026-02-10"
surface: "agent"
model: "Claude Sonnet 4"
feature: "todo-application"
branch: "main"
user: "smartyfahad"
command: "/sp.constitution"
labels: ["constitution", "todo-app", "hackathon", "phase2"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
  - ".specify/templates/plan-template.md"
  - ".specify/templates/spec-template.md"
  - ".specify/templates/tasks-template.md"
  - "README.md"
  - "Versions.md"
tests: []
---

# Constitution Update for Todo Full-Stack Web Application

## PROMPT_TEXT

```
---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
handoffs: 
  - label: Build Specification
    agent: sp.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.constitution 
You are the Constitution agent for this hackathon project: Todo Full-Stack Web Application (Phase II).

This constitution defines the unbreakable rules, principles, architecture, success criteria, and workflow for the entire project. All agents, skills, and implementations must strictly follow this constitution. No deviation allowed without explicit update to this file.

### Project Overview
- Name: hackathon-todo (multi-user Todo application)
- Phase: II – Full-Stack Web Application with persistent storage
- Goal: Transform console app into modern multi-user web app
- Development Approach: Spec-driven (Spec-Kit Plus workflow)
  - Write/Update spec → Generate plan → Break into tasks → Implement
  - No manual coding — agent implements everything
- Judging Focus: Process quality, prompts, iterations, spec adherence, clean code, security, user isolation

### Core Principles (Always Enforce)
1. Spec-Driven Development Only – Every change starts from @specs/... files
2. Monorepo Structure – Use the exact folder layout below
3. User Isolation & Security – Every user sees/modifies ONLY their own tasks
4. Stateless JWT Auth – Better Auth issues JWT, backend verifies independently
5. Server-First Where Possible – Minimize client JS, push logic to server
6. Clean, Readable, Production-Ready Code – Even in hackathon speed
7. Type Safety – TypeScript (frontend), Pydantic/SQLModel (backend)
8. Error Handling – User-friendly messages + proper HTTP status codes

### Technology Stack (Fixed – Do Not Change)
Frontend:
- Next.js 16+ (App Router only)
- TypeScript
- Tailwind CSS + shadcn/ui (preferred for components)
- Better Auth (with JWT plugin enabled)

Backend:
- Python FastAPI
- SQLModel (ORM)
- Neon Serverless PostgreSQL
- Pydantic for models

Database:
- Neon PostgreSQL (env var: DATABASE_URL)
- Tables: users (managed by Better Auth), tasks (user_id foreign key)

Authentication:
- Better Auth on frontend → issues JWT
- Shared secret: BETTER_AUTH_SECRET (env var in both services)
- Backend: JWT middleware verifies token → extracts user_id → enforces ownership

### Monorepo Folder Structure (Must Match Exactly)
hackathon-todo/
├── .spec-kit/                  # or .specify/ – Spec-Kit Plus config
│   └── config.yaml
├── specs/                      # All specifications here
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   ├── api/
│   │   ├── rest-endpoints.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       ├── components.md
│       └── pages.md
├── frontend/
│   ├── CLAUDE.md               # Frontend-specific rules (even if Qwen, keep naming)
│   └── ... (Next.js app)
├── backend/
│   ├── CLAUDE.md               # Backend-specific rules
│   └── ... (FastAPI app)
├── docker-compose.yml
└── README.md

### API Endpoints (Exact – Do Not Alter Paths)
All require Authorization: Bearer <jwt-token>
- GET    /api/{user_id}/tasks               → List tasks (filter by status optional)
- POST   /api/{user_id}/tasks               → Create task
- GET    /api/{user_id}/tasks/{id}          → Get single task
- PUT    /api/{user_id}/tasks/{id}          → Update task
- DELETE /api/{user_id}/tasks/{id}          → Delete task
- PATCH  /api/{user_id}/tasks/{id}/complete → Toggle complete

Backend must:
- Verify JWT
- Check token user_id matches {user_id} in URL
- Filter all queries by authenticated user_id
- Return 401 if no/invalid token
- Return 403 if user_id mismatch

### Database Schema Rules
- users: managed by Better Auth (id, email, name, etc.)
- tasks:
  - id: integer PK
  - user_id: string (FK → users.id)
  - title: string NOT NULL (1-200 chars)
  - description: text NULLABLE
  - completed: boolean DEFAULT false
  - created_at, updated_at: timestamps
- Indexes: tasks.user_id, tasks.completed

### Auth Flow Rules
1. Frontend login → Better Auth → JWT issued
2. Frontend stores token (localStorage / cookie)
3. Every API call → add header: Authorization: Bearer {token}
4. Backend middleware: verify signature with BETTER_AUTH_SECRET
5. Extract user_id from token → enforce on every operation

### CLAUDE.md Guidelines (Adapt for Qwen CLI)
Root CLAUDE.md:
- Always reference @specs/... before implementing
- Use @frontend/CLAUDE.md for Next.js rules
- Use @backend/CLAUDE.md for FastAPI rules

Frontend CLAUDE.md style:
- App Router only
- Server Components default
- 'use client' only for interactivity
- Use api client for backend calls (with JWT header)
- shadcn/ui + Tailwind
- Responsive design

Backend CLAUDE.md style:
- FastAPI routes in /routes/
- SQLModel for models
- Dependency injection for DB & current_user
- HTTPException for errors

### Success Criteria & Anti-Patterns
Success:
- Full user isolation
- All CRUD + complete toggle works
- JWT auth secure & stateless
- Responsive UI
- Clean code, proper loading/error states
- Spec adherence (no random changes)

Anti-Patterns (Forbidden):
- Shared DB access without user_id filter
- No JWT verification on backend
- Client-side filtering only
- No loading/error states
- Mixing frontend/backend logic
- Manual coding outside agent

This constitution is the supreme document. All agents must obey it. When in doubt, refer back to this file or ask for clarification.
```

## RESPONSE_TEXT

Updated the project constitution at `.specify/memory/constitution.md` with specific details for the Todo Full-Stack Web Application (Phase II) project. The constitution now includes:

- Core principles: Spec-Driven Development, Monorepo Structure, User Isolation & Security, Stateless JWT Auth, Server-First approach, Clean Code, Type Safety, and Error Handling
- Technology stack requirements for frontend (Next.js 16+, TypeScript, Tailwind CSS, Better Auth) and backend (Python FastAPI, SQLModel, Neon PostgreSQL, Pydantic)
- API endpoints with exact paths and requirements
- Database schema rules with proper user isolation
- Auth flow rules for JWT implementation
- Development workflow following spec-driven approach
- Success criteria and anti-patterns

Also updated dependent template files to align with the new constitution:
- `.specify/templates/plan-template.md` - Added constitution check and updated project structure
- `.specify/templates/spec-template.md` - Added functional requirements aligned with constitution
- `.specify/templates/tasks-template.md` - Added constitution compliance checks and specific task examples
- `README.md` - Added reference to the constitution file
- `Versions.md` - Added v0.4.0 entry documenting the constitution update

The constitution is now the authoritative document for the project, ensuring all agents follow the same principles and guidelines.