"""
Example workload definitions for demonstration
"""

from src.context.execution_context import (
    WorkloadContext,
    CriticalityLevel,
    UrgencyLevel
)


def get_example_workloads():
    """
    Get example workload definitions
    
    Returns:
        List of WorkloadContext objects
    """
    workloads = []
    
    # Example 1: Fraud Detection (from proposal)
    fraud_detection = WorkloadContext(
        workload_id="fraud_detection_v2",
        model_name="fraud_detection_v2",
        description="Detects fraudulent transactions in real-time",
        criticality=CriticalityLevel.HIGH,
        urgency=UrgencyLevel.URGENT,
        sla_window_hours=2.0,
        required_frequency_hours=2.0,
        current_frequency_hours=1.0,  # Over-serving: runs hourly but only needs 2-hour window
        current_schedule="every_1_hour",
        estimated_duration_seconds=45.0,
        cpu_cores=4,
        gpu_required=False,
        memory_gb=8.0,
        metadata={
            "domain": "security",
            "model_type": "classification",
            "training_frequency": "weekly"
        }
    )
    workloads.append(fraud_detection)
    
    # Example 2: Sales Report (deferrable batch job)
    sales_report = WorkloadContext(
        workload_id="batch_sales_report",
        model_name="batch_sales_report",
        description="Weekly sales analytics and reporting",
        criticality=CriticalityLevel.LOW,
        urgency=UrgencyLevel.BATCH,
        sla_window_hours=24.0,
        required_frequency_hours=24.0,
        current_frequency_hours=24.0,
        current_schedule="daily_at_2pm",
        estimated_duration_seconds=120.0,
        cpu_cores=2,
        gpu_required=False,
        memory_gb=4.0,
        metadata={
            "domain": "analytics",
            "model_type": "aggregation",
            "output_format": "report"
        }
    )
    workloads.append(sales_report)
    
    # Example 3: Customer Recommendations (high value, well-optimized)
    recommendations = WorkloadContext(
        workload_id="customer_recommendations",
        model_name="customer_recommendations",
        description="Personalized product recommendations",
        criticality=CriticalityLevel.HIGH,
        urgency=UrgencyLevel.NORMAL,
        sla_window_hours=1.0,
        required_frequency_hours=1.0,
        current_frequency_hours=1.0,  # Well-aligned
        current_schedule="every_1_hour",
        estimated_duration_seconds=30.0,
        cpu_cores=2,
        gpu_required=True,
        memory_gb=16.0,
        metadata={
            "domain": "recommendations",
            "model_type": "embedding",
            "serving_type": "real-time"
        }
    )
    workloads.append(recommendations)
    
    # Example 4: Forecasting Model (over-serving)
    forecasting = WorkloadContext(
        workload_id="demand_forecasting",
        model_name="demand_forecasting",
        description="Demand forecasting for inventory management",
        criticality=CriticalityLevel.MEDIUM,
        urgency=UrgencyLevel.NORMAL,
        sla_window_hours=6.0,
        required_frequency_hours=6.0,
        current_frequency_hours=2.0,  # Over-serving
        current_schedule="every_2_hours",
        estimated_duration_seconds=90.0,
        cpu_cores=4,
        gpu_required=False,
        memory_gb=8.0,
        metadata={
            "domain": "forecasting",
            "model_type": "time_series",
            "update_frequency": "daily"
        }
    )
    workloads.append(forecasting)
    
    # Example 5: Image Processing (deferrable)
    image_processing = WorkloadContext(
        workload_id="image_processing_batch",
        model_name="image_processing_batch",
        description="Batch image processing and tagging",
        criticality=CriticalityLevel.LOW,
        urgency=UrgencyLevel.DEFERRABLE,
        sla_window_hours=48.0,
        required_frequency_hours=48.0,
        current_frequency_hours=24.0,  # Over-serving
        current_schedule="daily_at_midnight",
        estimated_duration_seconds=300.0,
        cpu_cores=8,
        gpu_required=True,
        memory_gb=32.0,
        metadata={
            "domain": "computer_vision",
            "model_type": "classification",
            "batch_size": "large"
        }
    )
    workloads.append(image_processing)
    
    return workloads

