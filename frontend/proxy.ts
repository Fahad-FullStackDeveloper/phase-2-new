// middleware.ts - Authentication middleware
// This file handles authentication and protected routes for the application
// Utility functions are imported from lib/proxy.ts

import { NextRequest, NextResponse } from 'next/server';
import { 
  isProtectedPath, 
  redirectToLogin, 
  isAuthenticated 
} from './lib/proxy';

export function middleware(request: NextRequest) {
  // Check if the current path is protected
  if (isProtectedPath(request.nextUrl.pathname)) {
    // If the path is protected, check for JWT token
    if (!isAuthenticated(request)) {
      // Redirect to login if no token is found
      return redirectToLogin(request);
    }
  }

  return NextResponse.next();
}

// Specify which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};