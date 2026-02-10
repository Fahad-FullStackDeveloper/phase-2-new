// app/(app)/tasks/page.tsx
"use client";

import { useState, useEffect } from "react";
import TaskList from "@/components/task/TaskList";
import TaskForm from "@/components/task/TaskForm";
import { Task } from "@/types/task";

export default function TasksPage() {
  // In a real implementation, we'd get the user ID from the session
  // For now, we'll use a mock user ID
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    // In a real implementation, we'd get the user ID from the session
    // For now, we'll use a mock user ID
    setUserId("mock-user-id");
  }, []);

  const handleTaskAdded = (newTask: Task) => {
    // The task list will automatically refresh since we're using API calls
    console.log("Task added:", newTask);
  };

  if (!userId) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6 text-center">My Tasks</h1>
      
      <TaskForm userId={userId} onTaskAdded={handleTaskAdded} />
      
      <TaskList userId={userId} />
    </div>
  );
}