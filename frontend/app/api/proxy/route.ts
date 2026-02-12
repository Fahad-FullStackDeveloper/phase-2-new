// app/api/proxy/route.ts
// API route to proxy requests to the backend server
import { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  return proxyRequest(request);
}

export async function POST(request: NextRequest) {
  return proxyRequest(request);
}

export async function PUT(request: NextRequest) {
  return proxyRequest(request);
}

export async function DELETE(request: NextRequest) {
  return proxyRequest(request);
}

async function proxyRequest(request: NextRequest) {
  try {
    // Get the backend API URL from environment variables
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    // Get the path after /api/proxy
    const url = new URL(request.url);
    const path = url.pathname.replace(/^\/api\/proxy/, '');
    
    // Construct the target URL
    const targetUrl = `${backendUrl}${path}${url.search}`;
    
    // Prepare headers, including authorization if present
    const headers: Record<string, string> = {};
    request.headers.forEach((value, key) => {
      // Don't forward Next.js internal headers
      if (!key.startsWith('x-middleware') && key !== 'host' && key !== 'accept-encoding') {
        headers[key] = value;
      }
    });
    
    // Get the JWT token from cookies if available
    const cookieHeader = request.headers.get('cookie');
    if (cookieHeader) {
      // Extract JWT token from cookies if present
      const jwtMatch = cookieHeader.match(/jwt_token=([^;]+)/);
      if (jwtMatch) {
        headers['Authorization'] = `Bearer ${jwtMatch[1]}`;
      }
    }
    
    // Perform the fetch to the backend
    const response = await fetch(targetUrl, {
      method: request.method,
      headers,
      body: request.body ? await request.blob() : undefined,
    });
    
    // Return the response from the backend
    const responseBody = await response.blob();
    
    return new Response(responseBody, {
      status: response.status,
      headers: {
        'Content-Type': response.headers.get('Content-Type') || 'application/json',
      },
    });
  } catch (error) {
    console.error('Proxy error:', error);
    return new Response(JSON.stringify({ error: 'Proxy error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }
}