---
name: Next.js Core Conventions
description: Enforces App Router best practices, Server Components default, routing, metadata, and clean hackathon-friendly code style.
tags: [nextjs, app-router, server-components, hackathon]
version: 1.0
---

## Activation
Use for any task involving pages, layouts, routing, folder structure, components, or general Next.js code.

## Strict Rules (always enforce)
- App Router only — use app/ directory, never pages/
- Server Components by default — add 'use client' **only** when needed (hooks, browser APIs, event handlers)
- Use async Server Components for data fetching
- Always define metadata (export const metadata = {...} or generateMetadata)
- Add loading.js, error.js, not-found.js in important route groups
- Use route groups: (marketing)/, (dashboard)/, (auth)/ etc. for clean URLs
- TypeScript everywhere — strict types preferred
- Clean, commented code — explain non-obvious decisions
- Tailwind for styling unless otherwise specified

## Good Example
```tsx
// app/(dashboard)/page.tsx
import { Suspense } from 'react';

export const metadata = {
  title: 'Dashboard - Hackathon Project',
  description: 'Overview and key metrics',
};

export default async function Dashboard() {
  const data = await fetchSomeData(); // your data logic
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <main>{/* content */}</main>
    </Suspense>
  );
}