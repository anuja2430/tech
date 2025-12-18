# Carbon-Aware Execution Intelligence for Enterprise AI

**Reframing Sustainability from Reporting to Engineering Decisions**

A Carbon-Aware Execution Intelligence Agent that embeds sustainability considerations into AI workload execution decisions, helping engineers optimize for carbon efficiency alongside performance and cost.

## 🎯 Overview

This system provides a **decision companion** that:
- Measures carbon emissions at the AI workload level
- Interprets emissions in execution context
- Produces clear, explainable recommendations for optimization

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────┐
│     AI WORKLOADS (Production Environment)          │
└─────────────────────┬──────────────────────────────┘
                      │
                      ↓
┌────────────────────────────────────────────────────┐
│  EXECUTION CONTEXT LAYER                           │
│  • Business criticality                            │
│  • Urgency and SLA requirements                    │
│  • Acceptable execution window                     │
└─────────────────────┬──────────────────────────────┘
                      │
                      ↓
┌────────────────────────────────────────────────────┐
│  CARBON OBSERVABILITY LAYER                        │
│  • CodeCarbon (CO₂e calculation)                  │
│  • Grid carbon intensity data                      │
└─────────────────────┬──────────────────────────────┘
                      │
                      ↓
┌────────────────────────────────────────────────────┐
│  AGENTIC REASONING LAYER                           │
│  • Pattern detection                               │
│  • Trade-off evaluation                            │
│  • Recommendation generation                       │
└─────────────────────┬──────────────────────────────┘
                      │
                      ↓
┌────────────────────────────────────────────────────┐
│  RECOMMENDATION INTERFACE (Streamlit Dashboard)    │
│  • Ranked suggestions                              │
│  • Impact prediction                               │
│  • Approval workflow                               │
└────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd TECH

# Install dependencies
pip install -r requirements.txt
```

### Run the Dashboard

```bash
streamlit run dashboard/app.py
```

### Run Example Workloads

```bash
python examples/run_workloads.py
```

## 📁 Project Structure

```
TECH/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── carbon_agent.py      # Main CarbonAwareAgent class
│   │   └── reasoning.py          # Reasoning logic
│   ├── observability/
│   │   ├── __init__.py
│   │   ├── carbon_tracker.py    # CodeCarbon integration
│   │   └── metrics.py            # Metrics collection
│   ├── context/
│   │   ├── __init__.py
│   │   └── execution_context.py # Execution context management
│   └── utils/
│       ├── __init__.py
│       └── scoring.py            # Carbon Efficiency Score
├── dashboard/
│   └── app.py                    # Streamlit dashboard
├── examples/
│   ├── __init__.py
│   ├── workloads.py              # Example workload definitions
│   └── run_workloads.py          # Run example scenarios
└── tests/
    └── test_agent.py             # Unit tests
```

## 🔧 Core Components

### CarbonAwareAgent

The main agent class that orchestrates measurement, reasoning, and recommendation generation.

```python
from src.agent.carbon_agent import CarbonAwareAgent

agent = CarbonAwareAgent()
recommendation = agent.analyze_workload(workload_id)
```

### Execution Context

Defines workload metadata including business criticality, SLA requirements, and execution patterns.

### Carbon Tracking

Uses CodeCarbon to measure CO₂e emissions based on:
- Regional grid carbon intensity
- Hardware efficiency
- Runtime duration

### Reasoning Engine

Evaluates trade-offs between carbon impact and business value to generate actionable recommendations.

## 📊 Example Output

```
=== Carbon-Aware Execution Analysis ===

Workload: fraud_detection_v2
Current Schedule: Every 1 hour
Business Criticality: High
SLA Requirement: 2 hours

Recommendation:
→ Adjust schedule from hourly to bi-hourly execution
→ Estimated outcome: ~50% emission reduction
→ Business impact: None (maintains SLA margin)
→ Confidence: High

[Review Details] [Simulate] [Dismiss]
```

## 🧪 Testing

```bash
pytest tests/
```

## 📝 License

This project is part of Tech Mahindra Green IT Software Engineering Internship submission.

## 👤 Author

**Anuja**  
B.Tech Engineering  
Tech Mahindra Internship Program

