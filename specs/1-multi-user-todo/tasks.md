# Tasks: Multi-User Todo Application

**Input**: Design documents from `/specs/1-multi-user-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Monorepo structure**: Follow exact folder layout from constitution
- Paths shown below assume web app structure - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan with exact monorepo layout
- [X] T002 Initialize frontend (Next.js 16+, TypeScript, Tailwind) and backend (Python, FastAPI, SQLModel) projects
- [X] T003 [P] Configure linting and formatting tools for both frontend and backend
- [X] T004 Create docker-compose.yml for frontend + backend + Neon DB
- [X] T005 Create root-level configuration files (.env.example, .gitignore)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T006 Setup database schema and Neon PostgreSQL connection with SQLModel
- [X] T007 [P] Implement Better Auth with JWT plugin for frontend authentication
- [X] T008 [P] Setup JWT verification middleware in FastAPI backend
- [X] T009 Create base models (User, Task) with proper user_id foreign key relationships
- [X] T010 Configure error handling and logging infrastructure for both services
- [X] T011 Setup environment configuration management with proper secrets handling
- [X] T012 Create shared types/interfaces for API communication

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration & Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable new users to sign up with email and password and create their account

**Independent Test**: Can be fully tested by registering a new user account and verifying the account is created successfully, allowing the user to log in.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Contract test for registration endpoint in tests/contract/test_auth.py
- [ ] T014 [P] [US1] Integration test for user registration journey in tests/integration/test_auth.py

### Implementation for User Story 1

- [X] T015 [P] [US1] Create User model in backend/models/user.py (managed by Better Auth)
- [X] T016 [US1] Implement authentication service in backend/services/auth_service.py
- [X] T017 [US1] Implement POST /api/auth/register endpoint in backend/routes/auth.py (with validation)
- [X] T018 [US1] Create registration page in frontend/app/(auth)/register/page.tsx (using Server Components by default)
- [X] T019 [US1] Add client component for registration form if needed (with 'use client')
- [X] T020 [US1] Add proper error handling and validation for registration

**Constitution Compliance Check**:
- [X] User isolation enforced (backend filters by user_id)
- [X] JWT verification implemented
- [X] Server Components used by default
- [X] Type safety enforced with TypeScript/Pydantic

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Login & Session Management (Priority: P1)

**Goal**: Allow users to sign in securely to access their personal todo list

**Independent Test**: Can be fully tested by logging in with valid credentials and accessing a protected area of the application.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T021 [P] [US2] Contract test for login endpoint in tests/contract/test_auth.py
- [ ] T022 [P] [US2] Integration test for user login journey in tests/integration/test_auth.py

### Implementation for User Story 2

- [X] T023 [P] [US2] Implement POST /api/auth/login endpoint in backend/routes/auth.py (with JWT issuance)
- [X] T024 [US2] Create login page in frontend/app/(auth)/login/page.tsx (using Server Components by default)
- [X] T025 [US2] Add client component for login form if needed (with 'use client')
- [X] T026 [US2] Implement protected layout in frontend/app/(app)/layout.tsx
- [X] T027 [US2] Create middleware for protecting routes in frontend/middleware.ts
- [X] T028 [US2] Add proper error handling and validation for login

**Constitution Compliance Check**:
- [X] User isolation enforced (backend assigns correct user_id)
- [X] JWT verification implemented
- [X] Server Components used by default, Client Components only when necessary
- [X] Type safety enforced with TypeScript/Pydantic

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Create New Tasks (Priority: P1)

**Goal**: Allow logged-in users to create a new task with a required title and optional description

**Independent Test**: Can be fully tested by logging in and creating a new task, then verifying it appears in the user's task list.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T029 [P] [US3] Contract test for create task endpoint in tests/contract/test_tasks.py
- [ ] T030 [P] [US3] Integration test for task creation journey in tests/integration/test_tasks.py

### Implementation for User Story 3

- [X] T031 [P] [US3] Create Task model in backend/models/task.py with user_id foreign key
- [X] T032 [US3] Implement Task service in backend/services/task_service.py (enforces user_id filtering)
- [X] T033 [US3] Implement POST /api/{user_id}/tasks endpoint in backend/routes/tasks.py (with JWT verification and user_id matching)
- [X] T034 [US3] Create Server Action for creating tasks in frontend/app/actions/task_actions.ts
- [X] T035 [US3] Implement task creation form in frontend/app/(app)/tasks/create/page.tsx (using Server Components by default)
- [X] T036 [US3] Add client component for interactive form elements if needed (with 'use client')

**Constitution Compliance Check**:
- [X] User isolation enforced (backend assigns correct user_id)
- [X] JWT verification implemented
- [X] Server Components used by default, Client Components only when necessary
- [X] Type safety enforced with TypeScript/Pydantic

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - View Personal Task List (Priority: P1)

**Goal**: Allow logged-in users to view a list of all their own tasks, showing title, description summary, completion status, and creation date

**Independent Test**: Can be fully tested by logging in and viewing the task list, verifying only the user's own tasks are displayed.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T037 [P] [US4] Contract test for list tasks endpoint in tests/contract/test_tasks.py
- [ ] T038 [P] [US4] Integration test for task list journey in tests/integration/test_tasks.py

### Implementation for User Story 4

- [X] T039 [US4] Implement GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py (with JWT verification and user_id matching)
- [X] T040 [US4] Create Server Component for displaying tasks in frontend/app/(app)/tasks/page.tsx
- [X] T041 [US4] Create reusable TaskList component in frontend/components/task/TaskList.tsx
- [X] T042 [US4] Add loading and error states for task list
- [ ] T043 [US4] Implement pagination/filtering if needed

**Constitution Compliance Check**:
- [X] User isolation enforced (backend filters by user_id)
- [X] JWT verification implemented
- [X] Server Components used by default
- [X] Type safety enforced with TypeScript/Pydantic

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Mark Tasks as Complete (Priority: P2)

**Goal**: Allow logged-in users to mark any of their tasks as completed (toggle on/off)

**Independent Test**: Can be fully tested by logging in, selecting a task, toggling its completion status, and verifying the change persists.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T044 [P] [US5] Contract test for toggle complete endpoint in tests/contract/test_tasks.py
- [ ] T045 [P] [US5] Integration test for task completion journey in tests/integration/test_tasks.py

### Implementation for User Story 5

- [X] T046 [US5] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/routes/tasks.py (with JWT verification and user_id matching)
- [X] T047 [US5] Create Server Action for toggling task completion in frontend/app/actions/task_actions.ts
- [X] T048 [US5] Add completion toggle UI in frontend/components/task/TaskItem.tsx
- [X] T049 [US5] Add optimistic UI updates for completion toggle
- [X] T050 [US5] Add proper error handling for completion toggle

**Constitution Compliance Check**:
- [X] User isolation enforced (backend verifies user_id matches token)
- [X] JWT verification implemented
- [X] Server Components used by default
- [X] Type safety enforced with TypeScript/Pydantic

**Checkpoint**: At this point, User Stories 1-5 should all work independently

---

## Phase 8: User Story 6 - Edit Existing Tasks (Priority: P2)

**Goal**: Allow logged-in users to edit the title or description of any of their existing tasks

**Independent Test**: Can be fully tested by logging in, selecting a task to edit, modifying its details, and verifying the changes are saved.

### Tests for User Story 6 (OPTIONAL - only if tests requested) ⚠️

- [ ] T051 [P] [US6] Contract test for update task endpoint in tests/contract/test_tasks.py
- [ ] T052 [P] [US6] Integration test for task edit journey in tests/integration/test_tasks.py

### Implementation for User Story 6

- [X] T053 [US6] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py (with JWT verification and user_id matching)
- [X] T054 [US6] Create Server Action for updating tasks in frontend/app/actions/task_actions.ts
- [X] T055 [US6] Implement task edit form in frontend/app/(app)/tasks/[id]/edit/page.tsx
- [X] T056 [US6] Add client component for interactive form elements if needed (with 'use client')
- [X] T057 [US6] Add proper validation and error handling for task updates

**Constitution Compliance Check**:
- [X] User isolation enforced (backend verifies user_id matches token)
- [X] JWT verification implemented
- [X] Server Components used by default, Client Components only when necessary
- [X] Type safety enforced with TypeScript/Pydantic

**Checkpoint**: At this point, User Stories 1-6 should all work independently

---

## Phase 9: User Story 7 - Delete Tasks (Priority: P2)

**Goal**: Allow logged-in users to delete any of their tasks

**Independent Test**: Can be fully tested by logging in, selecting a task to delete, confirming the action, and verifying the task is removed.

### Tests for User Story 7 (OPTIONAL - only if tests requested) ⚠️

- [ ] T058 [P] [US7] Contract test for delete task endpoint in tests/contract/test_tasks.py
- [ ] T059 [P] [US7] Integration test for task deletion journey in tests/integration/test_tasks.py

### Implementation for User Story 7

- [X] T060 [US7] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py (with JWT verification and user_id matching)
- [X] T061 [US7] Create Server Action for deleting tasks in frontend/app/actions/task_actions.ts
- [X] T062 [US7] Add delete confirmation UI in frontend/components/task/TaskItem.tsx
- [X] T063 [US7] Add optimistic UI updates for task deletion
- [X] T064 [US7] Add proper error handling for task deletion

**Constitution Compliance Check**:
- [X] User isolation enforced (backend verifies user_id matches token)
- [X] JWT verification implemented
- [X] Server Components used by default
- [X] Type safety enforced with TypeScript/Pydantic

**Checkpoint**: At this point, User Stories 1-7 should all work independently

---

## Phase 10: User Story 8 - Data Isolation & Security (Priority: P1)

**Goal**: Ensure logged-in users only see and interact with their own tasks — complete data isolation

**Independent Test**: Can be fully tested by having multiple users with tasks, logging in as each user, and verifying they only see their own tasks.

### Tests for User Story 8 (OPTIONAL - only if tests requested) ⚠️

- [ ] T065 [P] [US8] Contract test for user data isolation in tests/contract/test_security.py
- [ ] T066 [P] [US8] Integration test for cross-user data access prevention in tests/integration/test_security.py

### Implementation for User Story 8

- [X] T067 [US8] Enhance all backend endpoints to enforce user_id matching between token and URL
- [X] T068 [US8] Add comprehensive user_id validation in all task operations
- [X] T069 [US8] Implement proper error responses (403 Forbidden) for unauthorized access attempts
- [X] T070 [US8] Add security audit logging for access violation attempts
- [X] T071 [US8] Add frontend validation to prevent user_id manipulation in URLs

**Constitution Compliance Check**:
- [X] User isolation enforced (backend verifies user_id matches token)
- [X] JWT verification implemented
- [X] Server Components used by default
- [X] Type safety enforced with TypeScript/Pydantic

**Checkpoint**: At this point, all user stories should work independently with complete data isolation

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T072 [P] Documentation updates in docs/
- [X] T073 Code cleanup and refactoring
- [X] T074 Performance optimization across all stories
- [X] T075 [P] Additional unit tests (if requested) in tests/unit/
- [X] T076 Security hardening (ensure all endpoints verify JWT and user_id)
- [X] T077 Run quickstart.md validation
- [X] T078 Verify all constitution principles are followed
- [X] T079 Add responsive design improvements
- [X] T080 Add loading states and user-friendly error messages
- [X] T081 Implement basic input validation (title length, required fields)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1-US3 but should be independently testable
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1-US4 but should be independently testable
- **User Story 6 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1-US5 but should be independently testable
- **User Story 7 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1-US6 but should be independently testable
- **User Story 8 (P1)**: Can start after Foundational (Phase 2) - Should be implemented across all other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for registration endpoint in tests/contract/test_auth.py"
Task: "Integration test for user registration journey in tests/integration/test_auth.py"

# Launch all models for User Story 1 together:
Task: "Create User model in backend/models/user.py"
Task: "Create authentication service in backend/services/auth_service.py"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

## Constitution Compliance Verification

Throughout implementation, verify:

- [ ] All changes originate from spec files (spec-driven development)
- [ ] Follow exact monorepo structure (frontend/, backend/, specs/, etc.)
- [ ] Enforce user isolation (each user sees only their own tasks)
- [ ] Implement stateless JWT auth with Better Auth and FastAPI verification
- [ ] Use Server Components by default, minimize client-side JS
- [ ] Implement proper error handling with user-friendly messages
- [ ] Enforce type safety with TypeScript and Pydantic/SQLModel
- [ ] All API endpoints verify JWT and match user_id from token with URL parameter

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Always ensure constitution compliance at each checkpoint