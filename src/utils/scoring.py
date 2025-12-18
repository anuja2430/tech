"""
Carbon Efficiency Score calculation
"""

from typing import Dict
from src.context.execution_context import WorkloadContext, CriticalityLevel, UrgencyLevel


def calculate_carbon_efficiency_score(
    workload: WorkloadContext,
    emissions_per_run_kg: float,
    optimization_potential: float = 0.0
) -> Dict:
    """
    Calculate Carbon Efficiency Score (CES) for a workload
    
    CES is a relative indicator that helps prioritize optimization opportunities.
    Higher scores indicate better balance of business value to emissions.
    
    Args:
        workload: Workload context
        emissions_per_run_kg: Average emissions per execution in kg CO₂
        optimization_potential: Estimated optimization potential (0-1)
        
    Returns:
        Dictionary with CES score and breakdown
    """
    # Business value component (higher criticality/urgency = higher value)
    criticality_weights = {
        CriticalityLevel.CRITICAL: 1.0,
        CriticalityLevel.HIGH: 0.8,
        CriticalityLevel.MEDIUM: 0.6,
        CriticalityLevel.LOW: 0.4,
        CriticalityLevel.DEFERRABLE: 0.2
    }
    
    urgency_weights = {
        UrgencyLevel.REAL_TIME: 1.0,
        UrgencyLevel.URGENT: 0.8,
        UrgencyLevel.NORMAL: 0.6,
        UrgencyLevel.BATCH: 0.4,
        UrgencyLevel.DEFERRABLE: 0.2
    }
    
    business_value = (
        criticality_weights.get(workload.criticality, 0.5) * 0.6 +
        urgency_weights.get(workload.urgency, 0.5) * 0.4
    )
    
    # Carbon intensity component (lower emissions = better)
    # Normalize emissions (assuming typical range 0.001-1.0 kg per run)
    normalized_emissions = min(emissions_per_run_kg / 1.0, 1.0)  # Cap at 1.0 kg
    carbon_intensity_score = 1.0 - normalized_emissions
    
    # Frequency alignment component (better alignment = better score)
    frequency_ratio = workload.get_frequency_ratio()
    if frequency_ratio >= 1.0:
        # Over-serving - reduces score
        alignment_score = max(0.0, 1.0 - (frequency_ratio - 1.0) * 0.5)
    else:
        # Under-serving - also reduces score (may miss SLAs)
        alignment_score = frequency_ratio
    
    # Optimization potential component (higher potential = lower score)
    optimization_penalty = optimization_potential * 0.3
    
    # Calculate composite score
    # Weighted combination of components
    ces = (
        business_value * 0.4 +
        carbon_intensity_score * 0.3 +
        alignment_score * 0.2 +
        (1.0 - optimization_penalty) * 0.1
    )
    
    # Normalize to 0-100 scale
    ces_normalized = ces * 100
    
    return {
        "ces_score": round(ces_normalized, 2),
        "business_value": round(business_value, 3),
        "carbon_intensity_score": round(carbon_intensity_score, 3),
        "alignment_score": round(alignment_score, 3),
        "optimization_potential": round(optimization_potential, 3),
        "breakdown": {
            "criticality_weight": criticality_weights.get(workload.criticality, 0.5),
            "urgency_weight": urgency_weights.get(workload.urgency, 0.5),
            "emissions_per_run_kg": emissions_per_run_kg,
            "frequency_ratio": round(frequency_ratio, 2)
        }
    }

