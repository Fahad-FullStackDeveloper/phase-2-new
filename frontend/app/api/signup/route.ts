// app/api/signup/route.ts
import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { name, email, password } = await request.json();
    
    // In a real application, you would validate and store user data in your database
    // For this example, we'll simulate a successful signup
    if (!name || !email || !password) {
      return new Response(
        JSON.stringify({ message: 'Name, email, and password are required' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }
    
    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return new Response(
        JSON.stringify({ message: 'Invalid email format' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }
    
    // Validate password strength
    if (password.length < 8) {
      return new Response(
        JSON.stringify({ message: 'Password must be at least 8 characters long' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }
    
    // Simulate JWT token generation (in a real app, use a proper JWT library)
    const token = 'fake-jwt-token-for-demo'; // This would be a real JWT in production
    
    return new Response(
      JSON.stringify({ 
        message: 'Signup successful', 
        token,
        user: { id: '1', email, name }
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