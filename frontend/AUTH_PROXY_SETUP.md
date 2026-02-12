# Authentication and Proxy Configuration

## Overview
This document explains the authentication and proxy setup for the Next.js frontend application.

## Files

### `middleware.ts`
- Handles route protection and authentication checks
- Redirects unauthenticated users from protected routes to the login page
- Uses utility functions from `lib/proxy.ts`

### `lib/proxy.ts`
- Contains utility functions for authentication-related operations
- Provides functions to check if a path is protected, extract tokens, etc.

### `next.config.js`
- Configured with API rewrites to proxy `/api/*` requests to the backend server
- Uses `NEXT_PUBLIC_API_URL` environment variable or defaults to `http://localhost:8000`

### `app/api/proxy/route.ts`
- An API route that acts as a proxy for backend API calls
- Forwards requests to the backend server with proper authentication headers

## Environment Variables
Make sure to set `NEXT_PUBLIC_API_URL` in your environment to point to your backend server.