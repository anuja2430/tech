# Quick Start Guide

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd TECH
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Dashboard

1. **Start the Streamlit dashboard:**
   ```bash
   streamlit run dashboard/app.py
   ```

2. **In the dashboard:**
   - Click "Load Example Workloads" in the sidebar
   - Navigate through different views:
     - **Dashboard**: Overview of all workloads
     - **Workload Analysis**: Detailed analysis for individual workloads
     - **Recommendations**: Prioritized optimization opportunities
     - **About**: System information

## Running Example Workloads

1. **Run the example script:**
   ```bash
   python examples/run_workloads.py
   ```

   This will:
   - Register example workloads
   - Simulate some executions
   - Generate emission metrics
   - Display analysis and recommendations

## Project Structure

```
TECH/
├── src/                    # Core source code
│   ├── agent/             # Agentic reasoning layer
│   ├── observability/     # Carbon tracking and metrics
│   ├── context/           # Execution context management
│   └── utils/             # Utility functions
├── dashboard/             # Streamlit dashboard
├── examples/              # Example workloads and scenarios
├── tests/                 # Unit tests
└── requirements.txt       # Python dependencies
```

## Key Components

### CarbonAwareAgent
Main agent class that orchestrates the system:
```python
from src.agent.carbon_agent import CarbonAwareAgent

agent = CarbonAwareAgent()
analysis = agent.analyze_workload("workload_id")
```

### WorkloadContext
Define workload metadata:
```python
from src.context.execution_context import WorkloadContext, CriticalityLevel, UrgencyLevel

workload = WorkloadContext(
    workload_id="my_model",
    model_name="my_model",
    description="Description",
    criticality=CriticalityLevel.HIGH,
    urgency=UrgencyLevel.NORMAL,
    sla_window_hours=2.0,
    required_frequency_hours=2.0,
    current_frequency_hours=1.0,
    current_schedule="every_1_hour",
    estimated_duration_seconds=30.0
)
```

## Next Steps

1. **Review the proposal:** See `PROPOSAL.md` for detailed documentation
2. **Explore the dashboard:** Load example workloads and review recommendations
3. **Run tests:** `pytest tests/` to verify functionality
4. **Customize:** Add your own workloads and scenarios

## Troubleshooting

### CodeCarbon Issues
- CodeCarbon requires internet access for grid carbon intensity data
- If offline, it will use default values
- Check `carbon_data/` directory for emission logs

### Import Errors
- Ensure you're in the project root directory
- Verify virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`

### Dashboard Not Loading
- Ensure Streamlit is installed: `pip install streamlit`
- Check that port 8501 is available
- Try: `streamlit run dashboard/app.py --server.port 8502`

## Support

For questions or issues, refer to:
- `README.md` for project overview
- `PROPOSAL.md` for detailed design documentation
- Code comments in source files

