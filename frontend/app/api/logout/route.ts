// app/api/logout/route.ts
import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // In a real application, you might invalidate the JWT token on the server
    // For this example, we'll just return a success response
    
    return new Response(
      JSON.stringify({ message: 'Logout successful' }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ message: 'Internal server error' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}