"use client";

import { useState } from "react";
import { Task } from "@/types/task";
import { taskApi } from "@/lib/api";

interface TaskItemProps {
  task: Task;
  userId: string;
  onToggleComplete: (taskId: number, completed: boolean) => void;
  onDelete: (taskId: number) => void;
  onUpdate: (taskId: number, updatedTask: Task) => void;
}

export default function TaskItem({ task, userId, onToggleComplete, onDelete, onUpdate }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || "");
  const [loading, setLoading] = useState(false);

  const handleSaveEdit = async () => {
    setLoading(true);
    try {
      const updatedTask = await taskApi.updateTask(userId, task.id, { 
        title: editTitle, 
        description: editDescription 
      });
      onUpdate(task.id, updatedTask);
      setIsEditing(false);
    } catch (error) {
      console.error("Error updating task:", error);
      alert("Failed to update task. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleToggleComplete = async () => {
    try {
      const result = await taskApi.toggleTaskComplete(userId, task.id);
      onToggleComplete(task.id, result.completed);
    } catch (error) {
      console.error("Error toggling task completion:", error);
      alert("Failed to update task. Please try again.");
    }
  };

  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to delete this task?")) {
      try {
        await taskApi.deleteTask(userId, task.id);
        onDelete(task.id);
      } catch (error) {
        console.error("Error deleting task:", error);
        alert("Failed to delete task. Please try again.");
      }
    }
  };

  return (
    <div className={`border rounded-lg p-4 mb-2 ${task.completed ? "bg-green-50" : "bg-white"}`}>
      {isEditing ? (
        <div className="space-y-2">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="w-full border rounded px-2 py-1"
            maxLength={50}
            disabled={loading}
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="w-full border rounded px-2 py-1"
            maxLength={500}
            rows={2}
            disabled={loading}
          />
          <div className="flex space-x-2 mt-2">
            <button
              onClick={handleSaveEdit}
              disabled={loading}
              className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 disabled:opacity-50"
            >
              {loading ? "Saving..." : "Save"}
            </button>
            <button
              onClick={() => setIsEditing(false)}
              disabled={loading}
              className="bg-gray-300 px-3 py-1 rounded hover:bg-gray-400 disabled:opacity-50"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="flex items-start">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleComplete}
              className="mt-1 mr-2"
              disabled={loading}
            />
            <div className="flex-1">
              <h3 className={`text-lg ${task.completed ? "line-through text-gray-500" : ""}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`mt-1 ${task.completed ? "line-through text-gray-500" : "text-gray-600"}`}>
                  {task.description}
                </p>
              )}
              <p className="text-xs text-gray-400 mt-1">
                Created: {new Date(task.created_at).toLocaleString()}
                {task.updated_at !== task.created_at && (
                  <> | Updated: {new Date(task.updated_at).toLocaleString()}</>
                )}
              </p>
            </div>
            <div className="flex space-x-1 ml-2">
              <button
                onClick={() => setIsEditing(true)}
                disabled={loading}
                className="text-blue-500 hover:text-blue-700 disabled:opacity-50"
                aria-label="Edit task"
              >
                ✏️
              </button>
              <button
                onClick={handleDelete}
                disabled={loading}
                className="text-red-500 hover:text-red-700 disabled:opacity-50"
                aria-label="Delete task"
              >
                🗑️
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}