"use client";

import { useState } from "react";
import { Task } from "@/types/task";
import { taskApi } from "@/lib/api";

interface TaskFormProps {
  userId: string;
  onTaskAdded: (task: Task) => void;
}

export default function TaskForm({ userId, onTaskAdded }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!title.trim()) {
      setError("Title is required");
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const newTask = await taskApi.createTask(userId, {
        title: title.trim(),
        description: description.trim(),
      });
      
      onTaskAdded(newTask);
      
      // Reset form
      setTitle("");
      setDescription("");
    } catch (err) {
      setError("Failed to create task. Please try again.");
      console.error("Error creating task:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6 p-4 bg-white border rounded-lg shadow-sm">
      {error && (
        <div className="mb-4 p-2 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}
      
      <div className="mb-4">
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={loading}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
          placeholder="Enter task title (1-50 characters)"
          maxLength={50}
          required
        />
      </div>
      
      <div className="mb-4">
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={loading}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
          placeholder="Enter task description (optional, up to 500 characters)"
          maxLength={500}
          rows={3}
        />
      </div>
      
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? "Adding Task..." : "Add Task"}
      </button>
    </form>
  );
}