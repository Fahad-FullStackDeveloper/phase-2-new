---
name: Next.js Auth & Security
description: Patterns for authentication, middleware, protected routes, secure practices.
tags: [nextjs, auth, security, middleware]
version: 1.0
---

## When to use
Login, signup, protected pages, sessions, middleware, security rules.

## Core Rules
- Use **Auth.js / NextAuth** (or your chosen lib) with App Router support
- Protect routes with **middleware.ts** at root level
- Use **Server Components** + session checks for protected data
- Never expose secrets in client code
- Hash passwords, use secure cookies, validate inputs
- Add **error handling** on auth failures
- Prefer **Server Actions** for login/logout flows

## Example – Middleware
```ts
// middleware.ts
import { withAuth } from 'next-auth/middleware';

export default withAuth({
  pages: {
    signIn: '/auth/signin',
  },
});

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
};