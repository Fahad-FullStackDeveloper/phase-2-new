<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles: None (new constitution)
Added sections: All principles and sections for Todo Full-Stack Web Application
Removed sections: Template placeholders
Templates requiring updates: 
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated  
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending
- README.md ⚠ pending
Follow-up TODOs: None
-->

# Todo Full-Stack Web Application (Phase II) Constitution

## Core Principles

### Spec-Driven Development Only
Every change starts from @specs/... files. No implementation without corresponding specification updates. All features must be documented in spec files before implementation begins.

### Monorepo Structure
Use the exact folder layout specified in the constitution. All code must reside in the designated directories (frontend/, backend/, specs/, etc.) with no deviations allowed.

### User Isolation & Security
Every user sees/modifies ONLY their own tasks. Backend must enforce user_id filtering on all database queries. No shared access to data without explicit user_id verification.

### Stateless JWT Auth
Better Auth issues JWT, backend verifies independently. Authentication must be stateless with proper JWT verification using shared secret. No session-based authentication allowed.

### Server-First Where Possible
Minimize client JS, push logic to server. Prefer Server Components over Client Components unless interactivity is required. Use Server Actions for mutations.

### Clean, Readable, Production-Ready Code
Even in hackathon speed, maintain production-quality standards. Code must be well-commented, properly structured, and follow best practices for the respective technologies.

### Type Safety
Use TypeScript (frontend), Pydantic/SQLModel (backend) for all type definitions. No untyped variables or functions allowed. Strict type checking must be enabled.

### Error Handling
Implement user-friendly messages and proper HTTP status codes. All error paths must be handled gracefully with appropriate feedback to users.

## Technology Stack Requirements

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

## API Endpoints

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

## Database Schema Rules

- users: managed by Better Auth (id, email, name, etc.)
- tasks:
  - id: integer PK
  - user_id: string (FK → users.id)
  - title: string NOT NULL (1-200 chars)
  - description: text NULLABLE
  - completed: boolean DEFAULT false
  - created_at, updated_at: timestamps
- Indexes: tasks.user_id, tasks.completed

## Auth Flow Rules

1. Frontend login → Better Auth → JWT issued
2. Frontend stores token (localStorage / cookie)
3. Every API call → add header: Authorization: Bearer {token}
4. Backend middleware: verify signature with BETTER_AUTH_SECRET
5. Extract user_id from token → enforce on every operation

## Development Workflow

- Write/Update spec → Generate plan → Break into tasks → Implement
- No manual coding — agent implements everything
- All changes must start from spec files
- Use the specialized agents for each development aspect
- Follow the skill guidelines for consistent implementation

## Success Criteria & Anti-Patterns

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

## Governance

This constitution is the supreme document. All agents must obey it. When in doubt, refer back to this file or ask for clarification. Amendments require explicit updates to this document and propagation to all dependent artifacts.

**Version**: 1.1.0 | **Ratified**: 2026-02-10 | **Last Amended**: 2026-02-10
