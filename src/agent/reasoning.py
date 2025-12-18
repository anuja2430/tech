"""
Agentic reasoning logic for carbon-aware recommendations
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from src.context.execution_context import WorkloadContext, CriticalityLevel, UrgencyLevel


class RecommendationType(str, Enum):
    """Types of recommendations"""
    REDUCE_FREQUENCY = "reduce_frequency"
    DEFER_EXECUTION = "defer_execution"
    OPTIMIZE_RESOURCES = "optimize_resources"
    TIME_SHIFT = "time_shift"
    NO_ACTION = "no_action"


class ConfidenceLevel(str, Enum):
    """Confidence levels for recommendations"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ImpactLevel(str, Enum):
    """Impact levels for recommendations"""
    SIGNIFICANT = "significant"
    MODERATE = "moderate"
    MINOR = "minor"


@dataclass
class Recommendation:
    """A carbon-aware execution recommendation"""
    
    workload_id: str
    recommendation_type: RecommendationType
    title: str
    description: str
    rationale: str
    
    # Current state
    current_state: Dict
    
    # Recommended action
    recommended_action: Dict
    
    # Impact prediction
    estimated_emission_reduction_kg: float
    estimated_emission_reduction_percent: float
    business_risk: str  # "low", "medium", "high"
    confidence: ConfidenceLevel
    impact_level: ImpactLevel
    
    # Additional context
    prerequisites: List[str]
    implementation_steps: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "workload_id": self.workload_id,
            "recommendation_type": self.recommendation_type.value,
            "title": self.title,
            "description": self.description,
            "rationale": self.rationale,
            "current_state": self.current_state,
            "recommended_action": self.recommended_action,
            "estimated_emission_reduction_kg": self.estimated_emission_reduction_kg,
            "estimated_emission_reduction_percent": self.estimated_emission_reduction_percent,
            "business_risk": self.business_risk,
            "confidence": self.confidence.value,
            "impact_level": self.impact_level.value,
            "prerequisites": self.prerequisites,
            "implementation_steps": self.implementation_steps
        }


class ReasoningEngine:
    """Engine for reasoning about carbon-aware optimizations"""
    
    def __init__(self):
        """Initialize reasoning engine"""
        pass
    
    def analyze_workload(self,
                        workload: WorkloadContext,
                        emissions_per_run_kg: float,
                        execution_history: Optional[List[Dict]] = None) -> List[Recommendation]:
        """
        Analyze a workload and generate recommendations
        
        Args:
            workload: Workload context
            emissions_per_run_kg: Average emissions per execution
            execution_history: Optional execution history
            
        Returns:
            List of recommendations sorted by impact
        """
        recommendations = []
        
        # Check for frequency optimization
        if workload.is_over_serving():
            freq_rec = self._analyze_frequency_optimization(workload, emissions_per_run_kg)
            if freq_rec:
                recommendations.append(freq_rec)
        
        # Check for time-shifting opportunities (if deferrable)
        if (workload.urgency in [UrgencyLevel.BATCH, UrgencyLevel.DEFERRABLE] and
            workload.criticality != CriticalityLevel.CRITICAL):
            time_rec = self._analyze_time_shift(workload, emissions_per_run_kg)
            if time_rec:
                recommendations.append(time_rec)
        
        # Check for resource optimization
        if workload.gpu_required and workload.estimated_duration_seconds > 300:
            resource_rec = self._analyze_resource_optimization(workload, emissions_per_run_kg)
            if resource_rec:
                recommendations.append(resource_rec)
        
        # If no optimizations found, provide no-action recommendation
        if not recommendations:
            recommendations.append(self._generate_no_action_recommendation(workload))
        
        # Sort by impact (highest first)
        recommendations.sort(
            key=lambda r: r.estimated_emission_reduction_kg,
            reverse=True
        )
        
        return recommendations
    
    def _analyze_frequency_optimization(self,
                                       workload: WorkloadContext,
                                       emissions_per_run_kg: float) -> Optional[Recommendation]:
        """Analyze frequency optimization opportunity"""
        
        if not workload.is_over_serving():
            return None
        
        # Calculate optimal frequency (align with SLA)
        optimal_frequency = workload.required_frequency_hours
        current_frequency = workload.current_frequency_hours
        
        # Calculate reduction
        executions_per_day_current = 24 / current_frequency
        executions_per_day_optimal = 24 / optimal_frequency
        reduction_per_day = executions_per_day_current - executions_per_day_optimal
        
        emission_reduction_per_day = reduction_per_day * emissions_per_run_kg
        emission_reduction_percent = (reduction_per_day / executions_per_day_current) * 100
        
        # Determine business risk
        sla_margin = (workload.sla_window_hours - optimal_frequency) / workload.sla_window_hours
        if sla_margin > 0.3:
            business_risk = "low"
        elif sla_margin > 0.1:
            business_risk = "medium"
        else:
            business_risk = "high"
        
        # Only recommend if significant and low risk
        if emission_reduction_percent < 10 or business_risk == "high":
            return None
        
        # Determine impact level
        if emission_reduction_percent > 30:
            impact_level = ImpactLevel.SIGNIFICANT
        elif emission_reduction_percent > 15:
            impact_level = ImpactLevel.MODERATE
        else:
            impact_level = ImpactLevel.MINOR
        
        return Recommendation(
            workload_id=workload.workload_id,
            recommendation_type=RecommendationType.REDUCE_FREQUENCY,
            title=f"Optimize Execution Frequency for {workload.model_name}",
            description=f"Current execution frequency exceeds business requirements. "
                       f"Adjusting from {current_frequency}h to {optimal_frequency}h interval "
                       f"would maintain SLA compliance while reducing emissions.",
            rationale=f"The workload currently runs every {current_frequency} hours, but the "
                     f"business SLA only requires execution within {workload.sla_window_hours} hours. "
                     f"By aligning frequency with requirements, we can reduce emissions without "
                     f"impacting service levels.",
            current_state={
                "frequency_hours": current_frequency,
                "executions_per_day": round(executions_per_day_current, 1),
                "emissions_per_day_kg": round(executions_per_day_current * emissions_per_run_kg, 4)
            },
            recommended_action={
                "frequency_hours": optimal_frequency,
                "executions_per_day": round(executions_per_day_optimal, 1),
                "new_schedule": f"every_{optimal_frequency}_hours"
            },
            estimated_emission_reduction_kg=round(emission_reduction_per_day, 4),
            estimated_emission_reduction_percent=round(emission_reduction_percent, 1),
            business_risk=business_risk,
            confidence=ConfidenceLevel.HIGH if business_risk == "low" else ConfidenceLevel.MEDIUM,
            impact_level=impact_level,
            prerequisites=[
                "Validate SLA requirements are accurate",
                "Confirm business stakeholders approve frequency change"
            ],
            implementation_steps=[
                f"Update scheduler configuration to {optimal_frequency}h interval",
                "Monitor execution for 1 week in test environment",
                "Validate SLA compliance metrics",
                "Deploy to production after validation"
            ]
        )
    
    def _analyze_time_shift(self,
                           workload: WorkloadContext,
                           emissions_per_run_kg: float) -> Optional[Recommendation]:
        """Analyze time-shifting opportunity"""
        
        # Simplified: recommend shifting to off-peak hours
        # In production, this would use actual grid carbon intensity data
        
        return Recommendation(
            workload_id=workload.workload_id,
            recommendation_type=RecommendationType.TIME_SHIFT,
            title=f"Consider Time-Shifting {workload.model_name}",
            description=f"This deferrable workload could be shifted to off-peak hours "
                       f"when grid carbon intensity is typically lower.",
            rationale=f"The workload has flexibility in execution timing. Shifting to "
                     f"off-peak hours (typically 2-6 AM) can reduce carbon intensity by "
                     f"10-20% depending on regional grid mix.",
            current_state={
                "current_schedule": workload.current_schedule,
                "flexibility": "high"
            },
            recommended_action={
                "suggested_time": "off_peak_hours",
                "estimated_carbon_intensity_reduction": "10-20%"
            },
            estimated_emission_reduction_kg=round(emissions_per_run_kg * 0.15, 4),  # ~15% reduction
            estimated_emission_reduction_percent=15.0,
            business_risk="low",
            confidence=ConfidenceLevel.MEDIUM,
            impact_level=ImpactLevel.MODERATE,
            prerequisites=[
                "Verify workload can be deferred without business impact",
                "Check regional grid carbon intensity patterns"
            ],
            implementation_steps=[
                "Identify optimal time window based on grid data",
                "Update scheduler to preferred time slot",
                "Monitor for any business impact"
            ]
        )
    
    def _analyze_resource_optimization(self,
                                     workload: WorkloadContext,
                                     emissions_per_run_kg: float) -> Optional[Recommendation]:
        """Analyze resource optimization opportunity"""
        
        # Simplified recommendation
        return Recommendation(
            workload_id=workload.workload_id,
            recommendation_type=RecommendationType.OPTIMIZE_RESOURCES,
            title=f"Review Resource Allocation for {workload.model_name}",
            description=f"Long-running workload may benefit from resource optimization review.",
            rationale=f"The workload runs for {workload.estimated_duration_seconds}s and uses "
                     f"GPU resources. A review of resource allocation could identify optimization "
                     f"opportunities.",
            current_state={
                "duration_seconds": workload.estimated_duration_seconds,
                "gpu_required": workload.gpu_required,
                "memory_gb": workload.memory_gb
            },
            recommended_action={
                "action": "review_resource_allocation",
                "suggested_review_areas": ["GPU utilization", "Memory allocation", "Batch sizing"]
            },
            estimated_emission_reduction_kg=round(emissions_per_run_kg * 0.1, 4),  # ~10% potential
            estimated_emission_reduction_percent=10.0,
            business_risk="low",
            confidence=ConfidenceLevel.LOW,
            impact_level=ImpactLevel.MINOR,
            prerequisites=[
                "Collect detailed resource utilization metrics",
                "Profile workload performance characteristics"
            ],
            implementation_steps=[
                "Run resource profiling analysis",
                "Identify optimization opportunities",
                "Test optimized configuration",
                "Deploy if validated"
            ]
        )
    
    def _generate_no_action_recommendation(self, workload: WorkloadContext) -> Recommendation:
        """Generate no-action recommendation when no optimizations are identified"""
        
        return Recommendation(
            workload_id=workload.workload_id,
            recommendation_type=RecommendationType.NO_ACTION,
            title=f"No Optimization Recommended for {workload.model_name}",
            description=f"Current execution pattern appears well-optimized for business requirements.",
            rationale=f"The workload execution frequency aligns with business requirements, "
                     f"and the workload has appropriate criticality/urgency levels. No immediate "
                     f"optimization opportunities identified.",
            current_state={
                "frequency_alignment": "good",
                "criticality": workload.criticality.value,
                "urgency": workload.urgency.value
            },
            recommended_action={
                "action": "maintain_current_configuration"
            },
            estimated_emission_reduction_kg=0.0,
            estimated_emission_reduction_percent=0.0,
            business_risk="none",
            confidence=ConfidenceLevel.HIGH,
            impact_level=ImpactLevel.MINOR,
            prerequisites=[],
            implementation_steps=[
                "Continue monitoring for future optimization opportunities"
            ]
        )

