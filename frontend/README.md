# Modern Todo Application - Frontend

This is the frontend for a modern, beautiful todo application built with Next.js 16.1.16, TypeScript, and Tailwind CSS.

## Features

- Beautiful, responsive UI with modern design
- Authentication system with login/signup
- Task management (create, edit, delete, mark as complete)
- Protected routes and layouts
- JWT token handling for authentication
- Local storage for task persistence (during demo)
- Smooth animations and transitions

## Tech Stack

- Next.js 16.1.16 (App Router)
- TypeScript
- Tailwind CSS
- Better Auth with JWT plugin
- Axios for API requests

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Environment Variables

Create a `.env.local` file in the root of the frontend directory with the following variables:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-change-this
JWT_SECRET=your-jwt-secret-change-this
DATABASE_URL=sqlite:./db.sqlite
```

## Project Structure

```
frontend/
├── app/
│   ├── api/
│   │   ├── login/
│   │   └── signup/
│   ├── login/
│   ├── signup/
│   ├── dashboard/
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── TaskCard.tsx
│   └── TaskForm.tsx
├── lib/
│   ├── api.ts
│   └── auth.ts
├── public/
└── package.json
```

## API Integration

The application integrates with a backend API at `http://localhost:8000` by default. The API client in `lib/api.ts` automatically includes the JWT token in the Authorization header for all requests.

## Authentication and Proxy Setup

The application implements a robust authentication system with the following components:

- `middleware.ts`: Handles route protection and redirects unauthenticated users from protected routes
- `lib/proxy.ts`: Contains utility functions for authentication-related operations
- `next.config.js`: Configured with API rewrites to proxy `/api/*` requests to the backend server
- `app/api/proxy/route.ts`: An API route that acts as a proxy for backend API calls with proper authentication headers

## Authentication Flow

1. Users can sign up or log in via the respective pages
2. JWT tokens are stored in localStorage
3. Protected routes check for the presence of a valid token
4. Tokens are included in all API requests automatically
5. On token expiration, users are redirected to the login page

## Components

- `TaskCard`: Displays individual tasks with options to edit, delete, or mark as complete
- `TaskForm`: Handles creation and editing of tasks with validation
- `ProtectedLayout`: Ensures only authenticated users can access certain routes

## Styling

The application uses Tailwind CSS with a custom configuration that includes:
- Primary and secondary color palettes
- Custom animations for smooth transitions
- Component classes for consistent styling