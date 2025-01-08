# Frontend Architecture Documentation
`frontend-architecture.md`

# Next.js Frontend Architecture Plan for Pea Protein Extraction Analysis System

## 1. Technical Stack & Requirements

### 1.1 Core Technologies
- Next.js 14 (App Router)
- TypeScript
- TailwindCSS for styling
- React Query for API state management
- Zod for runtime type validation
- Recharts for data visualization
- shadcn/ui for component library

### 1.2 Key Features Support
- Authentication flow integration with Django backend
- Real-time process analysis visualization
- Interactive data input forms
- Dynamic result displays for:
  - Technical analysis (protein recovery, separation efficiency)
  - Economic analysis (CAPEX, OPEX, NPV)
  - Environmental impact assessment
  - Eco-efficiency analysis
  - Process comparisons

## 2. Application Structure

```
src/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/
│   │   ├── processes/
│   │   ├── equipment/
│   │   └── analysis/
│   ├── analysis/
│   │   ├── technical/
│   │   ├── economic/
│   │   ├── environmental/
│   │   └── eco-efficiency/
│   └── layout.tsx
├── components/
│   ├── analysis/
│   │   ├── ProteinRecoveryChart.tsx
│   │   ├── EconomicMetricsDisplay.tsx
│   │   ├── EnvironmentalImpactGrid.tsx
│   │   └── EcoEfficiencyComparison.tsx
│   ├── process/
│   │   ├── ProcessConfigurationForm.tsx
│   │   └── EquipmentSelectionGrid.tsx
│   ├── shared/
│   │   ├── DataTable.tsx
│   │   ├── LoadingStates.tsx
│   │   └── ErrorBoundary.tsx
│   └── ui/
├── lib/
│   ├── api/
│   │   ├── auth.ts
│   │   ├── process.ts
│   │   ├── equipment.ts
│   │   └── analysis.ts
│   └── utils/
└── types/
    ├── process.ts
    ├── analysis.ts
    └── api.ts
```

## 3. Data Flow Architecture

### 3.1 API Integration Layer
```typescript
interface AnalysisService {
  technicalAnalysis: (processId: string) => Promise<TechnicalAnalysisResult>;
  economicAnalysis: (processId: string) => Promise<EconomicAnalysisResult>;
  environmentalAnalysis: (processId: string) => Promise<EnvironmentalAnalysisResult>;
  ecoEfficiencyAnalysis: (processId: string) => Promise<EcoEfficiencyResult>;
}
```

### 3.2 State Management
- React Query for server state
- Context API for application state
- Local state for form management

## 4. Key Components

### 4.1 Process Configuration
```typescript
interface ProcessConfig {
  processType: 'Baseline' | 'RF' | 'IR';
  inputMass: number;
  proteinContent: number;
  equipmentIds: string[];
  operatingParameters: {
    temperature: number;
    pressure: number;
    duration: number;
  };
}
```

### 4.2 Analysis Dashboards
- Technical Analysis Dashboard
  - Protein recovery trends
  - Separation efficiency metrics
  - Particle size distribution
- Economic Analysis Dashboard
  - CAPEX/OPEX breakdown
  - NPV/ROI calculations
  - Profitability indicators
- Environmental Analysis Dashboard
  - Impact assessment visualizations
  - Resource consumption metrics
  - Allocation analysis
- Eco-efficiency Dashboard
  - Comparative analysis
  - Trade-off visualizations
  - Process optimization recommendations

## 5. Authentication & Authorization

### 5.1 Integration with Django Auth
```typescript
interface AuthService {
  login: (credentials: LoginCredentials) => Promise<AuthResponse>;
  register: (userData: RegistrationData) => Promise<AuthResponse>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<string>;
}
```

## 6. Real-time Updates

### 6.1 WebSocket Integration
- Real-time process monitoring
- Live analysis updates
- Status notifications

### 6.2 Polling Strategy
- Fallback for WebSocket failures
- Configurable polling intervals
- Optimistic updates

## 7. Error Handling & Loading States

### 7.1 Global Error Boundary
- Graceful error recovery
- User-friendly error messages
- Retry mechanisms

### 7.2 Loading States
- Skeleton loaders
- Progress indicators
- Cancelable operations

## 8. Development Phases

### Phase 1: Core Infrastructure
- Setup Next.js project with TypeScript
- Implement authentication flow
- Create base components
- Setup API integration layer

### Phase 2: Process Management
- Process configuration forms
- Equipment management interface
- Basic analysis visualization

### Phase 3: Analysis Features
- Technical analysis dashboard
- Economic analysis interface
- Environmental impact visualization
- Eco-efficiency comparisons

### Phase 4: Advanced Features
- Real-time updates
- Export functionality
- Advanced visualizations
- Process optimization recommendations

## 9. Testing Strategy

### 9.1 Unit Tests
- Component testing with React Testing Library
- API integration tests
- Utility function tests

### 9.2 Integration Tests
- User flow testing
- API interaction testing
- State management testing

### 9.3 E2E Tests
- Critical path testing with Cypress
- Authentication flow testing
- Analysis workflow testing
