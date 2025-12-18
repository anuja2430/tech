"""
Metrics collection for workload monitoring
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import os


class MetricsCollector:
    """Collects and stores workload execution metrics"""
    
    def __init__(self, storage_path: str = "./metrics_data"):
        """
        Initialize metrics collector
        
        Args:
            storage_path: Directory to store metrics
        """
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.metrics: Dict[str, List[Dict]] = {}
    
    def record_execution(self, 
                       workload_id: str,
                       emissions_kg: float,
                       duration_seconds: float,
                       energy_kwh: float,
                       metadata: Optional[Dict] = None) -> None:
        """
        Record a workload execution
        
        Args:
            workload_id: Unique identifier for the workload
            emissions_kg: CO₂ emissions in kg
            duration_seconds: Execution duration
            energy_kwh: Energy consumed in kWh
            metadata: Additional metadata
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "emissions_kg": emissions_kg,
            "duration_seconds": duration_seconds,
            "energy_kwh": energy_kwh,
            "metadata": metadata or {}
        }
        
        if workload_id not in self.metrics:
            self.metrics[workload_id] = []
        
        self.metrics[workload_id].append(record)
        
        # Persist to disk
        self._save_metrics(workload_id)
    
    def get_workload_history(self, workload_id: str, days: int = 30) -> List[Dict]:
        """
        Get execution history for a workload
        
        Args:
            workload_id: Unique identifier for the workload
            days: Number of days of history to retrieve
            
        Returns:
            List of execution records
        """
        if workload_id not in self.metrics:
            return []
        
        cutoff_date = datetime.now() - timedelta(days=days)
        history = []
        
        for record in self.metrics[workload_id]:
            record_date = datetime.fromisoformat(record["timestamp"])
            if record_date >= cutoff_date:
                history.append(record)
        
        return sorted(history, key=lambda x: x["timestamp"])
    
    def get_aggregate_stats(self, workload_id: str, days: int = 30) -> Dict:
        """
        Get aggregate statistics for a workload
        
        Args:
            workload_id: Unique identifier for the workload
            days: Number of days to aggregate
            
        Returns:
            Aggregate statistics
        """
        history = self.get_workload_history(workload_id, days)
        
        if not history:
            return {
                "total_executions": 0,
                "total_emissions_kg": 0,
                "total_energy_kwh": 0,
                "avg_emissions_per_run_kg": 0,
                "avg_duration_seconds": 0
            }
        
        total_emissions = sum(r["emissions_kg"] for r in history)
        total_energy = sum(r["energy_kwh"] for r in history)
        avg_duration = sum(r["duration_seconds"] for r in history) / len(history)
        
        return {
            "total_executions": len(history),
            "total_emissions_kg": total_emissions,
            "total_energy_kwh": total_energy,
            "avg_emissions_per_run_kg": total_emissions / len(history),
            "avg_duration_seconds": avg_duration,
            "period_days": days
        }
    
    def _save_metrics(self, workload_id: str) -> None:
        """Save metrics to disk"""
        file_path = os.path.join(self.storage_path, f"{workload_id}_metrics.json")
        with open(file_path, 'w') as f:
            json.dump(self.metrics[workload_id], f, indent=2)
    
    def _load_metrics(self, workload_id: str) -> None:
        """Load metrics from disk"""
        file_path = os.path.join(self.storage_path, f"{workload_id}_metrics.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.metrics[workload_id] = json.load(f)

