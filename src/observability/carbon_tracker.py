"""
Carbon tracking using CodeCarbon
"""

import os
from typing import Dict, Optional
from codecarbon import EmissionsTracker
from datetime import datetime


class CarbonTracker:
    """Tracks carbon emissions for AI workloads using CodeCarbon"""
    
    def __init__(self, output_dir: str = "./carbon_data"):
        """
        Initialize carbon tracker
        
        Args:
            output_dir: Directory to store emission data
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.active_trackers: Dict[str, EmissionsTracker] = {}
    
    def start_tracking(self, workload_id: str, project_name: Optional[str] = None) -> None:
        """
        Start tracking emissions for a workload
        
        Args:
            workload_id: Unique identifier for the workload
            project_name: Optional project name for organization
        """
        if workload_id in self.active_trackers:
            raise ValueError(f"Tracking already active for workload: {workload_id}")
        
        tracker = EmissionsTracker(
            project_name=project_name or workload_id,
            output_dir=self.output_dir,
            log_level="error"  # Reduce verbosity
        )
        
        tracker.start()
        self.active_trackers[workload_id] = tracker
    
    def stop_tracking(self, workload_id: str) -> Dict:
        """
        Stop tracking and return emission data
        
        Args:
            workload_id: Unique identifier for the workload
            
        Returns:
            Dictionary with emission metrics
        """
        if workload_id not in self.active_trackers:
            raise ValueError(f"No active tracking for workload: {workload_id}")
        
        tracker = self.active_trackers[workload_id]
        emissions_data = tracker.stop()
        
        # Extract key metrics
        result = {
            "workload_id": workload_id,
            "timestamp": datetime.now().isoformat(),
            "emissions_kg": emissions_data.get("emissions", 0),
            "energy_consumed_kwh": emissions_data.get("energy_consumed", 0),
            "duration_seconds": emissions_data.get("duration", 0),
            "cpu_power_watts": emissions_data.get("cpu_power", 0),
            "gpu_power_watts": emissions_data.get("gpu_power", 0),
            "ram_power_watts": emissions_data.get("ram_power", 0),
            "country_iso_code": emissions_data.get("country_iso_code", "Unknown"),
            "region": emissions_data.get("region", "Unknown")
        }
        
        del self.active_trackers[workload_id]
        return result
    
    def get_current_emissions(self, workload_id: str) -> Optional[Dict]:
        """
        Get current emission estimate without stopping tracking
        
        Args:
            workload_id: Unique identifier for the workload
            
        Returns:
            Current emission estimate or None if not tracking
        """
        if workload_id not in self.active_trackers:
            return None
        
        tracker = self.active_trackers[workload_id]
        # CodeCarbon doesn't provide real-time estimates easily
        # This is a placeholder for future enhancement
        return {
            "workload_id": workload_id,
            "status": "tracking_active",
            "note": "Real-time estimates require stopping tracker"
        }
    
    def estimate_emissions(self, 
                          duration_seconds: float,
                          cpu_power_watts: float = 0,
                          gpu_power_watts: float = 0,
                          ram_power_watts: float = 0,
                          carbon_intensity_g_per_kwh: float = 500) -> Dict:
        """
        Estimate emissions for a workload without running it
        
        Args:
            duration_seconds: Expected runtime in seconds
            cpu_power_watts: CPU power consumption
            gpu_power_watts: GPU power consumption
            ram_power_watts: RAM power consumption
            carbon_intensity_g_per_kwh: Grid carbon intensity (g CO₂/kWh)
            
        Returns:
            Estimated emission metrics
        """
        total_power_watts = cpu_power_watts + gpu_power_watts + ram_power_watts
        energy_kwh = (total_power_watts * duration_seconds) / (1000 * 3600)
        emissions_kg = (energy_kwh * carbon_intensity_g_per_kwh) / 1000
        
        return {
            "estimated_emissions_kg": emissions_kg,
            "estimated_energy_kwh": energy_kwh,
            "duration_seconds": duration_seconds,
            "total_power_watts": total_power_watts,
            "carbon_intensity_g_per_kwh": carbon_intensity_g_per_kwh
        }

