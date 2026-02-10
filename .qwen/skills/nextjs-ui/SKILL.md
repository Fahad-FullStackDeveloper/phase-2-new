---
name: Next.js UI Components & Styling
description: Patterns for reusable components, shadcn/ui, Tailwind, client components, responsiveness.
tags: [nextjs, ui, tailwind, shadcn, components]
version: 1.0
---

## When to use
Creating or editing UI, components, layouts, styling, responsiveness.

## Core Rules
- Use **shadcn/ui** components whenever possible (button, card, dialog, etc.)
- Style with **Tailwind** – utility-first, avoid custom CSS when shadcn covers it
- Client components: name them `FeatureXClient.tsx` when they use `'use client'`
- Make UI **mobile responsive** — use responsive Tailwind classes (sm:, md:, lg:)
- Use **Suspense** for loading states inside components
- Prefer **Server Components** for layout/static parts
- Keep components small and composable

## Example
```tsx
// components/ui/StatsCard.tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface StatsCardProps {
  title: string;
  value: string | number;
}

export function StatsCard({ title, value }: StatsCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-3xl font-bold">{value}</p>
      </CardContent>
    </Card>
  );
}