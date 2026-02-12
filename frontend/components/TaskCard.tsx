'use client';

import { useState } from 'react';

interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  createdAt: Date;
}

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: string) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
}

export default function TaskCard({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) {
  const [showActions, setShowActions] = useState(false);

  const formatDate = (date: Date) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  return (
    <div 
      className={`card relative overflow-hidden transition-all duration-300 ${
        task.completed ? 'opacity-80 border-l-4 border-green-500' : 'border-l-4 border-primary-500'
      }`}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      <div className="flex items-start">
        <button
          onClick={() => onToggleComplete(task.id)}
          className={`mt-1 flex-shrink-0 h-5 w-5 rounded-full border flex items-center justify-center mr-3 ${
            task.completed 
              ? 'bg-green-500 border-green-500' 
              : 'border-gray-300 hover:border-primary-500'
          }`}
          aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
        >
          {task.completed && (
            <svg className="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
            </svg>
          )}
        </button>
        
        <div className="flex-grow">
          <h3 className={`font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
            {task.title}
          </h3>
          <p className={`mt-1 text-gray-600 ${task.completed ? 'line-through' : ''}`}>
            {task.description}
          </p>
          <div className="mt-3 text-xs text-gray-500">
            Created: {formatDate(task.createdAt)}
          </div>
        </div>
      </div>
      
      <div 
        className={`absolute right-4 top-4 transition-opacity duration-200 ${
          showActions ? 'opacity-100' : 'opacity-0'
        }`}
      >
        <div className="flex space-x-2">
          <button
            onClick={() => onEdit(task)}
            className="p-1.5 rounded-full hover:bg-gray-100 text-gray-600 hover:text-blue-600 transition-colors"
            aria-label="Edit task"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="p-1.5 rounded-full hover:bg-gray-100 text-gray-600 hover:text-red-600 transition-colors"
            aria-label="Delete task"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}