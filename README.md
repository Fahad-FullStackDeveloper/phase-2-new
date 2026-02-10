# Phase 2 TODO Application

Welcome to the Phase 2 TODO Application project! This is a full-stack TODO application built using a specialized agent-based development approach.

## Project Overview

This project implements a comprehensive TODO application with user authentication, task management, and a responsive frontend. The development approach leverages specialized AI agents to handle different aspects of the application, ensuring efficient and focused development across frontend, backend, and infrastructure concerns.

## Project Scope

The Phase 2 TODO Application encompasses:

- **Authentication System**: Secure user registration, login, and session management
- **Task Management**: Create, read, update, and delete (CRUD) operations for user tasks
- **Full-Stack Architecture**: Modern frontend and robust backend integration
- **Database Management**: Efficient storage and retrieval of user data and tasks
- **Security**: JWT-based authentication and authorization
- **Testing**: Integration and unit testing for reliable functionality

## Specialized Agents

This project utilizes specialized AI agents to handle different development aspects:

- **Auth-Security Agent**: Manages authentication and security features, including Better Auth integration and JWT token handling
- **DB Architect Agent**: Designs and manages database models, connections, and migrations using SQLModel and Neon PostgreSQL
- **FastAPI Backend Engineer**: Develops secure REST API endpoints with proper user data protection
- **Fullstack Todo Agent**: Implements features spanning both backend and frontend components
- **NextJS Frontend Agent**: Builds the Next.js frontend with authentication and task management interfaces
- **Integration Tester**: Verifies that frontend and backend components work together properly
- **Project Coordinator**: Organizes the monorepo structure and manages infrastructure files
- **Spec Writer Documentation Agent**: Creates and maintains specification documents

## Development Skills

To ensure consistent, high-quality development across all agents, we've implemented specialized skills that enforce best practices:

- **Next.js Core Conventions**: Enforces App Router best practices, Server Components default, routing, metadata, and clean hackathon-friendly code style
- **Next.js Data Fetching & Mutations**: Best patterns for data loading, caching, revalidation, Server Actions, and route handlers
- **Next.js UI Components & Styling**: Patterns for reusable components, shadcn/ui, Tailwind, client components, and responsiveness
- **Next.js Auth & Security**: Patterns for authentication, middleware, protected routes, and secure practices
- **Hackathon Phase 2 Success Rules**: Overall guidelines, success criteria, and anti-patterns for Phase 2 judging

These skills ensure consistent code quality and adherence to Next.js best practices across all development tasks.

## Technologies Used

- **Backend**: FastAPI with JWT authentication
- **Frontend**: Next.js 16+ with App Router, TypeScript, and Tailwind CSS
- **Database**: Neon PostgreSQL with SQLModel
- **Authentication**: Better Auth with JWT tokens
- **Infrastructure**: Docker Compose for containerization

## Features

- User registration and authentication
- Secure task management with user isolation
- Responsive web interface
- Real-time task updates
- Protected routes and user data privacy

## Getting Started

Detailed setup instructions will be added as the project develops. Each specialized agent contributes to different aspects of the application, allowing for parallel development and expertise-focused implementation.

## Contributing

This project uses a unique agent-based development methodology. Contributions should align with the specialized roles of each agent to maintain consistency and efficiency.

All development must follow the project constitution located at `.specify/memory/constitution.md`. This document defines the unbreakable rules, principles, architecture, success criteria, and workflow for the entire project. All agents, skills, and implementations must strictly follow this constitution. No deviation is allowed without explicit update to this file.

## Project Status

Current Phase: II - Full-Stack Web Application with persistent storage
- Multi-user Todo application with secure authentication
- Complete CRUD operations for user tasks
- Strict user isolation ensuring data privacy
- Responsive UI with clean, modern design
- JWT-based authentication with Better Auth integration
- Server-first architecture with Next.js App Router

## License

This project is licensed under the MIT License - see the LICENSE file for details.