"""
Streamlit Dashboard for Carbon-Aware Execution Intelligence
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.agent.carbon_agent import CarbonAwareAgent
from src.context.execution_context import WorkloadContext, CriticalityLevel, UrgencyLevel
from src.observability.metrics import MetricsCollector


# Page configuration
st.set_page_config(
    page_title="Carbon-Aware Execution Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = CarbonAwareAgent()
    # Load example workloads if not already loaded
    if 'workloads_loaded' not in st.session_state:
        st.session_state.workloads_loaded = False


def load_example_workloads():
    """Load example workloads"""
    agent = st.session_state.agent
    
    # Fraud Detection Model (from proposal example)
    fraud_detection = WorkloadContext(
        workload_id="fraud_detection_v2",
        model_name="fraud_detection_v2",
        description="Detects fraudulent transactions in real-time",
        criticality=CriticalityLevel.HIGH,
        urgency=UrgencyLevel.URGENT,
        sla_window_hours=2.0,
        required_frequency_hours=2.0,
        current_frequency_hours=1.0,  # Over-serving
        current_schedule="every_1_hour",
        estimated_duration_seconds=45.0,
        cpu_cores=4,
        gpu_required=False,
        memory_gb=8.0
    )
    agent.register_workload(fraud_detection)
    
    # Sales Report (deferrable)
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
        memory_gb=4.0
    )
    agent.register_workload(sales_report)
    
    # Customer Recommendations (high value)
    recommendations = WorkloadContext(
        workload_id="customer_recommendations",
        model_name="customer_recommendations",
        description="Personalized product recommendations",
        criticality=CriticalityLevel.HIGH,
        urgency=UrgencyLevel.NORMAL,
        sla_window_hours=1.0,
        required_frequency_hours=1.0,
        current_frequency_hours=1.0,
        current_schedule="every_1_hour",
        estimated_duration_seconds=30.0,
        cpu_cores=2,
        gpu_required=True,
        memory_gb=16.0
    )
    agent.register_workload(recommendations)
    
    st.session_state.workloads_loaded = True


# Sidebar
with st.sidebar:
    st.title("🌱 Carbon-Aware AI")
    st.markdown("**Decision Companion for Sustainable AI Execution**")
    
    st.divider()
    
    if st.button("Load Example Workloads", use_container_width=True):
        load_example_workloads()
        st.success("Example workloads loaded!")
    
    st.divider()
    
    st.markdown("### Navigation")
    page = st.radio(
        "Select View",
        ["Dashboard", "Workload Analysis", "Recommendations", "About"],
        label_visibility="collapsed"
    )


# Main content
if page == "Dashboard":
    st.title("Carbon-Aware Execution Intelligence Dashboard")
    st.markdown("**Overview of AI workload emissions and optimization opportunities**")
    
    if not st.session_state.workloads_loaded:
        st.info("👆 Click 'Load Example Workloads' in the sidebar to get started")
    else:
        agent = st.session_state.agent
        
        # Get all analyses
        analyses = agent.get_all_workloads_analysis()
        opportunities = agent.get_optimization_opportunities()
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_workloads = len(analyses)
        total_recommendations = sum(a.get("summary", {}).get("total_recommendations", 0) for a in analyses)
        high_impact = sum(a.get("summary", {}).get("high_impact_count", 0) for a in analyses)
        total_potential_reduction = sum(a.get("summary", {}).get("estimated_total_reduction_kg", 0) for a in analyses)
        
        with col1:
            st.metric("Total Workloads", total_workloads)
        with col2:
            st.metric("Recommendations", total_recommendations)
        with col3:
            st.metric("High Impact", high_impact)
        with col4:
            st.metric("Potential Reduction", f"{total_potential_reduction:.4f} kg CO₂/day")
        
        st.divider()
        
        # Workloads overview table
        st.subheader("Workload Overview")
        
        workload_data = []
        for analysis in analyses:
            if "error" in analysis:
                continue
            workload_data.append({
                "Workload": analysis["workload_name"],
                "ID": analysis["workload_id"],
                "CES Score": analysis["carbon_efficiency_score"]["ces_score"],
                "Recommendations": analysis["summary"]["total_recommendations"],
                "Potential Reduction (kg/day)": analysis["summary"]["estimated_total_reduction_kg"],
                "Criticality": analysis["workload_context"]["criticality"],
                "Urgency": analysis["workload_context"]["urgency"]
            })
        
        if workload_data:
            df = pd.DataFrame(workload_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Optimization opportunities
        if opportunities:
            st.divider()
            st.subheader("Top Optimization Opportunities")
            
            opp_data = []
            for opp in opportunities[:5]:  # Top 5
                rec = opp["recommendation"]
                opp_data.append({
                    "Workload": opp["workload_name"],
                    "Recommendation": rec["title"],
                    "Impact": rec["impact_level"],
                    "Reduction (kg/day)": rec["estimated_emission_reduction_kg"],
                    "Risk": rec["business_risk"],
                    "Confidence": rec["confidence"]
                })
            
            df_opp = pd.DataFrame(opp_data)
            st.dataframe(df_opp, use_container_width=True, hide_index=True)


elif page == "Workload Analysis":
    st.title("Workload Analysis")
    st.markdown("**Detailed analysis for individual workloads**")
    
    if not st.session_state.workloads_loaded:
        st.info("👆 Click 'Load Example Workloads' in the sidebar to get started")
    else:
        agent = st.session_state.agent
        workload_ids = agent.execution_context.list_workloads()
        
        if not workload_ids:
            st.warning("No workloads registered")
        else:
            selected_workload = st.selectbox("Select Workload", workload_ids)
            
            if selected_workload:
                analysis = agent.analyze_workload(selected_workload)
                
                # Workload context
                st.subheader("Workload Context")
                context = analysis["workload_context"]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Model:** {context['model_name']}")
                    st.markdown(f"**Description:** {context['description']}")
                    st.markdown(f"**Criticality:** {context['criticality']}")
                    st.markdown(f"**Urgency:** {context['urgency']}")
                
                with col2:
                    st.markdown(f"**SLA Window:** {context['sla_window_hours']} hours")
                    st.markdown(f"**Required Frequency:** {context['required_frequency_hours']} hours")
                    st.markdown(f"**Current Frequency:** {context['current_frequency_hours']} hours")
                    st.markdown(f"**Current Schedule:** {context['current_schedule']}")
                
                # Carbon Efficiency Score
                st.divider()
                st.subheader("Carbon Efficiency Score")
                ces = analysis["carbon_efficiency_score"]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("CES Score", f"{ces['ces_score']}/100")
                with col2:
                    st.metric("Business Value", f"{ces['business_value']:.3f}")
                with col3:
                    st.metric("Optimization Potential", f"{ces['optimization_potential']:.3f}")
                
                # Execution stats
                st.divider()
                st.subheader("Execution Statistics")
                stats = analysis["execution_stats"]
                
                if stats["total_executions"] > 0:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Executions", stats["total_executions"])
                    with col2:
                        st.metric("Total Emissions", f"{stats['total_emissions_kg']:.4f} kg CO₂")
                    with col3:
                        st.metric("Avg per Run", f"{stats['avg_emissions_per_run_kg']:.4f} kg CO₂")
                    with col4:
                        st.metric("Avg Duration", f"{stats['avg_duration_seconds']:.1f} s")
                else:
                    st.info("No execution history available. Run workloads to collect metrics.")
                
                # Recommendations
                st.divider()
                st.subheader("Recommendations")
                
                recommendations = analysis["recommendations"]
                if recommendations:
                    for i, rec in enumerate(recommendations, 1):
                        with st.expander(f"**{i}. {rec['title']}**", expanded=(i == 1)):
                            st.markdown(f"**Type:** {rec['recommendation_type']}")
                            st.markdown(f"**Description:** {rec['description']}")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric(
                                    "Emission Reduction",
                                    f"{rec['estimated_emission_reduction_kg']:.4f} kg/day",
                                    f"{rec['estimated_emission_reduction_percent']:.1f}%"
                                )
                            with col2:
                                st.metric("Business Risk", rec['business_risk'].title())
                            with col3:
                                st.metric("Confidence", rec['confidence'].title())
                            
                            st.markdown("**Rationale:**")
                            st.markdown(rec['rationale'])
                            
                            st.markdown("**Recommended Action:**")
                            st.json(rec['recommended_action'])
                            
                            if rec['implementation_steps']:
                                st.markdown("**Implementation Steps:**")
                                for step in rec['implementation_steps']:
                                    st.markdown(f"- {step}")
                else:
                    st.info("No recommendations available")


elif page == "Recommendations":
    st.title("Optimization Recommendations")
    st.markdown("**Prioritized recommendations across all workloads**")
    
    if not st.session_state.workloads_loaded:
        st.info("👆 Click 'Load Example Workloads' in the sidebar to get started")
    else:
        agent = st.session_state.agent
        opportunities = agent.get_optimization_opportunities()
        
        if not opportunities:
            st.info("No optimization opportunities identified at this time")
        else:
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                impact_filter = st.multiselect(
                    "Filter by Impact",
                    ["significant", "moderate", "minor"],
                    default=["significant", "moderate"]
                )
            with col2:
                risk_filter = st.multiselect(
                    "Filter by Risk",
                    ["low", "medium", "high"],
                    default=["low", "medium"]
                )
            
            # Filter opportunities
            filtered = [
                opp for opp in opportunities
                if opp["recommendation"]["impact_level"] in impact_filter
                and opp["recommendation"]["business_risk"] in risk_filter
            ]
            
            st.metric("Filtered Opportunities", len(filtered))
            
            # Display recommendations
            for i, opp in enumerate(filtered, 1):
                rec = opp["recommendation"]
                
                with st.container():
                    st.markdown(f"### {i}. {rec['title']}")
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown(f"**Workload:** {opp['workload_name']}")
                        st.markdown(f"**Description:** {rec['description']}")
                    with col2:
                        st.metric(
                            "Reduction",
                            f"{rec['estimated_emission_reduction_kg']:.4f} kg/day"
                        )
                    with col3:
                        badge_color = {
                            "low": "🟢",
                            "medium": "🟡",
                            "high": "🔴"
                        }.get(rec['business_risk'], "⚪")
                        st.markdown(f"**Risk:** {badge_color} {rec['business_risk'].title()}")
                    
                    with st.expander("View Details"):
                        st.markdown("**Rationale:**")
                        st.markdown(rec['rationale'])
                        st.markdown("**Current State:**")
                        st.json(rec['current_state'])
                        st.markdown("**Recommended Action:**")
                        st.json(rec['recommended_action'])
                    
                    st.divider()


elif page == "About":
    st.title("About Carbon-Aware Execution Intelligence")
    
    st.markdown("""
    ### Overview
    
    This system provides a **decision companion** for Green IT and AI engineers, helping 
    them make carbon-aware decisions about AI workload execution.
    
    ### Key Features
    
    - **Carbon Measurement**: Track CO₂ emissions at the workload level using CodeCarbon
    - **Context-Aware Analysis**: Consider business criticality, SLA requirements, and urgency
    - **Intelligent Recommendations**: Generate actionable optimization suggestions
    - **Carbon Efficiency Scoring**: Prioritize optimization opportunities
    
    ### Architecture
    
    The system consists of four main layers:
    
    1. **Execution Context Layer**: Captures workload metadata and business requirements
    2. **Carbon Observability Layer**: Measures emissions using CodeCarbon
    3. **Agentic Reasoning Layer**: Analyzes patterns and generates recommendations
    4. **Recommendation Interface**: Streamlit dashboard for visualization and interaction
    
    ### Design Principles
    
    - **Transparency**: Every recommendation includes clear rationale
    - **Safety**: No automated execution without approval
    - **Respect**: Engineers remain in control
    - **Trust**: Build confidence through explainability
    
    ### Technology Stack
    
    - **Python 3.8+**: Core language
    - **CodeCarbon**: Carbon emission tracking
    - **Streamlit**: Dashboard interface
    - **LangChain**: Agentic reasoning (future enhancement)
    
    ### Contact
    
    **Author:** Anuja  
    **Program:** B.Tech Engineering  
    **Institution:** Tech Mahindra Green IT Software Engineering Internship
    """)


# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Carbon-Aware Execution Intelligence | Tech Mahindra Green IT Initiative"
    "</div>",
    unsafe_allow_html=True
)

