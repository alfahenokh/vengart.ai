# Design Document: Verdant AI Integrated Dashboard

## Overview

The Verdant AI Integrated Dashboard is a comprehensive Single Page Application (SPA) that unifies four existing HTML components into a cohesive platform for spatial-temporal waste management intelligence. The system leverages modern web technologies, AI/ML capabilities, and real-time data processing to provide an innovative solution for waste management optimization.

The platform integrates:
- **Master Dashboard**: Global operations control center
- **Analytics & Reports**: Data visualization and reporting module  
- **Operational Simulator**: Interactive simulation with maps
- **Resource Manager**: Fleet and personnel management system

The design philosophy follows the existing Obsidian Moss theme, emphasizing "Quiet Luxury" for technical environments with a sophisticated, calm interface that prioritizes cognitive clarity over hyper-stimulated aesthetics.

## Architecture

### System Architecture Pattern
The system follows a **Modular Monolith** architecture pattern, structured as a Single Page Application with clear module boundaries. This approach provides the benefits of modularity while maintaining deployment simplicity and data consistency.

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (SPA)                           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │   Master    │ │ Analytics & │ │ Operational │ │Resource │ │
│  │ Dashboard   │ │  Reports    │ │ Simulator   │ │Manager  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
├─────────────────────────────────────────────────────────────┤
│                 Shared Services Layer                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │    Auth     │ │   State     │ │   Theme     │ │   API   │ │
│  │  Service    │ │ Management  │ │  Service    │ │ Client  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend Services                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │   REST API  │ │  WebSocket  │ │   AI/ML     │ │  Auth   │ │
│  │   Gateway   │ │   Service   │ │  Service    │ │Service  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
├─────────────────────────────────────────────────────────────┤
│                   Data Layer                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │ PostgreSQL  │ │    Redis    │ │   File      │ │External │ │
│  │  Database   │ │   Cache     │ │  Storage    │ │   APIs  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Frontend:**
- **Framework**: React.js 18+ with TypeScript
- **State Management**: Zustand for lightweight state management
- **Routing**: React Router v6 for SPA navigation
- **Styling**: Tailwind CSS with custom Obsidian Moss theme
- **Charts**: Chart.js with react-chartjs-2 for data visualization
- **Maps**: Leaflet.js for interactive mapping
- **Real-time**: Socket.IO client for WebSocket connections

**Backend:**
- **API Framework**: FastAPI (Python) for high-performance REST APIs
- **WebSocket**: FastAPI WebSocket support for real-time features
- **Authentication**: JWT with refresh tokens
- **AI/ML Integration**: OpenAI API and Hugging Face Transformers
- **Task Queue**: Celery with Redis for background processing

**Database & Storage:**
- **Primary Database**: PostgreSQL 15+ for relational data
- **Cache**: Redis for session storage and caching
- **File Storage**: MinIO (S3-compatible) for file uploads
- **Search**: PostgreSQL full-text search with GIN indexes

**Infrastructure:**
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose for development, Kubernetes for production
- **Reverse Proxy**: Nginx for load balancing and SSL termination
- **Monitoring**: Prometheus + Grafana for metrics and monitoring

## Components and Interfaces

### Frontend Component Architecture

```typescript
// Core Application Structure
src/
├── components/
│   ├── shared/           // Shared UI components
│   │   ├── Navigation/
│   │   ├── Layout/
│   │   └── Theme/
│   ├── dashboard/        // Master Dashboard components
│   ├── analytics/        // Analytics & Reports components
│   ├── simulator/        // Operational Simulator components
│   └── resources/        // Resource Manager components
├── services/
│   ├── api/             // API client services
│   ├── auth/            // Authentication services
│   ├── websocket/       // Real-time services
│   └── ai/              // AI/ML integration services
├── stores/              // Zustand state stores
├── hooks/               // Custom React hooks
├── utils/               // Utility functions
└── types/               // TypeScript type definitions
```

### Shared Component Library

**Navigation Component:**
```typescript
interface NavigationProps {
  currentModule: 'dashboard' | 'analytics' | 'simulator' | 'resources';
  user: User;
  onModuleChange: (module: string) => void;
}

const Navigation: React.FC<NavigationProps> = ({
  currentModule,
  user,
  onModuleChange
}) => {
  // Unified navigation bar with module switching
  // Maintains Obsidian Moss theme consistency
  // Includes user profile and system notifications
};
```

**Theme Provider:**
```typescript
interface ThemeContextValue {
  theme: ObsidianMossTheme;
  toggleDarkMode: () => void;
  updateThemeColors: (colors: Partial<ThemeColors>) => void;
}

const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  // Provides consistent Obsidian Moss theme across all modules
  // Supports dynamic theme customization
  // Manages responsive design breakpoints
};
```

### Module-Specific Components

**Master Dashboard Module:**
- `SystemOverview`: Global operations metrics
- `NetworkStatus`: Real-time network throughput visualization
- `NodePerformance`: Temporal node performance table
- `MaterialDistribution`: Resource allocation charts

**Analytics Module:**
- `KPICards`: Key performance indicator summaries
- `ForecastChart`: Waste volume prediction visualization
- `EfficiencyGains`: Performance improvement metrics
- `RegionalDistribution`: Geographic data analysis

**Simulator Module:**
- `InteractiveMap`: Leaflet-based mapping interface
- `ParameterControls`: Simulation configuration panel
- `SimulationLog`: Real-time execution logging
- `RouteVisualization`: Optimized path display

**Resource Manager Module:**
- `FleetStatusTable`: Real-time fleet tracking
- `PersonnelRoster`: Staff management interface
- `ShiftScheduler`: Personnel scheduling system
- `MaintenanceTracker`: Fleet maintenance management

### API Interface Design

**RESTful API Endpoints:**

```python
# Authentication
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout

# Dashboard Data
GET /api/v1/dashboard/overview
GET /api/v1/dashboard/network-status
GET /api/v1/dashboard/nodes

# Analytics
GET /api/v1/analytics/kpis
GET /api/v1/analytics/forecast
POST /api/v1/analytics/reports/generate
GET /api/v1/analytics/reports/{report_id}

# Simulation
POST /api/v1/simulation/scenarios
GET /api/v1/simulation/scenarios/{scenario_id}
POST /api/v1/simulation/execute
GET /api/v1/simulation/results/{execution_id}

# Resources
GET /api/v1/resources/fleet
PUT /api/v1/resources/fleet/{unit_id}
GET /api/v1/resources/personnel
POST /api/v1/resources/shifts

# AI/ML Services
POST /api/v1/ai/predict/waste-volume
POST /api/v1/ai/optimize/routes
POST /api/v1/ai/query/natural-language
```

**WebSocket Events:**

```typescript
// Real-time event types
interface WebSocketEvents {
  // Fleet updates
  'fleet:status_update': FleetStatusUpdate;
  'fleet:location_update': FleetLocationUpdate;
  
  // Analytics updates
  'analytics:kpi_update': KPIUpdate;
  'analytics:forecast_update': ForecastUpdate;
  
  // Simulation events
  'simulation:progress': SimulationProgress;
  'simulation:complete': SimulationResult;
  
  // System events
  'system:alert': SystemAlert;
  'system:maintenance': MaintenanceNotification;
}
```

## Data Models

### Core Entity Models

**User Management:**
```typescript
interface User {
  id: string;
  username: string;
  email: string;
  role: 'admin' | 'operator' | 'analyst' | 'viewer';
  permissions: Permission[];
  profile: UserProfile;
  createdAt: Date;
  lastLoginAt: Date;
}

interface UserProfile {
  firstName: string;
  lastName: string;
  department: string;
  preferences: UserPreferences;
}
```

**Fleet Management:**
```typescript
interface FleetUnit {
  id: string;
  identifier: string; // e.g., "UX-9012A"
  type: 'collection' | 'transport' | 'processing';
  status: 'active' | 'idle' | 'maintenance' | 'offline';
  location: GeoLocation;
  capacity: {
    current: number;
    maximum: number;
    unit: 'tons' | 'cubic_meters';
  };
  lastUpdate: Date;
  assignedRoute?: Route;
}

interface GeoLocation {
  latitude: number;
  longitude: number;
  address?: string;
  zone?: string;
}
```

**Analytics Data:**
```typescript
interface WasteForecast {
  id: string;
  region: string;
  timeframe: DateRange;
  predictions: ForecastPoint[];
  accuracy: number;
  modelVersion: string;
  generatedAt: Date;
}

interface ForecastPoint {
  date: Date;
  predictedVolume: number;
  confidence: number;
  factors: PredictionFactor[];
}

interface KPIMetric {
  id: string;
  name: string;
  value: number;
  unit: string;
  trend: 'up' | 'down' | 'stable';
  changePercent: number;
  target?: number;
  updatedAt: Date;
}
```

**Simulation Models:**
```typescript
interface SimulationScenario {
  id: string;
  name: string;
  description: string;
  parameters: SimulationParameters;
  createdBy: string;
  createdAt: Date;
  lastExecuted?: Date;
}

interface SimulationParameters {
  operationalMode: 'efficiency' | 'carbon_neutral' | 'cost_reduction';
  spatialRadius: number; // kilometers
  fleetCapacityLoad: number; // percentage
  timeHorizon: number; // hours
  constraints: SimulationConstraint[];
}

interface SimulationResult {
  id: string;
  scenarioId: string;
  executionTime: number; // milliseconds
  results: {
    efficiency: number;
    costSavings: number;
    carbonReduction: number;
    routeOptimization: RouteOptimization[];
  };
  logs: SimulationLogEntry[];
  completedAt: Date;
}
```

### Database Schema Design

**PostgreSQL Tables:**

```sql
-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP
);

-- Fleet Management
CREATE TABLE fleet_units (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identifier VARCHAR(20) UNIQUE NOT NULL,
    type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    current_capacity DECIMAL(10, 2),
    maximum_capacity DECIMAL(10, 2),
    capacity_unit VARCHAR(20),
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics Data
CREATE TABLE waste_forecasts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    predictions JSONB NOT NULL,
    accuracy DECIMAL(5, 2),
    model_version VARCHAR(50),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Simulation Data
CREATE TABLE simulation_scenarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    parameters JSONB NOT NULL,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_fleet_units_status ON fleet_units(status);
CREATE INDEX idx_fleet_units_location ON fleet_units USING GIST(point(longitude, latitude));
CREATE INDEX idx_waste_forecasts_region_date ON waste_forecasts(region, start_date, end_date);
CREATE INDEX idx_simulation_scenarios_created_by ON simulation_scenarios(created_by);
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Module Integration and Navigation

*For any* sequence of module navigation operations, the system SHALL maintain consistent state and functionality across all integrated modules without page reloads.

**Validates: Requirements 1.1, 1.2, 1.5**

### Property 2: Theme Consistency

*For any* module or device configuration, the system SHALL maintain consistent Obsidian Moss theme styling and responsive behavior across all screen sizes from 320px to 1920px.

**Validates: Requirements 1.3, 9.1, 9.2, 9.4**

### Property 3: Authentication and Authorization

*For any* user credentials and role combination, the authentication system SHALL provide appropriate access control, session management, and error handling according to the user's permissions.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4**

### Property 4: API Performance and Reliability

*For any* valid API request, the backend SHALL respond within specified time limits (200ms for standard operations) with proper HTTP status codes and data validation.

**Validates: Requirements 3.1, 3.3, 3.4, 3.5**

### Property 5: Real-time Data Synchronization

*For any* operational data change, the WebSocket service SHALL broadcast updates to all connected clients within 100ms and maintain connection resilience with automatic reconnection.

**Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5**

### Property 6: AI/ML Service Performance

*For any* prediction or optimization request, the AI/ML service SHALL provide responses within specified time limits (2 seconds for predictions, 5 seconds for route optimization) while maintaining accuracy requirements.

**Validates: Requirements 5.2, 5.3, 5.4, 5.6, 14.3**

### Property 7: Analytics and Reporting Functionality

*For any* data set and export format, the analytics module SHALL generate interactive visualizations, support data export in multiple formats, and complete report processing within 10 seconds.

**Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5, 6.6**

### Property 8: Simulation Execution and Visualization

*For any* simulation scenario and parameter configuration, the simulator SHALL execute within 30 seconds, provide interactive map visualization, and maintain detailed execution logging.

**Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5, 7.6**

### Property 9: Resource Management Operations

*For any* fleet or personnel management operation, the resource manager SHALL track real-time status, manage scheduling, and propagate changes to all related modules correctly.

**Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6**

### Property 10: System Performance and Scalability

*For any* system load up to 100 concurrent users, the system SHALL maintain response times under 500ms, load initial pages within 3 seconds, and support efficient caching strategies.

**Validates: Requirements 10.1, 10.2, 10.3, 10.4**

### Property 11: Security and Data Protection

*For any* data transmission or storage operation, the system SHALL implement HTTPS/TLS 1.3 encryption, input validation, rate limiting, and audit logging to prevent security vulnerabilities.

**Validates: Requirements 11.1, 11.2, 11.3, 11.4, 11.5**

### Property 12: Deployment and Configuration Management

*For any* deployment environment, the system SHALL support containerized deployment, environment-specific configuration, health monitoring, and automated database migrations.

**Validates: Requirements 12.1, 12.2, 12.3, 12.4, 12.5**

### Property 13: Spatial-Temporal Intelligence Features

*For any* spatial-temporal data scenario, the system SHALL implement unique intelligence features that demonstrate innovative problem-solving approaches for waste management optimization.

**Validates: Requirements 14.1, 14.4**

## Error Handling

### Frontend Error Handling Strategy

**Error Boundary Implementation:**
```typescript
class ModuleErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to monitoring service
    errorReportingService.captureException(error, {
      module: this.props.moduleName,
      errorInfo,
      user: this.props.user
    });
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback 
        error={this.state.error} 
        onRetry={() => this.setState({ hasError: false, error: null })}
      />;
    }
    return this.props.children;
  }
}
```

**API Error Handling:**
```typescript
class APIClient {
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      
      switch (response.status) {
        case 401:
          authService.logout();
          throw new AuthenticationError('Session expired');
        case 403:
          throw new AuthorizationError('Insufficient permissions');
        case 429:
          throw new RateLimitError('Too many requests');
        case 500:
          throw new ServerError('Internal server error');
        default:
          throw new APIError(`Request failed: ${response.status}`, errorData);
      }
    }
    
    return response.json();
  }
}
```

### Backend Error Handling

**FastAPI Exception Handlers:**
```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": exc.errors(),
            "request_id": request.state.request_id
        }
    )

@app.exception_handler(DatabaseError)
async def database_exception_handler(request: Request, exc: DatabaseError):
    logger.error(f"Database error: {exc}", extra={"request_id": request.state.request_id})
    return JSONResponse(
        status_code=500,
        content={
            "error": "Database Error",
            "message": "An internal error occurred",
            "request_id": request.state.request_id
        }
    )
```

**AI/ML Service Error Handling:**
```python
class AIServiceError(Exception):
    """Base exception for AI service errors"""
    pass

class PredictionTimeoutError(AIServiceError):
    """Raised when AI prediction exceeds timeout"""
    pass

class ModelUnavailableError(AIServiceError):
    """Raised when AI model is not available"""
    pass

async def handle_ai_prediction(request: PredictionRequest) -> PredictionResponse:
    try:
        async with asyncio.timeout(2.0):  # 2 second timeout
            result = await ai_service.predict(request)
            return result
    except asyncio.TimeoutError:
        raise PredictionTimeoutError("Prediction request timed out")
    except ModelNotFoundError:
        raise ModelUnavailableError("AI model is currently unavailable")
```

### Error Recovery Strategies

**Graceful Degradation:**
- When AI services are unavailable, fall back to cached predictions
- When real-time updates fail, display last known data with timestamp
- When map services are down, provide tabular data alternatives

**Retry Mechanisms:**
- Exponential backoff for API requests
- Circuit breaker pattern for external services
- Queue failed operations for retry when services recover

**User Experience:**
- Clear error messages with actionable guidance
- Offline mode for critical functions
- Progress indicators for long-running operations

## Testing Strategy

### Dual Testing Approach

The testing strategy employs both **unit tests** for specific examples and edge cases, and **property-based tests** for universal properties across all inputs. This comprehensive approach ensures both concrete bug detection and general correctness verification.

### Property-Based Testing Implementation

**Framework Selection:**
- **Frontend**: fast-check for TypeScript/JavaScript property-based testing
- **Backend**: Hypothesis for Python property-based testing
- **Integration**: Custom property generators for end-to-end scenarios

**Property Test Configuration:**
- Minimum 100 iterations per property test
- Each property test references its design document property
- Tag format: **Feature: verdant-ai-integrated-dashboard, Property {number}: {property_text}**

**Example Property Test Implementation:**

```typescript
// Frontend Property Test Example
import fc from 'fast-check';
import { render, screen } from '@testing-library/react';
import { Navigation } from '../components/Navigation';

describe('Property 2: Theme Consistency', () => {
  it('maintains Obsidian Moss theme across all screen sizes', () => {
    // Feature: verdant-ai-integrated-dashboard, Property 2: Theme Consistency
    fc.assert(fc.property(
      fc.record({
        width: fc.integer({ min: 320, max: 1920 }),
        height: fc.integer({ min: 568, max: 1080 }),
        module: fc.constantFrom('dashboard', 'analytics', 'simulator', 'resources')
      }),
      ({ width, height, module }) => {
        // Set viewport size
        Object.defineProperty(window, 'innerWidth', { value: width });
        Object.defineProperty(window, 'innerHeight', { value: height });
        
        const { container } = render(
          <ThemeProvider>
            <Navigation currentModule={module} />
          </ThemeProvider>
        );
        
        // Verify theme colors are applied
        const nav = container.querySelector('nav');
        const computedStyle = window.getComputedStyle(nav);
        
        expect(computedStyle.backgroundColor).toBe('rgb(16, 20, 22)'); // surface color
        expect(computedStyle.borderColor).toBe('rgb(68, 72, 66)'); // outline-variant
      }
    ), { numRuns: 100 });
  });
});
```

```python
# Backend Property Test Example
from hypothesis import given, strategies as st
import pytest
from fastapi.testclient import TestClient

class TestAPIPerformance:
    @given(
        endpoint=st.sampled_from([
            '/api/v1/dashboard/overview',
            '/api/v1/analytics/kpis',
            '/api/v1/resources/fleet'
        ]),
        params=st.dictionaries(
            st.text(min_size=1, max_size=20),
            st.one_of(st.text(), st.integers(), st.booleans()),
            max_size=5
        )
    )
    def test_api_response_time_property(self, client: TestClient, endpoint: str, params: dict):
        """
        Feature: verdant-ai-integrated-dashboard, Property 4: API Performance and Reliability
        For any valid API request, the backend SHALL respond within 200ms
        """
        import time
        
        start_time = time.time()
        response = client.get(endpoint, params=params)
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        # Verify response time requirement
        assert response_time_ms < 200, f"Response time {response_time_ms}ms exceeds 200ms limit"
        
        # Verify proper HTTP status codes
        assert response.status_code in [200, 400, 401, 403, 422], f"Unexpected status code: {response.status_code}"
```

### Unit Testing Strategy

**Frontend Unit Tests:**
- Component rendering and interaction testing with React Testing Library
- State management testing with Zustand stores
- API client testing with MSW (Mock Service Worker)
- Custom hook testing with React Hooks Testing Library

**Backend Unit Tests:**
- FastAPI endpoint testing with TestClient
- Database operation testing with pytest fixtures
- AI/ML service mocking and integration testing
- WebSocket connection testing

**Integration Testing:**
- End-to-end user workflows with Playwright
- Database migration testing
- Docker container deployment testing
- Performance testing under load

### Test Coverage Requirements

- **Unit Test Coverage**: Minimum 80% code coverage
- **Property Test Coverage**: All 13 correctness properties must have corresponding property tests
- **Integration Test Coverage**: All critical user journeys must be covered
- **Performance Test Coverage**: All performance requirements must be validated

### Continuous Testing Pipeline

```yaml
# GitHub Actions CI/CD Pipeline
name: Verdant AI Testing Pipeline

on: [push, pull_request]

jobs:
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run test:unit
      - run: npm run test:property
      - run: npm run test:e2e

  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements-test.txt
      - run: pytest tests/unit/
      - run: pytest tests/property/
      - run: pytest tests/integration/

  performance-tests:
    runs-on: ubuntu-latest
    needs: [frontend-tests, backend-tests]
    steps:
      - uses: actions/checkout@v3
      - run: docker-compose up -d
      - run: npm run test:performance
      - run: python scripts/load_test.py
```

This comprehensive testing strategy ensures that the Verdant AI Integrated Dashboard meets all functional requirements, performance criteria, and maintains high code quality throughout development and deployment.