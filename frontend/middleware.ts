import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// This function handles protected routes
export function middleware(request: NextRequest) {
  // In a real implementation with Better Auth, we would verify the JWT here
  // For now, we'll implement a basic check
  
  // Check if the user is trying to access a protected route
  const protectedPaths = ['/tasks', '/profile'];
  const isAuthenticated = checkAuth(request); // Placeholder function

  // If user is accessing a protected route but isn't authenticated
  if (protectedPaths.some(path => request.nextUrl.pathname.startsWith(path)) && !isAuthenticated) {
    // Redirect to login page
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Continue to the requested page
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

// Placeholder function to check authentication
// In a real implementation, this would verify the JWT token
function checkAuth(request: NextRequest): boolean {
  // In a real app with Better Auth, we would verify the token from cookies/headers
  // For now, we'll just check if there's a mock token in localStorage (client-side) or a header (server-side)
  
  // This is a simplified check - in reality, Better Auth provides middleware for this
  if (typeof window !== 'undefined') {
    // Client-side check
    return !!localStorage.getItem('auth_token');
  } else {
    // Server-side check - look for auth header or cookie
    // This is a simplified check - Better Auth would handle this properly
    return request.cookies.has('better-auth.session_token') || 
           !!request.headers.get('Authorization')?.startsWith('Bearer ');
  }
}