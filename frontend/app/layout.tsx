import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Modern Todo App',
  description: 'A beautiful and functional todo application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 antialiased">
        {children}
      </body>
    </html>
  );
}