// Task type definition
export interface Task {
  id: number;
  user_id: string;  // Foreign key to User
  title: string;    // Required, 1-50 characters
  description?: string; // Optional, up to 500 characters
  completed: boolean;   // Default: false
  created_at: string;   // ISO date string
  updated_at: string;   // ISO date string
}

// Task creation type (without id, user_id, timestamps)
export interface TaskCreationData {
  title: string;
  description?: string;
  completed?: boolean;
}

// Task update type (all fields optional)
export interface TaskUpdateData {
  title?: string;
  description?: string;
  completed?: boolean;
}