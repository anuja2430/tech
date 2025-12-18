"""
Execution context management for AI workloads
"""

from typing import Dict, Optional, Literal
from dataclasses import dataclass, asdict
from enum import Enum


class CriticalityLevel(str, Enum):
    """Business criticality levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    DEFERRABLE = "deferrable"


class UrgencyLevel(str, Enum):
    """Execution urgency levels"""
    REAL_TIME = "real_time"
    URGENT = "urgent"
    NORMAL = "normal"
    BATCH = "batch"
    DEFERRABLE = "deferrable"


@dataclass
class WorkloadContext:
    """Context information for an AI workload"""
    
    workload_id: str
    model_name: str
    description: str
    
    # Business context
    criticality: CriticalityLevel
    urgency: UrgencyLevel
    
    # SLA requirements
    sla_window_hours: float  # Acceptable delay window
    required_frequency_hours: float  # Minimum required frequency
    
    # Current execution pattern
    current_frequency_hours: float  # Current actual frequency
    current_schedule: str  # e.g., "every_1_hour", "daily_at_2pm"
    
    # Resource requirements
    estimated_duration_seconds: float
    cpu_cores: int = 1
    gpu_required: bool = False
    memory_gb: float = 4.0
    
    # Additional metadata
    metadata: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        result = asdict(self)
        result['criticality'] = self.criticality.value
        result['urgency'] = self.urgency.value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'WorkloadContext':
        """Create from dictionary"""
        data = data.copy()
        data['criticality'] = CriticalityLevel(data['criticality'])
        data['urgency'] = UrgencyLevel(data['urgency'])
        return cls(**data)
    
    def is_over_serving(self) -> bool:
        """
        Check if current frequency exceeds required frequency
        
        Returns:
            True if running more frequently than required
        """
        return self.current_frequency_hours < self.required_frequency_hours
    
    def get_frequency_ratio(self) -> float:
        """
        Get ratio of current to required frequency
        
        Returns:
            Ratio (values > 1 indicate over-serving)
        """
        if self.required_frequency_hours == 0:
            return float('inf')
        return self.required_frequency_hours / self.current_frequency_hours


class ExecutionContext:
    """Manages execution context for multiple workloads"""
    
    def __init__(self):
        """Initialize context manager"""
        self.workloads: Dict[str, WorkloadContext] = {}
    
    def register_workload(self, context: WorkloadContext) -> None:
        """
        Register a workload context
        
        Args:
            context: Workload context to register
        """
        self.workloads[context.workload_id] = context
    
    def get_workload(self, workload_id: str) -> Optional[WorkloadContext]:
        """
        Get workload context
        
        Args:
            workload_id: Unique identifier for the workload
            
        Returns:
            Workload context or None if not found
        """
        return self.workloads.get(workload_id)
    
    def list_workloads(self) -> list[str]:
        """
        List all registered workload IDs
        
        Returns:
            List of workload IDs
        """
        return list(self.workloads.keys())
    
    def get_workloads_by_criticality(self, criticality: CriticalityLevel) -> list[WorkloadContext]:
        """
        Get workloads filtered by criticality
        
        Args:
            criticality: Criticality level to filter by
            
        Returns:
            List of matching workload contexts
        """
        return [w for w in self.workloads.values() if w.criticality == criticality]
    
    def get_optimization_candidates(self) -> list[WorkloadContext]:
        """
        Get workloads that may be over-serving their requirements
        
        Returns:
            List of workloads that are candidates for optimization
        """
        candidates = []
        for workload in self.workloads.values():
            if (workload.is_over_serving() and 
                workload.criticality != CriticalityLevel.CRITICAL and
                workload.urgency != UrgencyLevel.REAL_TIME):
                candidates.append(workload)
        return candidates

