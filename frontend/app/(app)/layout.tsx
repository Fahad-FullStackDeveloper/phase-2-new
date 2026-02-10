// app/(app)/layout.tsx
import { ReactNode } from 'react';
import Link from 'next/link';

export default function AppLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navigation Bar */}
      <nav className="bg-blue-600 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <Link href="/" className="text-xl font-bold">
            Todo App
          </Link>
          <div className="flex space-x-4">
            <Link href="/tasks" className="hover:underline">
              My Tasks
            </Link>
            <Link href="/profile" className="hover:underline">
              Profile
            </Link>
            <Link href="/api/auth/logout" className="hover:underline">
              Logout
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-grow container mx-auto px-4 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white p-4 text-center">
        <p>© {new Date().getFullYear()} Todo App. All rights reserved.</p>
      </footer>
    </div>
  );
}