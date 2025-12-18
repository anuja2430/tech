"""
Main Carbon-Aware Agent class
"""

from typing import Dict, List, Optional
from src.observability.carbon_tracker import CarbonTracker
from src.observability.metrics import MetricsCollector
from src.context.execution_context import ExecutionContext, WorkloadContext
from src.agent.reasoning import ReasoningEngine, Recommendation
from src.utils.scoring import calculate_carbon_efficiency_score


class CarbonAwareAgent:
    """
    Carbon-Aware Execution Intelligence Agent
    
    Orchestrates carbon measurement, context analysis, and recommendation generation.
    """
    
    def __init__(self):
        """Initialize the carbon-aware agent"""
        self.carbon_tracker = CarbonTracker()
        self.metrics_collector = MetricsCollector()
        self.execution_context = ExecutionContext()
        self.reasoning_engine = ReasoningEngine()
    
    def register_workload(self, workload_context: WorkloadContext) -> None:
        """
        Register a workload with the agent
        
        Args:
            workload_context: Workload context to register
        """
        self.execution_context.register_workload(workload_context)
    
    def analyze_workload(self, workload_id: str) -> Dict:
        """
        Analyze a workload and generate recommendations
        
        Args:
            workload_id: Unique identifier for the workload
            
        Returns:
            Dictionary with analysis results and recommendations
        """
        # Get workload context
        workload = self.execution_context.get_workload(workload_id)
        if not workload:
            raise ValueError(f"Workload {workload_id} not found")
        
        # Get execution history and aggregate stats
        history = self.metrics_collector.get_workload_history(workload_id, days=30)
        stats = self.metrics_collector.get_aggregate_stats(workload_id, days=30)
        
        # Get average emissions per run
        emissions_per_run = stats.get("avg_emissions_per_run_kg", 0.0)
        if emissions_per_run == 0 and history:
            # Calculate from history if not in stats
            emissions_per_run = sum(r["emissions_kg"] for r in history) / len(history)
        
        # Calculate optimization potential
        optimization_potential = 0.0
        if workload.is_over_serving():
            frequency_ratio = workload.get_frequency_ratio()
            optimization_potential = min(1.0, (frequency_ratio - 1.0) * 0.5)
        
        # Calculate Carbon Efficiency Score
        ces = calculate_carbon_efficiency_score(
            workload=workload,
            emissions_per_run_kg=emissions_per_run,
            optimization_potential=optimization_potential
        )
        
        # Generate recommendations
        recommendations = self.reasoning_engine.analyze_workload(
            workload=workload,
            emissions_per_run_kg=emissions_per_run,
            execution_history=history
        )
        
        # Compile analysis result
        return {
            "workload_id": workload_id,
            "workload_name": workload.model_name,
            "analysis_timestamp": self._get_timestamp(),
            "workload_context": workload.to_dict(),
            "execution_stats": stats,
            "carbon_efficiency_score": ces,
            "recommendations": [r.to_dict() for r in recommendations],
            "summary": {
                "total_recommendations": len(recommendations),
                "high_impact_count": sum(1 for r in recommendations 
                                        if r.impact_level.value == "significant"),
                "estimated_total_reduction_kg": sum(r.estimated_emission_reduction_kg 
                                                   for r in recommendations),
                "low_risk_count": sum(1 for r in recommendations 
                                     if r.business_risk == "low")
            }
        }
    
    def track_execution(self, workload_id: str, execution_function) -> Dict:
        """
        Track emissions for a workload execution
        
        Args:
            workload_id: Unique identifier for the workload
            execution_function: Function to execute (will be wrapped with tracking)
            
        Returns:
            Execution result with emission data
        """
        workload = self.execution_context.get_workload(workload_id)
        if not workload:
            raise ValueError(f"Workload {workload_id} not found")
        
        # Start tracking
        self.carbon_tracker.start_tracking(workload_id, workload.model_name)
        
        try:
            # Execute the workload
            result = execution_function()
            
            # Stop tracking and get emissions
            emission_data = self.carbon_tracker.stop_tracking(workload_id)
            
            # Record in metrics
            self.metrics_collector.record_execution(
                workload_id=workload_id,
                emissions_kg=emission_data["emissions_kg"],
                duration_seconds=emission_data["duration_seconds"],
                energy_kwh=emission_data["energy_consumed_kwh"],
                metadata={
                    "model_name": workload.model_name,
                    "criticality": workload.criticality.value
                }
            )
            
            return {
                "workload_id": workload_id,
                "execution_result": result,
                "emissions": emission_data
            }
        
        except Exception as e:
            # Stop tracking even on error
            try:
                self.carbon_tracker.stop_tracking(workload_id)
            except:
                pass
            raise e
    
    def get_all_workloads_analysis(self) -> List[Dict]:
        """
        Analyze all registered workloads
        
        Returns:
            List of analysis results for all workloads
        """
        workload_ids = self.execution_context.list_workloads()
        analyses = []
        
        for workload_id in workload_ids:
            try:
                analysis = self.analyze_workload(workload_id)
                analyses.append(analysis)
            except Exception as e:
                # Log error but continue with other workloads
                analyses.append({
                    "workload_id": workload_id,
                    "error": str(e)
                })
        
        # Sort by total estimated reduction potential
        analyses.sort(
            key=lambda x: x.get("summary", {}).get("estimated_total_reduction_kg", 0),
            reverse=True
        )
        
        return analyses
    
    def get_optimization_opportunities(self) -> List[Dict]:
        """
        Get high-priority optimization opportunities across all workloads
        
        Returns:
            List of high-impact recommendations
        """
        all_analyses = self.get_all_workloads_analysis()
        opportunities = []
        
        for analysis in all_analyses:
            if "recommendations" not in analysis:
                continue
            
            for rec in analysis["recommendations"]:
                if (rec["impact_level"] in ["significant", "moderate"] and
                    rec["business_risk"] in ["low", "medium"]):
                    opportunities.append({
                        "workload_id": analysis["workload_id"],
                        "workload_name": analysis.get("workload_name", "Unknown"),
                        "recommendation": rec,
                        "ces_score": analysis.get("carbon_efficiency_score", {}).get("ces_score", 0)
                    })
        
        # Sort by impact
        opportunities.sort(
            key=lambda x: x["recommendation"]["estimated_emission_reduction_kg"],
            reverse=True
        )
        
        return opportunities
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as ISO string"""
        from datetime import datetime
        return datetime.now().isoformat()

