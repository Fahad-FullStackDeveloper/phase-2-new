---
name: Next.js Data Fetching & Mutations
description: Best patterns for data loading, caching, revalidation, Server Actions, route handlers.
tags: [nextjs, data, server-actions, caching]
version: 1.0
---

## Activation
Any task with fetching data, forms, mutations, API calls, caching.

## Rules
- Fetch in Server Components using fetch() — prefer { next: { revalidate: ... } } or cache: 'force-cache'
- Use Server Actions ('use server') for mutations/forms — strongly preferred over client fetches
- Route Handlers (route.ts) for public/external APIs
- Always handle errors gracefully (try/catch + user messages)
- Revalidate after mutations: revalidatePath() or revalidateTag()
- Dynamic routes: export const dynamic = 'force-dynamic' when needed
- Push logic to server — minimize client-side fetching

## Example – Server Action
```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function addTodo(formData: FormData) {
  try {
    // db or logic here
    revalidatePath('/todos');
    return { success: true };
  } catch {
    return { error: 'Failed to add todo' };
  }
}