"""
Basic tests for CarbonAwareAgent
"""

import pytest
from src.agent.carbon_agent import CarbonAwareAgent
from src.context.execution_context import (
    WorkloadContext,
    CriticalityLevel,
    UrgencyLevel
)


def test_agent_initialization():
    """Test agent can be initialized"""
    agent = CarbonAwareAgent()
    assert agent is not None
    assert agent.carbon_tracker is not None
    assert agent.metrics_collector is not None
    assert agent.execution_context is not None
    assert agent.reasoning_engine is not None


def test_workload_registration():
    """Test workload registration"""
    agent = CarbonAwareAgent()
    
    workload = WorkloadContext(
        workload_id="test_workload",
        model_name="test_model",
        description="Test workload",
        criticality=CriticalityLevel.MEDIUM,
        urgency=UrgencyLevel.NORMAL,
        sla_window_hours=2.0,
        required_frequency_hours=2.0,
        current_frequency_hours=1.0,
        current_schedule="every_1_hour",
        estimated_duration_seconds=30.0
    )
    
    agent.register_workload(workload)
    
    assert "test_workload" in agent.execution_context.list_workloads()
    assert agent.execution_context.get_workload("test_workload") == workload


def test_workload_analysis():
    """Test workload analysis"""
    agent = CarbonAwareAgent()
    
    workload = WorkloadContext(
        workload_id="test_workload",
        model_name="test_model",
        description="Test workload",
        criticality=CriticalityLevel.MEDIUM,
        urgency=UrgencyLevel.NORMAL,
        sla_window_hours=2.0,
        required_frequency_hours=2.0,
        current_frequency_hours=1.0,  # Over-serving
        current_schedule="every_1_hour",
        estimated_duration_seconds=30.0
    )
    
    agent.register_workload(workload)
    
    analysis = agent.analyze_workload("test_workload")
    
    assert analysis is not None
    assert analysis["workload_id"] == "test_workload"
    assert "recommendations" in analysis
    assert "carbon_efficiency_score" in analysis
    assert "summary" in analysis


def test_over_serving_detection():
    """Test detection of over-serving workloads"""
    agent = CarbonAwareAgent()
    
    # Workload that over-serves
    workload = WorkloadContext(
        workload_id="over_serving",
        model_name="over_serving_model",
        description="Over-serving workload",
        criticality=CriticalityLevel.MEDIUM,
        urgency=UrgencyLevel.NORMAL,
        sla_window_hours=4.0,
        required_frequency_hours=4.0,
        current_frequency_hours=1.0,  # Runs hourly but only needs 4-hour window
        current_schedule="every_1_hour",
        estimated_duration_seconds=30.0
    )
    
    agent.register_workload(workload)
    
    assert workload.is_over_serving() is True
    assert workload.get_frequency_ratio() > 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

