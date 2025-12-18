"""
Basic Carbon-Aware Agent - Simplified Version
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Workload:
    """Basic workload definition"""
    name: str
    current_frequency_hours: float  # How often it runs now
    required_frequency_hours: float   # How often it needs to run (SLA)
    emissions_per_run_kg: float      # CO2 per execution


class BasicCarbonAgent:
    """Basic carbon-aware agent with simple reasoning"""
    
    def __init__(self):
        self.workloads = {}
    
    def add_workload(self, workload: Workload):
        """Add a workload to track"""
        self.workloads[workload.name] = workload
    
    def analyze(self, workload_name: str) -> Dict:
        """Analyze a workload and suggest optimizations"""
        workload = self.workloads.get(workload_name)
        if not workload:
            return {"error": f"Workload {workload_name} not found"}
        
        # Simple check: is it running more often than needed?
        is_over_serving = workload.current_frequency_hours < workload.required_frequency_hours
        
        if is_over_serving:
            # Calculate potential savings
            current_runs_per_day = 24 / workload.current_frequency_hours
            optimal_runs_per_day = 24 / workload.required_frequency_hours
            reduction_per_day = current_runs_per_day - optimal_runs_per_day
            savings_kg_per_day = reduction_per_day * workload.emissions_per_run_kg
            savings_percent = (reduction_per_day / current_runs_per_day) * 100
            
            return {
                "workload": workload_name,
                "status": "optimization_opportunity",
                "current": f"Runs every {workload.current_frequency_hours} hours",
                "recommended": f"Run every {workload.required_frequency_hours} hours",
                "savings_kg_per_day": round(savings_kg_per_day, 4),
                "savings_percent": round(savings_percent, 1),
                "message": f"Running {workload.current_frequency_hours}h but only needs {workload.required_frequency_hours}h. "
                          f"Can reduce emissions by {round(savings_percent, 1)}%"
            }
        else:
            return {
                "workload": workload_name,
                "status": "optimized",
                "message": "Workload frequency aligns with requirements"
            }
    
    def list_workloads(self):
        """List all workloads"""
        return list(self.workloads.keys())

