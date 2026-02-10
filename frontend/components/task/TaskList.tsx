"use client";

import { useState, useEffect } from "react";
import TaskItem from "./TaskItem";
import { Task } from "@/types/task";
import { taskApi } from "@/lib/api";

interface TaskListProps {
  userId: string;
}

export default function TaskList({ userId }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await taskApi.getTasks(userId);
      setTasks(tasksData);
    } catch (err) {
      setError("Failed to load tasks");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    try {
      const result = await taskApi.toggleTaskComplete(userId, taskId);
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? { ...task, completed: result.completed } : task
        )
      );
    } catch (err) {
      setError("Failed to update task");
      console.error(err);
    }
  };

  const handleDelete = async (taskId: number) => {
    try {
      await taskApi.deleteTask(userId, taskId);
      setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
    } catch (err) {
      setError("Failed to delete task");
      console.error(err);
    }
  };

  const handleUpdate = async (taskId: number, updatedTask: Partial<Task>) => {
    try {
      const updated = await taskApi.updateTask(userId, taskId, updatedTask);
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? updated : task
        )
      );
    } catch (err) {
      setError("Failed to update task");
      console.error(err);
    }
  };

  if (loading) return <div className="text-center py-4">Loading tasks...</div>;
  if (error) return <div className="text-center py-4 text-red-500">Error: {error}</div>;

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Your Tasks</h2>
      {tasks.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No tasks yet. Add a new task to get started!
        </div>
      ) : (
        <div>
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              userId={userId}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDelete}
              onUpdate={handleUpdate}
            />
          ))}
        </div>
      )}
    </div>
  );
}