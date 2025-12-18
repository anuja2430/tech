"""
Example script to run workloads and demonstrate carbon tracking
"""

import time
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.agent.carbon_agent import CarbonAwareAgent
from examples.workloads import get_example_workloads


def simulate_model_execution(workload_id: str, duration_seconds: float):
    """
    Simulate a model execution
    
    Args:
        workload_id: Workload identifier
        duration_seconds: How long to simulate execution
    """
    print(f"  Executing {workload_id}...")
    # Simulate CPU/GPU work
    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        # Simulate computation
        _ = sum(range(1000))
        time.sleep(0.1)
    print(f"  ✓ Completed {workload_id}")


def main():
    """Main function to demonstrate the system"""
    
    print("=" * 70)
    print("Carbon-Aware Execution Intelligence - Example Workload Runner")
    print("=" * 70)
    print()
    
    # Initialize agent
    print("Initializing Carbon-Aware Agent...")
    agent = CarbonAwareAgent()
    print("✓ Agent initialized")
    print()
    
    # Register example workloads
    print("Registering example workloads...")
    workloads = get_example_workloads()
    for workload in workloads:
        agent.register_workload(workload)
        print(f"  ✓ Registered: {workload.workload_id}")
    print()
    
    # Run a few example executions to generate metrics
    print("Running example executions (this will take a moment)...")
    print()
    
    # Run fraud detection a few times
    for i in range(3):
        print(f"Execution {i+1}/3: fraud_detection_v2")
        try:
            result = agent.track_execution(
                "fraud_detection_v2",
                lambda: simulate_model_execution("fraud_detection_v2", 2.0)
            )
            emissions = result["emissions"]
            print(f"  Emissions: {emissions['emissions_kg']:.6f} kg CO₂")
            print(f"  Energy: {emissions['energy_consumed_kwh']:.6f} kWh")
            print(f"  Duration: {emissions['duration_seconds']:.2f} s")
            print()
        except Exception as e:
            print(f"  Error: {e}")
            print()
    
    # Run demand forecasting
    print("Execution: demand_forecasting")
    try:
        result = agent.track_execution(
            "demand_forecasting",
            lambda: simulate_model_execution("demand_forecasting", 3.0)
        )
        emissions = result["emissions"]
        print(f"  Emissions: {emissions['emissions_kg']:.6f} kg CO₂")
        print()
    except Exception as e:
        print(f"  Error: {e}")
        print()
    
    # Analyze workloads
    print("=" * 70)
    print("Analyzing Workloads")
    print("=" * 70)
    print()
    
    for workload_id in agent.execution_context.list_workloads():
        print(f"Analyzing: {workload_id}")
        print("-" * 70)
        
        try:
            analysis = agent.analyze_workload(workload_id)
            
            # Display key metrics
            ces = analysis["carbon_efficiency_score"]
            print(f"  Carbon Efficiency Score: {ces['ces_score']}/100")
            print(f"  Business Value: {ces['business_value']:.3f}")
            print(f"  Optimization Potential: {ces['optimization_potential']:.3f}")
            
            # Display recommendations
            recommendations = analysis["recommendations"]
            print(f"  Recommendations: {len(recommendations)}")
            
            for rec in recommendations[:2]:  # Show top 2
                if rec["recommendation_type"] != "no_action":
                    print(f"    • {rec['title']}")
                    print(f"      Reduction: {rec['estimated_emission_reduction_kg']:.4f} kg/day "
                          f"({rec['estimated_emission_reduction_percent']:.1f}%)")
                    print(f"      Risk: {rec['business_risk']}, Confidence: {rec['confidence']}")
            
            print()
        
        except Exception as e:
            print(f"  Error analyzing {workload_id}: {e}")
            print()
    
    # Get optimization opportunities
    print("=" * 70)
    print("Top Optimization Opportunities")
    print("=" * 70)
    print()
    
    opportunities = agent.get_optimization_opportunities()
    
    if opportunities:
        for i, opp in enumerate(opportunities[:3], 1):  # Top 3
            rec = opp["recommendation"]
            print(f"{i}. {opp['workload_name']}")
            print(f"   {rec['title']}")
            print(f"   Impact: {rec['impact_level']}, "
                  f"Reduction: {rec['estimated_emission_reduction_kg']:.4f} kg/day")
            print(f"   Risk: {rec['business_risk']}, Confidence: {rec['confidence']}")
            print()
    else:
        print("No optimization opportunities identified")
        print()
    
    print("=" * 70)
    print("Analysis Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Review recommendations in the Streamlit dashboard:")
    print("     streamlit run dashboard/app.py")
    print("  2. Validate recommendations in test environment")
    print("  3. Implement approved optimizations")
    print()


if __name__ == "__main__":
    main()

