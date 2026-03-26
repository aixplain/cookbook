# Customer Analysis Agent

An AI-powered multi-agent system that automatically analyzes customer support data and generates actionable insights and recommendations.

## 🎯 Overview

This system creates a team of three specialized AI agents that work together to transform raw customer support metrics into clear, actionable business intelligence:

- **Data Analyst**: Analyzes support metrics and identifies key patterns
- **Process Optimizer**: Identifies bottlenecks and recommends improvements
- **Report Writer**: Creates executive summaries for decision-makers

## 🚀 Features

- **Automated Analysis**: Processes support data automatically without manual intervention
- **Multi-Agent Collaboration**: Three specialized agents work together with clear task dependencies
- **Markdown Output**: Generates well-formatted reports ready for sharing
- **Customizable LLMs**: Easy to swap different language models for different use cases
- **Error Handling**: Built-in debugging and execution tracing
- **Scalable Architecture**: Easy to extend with additional agents or data sources

## 📋 Prerequisites

- Python 3.7+
- AIXplain SDK
- Valid TEAM_API_KEY

## 🛠️ Installation

1. Install the AIXplain SDK:
```bash
pip install aixplain
```

2. Set your API key:
```python
os.environ["TEAM_API_KEY"] = "YOUR-TEAM-API-KEY"
```

## ��️ Architecture

### Components

1. **Utility Model** (`get_support_data`): Simulates fetching customer support metrics
2. **Data Tool**: Wraps the utility model for agent consumption
3. **Three Specialized Agents**:
   - Data Analyst (analyzes metrics)
   - Process Optimizer (identifies issues and recommendations)
   - Report Writer (creates executive summaries)
4. **Team Orchestrator**: Coordinates agent collaboration

### Task Dependencies

```
Data Analyst → Process Optimizer → Report Writer
     ↓              ↓                ↓
  Analysis → Optimization → Executive Summary
```

## ⚙️ Configuration

### Swapping LLMs

To use different language models, simply change the `llm_id` parameter in each agent:

```python
data_analyst = AgentFactory.create(
    name="Data Analyst V6",
    # ... other parameters ...
    llm_id="YOUR-LLM-ID"  # Change this to use different models
)
```

### Customizing Data Source

Replace the `get_support_data` function with your actual data fetching logic:

```python
def get_support_data(dummy: str = "unused"):
    # Replace with your actual data fetching code
    # e.g., API calls to your support system
    return your_actual_support_data
```

## 🚀 Usage

1. **Run the script**:
```bash
python customer_analysis.py
```

2. **Monitor execution**:
   - The script will deploy all agents and tools
   - Run the analysis with the team
   - Display results and debug information

3. **Review output**:
   - Analysis results in markdown format
   - Debug execution steps for troubleshooting

## �� Sample Output

The system generates a comprehensive analysis including:

- **Top Issues**: Ranked by volume and impact
- **Performance Metrics**: SLA compliance, response times, satisfaction scores
- **Key Trends**: Month-over-month changes and patterns
- **Process Issues**: Identified bottlenecks and inefficiencies
- **Recommendations**: Specific actionable improvements
- **Executive Summary**: High-level insights for decision-makers

## 🔍 Debugging

The system includes comprehensive debugging:

- Execution step tracing
- Error handling with detailed messages
- Intermediate step logging
- Timeout and iteration controls

## 🎯 Customization Examples

### Adding New Agents

```python
new_agent = AgentFactory.create(
    name="Custom Agent",
    description="Your custom functionality",
    instructions="Your agent instructions",
    tasks=[your_task],
    llm_id="YOUR-LLM-ID"
)
```

### Modifying Task Dependencies

```python
custom_task = AgentTask(
    name="custom_task",
    description="Your task description",
    dependencies=["analyze_support_data"]  # Depend on existing tasks
)
```

### Changing Output Format

```python
result = support_team.run(
    query="Your query",
    output_format=OutputFormat.JSON,  # Change output format
    max_iterations=50,
    timeout=600
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the debug output for execution traces
- Review the AIXplain SDK documentation
- Ensure your API key is valid and has proper permissions
