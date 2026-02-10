---
name: Hackathon Phase 2 Success Rules
description: Overall guidelines, success criteria, and anti-patterns for Phase 2 judging. Enforces Next.js App Router best practices, server/client boundaries, file-system routing, and hackathon-optimized patterns.
tags: [hackathon, phase2, judging, nextjs, app-router]
version: 1.0
---

## When to use
Any task — this skill gives high-level direction and reminds of judging criteria.

## Core Goals
- Clean, readable, well-structured code
- Good UX (responsive, loading states, error messages)
- Performance & SEO basics covered
- Security & auth implemented
- Fast iteration — use server-first patterns
- Clear comments explaining key decisions
- Use **App Router** only (`app/` directory) — no `pages/`
- **Server Components by default** — only add `'use client'` for interactivity, hooks, browser APIs (window, localStorage, etc.)
- Use **async/await** in Server Components for data fetching
- Always add **metadata** (export const metadata or generateMetadata) for SEO/title
- Create **loading.js**, **error.js**, **not-found.js** in major route groups
- Folder structure: use route groups `(marketing)/`, `(app)/dashboard/`, `(auth)/` etc.
- Naming: PascalCase for components, kebab-case for folders/files
- Keep code clean, readable, well-commented — judges read code
- Use TypeScript everywhere
- Prefer Tailwind for styling unless another library is explicitly required

## Anti-patterns to avoid
- Massive client bundles
- No loading/error states
- Client-side data fetching when server is better
- Inconsistent styling
- Missing auth on protected routes
- Using Client Components when Server Components would suffice
- Fetching data in Client Components when Server Components are available
- Not implementing proper error/loading states
- Ignoring metadata for SEO
- Creating deeply nested component trees without proper separation
- Not using Next.js Image component for images
- Forgetting to implement proper fallbacks for dynamic imports

Always ask: "Is this production-grade yet fast to build?"