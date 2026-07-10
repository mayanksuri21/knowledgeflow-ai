# KnowledgeFlow AI - Project Architecture & Design

## Overview
KnowledgeFlow AI is a production-quality AI-powered document assistant that allows users to securely upload PDF documents and chat with them using Google Gemini.

## Tech Stack
- **Frontend**: Next.js 15, TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: Clerk
- **AI**: Google Gemini API

---

## 1. Project Folder Structure

### Root Level
```
knowledgeflow-ai/
├── frontend/                 # Next.js 15 frontend application
├── backend/                  # FastAPI backend application
├── docker/                   # Docker configuration files
├── docs/                     # Project documentation
└── README.md                 # Project overview
```

### Frontend Structure (`frontend/`)
```
frontend/
├── public/                   # Static assets (images, fonts, etc.)
├── src/
│   ├── app/                  # Next.js App Router
│   │   ├── (auth)/           # Auth routes (sign-in, sign-up)
│   │   ├── (dashboard)/      # Dashboard routes
│   │   │   ├── dashboard/    # Main dashboard page
│   │   │   ├── documents/    # Document management
│   │   │   └── chat/         # Chat interface
│   │   ├── layout.tsx        # Root layout
│   │   └── page.tsx          # Landing page
│   ├── components/           # Reusable UI components
│   │   ├── ui/               # shadcn/ui components
│   │   ├── layout/           # Layout components (Header, Sidebar, Footer)
│   │   └── features/         # Feature-specific components
│   ├── lib/                  # Utility functions, hooks, API clients
│   │   ├── api/              # API client functions
│   │   ├── hooks/            # Custom React hooks
│   │   └── utils.ts          # Helper functions
│   ├── types/                # TypeScript type definitions
│   └── styles/               # Global styles
├── .env.local.example        # Environment variables template
├── .env.local                # Environment variables (local)
├── package.json
├── tsconfig.json
└── tailwind.config.ts
```

#### Frontend Folder Explanations
- **`src/app/(auth)/`**: Contains authentication-related routes protected by Clerk middleware
- **`src/app/(dashboard)/`**: Protected routes for authenticated users (dashboard, documents, chat)
- **`src/components/ui/`**: shadcn/ui component library
- **`src/components/layout/`**: Reusable layout components for consistent UI
- **`src/components/features/`**: Components specific to features (document upload, chat interface, etc.)
- **`src/lib/api/`**: Functions to interact with the backend API
- **`src/lib/hooks/`**: Custom hooks for data fetching, state management, etc.

### Backend Structure (`backend/`)
```
backend/
├── app/
│   ├── api/                  # API routes (endpoints)
│   │   ├── v1/               # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── auth.py       # Auth-related endpoints
│   │   │   ├── documents.py  # Document management endpoints
│   │   │   └── chat.py       # Chat endpoints
│   │   └── deps.py           # Dependencies (auth, DB session)
│   ├── core/                 # Core configuration and utilities
│   │   ├── config.py         # Settings and environment variables
│   │   ├── security.py       # Security utilities
│   │   └── database.py       # Database connection setup
│   ├── models/               # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── document.py
│   │   └── chat.py
│   ├── schemas/              # Pydantic schemas for request/response validation
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── document.py
│   │   └── chat.py
│   ├── repositories/         # Data access layer (repositories)
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user_repository.py
│   │   ├── document_repository.py
│   │   └── chat_repository.py
│   ├── services/             # Business logic layer
│   │   ├── __init__.py
│   │   ├── document_service.py
│   │   ├── chat/
│   │   │   ├── __init__.py
│   │   │   └── chat_service.py
│   │   └── ai/
│   │       ├── __init__.py
│   │       ├── ai_service.py
│   │       ├── providers/
│   │       │   ├── __init__.py
│   │       │   └── gemini_provider.py
│   │       └── context/
│   │           ├── __init__.py
│   │           └── document_provider.py
│   ├── storage/              # File storage abstraction
│   │   ├── __init__.py
│   │   ├── storage_interface.py
│   │   └── local_storage.py
│   ├── utils/                # Utility functions
│   │   └── __init__.py
│   └── main.py               # FastAPI application entry point
├── alembic/                  # Database migrations
├── tests/                    # Test files
├── .env.example              # Environment variables template
├── .env                      # Environment variables
├── requirements.txt
└── main.py
```

#### Backend Folder Explanations
- **`app/api/v1/`**: Versioned API endpoints for scalability. Thin layer: validate → call service → return response.
- **`app/api/deps.py`**: Dependency injection for auth and database sessions
- **`app/core/`**: Core application configuration, database setup, and security utilities
- **`app/models/`**: SQLAlchemy ORM models representing database tables
- **`app/schemas/`**: Pydantic models for data validation and serialization
- **`app/repositories/`**: Data access layer, abstracting database operations
- **`app/services/`**: Business logic layer
  - **`chat/`**: Chat-related services (future: memory.py, prompt_builder.py, response_formatter.py)
  - **`ai/`**: AI abstraction layer
    - **`providers/`**: AI provider implementations (Gemini, future: OpenAI, etc.)
    - **`context/`**: Context providers (document content, future: RAG)
- **`app/storage/`**: Storage abstraction layer (local storage, future: S3)
- **`app/utils/`**: Utility functions
- **`alembic/`**: Database migration files

---

## 2. Backend Architecture (FastAPI)

### Architecture Pattern: Clean Architecture with Separation of Concerns
We follow a clean architecture pattern with clear layers:
- **Routes (API)**: Thin layer - validate request → call service → return response
- **Services**: Business logic layer
- **Repositories**: Data access layer
- **Models**: SQLAlchemy ORM models
- **Schemas**: Pydantic validation schemas

### Key Components
1. **Clerk Authentication**: Validates JWT tokens from Clerk
2. **Database Layer**: SQLAlchemy ORM + Repository pattern
3. **Storage Abstraction**: Pluggable storage providers
4. **AI Abstraction**: Pluggable AI providers and context sources
5. **API Versioning**: `/api/v1/` prefix for future scalability

---

## 3. Database Design (PostgreSQL)

### Tables

#### `users` Table
| Column         | Type         | Constraints                | Description                          |
|----------------|--------------|----------------------------|--------------------------------------|
| `id`           | UUID         | PRIMARY KEY                | Unique user ID (from Clerk)          |
| `clerk_id`     | VARCHAR(255) | UNIQUE, NOT NULL           | Clerk user ID                        |
| `email`        | VARCHAR(255) | UNIQUE, NOT NULL           | User email address                   |
| `first_name`   | VARCHAR(100) |                            | User first name                      |
| `last_name`    | VARCHAR(100) |                            | User last name                       |
| `created_at`   | TIMESTAMPTZ  | DEFAULT NOW(), NOT NULL    | Account creation timestamp           |
| `updated_at`   | TIMESTAMPTZ  | DEFAULT NOW(), NOT NULL    | Last update timestamp                |

#### `documents` Table
| Column              | Type         | Constraints                | Description                          |
|---------------------|--------------|----------------------------|--------------------------------------|
| `id`                | UUID         | PRIMARY KEY                | Unique document ID                   |
| `user_id`           | UUID         | FOREIGN KEY (users.id)     | Owner of the document                |
| `filename`          | VARCHAR(255) | NOT NULL                   | Original filename                    |
| `file_path`         | TEXT         | NOT NULL                   | Storage path of the PDF              |
| `file_size`         | INTEGER      | NOT NULL                   | File size in bytes                   |
| `processing_status` | VARCHAR(50)  | NOT NULL DEFAULT 'uploaded' | Processing status (uploaded, processing, ready, failed) |
| `uploaded_at`       | TIMESTAMPTZ  | DEFAULT NOW(), NOT NULL    | Upload timestamp                     |
| `updated_at`        | TIMESTAMPTZ  | DEFAULT NOW(), NOT NULL    | Last update timestamp                |

#### `chat_sessions` Table
| Column           | Type         | Constraints                | Description                          |
|------------------|--------------|----------------------------|--------------------------------------|
| `id`             | UUID         | PRIMARY KEY                | Unique chat session ID               |
| `user_id`        | UUID         | FOREIGN KEY (users.id)     | Owner of the chat session            |
| `document_id`    | UUID         | FOREIGN KEY (documents.id) | Associated document                  |
| `title`          | VARCHAR(255) |                            | Chat session title                   |
| `created_at`     | TIMESTAMPTZ  | DEFAULT NOW(), NOT NULL    | Session creation timestamp           |
| `updated_at`     | TIMESTAMPTZ  | DEFAULT NOW(), NOT NULL    | Last message timestamp               |

#### `chat_messages` Table
| Column           | Type         | Constraints                | Description                          |
|------------------|--------------|----------------------------|--------------------------------------|
| `id`             | UUID         | PRIMARY KEY                | Unique message ID                    |
| `chat_session_id`| UUID         | FOREIGN KEY (chat_sessions.id) | Associated chat session        |
| `role`           | VARCHAR(20)  | NOT NULL                   | Message role ('user' or 'model')     |
| `content`        | TEXT         | NOT NULL                   | Message content                      |
| `created_at`     | TIMESTAMPTZ  | DEFAULT NOW(), NOT NULL    | Message timestamp                    |

---

## 4. API Flow

### Authentication Flow
1. User signs in via Clerk on frontend
2. Frontend receives JWT token from Clerk
3. Frontend includes JWT token in `Authorization` header for all backend requests
4. Backend validates JWT token with Clerk's public keys
5. Backend retrieves or creates user record in database

### Document Upload Flow
1. User selects PDF file on frontend
2. Frontend sends file to `POST /api/v1/documents/upload`
3. Backend validates file (type, size)
4. Backend stores file using Storage abstraction
5. Backend creates document record in database with `processing_status = 'uploaded'`
6. Backend returns document metadata to frontend

### Chat Flow
1. User selects a document and starts a new chat session
2. Frontend creates chat session via `POST /api/v1/chat/sessions`
3. User types a message
4. Frontend sends message to `POST /api/v1/chat/messages`
5. Chat Service calls AI Service
6. AI Service calls Document Provider to get document context
7. AI Service calls AI Provider (Gemini) with context and user message
8. AI Service returns response to Chat Service
9. Chat Service saves both user message and model response to database
10. Chat Service returns model response to frontend
11. Frontend displays response in chat interface

### Chat History Flow
1. User navigates to chat history
2. Frontend requests chat sessions via `GET /api/v1/chat/sessions`
3. Backend returns list of chat sessions for the authenticated user
4. User selects a chat session
5. Frontend requests messages via `GET /api/v1/chat/sessions/{session_id}/messages`
6. Backend returns messages for the selected session
7. Frontend displays chat history

---

## 5. Future Compatibility
The architecture is designed to naturally support these future features without major refactoring:
- Vector Database
- Embeddings
- Chunking
- Hybrid Search
- BM25
- Reranking
- Agents

---

## 6. Implementation Strategy
1. Implement one module at a time
2. For each module:
   - Explain why it exists
   - Explain how it fits into the architecture
   - Generate production-quality code
   - Wait for user approval before continuing
3. First module: Complete project structure and initialization (frontend + backend setup, dependencies, config files, env templates, Docker-ready layout)

---

## Next Steps
Please review the updated architecture and confirm if you're ready to proceed with implementing the first module (project foundation setup).
