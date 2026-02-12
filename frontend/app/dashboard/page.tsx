// app/dashboard/page.tsx
// Since we already have the dashboard in the main page.tsx, 
// we'll create a redirect to the main page
import { redirect } from 'next/navigation';

export default function DashboardPage() {
  redirect('/');
}