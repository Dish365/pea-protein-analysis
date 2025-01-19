# Frontend Development Guide - Process Analysis Application (Next.js 15)

## Table of Contents
1. [Project Structure](#project-structure)
2. [Server and Client Components](#server-and-client-components)
3. [API Integration](#api-integration)
4. [Forms and Mutations](#forms-and-mutations)
5. [Data Fetching and Caching](#data-fetching-and-caching)
6. [Component Architecture](#component-architecture)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)

## Project Structure

```
src/
├── app/                      # Next.js 15 App Router
│   ├── layout.tsx           # Root layout (Server Component)
│   ├── page.tsx             # Landing page (Server Component)
│   ├── api/                 # API Routes for client-side operations
│   │   └── proxy/          # Backend API proxy endpoints
│   └── processes/          # Process analysis routes
│       ├── page.tsx        # Process list (Server Component)
│       ├── new/           # New analysis
│       │   └── page.tsx   # Analysis form (Client Component)
│       └── [id]/          # Dynamic process routes
│           ├── page.tsx   # Process details (Server Component)
│           └── loading.tsx # Loading UI
├── components/
│   ├── analysis/          # Analysis components
│   │   ├── ProcessForm/   # Form components (Client)
│   │   ├── ResultsView/   # Results display (Server)
│   │   └── StatusTracker/ # Real-time status (Client)
│   └── ui/               # Shared UI components
├── lib/
│   ├── actions/          # Server Actions
│   ├── api/             # API utilities
│   └── hooks/           # Custom hooks
└── types/               # TypeScript definitions
```

## Server and Client Components

### Server Components (Default)
```typescript
// app/processes/page.tsx
export default async function ProcessList() {
  // Direct database queries using Server Components
  const processes = await getProcesses();
  
  return (
    <div>
      <h1>Process Analysis List</h1>
      <ProcessGrid processes={processes} />
    </div>
  );
}
```

### Client Components
```typescript
// components/analysis/ProcessForm/index.tsx
'use client';

export function ProcessForm() {
  const [isPending, startTransition] = useTransition();
  
  async function submitProcess(formData: FormData) {
    startTransition(async () => {
      await createProcess(formData);
    });
  }
  
  return (
    <form action={submitProcess}>
      <ProcessTypeField />
      <TechnicalInputs />
      <SubmitButton pending={isPending} />
    </form>
  );
}
```

## API Integration

### Server-Side API Calls
```typescript
// lib/actions/process.ts
'use server';

export async function getProcessDetails(id: string) {
  const res = await fetch(`${process.env.API_URL}/api/v1/process/${id}`, {
    next: { 
      revalidate: 30,
      tags: ['process', id]
    }
  });
  
  if (!res.ok) throw new Error('Failed to fetch process');
  return res.json();
}
```

### Client-Side API Proxy
```typescript
// app/api/proxy/process/route.ts
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const data = await request.json();
  
  const response = await fetch(`${process.env.API_URL}/api/v1/process/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  
  return NextResponse.json(await response.json());
}
```

## Forms and Mutations

### Server Actions Form
```typescript
// components/analysis/ProcessForm/actions.ts
'use server';

export async function createProcess(formData: FormData) {
  const rawData = Object.fromEntries(formData);
  
  try {
    const response = await fetch(`${process.env.API_URL}/api/v1/process/`, {
      method: 'POST',
      body: JSON.stringify(rawData),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) throw new Error('Failed to create process');
    
    revalidateTag('processes');
    redirect('/processes');
    
  } catch (error) {
    return { error: 'Failed to create process' };
  }
}
```

## Data Fetching and Caching

### Cached Data Fetching
```typescript
// app/processes/[id]/page.tsx
export default async function ProcessDetails({ 
  params: { id } 
}: { 
  params: { id: string } 
}) {
  const process = await getProcessDetails(id);
  
  return (
    <ProcessDetailsLayout>
      <ProcessHeader process={process} />
      <Suspense fallback={<ResultsLoadingSkeleton />}>
        <ProcessResults processId={id} />
      </Suspense>
    </ProcessDetailsLayout>
  );
}
```

### Real-time Updates
```typescript
// components/analysis/StatusTracker/StatusPoller.tsx
'use client';

export function StatusPoller({ processId }: { processId: string }) {
  const status = useProcessStatus(processId);
  
  useEffect(() => {
    if (status === 'completed') {
      revalidateTag(`process-${processId}`);
      toast.success('Analysis completed!');
    }
  }, [status, processId]);
  
  return <StatusDisplay status={status} />;
}
```

## Component Architecture

### Layout Components
```typescript
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <Header />
          <main>{children}</main>
          <Footer />
        </Providers>
      </body>
    </html>
  );
}
```

### Loading UI
```typescript
// app/processes/[id]/loading.tsx
export default function LoadingUI() {
  return (
    <div>
      <ProcessHeaderSkeleton />
      <ResultsSkeleton />
    </div>
  );
}
```

## Error Handling

### Error Components
```typescript
// app/processes/[id]/error.tsx
'use client';

export default function ErrorComponent({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

## Best Practices

### 1. Performance
- Use Server Components for static content
- Implement Streaming with Suspense
- Utilize Next.js Image component
- Enable static/dynamic rendering appropriately

### 2. Security
- Implement Content Security Policy
- Use Server Actions for mutations
- Validate data server-side
- Handle CORS properly

### 3. SEO and Metadata
```typescript
// app/processes/[id]/page.tsx
export async function generateMetadata({ 
  params 
}: { 
  params: { id: string } 
}) {
  const process = await getProcessDetails(params.id);
  
  return {
    title: `Process Analysis - ${process.name}`,
    description: `Analysis results for process ${process.name}`,
  };
}
```

### 4. Testing
- Use experimental test mode for Playwright
- Implement Jest tests for App Router
- Test Server Components
- Test Client Components

### 5. Development
- Use `next dev --turbo` for faster development
- Implement proper TypeScript types
- Use ESLint for code quality
- Follow Next.js coding standards

Remember to:
- Keep Server/Client Component separation clear
- Use proper data fetching patterns
- Implement proper loading states
- Handle all error cases
- Follow accessibility guidelines
- Document component usage
- Write comprehensive tests


