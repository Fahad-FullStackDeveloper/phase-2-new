// app/api/login/route.ts
import { NextRequest } from 'next/server';
import { jwtVerify } from 'jose';

export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json();
    
    // In a real application, you would verify credentials against your database
    // For this example, we'll simulate a successful login
    if (!email || !password) {
      return new Response(
        JSON.stringify({ message: 'Email and password are required' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }
    
    // Simulate JWT token generation (in a real app, use a proper JWT library)
    const token = 'fake-jwt-token-for-demo'; // This would be a real JWT in production
    
    return new Response(
      JSON.stringify({ 
        message: 'Login successful', 
        token,
        user: { id: '1', email, name: 'Demo User' }
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ message: 'Internal server error' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}