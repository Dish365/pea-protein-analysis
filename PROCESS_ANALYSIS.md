# Process Analysis System Documentation

## Overview
The Process Analysis System is designed to analyze different protein extraction processes through various workflow types. The system integrates FastAPI endpoints, Django models, and specialized analysis components to provide comprehensive process analysis.

## Workflow Types
The system supports three main workflow types:

1. **Baseline Process** (`baseline`)
   - Basic air classification process
   - Parameters:
     - Feed rate
     - Air flow rate
     - Classifier speed
     - Process conditions (temperature, humidity, pressure)

2. **RF Treatment** (`rf_treatment`)
   - Radio Frequency treatment process
   - Parameters:
     - RF power
     - Frequency
     - Treatment time
     - Material properties (moisture content, dielectric properties)

3. **IR Treatment** (`ir_treatment`)
   - Infrared treatment process
   - Parameters:
     - Power density
     - Wavelength
     - Treatment time
     - Material properties (surface temperature, moisture content)

## System Components

### 1. API Layer (`pipeline_endpoints.py`)
- Receives analysis requests
- Validates workflow types
- Orchestrates the analysis process
- Returns results to clients

### 2. Workflow Orchestration (`workflow.py`)
- Defines workflow types using `WorkflowType` enum
- Manages workflow execution
- Coordinates between different components
- Handles error cases and retries

### 3. Model Integration (`model_integration.py`)
- Maps workflow types to Django models
- Transforms data between models and analysis format
- Handles data validation and persistence
- Supports:
  - BaselineProcess
  - RFTreatmentProcess
  - IRTreatmentProcess

### 4. Technical Analysis (`technical.py`)
Integrates three main analysis components:
- Protein Recovery Analysis
- Separation Efficiency Analysis
- Particle Size Analysis

### 5. Protein Analysis Components
Core analysis modules that provide fundamental calculations:

#### a. Particle Size Analysis (`particle_size.py`)
- Analyzes particle size distributions
- Calculates:
  - D10, D50, D90 values
  - Distribution statistics
  - Surface area calculations
- Used across all workflow types

#### b. Protein Recovery (`recovery.py`)
- Calculates:
  - Recovery rates
  - Protein loss tracking
  - Concentration factors
  - Theoretical/practical yield estimation

#### c. Separation Efficiency (`separation.py`)
- Analyzes:
  - Component separation factors
  - Protein enrichment
  - Process efficiency
  - Multi-stage separation performance

## Process Flow

1. **Request Reception**
   ```
   Client Request → FastAPI Endpoint → Workflow Validation
   ```

2. **Workflow Processing**
   ```
   Workflow Orchestrator → Model Integration → Technical Analysis
   ```

3. **Analysis Execution**
   ```
   Technical Analysis → Protein Analysis Components → Results Collection
   ```

4. **Results Processing**
   ```
   Results Collection → Model Transformation → Response Formation
   ```

## Data Flow Example

### Baseline Workflow
1. Client submits analysis request:
   ```json
   {
     "workflow_type": "baseline",
     "process_id": "test_001",
     "analysis_type": "technical",
     "input_data": {
       "technical": {
         "process_parameters": {
           "feed_rate": 50.0,
           "air_flow_rate": 35.0,
           "classifier_speed": 3000
         },
         "material_properties": {
           "initial_protein_content": 23.5,
           "initial_moisture": 12.0,
           "particle_size": {
             "d10": 15.0,
             "d50": 45.0,
             "d90": 120.0
           }
         }
       }
     }
   }
   ```

2. System processes the request:
   - Validates workflow type
   - Maps to BaselineProcess model
   - Executes technical analysis
   - Returns comprehensive results

## Error Handling
- Workflow type validation
- Input data validation
- Process parameter validation
- Analysis error handling
- Result validation

## Integration Points
1. **FastAPI - Django Integration**
   - Shared model definitions
   - Data persistence
   - Process tracking

2. **Analysis Integration**
   - Workflow orchestration
   - Technical analysis
   - Results processing

3. **Model Integration**
   - Data transformation
   - Validation
   - Persistence

## Performance Considerations
- Asynchronous processing
- Efficient data handling
- Modular component design
- Scalable architecture

## Monitoring and Logging
- Workflow execution tracking
- Performance metrics
- Error logging
- Process analytics
