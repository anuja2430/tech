

**Tech Mahindra – Green IT Software Engineering Internship Submission**

**Name:** Anuja  
**PRN:** [Your PRN]  
**Program:** B.Tech Engineering  
**Submission Type:** Individual  
**Email:** [Your Email]  
**Date:** December 17, 2025

---

## 📋 Executive Summary

**The Problem:** Enterprises run numerous AI models daily. Engineers optimize for accuracy and cost — but carbon rarely participates in execution decisions until retrospective reporting.

**The Solution:** A Carbon-Aware Execution Intelligence Agent that embeds sustainability considerations into decision-making before energy is consumed, rather than after it's reported.

**Expected Outcome:** Identification of high-impact optimization opportunities and improved decision-making around AI workload execution, with potential for meaningful emission reduction when validated on real workloads.

---

## 1. Problem Statement — When Carbon Becomes an Invisible Engineering Variable

Recent studies in sustainable computing and Green AI consistently highlight a paradox in modern AI operations: while organizations can measure energy consumption at an infrastructure level, **carbon rarely participates in engineering decisions at the moment those decisions are made**.

In large-scale AI deployments, execution choices — such as *when to run a model, how often to retrain it, or whether to scale it aggressively* — are primarily driven by performance, cost, and reliability considerations. Environmental impact, when assessed, is typically reviewed retrospectively as part of sustainability reporting or audits.

### The Structural Blind Spot

This creates a fundamental disconnect in AI systems:

* **Engineers optimize for:** Accuracy, latency, throughput
* **Operations teams optimize for:** Availability, cost, resource efficiency
* **Carbon impact remains:** An external metric, detached from execution logic

**Illustrative scenario:**

A fraud detection model runs hourly around the clock. The business requirement is detection within a two-hour window. Running at this higher frequency consumes more energy than necessary to meet the stated SLA, yet this optimization opportunity remains invisible because carbon isn't evaluated during scheduling decisions.

As a result, AI workloads that are technically correct and economically viable may still be environmentally inefficient — not due to negligence, but due to **the absence of carbon as a first-class engineering signal**.

This proposal approaches the problem of measuring AI's carbon footprint from a different angle: **how can carbon awareness be embedded directly into AI execution decisions, before energy is consumed, rather than after it is reported?**

---

## 2. Limitations of Current Sustainability-Oriented AI Monitoring

A growing body of Green IT and sustainable AI research indicates that visibility alone does not change system behavior. While dashboards and carbon reports are essential for awareness, they fall short as mechanisms for intervention in AI-heavy environments.

Three practical limitations emerge repeatedly across enterprise deployments:

### 2.1 Temporal Disconnect
Carbon insights are often generated after model execution, leaving no opportunity to influence scheduling, scaling, or execution strategy.

**Example:** A training job runs during high grid carbon intensity hours. The emission report arrives after completion, too late to inform scheduling decisions.

### 2.2 Context-Free Metrics
Emission data is typically detached from workload intent. Systems lack the ability to distinguish between business-critical AI tasks and deferrable analytical jobs.

**Example:** A dashboard displays aggregate emissions per model but provides no context about business requirements, making it unclear which emissions are necessary versus which represent optimization opportunities.

### 2.3 Cognitive Overload for Engineers
Raw sustainability metrics increase informational load without clarifying actionable next steps.

**Example:** Being told total monthly emissions doesn't indicate which specific model, schedule, or configuration to adjust first.

Consequently, sustainability remains adjacent to engineering workflows rather than embedded within them — limiting its operational impact.

### Why Traditional Dashboards Fall Short

| What They Show | What Engineers Need |
|----------------|---------------------|
| Aggregate emission totals | Per-model attribution |
| Historical charts | Real-time decision support |
| Generic metrics | Context-aware recommendations |
| After-the-fact reports | Before-execution guidance |

---

## 3. A Different Lens — Treating Carbon as an Engineering Constraint

This proposal adopts a different perspective:

> **Carbon should be treated as an execution constraint, similar to cost, latency, or reliability — not just a reporting metric.**

When carbon is introduced into the decision layer, engineers can make informed trade-offs such as:

* Should this model run now or during a lower-impact time window?
* Does the increased execution frequency provide proportional business value?
* Can the same business outcome be achieved through alternative execution patterns?

### The Shift in Thinking

**Traditional approach:**
```
Run Model → Measure Emissions → Report to ESG Team → Hope for improvement
```

**Carbon-aware approach:**
```
Evaluate Carbon Context → Decide Execution Strategy → Run Optimally → Measure Impact
```

This mindset shift forms the foundation of the proposed solution.

---

## 4. Proposed Solution — Carbon-Aware Execution Intelligence Agent

The proposed system is a **Carbon-Aware Execution Intelligence Agent** designed to assist Green IT and AI engineers during execution planning and runtime review.

Rather than acting as an autonomous controller, the agent functions as a **decision companion** that:

* Measures carbon emissions at the AI workload level
* Interprets emissions in execution context
* Produces clear, explainable recommendations

### Core Philosophy

The goal is not automation, but **better engineering judgment supported by data**.

Think of it as a **sustainability co-pilot** — it suggests, you decide.

### What Makes This "Agentic"

Traditional dashboards show data and wait for humans to determine next steps.

An agentic system observes patterns, contextualizes against requirements, reasons through optimization opportunities, and recommends specific actions with clear rationale.

The agent doesn't just report — it reasons through potential solutions.

---

## 5. Decision-First System Architecture

Unlike traditional monitoring pipelines, this architecture is organized around *decision-making* rather than data collection.

### System Design Flow

```
┌────────────────────────────────────────────────────┐
│     AI WORKLOADS (Production Environment)          │
│  [Fraud Detection] [Recommendations] [Forecasting] │
└─────────────────────┬──────────────────────────────┘
                      │
                      ↓
┌────────────────────────────────────────────────────┐
│  EXECUTION CONTEXT LAYER                           │
│  • Business criticality (critical vs deferrable)   │
│  • Urgency (real-time vs batch)                    │
│  • Acceptable execution window                     │
└─────────────────────┬──────────────────────────────┘
                      │
                      ↓
┌────────────────────────────────────────────────────┐
│  CARBON OBSERVABILITY LAYER                        │
│  • Prometheus (CPU/GPU/memory metrics)             │
│  • CodeCarbon (CO₂e calculation)                   │
│  • Grid carbon intensity data                      │
└─────────────────────┬──────────────────────────────┘
                      │
                      ↓
┌────────────────────────────────────────────────────┐
│  AGENTIC REASONING LAYER (LangChain + Python)      │
│  • Pattern detection                               │
│  • Trade-off evaluation                            │
│  • Recommendation generation                       │
│  • Explainable rationale                           │
└─────────────────────┬──────────────────────────────┘
                      │
                      ↓
┌────────────────────────────────────────────────────┐
│  RECOMMENDATION INTERFACE (Streamlit Dashboard)    │
│  • Ranked suggestions                              │
│  • Impact prediction                               │
│  • Approval workflow                               │
│  • Feedback loop                                   │
└────────────────────────────────────────────────────┘
```

### 5.1 Execution Context Layer

**Purpose:** Capture *why* an AI task is running

**Data collected:**
- Business criticality (critical vs deferrable)
- Urgency (real-time vs batch)
- Acceptable execution window
- Required versus current frequency

**Example context:**
```json
{
  "model": "fraud_detection_v2",
  "criticality": "high",
  "sla": "2_hours",
  "current_schedule": "every_1_hour",
  "acceptable_delay": "up_to_2_hours"
}
```

### 5.2 Carbon Observability Layer

**Purpose:** Measure *what the task costs environmentally*

**Components:**
- **Prometheus:** Real-time CPU/GPU/memory usage tracking
- **CodeCarbon:** CO₂e emission calculation based on regional grid intensity
- **Workload metadata:** Runtime duration, resource allocation

**Example measurement approach:**
```python
from codecarbon import EmissionsTracker

tracker = EmissionsTracker(project_name="fraud_detection")
tracker.start()

# Model execution
model.predict(batch_data)

emissions = tracker.stop()  # Returns emissions measurement
```

### 5.3 Agentic Reasoning Layer (Python + LangChain)

**Purpose:** Correlate execution context with carbon cost to evaluate trade-offs

**Reasoning process:**
1. **Analyze current state:** Examine execution patterns and emission levels
2. **Check requirements:** Compare against stated business SLAs
3. **Calculate optimization potential:** Identify gaps between current and optimal execution
4. **Validate impact:** Assess business risk of proposed changes
5. **Generate recommendation:** Formulate actionable suggestion with rationale

**Agent logic example:**
```python
if (emissions_per_run > threshold 
    and current_frequency > required_frequency 
    and criticality != "real_time"):
    
    recommendation = {
        "action": "reduce_frequency",
        "from": current_schedule,
        "to": optimized_schedule,
        "estimated_impact": "significant_reduction",
        "business_risk": "low",
        "confidence": "high"
    }
```

### 5.4 Recommendation Layer

**Purpose:** Generate ranked, actionable suggestions

**Output format:**
```
HIGH IMPACT OPPORTUNITY

Model: fraud_detection_v2
Current: Runs hourly
Issue: Over-serving stated SLA requirements

Recommended Action:
→ Adjust schedule to align with business requirements

Estimated Outcome:
✓ Significant emission reduction
✓ Maintained service level compliance
✓ Low business risk

[Review Details] [Simulate First] [Dismiss]
```

### 5.5 Human Feedback Loop

All recommendations remain advisory, ensuring human-in-the-loop control and operational safety.

**Why this matters:**
- Engineers retain final decision authority
- No unexpected system changes
- Builds trust through transparency
- Allows gradual adoption and validation

This structure mirrors Tech Mahindra's Green IT systems while shifting emphasis from monitoring-first to **decision-first intelligence**.

---

## 6. Agent Reasoning Flow

The agent follows a transparent reasoning cycle:

### Step 1: Observe
Capture compute usage for each AI workload in real-time via Prometheus and CodeCarbon.

### Step 2: Measure
Calculate CO₂e emissions using CodeCarbon, factoring in:
- Regional grid carbon intensity
- Hardware efficiency
- Runtime duration

### Step 3: Contextualize
Associate emissions with task purpose and urgency from execution context layer.

### Step 4: Reason
Evaluate trade-offs between carbon impact and business value:
- Is this workload running more frequently than business requirements dictate?
- Could it be deferred to a lower-impact time window?
- Is the resource allocation optimal for the task?

### Step 5: Recommend
Propose the most sustainable execution option with clear rationale.

---

## 7. Carbon Efficiency Score — A Prioritization Tool, Not a Formula

To support comparison across workloads, the agent uses a **Carbon Efficiency Score (CES)**.

### What CES Represents

Rather than acting as a rigid equation, CES serves as a **relative indicator** that answers:

> "Which AI tasks may represent the best optimization opportunities relative to business value?"

### How It Works

CES considers three dimensions:

1. **Carbon intensity:** Emissions per execution
2. **Business value:** Criticality and frequency requirements
3. **Optimization potential:** Gap between current and optimal execution

**Higher CES:** Better balance of business value to emissions  
**Lower CES:** Potential optimization opportunity worth investigating

### Example Comparison

| Model | Business Value | Relative CES | Investigation Priority |
|-------|----------------|--------------|------------------------|
| Real-time fraud detection | Critical | Higher | Maintain current optimization |
| Weekly sales report | Low urgency | Lower | Review for optimization potential |
| Customer recommendations | High | Higher | Good balance |

This allows Green IT teams to prioritize optimization efforts where they may have the most impact.

**Important:** CES is not a definitive metric — it's a decision-support tool to guide human judgment.

---

## 8. Concrete Example — Fraud Detection Analysis

### Current State

**Model:** fraud_detection_v2  
**Purpose:** Detect fraudulent transactions  
**Current execution:** Hourly, continuously  
**Business requirement:** Detection within 2-hour window

### Agent Analysis

```
Agent observes:
- Model runs 24 times daily
- Execution frequency exceeds stated SLA by factor of 2

Agent reasons:
- Business SLA: 2-hour window
- Current: 1-hour frequency (over-serving stated requirement)
- Opportunity: Frequency adjustment without SLA impact

Agent recommends:
Action: Adjust from hourly to bi-hourly execution
Estimated outcome: Significant emission reduction potential
Risk: Low (maintains comfortable SLA margin)
```

### Predicted Outcome

**After optimization:**
- Execution frequency aligned with business requirements
- Maintained service level compliance
- Material emission reduction
- No business impact

### Implementation

1. Engineer reviews recommendation in dashboard
2. Selects "Simulate First" to validate in test environment
3. Monitors business metrics over validation period
4. Approves permanent change if validated
5. System adjusts schedule per approval

**This demonstrates carbon-aware decision-making in practice.**

---

## 9. Prototype Validation (Simulated)

A lightweight Python prototype was developed to validate the feasibility of carbon-aware decision logic.

### Prototype Scope

**What it demonstrates:**
- Simulated AI workload execution scenarios
- CO₂e measurement using CodeCarbon
- Context-aware recommendation logic
- Basic decision-support interface

**What it validates:**
- Carbon measurement at workload level is technically feasible
- Context-aware recommendations can be generated programmatically
- Decision logic can distinguish between different workload types
- Integration with CodeCarbon library functions as expected

### Key Technical Learnings

1. **CodeCarbon integration works reliably** for Python-based ML workloads
2. **Grid carbon intensity varies significantly** throughout the day — timing decisions matter
3. **Contextual metadata is essential** — emissions data alone isn't actionable
4. **Human approval workflow is critical** for operational trust and safety

### Prototype Architecture

```python
# Core components implemented

class CarbonAwareAgent:
    def measure_emissions(self, workload):
        # Uses CodeCarbon to track CO₂
        
    def get_execution_context(self, workload):
        # Retrieves business criticality, SLA
        
    def generate_recommendation(self, workload, emissions, context):
        # Applies reasoning logic
        
    def predict_impact(self, recommendation):
        # Estimates potential optimization outcomes
```

### Sample Output

```
=== Carbon-Aware Execution Analysis ===

Workload: batch_sales_report
Current Schedule: Daily at 2 PM
Business Criticality: Low (deferrable)

Recommendation:
→ Consider moving to off-peak hours (lower grid intensity)
→ Estimated outcome: Meaningful reduction in carbon footprint
→ Business impact: None (timing flexibility available)

[Review Details] [Simulate] [Dismiss]
```

### Repository

**GitHub:** [Link to be provided upon request]  
**Demo:** [Optional walkthrough available]

**Important limitation:** Exact carbon savings require validation on production workloads with real business data. This prototype demonstrates the feasibility of the approach and reasoning logic, not production-validated emission reductions.

---

## 10. Alignment with Green IT Vision

The proposed approach aligns with existing Green IT initiatives by:

### Enhancing Workload-Level Insights
- Granular emissions tracking beyond infrastructure-level monitoring
- Decision-support for cloud operations
- Real-time optimization opportunities

### Supporting Green IT Transformation
- Execution-aware sustainability approach
- Integration into engineering workflows
- Enabling continuous improvement culture

### Facilitating ESG Reporting
- Granular, attributable emissions data
- Support for reporting standards
- Demonstrable sustainability actions

The agent is designed to complement the existing sustainability ecosystem as an integrated decision layer.

---

## 11. Boundaries and Responsible Design

To ensure safety and trust, the system intentionally does not:

### What the Agent Does NOT Do

1. **Perform autonomous shutdowns**
   - Never stops running workloads without explicit approval
   
2. **Modify infrastructure automatically**
   - All changes require human confirmation
   
3. **Replace models or workloads**
   - Suggests alternatives, doesn't force implementation
   
4. **Override business priorities**
   - Carbon is one factor among many in decision-making
   
5. **Make unilateral decisions**
   - Functions as advisory system, not autonomous controller

### What the Agent DOES Do

1. **Observe and measure** carbon emissions accurately
2. **Reason and recommend** optimization opportunities
3. **Explain decisions** with clear rationale
4. **Predict potential impact** before changes are made
5. **Support learning** through feedback incorporation

### Design Principles

- **Transparency:** Every recommendation includes reasoning
- **Safety:** No automated execution without approval
- **Respect:** Engineers remain in control
- **Trust:** Build confidence through consistent accuracy and explainability

**The agent augments engineers — it does not override them.**

This approach ensures the system enhances decision-making without introducing operational risk.

---

## 12. Feasibility for an Internship

This solution is feasible within an internship scope because:

### 1. Problem is Well-Defined
The problem statement provides clear direction and requirements.

### 2. Tech Stack is Specified
Python, CodeCarbon, Prometheus, LangChain, Streamlit — all explicitly suggested.

### 3. Can Start with Simulated Workloads
No production access required to build and validate core decision logic.

### 4. Modular Architecture
Can be developed incrementally:
- Month 1-2: Carbon tracking and measurement validation
- Month 3-4: Agent reasoning and recommendation logic
- Month 5-6: Dashboard interface and refinement

### 5. Learning-Oriented
Provides exposure to:
- Green IT principles and practices
- Agentic AI system design
- Production software considerations
- Enterprise sustainability approaches

### 6. Mentorship Opportunities
Areas where guidance would be valuable:
- Production-grade design patterns
- Integration approaches with existing tools
- Enterprise deployment considerations

This makes the proposal practical, buildable, and educational — well-suited for an internship project.

---

## 13. Conclusion

This proposal reframes AI sustainability from a reporting exercise into an **engineering decision problem**.

### The Core Shift

Most sustainability tools ask: **"How much did we emit?"**  
This system asks: **"Should we execute this workload now, or could we do it more sustainably?"**

That shift — from measurement to decision — is where practical impact becomes possible.

### Why This Approach Has Potential

1. **Practical:** Uses the recommended technology stack
2. **Safe:** Human-in-the-loop by design
3. **Actionable:** Focuses on specific, implementable recommendations
4. **Scalable:** Starts with simulation, can grow with validation
5. **Aligned:** Complements existing Green IT initiatives

### What I'm Proposing

Build a decision companion for AI sustainability that:
- Embeds carbon awareness into engineering workflows
- Identifies optimization opportunities before waste occurs
- Maintains safety through human oversight
- Demonstrates feasibility through working prototype

### What I Hope to Contribute

As an intern, I bring thoughtful problem analysis, technical foundation in the required stack, and commitment to building something meaningful.

I'm not claiming this is production-ready. I'm proposing an approach worth exploring, with guidance from experienced Green IT practitioners.

---
