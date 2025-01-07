## 6. API Design and Endpoints

### 6.1 Django APIs
```python
# Authentication & User Management
POST   /api/auth/register/
POST   /api/auth/login/
GET    /api/auth/logout/

# Process Configuration
POST   /api/process/create/
GET    /api/process/{id}/
PUT    /api/process/{id}/
DELETE /api/process/{id}/

# Equipment Management
POST   /api/equipment/create/
GET    /api/equipment/{id}/
PUT    /api/equipment/{id}/settings/
GET    /api/equipment/{id}/efficiency/

# Analysis Results
GET    /api/analysis/technical/{process_id}/
GET    /api/analysis/economic/{process_id}/
GET    /api/analysis/environmental/{process_id}/
GET    /api/analysis/eco-efficiency/{process_id}/
POST   /api/analysis/export/{format}/
```

### 6.2 FastAPI Endpoints
```python
# Technical Analysis
POST   /process/technical/protein-recovery/
POST   /process/technical/separation-efficiency/
POST   /process/technical/particle-size/

# Economic Analysis
POST   /process/economic/capex/
POST   /process/economic/opex/
POST   /process/economic/npv/
POST   /process/economic/roi/
POST   /process/economic/mcsp/
POST   /process/economic/profitability/

# Environmental Analysis
POST   /process/environmental/gwp/
POST   /process/environmental/hct/
POST   /process/environmental/frs/
POST   /process/environmental/water-consumption/
POST   /process/environmental/allocation/

# Eco-efficiency Analysis
POST   /process/eco-efficiency/economic-based/
POST   /process/eco-efficiency/quality-based/
POST   /process/eco-efficiency/relative/

# Simulation
POST   /process/simulation/monte-carlo/
POST   /process/simulation/sensitivity/
```

### 6.3 API Documentation
```python
# Technical Analysis Endpoints
@router.post("/technical/protein-recovery/")
async def calculate_protein_recovery(
    input_data: ProteinRecoveryInput
) -> ProteinRecoveryResult:
    """
    Calculate protein recovery rate and separation efficiency
    
    Parameters:
    - input_mass: float
    - output_mass: float
    - protein_content: float
    - process_type: str (Baseline/RF/IR)
    
    Returns:
    - protein_yield: float
    - protein_purity: float
    - separation_efficiency: float
    - particle_size_distribution: Dict[str, float]
    """

@router.post("/economic/profitability/")
async def analyze_profitability(
    input_data: ProfitabilityInput
) -> ProfitabilityResult:
    """
    Calculate comprehensive economic metrics
    
    Parameters:
    - capex: Dict[str, float]
    - opex: Dict[str, float]
    - production_volume: float
    - project_duration: int
    - discount_rate: float
    
    Returns:
    - npv: float
    - roi: float
    - payback_period: float
    - mcsp: float
    - tor: float
    """

@router.post("/environmental/impact/")
async def calculate_environmental_impact(
    input_data: EnvironmentalInput
) -> EnvironmentalResult:
    """
    Calculate environmental impact metrics
    
    Parameters:
    - energy_consumption: Dict[str, float]
    - water_consumption: float
    - emission_factors: Dict[str, float]
    - allocation_method: str
    
    Returns:
    - gwp: float
    - hct: float
    - frs: float
    - wc: float
    - allocated_impacts: Dict[str, float]
    """

@router.post("/eco-efficiency/indicators/")
async def calculate_eco_efficiency(
    input_data: EcoEfficiencyInput
) -> EcoEfficiencyResult:
    """
    Calculate eco-efficiency indicators
    
    Parameters:
    - economic_values: Dict[str, float]
    - environmental_impacts: Dict[str, float]
    - protein_purity: float
    - process_type: str
    
    Returns:
    - ee_npv: float
    - ee_profit: float
    - ee_quality: float
    - relative_ee: float
    """
```