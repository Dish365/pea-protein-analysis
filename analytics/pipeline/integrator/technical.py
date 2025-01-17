from typing import Dict, List, Optional, Any
import ctypes
import httpx
import asyncio
from pathlib import Path

from analytics.protein_analysis.recovery import ProteinRecoveryCalculator
from analytics.protein_analysis.separation import SeparationEfficiencyAnalyzer
from analytics.protein_analysis.particle_size import ParticleSizeAnalyzer

class TechnicalIntegrator:
    """Integrates technical analysis components with FastAPI and Rust"""
    
    def __init__(self):
        # Initialize service components
        self.recovery_calculator = ProteinRecoveryCalculator(initial_protein_content=100.0)
        self.separation_analyzer = SeparationEfficiencyAnalyzer()
        self.particle_analyzer = ParticleSizeAnalyzer()
        
        # Initialize FastAPI client
        self.client = httpx.AsyncClient()
        self.api_base_url = "http://localhost:8000/process/technical"
        
        # Load Rust library
        lib_path = (
            Path(__file__).parent.parent.parent.parent
            / "backend/rust_modules/target/release/libprotein_analysis.so"
        )
        self.lib = ctypes.CDLL(str(lib_path))
        self._configure_rust_functions()

    def _configure_rust_functions(self) -> None:
        """Configure Rust function signatures"""
        # Protein recovery calculation
        self.lib.calculate_protein_recovery.argtypes = [
            ctypes.c_double,  # protein_yield
            ctypes.c_double,  # protein_content
            ctypes.c_double,  # separation_efficiency
        ]
        self.lib.calculate_protein_recovery.restype = ctypes.c_double

        # Particle distribution analysis
        self.lib.analyze_particle_distribution.argtypes = [
            ctypes.POINTER(ctypes.c_double),  # particles
            ctypes.c_size_t,  # len
            ctypes.POINTER(ctypes.c_double),  # d10
            ctypes.POINTER(ctypes.c_double),  # d50
            ctypes.POINTER(ctypes.c_double),  # d90
        ]

    async def analyze_technical(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate complete technical analysis"""
        try:
            # Calculate protein recovery
            recovery_results = await self.analyze_protein_recovery(process_data)
            
            # Calculate separation efficiency
            separation_results = await self.analyze_separation_efficiency(process_data)
            
            # Analyze particle size distribution
            particle_results = await self.analyze_particle_size(process_data)
            
            # Combine results
            return {
                'protein_recovery': recovery_results,
                'separation_efficiency': separation_results,
                'particle_analysis': particle_results
            }
            
        except Exception as e:
            raise RuntimeError(f"Technical analysis failed: {str(e)}")

    async def analyze_protein_recovery(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate protein recovery using FastAPI endpoint and Rust"""
        try:
            response = await self.client.post(
                f"{self.api_base_url}/protein-recovery/",
                json={
                    'initial_protein_content': process_data.get('initial_protein_content'),
                    'output_mass': process_data.get('output_mass'),
                    'input_mass': process_data.get('input_mass'),
                    'output_protein_content': process_data.get('output_protein_content')
                }
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Protein recovery API call failed: {response.text}")
                
            # Enhance results with Rust calculation
            recovery = self.lib.calculate_protein_recovery(
                ctypes.c_double(process_data.get('protein_yield', 0.0)),
                ctypes.c_double(process_data.get('protein_content', 0.0)),
                ctypes.c_double(process_data.get('separation_efficiency', 0.0))
            )
            
            results = response.json()
            results['rust_calculated_recovery'] = recovery
            return results
            
        except Exception as e:
            raise RuntimeError(f"Protein recovery analysis failed: {str(e)}")

    async def analyze_separation_efficiency(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate separation efficiency using FastAPI endpoint"""
        try:
            response = await self.client.post(
                f"{self.api_base_url}/separation-efficiency/",
                json={
                    'feed_composition': process_data.get('feed_composition', {}),
                    'product_composition': process_data.get('product_composition', {}),
                    'mass_flow': process_data.get('mass_flow', {}),
                    'process_data': process_data.get('process_data', []),
                    'target_purity': process_data.get('target_purity', 0.0)
                }
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Separation efficiency API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            raise RuntimeError(f"Separation efficiency analysis failed: {str(e)}")

    async def analyze_particle_size(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Analyze particle size distribution using FastAPI endpoint and Rust"""
        try:
            # Get particle data
            particles = process_data.get('particle_sizes', [])
            if not particles:
                raise ValueError("No particle size data provided")
                
            # Call FastAPI endpoint
            response = await self.client.post(
                f"{self.api_base_url}/particle-size/",
                json={
                    'particle_sizes': particles,
                    'weights': process_data.get('weights'),
                    'target_ranges': process_data.get('target_ranges'),
                    'density': process_data.get('density')
                }
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Particle size API call failed: {response.text}")
                
            # Enhance with Rust calculation
            results = response.json()
            rust_results = self._calculate_particle_distribution(particles)
            results.update(rust_results)
            
            return results
            
        except Exception as e:
            raise RuntimeError(f"Particle size analysis failed: {str(e)}")

    def _calculate_particle_distribution(self, particles: List[float]) -> Dict[str, float]:
        """Calculate particle distribution using Rust"""
        arr = (ctypes.c_double * len(particles))(*particles)
        d10 = ctypes.c_double()
        d50 = ctypes.c_double()
        d90 = ctypes.c_double()

        self.lib.analyze_particle_distribution(
            arr, 
            len(particles),
            ctypes.byref(d10),
            ctypes.byref(d50),
            ctypes.byref(d90)
        )

        return {
            "rust_d10": d10.value,
            "rust_d50": d50.value,
            "rust_d90": d90.value,
            "rust_distribution_width": (d90.value - d10.value) / d50.value
        }
