"""
FIXED: Updated inner_team.py with proper tool integration
"""
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
from config import OPENAI_CONFIG
from tools.environmental_tools import dynamic_environmental_data_tool
from tools.web_search_tools import dynamic_web_search_tool
from tools.analysis_tools import dynamic_data_analysis_tool, report_generation_tool
import json
from datetime import datetime

def create_model_client():
    """Create OpenAI model client for agents"""
    return OpenAIChatCompletionClient(**OPENAI_CONFIG)

class ResearchAgent(AssistantAgent):
    """FIXED: Research Agent with proper AutoGen 0.5.7 tool integration"""
    
    def __init__(self, name="research_specialist"):
        system_message = """You are a Research Specialist with real data collection tools.

Your capabilities:
1. Environmental data collection with location-specific information
2. Web search with relevance filtering
3. Multi-source data validation

Always use your tools to gather real information. Request human approval for research plans."""

        # FIXED: Proper FunctionTool creation for AutoGen 0.5.7
        tools = [
            FunctionTool(
                dynamic_environmental_data_tool,
                description="Get real environmental pollution data for any location with year-over-year comparisons"
            ),
            FunctionTool(
                dynamic_web_search_tool, 
                description="Search the web for current information on any topic"
            )
        ]

        super().__init__(
            name=name,
            model_client=create_model_client(),
            system_message=system_message,
            tools=tools
        )
    
    def create_research_plan(self, topic):
        """Create research plan using real tools"""
        return f"""
📋 RESEARCH PLAN FOR: {topic}

🔧 REAL TOOLS AVAILABLE:
- Environmental Data Tool: Live pollution monitoring data
- Web Search Tool: Current information with date filtering

⚡ EXECUTION STRATEGY:
1. Use environmental data tool if topic involves pollution/environment
2. Use web search tool for general information gathering
3. Validate findings across multiple sources

🎯 EXPECTED OUTPUTS:
- Real-time data collection
- Current, verified information
- Multi-source validation

HUMAN_APPROVAL_NEEDED: Please approve this tool-based research approach.
        """

class AnalysisAgent(AssistantAgent):
    """FIXED: Analysis Agent with proper tool integration"""
    
    def __init__(self, name="analysis_specialist"):
        system_message = """You are a Data Analysis Specialist with real analytical capabilities.

Use your analysis tool to process research data and generate insights.
Request human validation for analysis findings."""

        tools = [
            FunctionTool(
                dynamic_data_analysis_tool,
                description="Perform comprehensive statistical analysis on research data"
            )
        ]

        super().__init__(
            name=name,
            model_client=create_model_client(),
            system_message=system_message,
            tools=tools
        )
    
    def analyze_data(self, research_data):
        """Analyze data using real analysis tools"""
        return f"""
📊 DATA ANALYSIS REQUEST

🔧 ANALYSIS TOOL READY:
- Statistical Analysis: Real mathematical computations
- Pattern Recognition: Trend identification
- Quality Assessment: Data reliability scoring

📈 DATA TO ANALYZE:
{research_data[:200] if len(research_data) > 200 else research_data}...

HUMAN_VALIDATION_NEEDED: Please validate the analysis approach.
        """

class ValidationAgent(AssistantAgent):
    """FIXED: Validation Agent with report generation"""
    
    def __init__(self, name="validation_specialist"):
        system_message = """You are a Validation Specialist with report generation capabilities.

Use your report generation tool to create comprehensive final reports.
Request human final approval for all recommendations."""

        tools = [
            FunctionTool(
                report_generation_tool,
                description="Generate comprehensive reports from research and analysis data"
            )
        ]

        super().__init__(
            name=name,
            model_client=create_model_client(),
            system_message=system_message,
            tools=tools
        )
    
    def validate_and_recommend(self, research_results, analysis_results):
        """Create recommendations using report generation tool"""
        return f"""
✅ VALIDATION & REPORT GENERATION

🔧 REPORT GENERATION TOOL ACTIVE:
- Comprehensive reporting with executive summary
- Quality validation with metrics
- Implementation planning

📋 INPUT DATA:
- Research Results: {len(str(research_results))} characters
- Analysis Results: {len(str(analysis_results))} characters

HUMAN_FINAL_APPROVAL_NEEDED: Please approve final report generation.
        """

# InnerTeamUserProxy remains the same as in previous fix
class InnerTeamUserProxy(UserProxyAgent):
    """Real Human-in-the-Loop UserProxyAgent"""
    
    def __init__(self, name="inner_team_human"):
        super().__init__(
            name=name,
            description="Human supervisor for inner team decisions",
            input_func=self.get_real_human_input
        )
        
        self.decision_history = []
    
    def get_real_human_input(self, prompt):
        """Real human input - pauses execution"""
        print(f"\n{'='*60}")
        print("🤝 HUMAN INPUT REQUIRED - EXECUTION PAUSED")
        print(f"{'='*60}")
        print(f"Agent: {self.name}")
        print(f"{'='*60}")
        print(prompt)
        print(f"\n{'='*60}")
        print("Response Options:")
        print("• APPROVE - Accept the proposal")
        print("• REJECT: [reason] - Reject with specific reason")
        print("• MODIFY: [changes] - Request modifications")
        print("• OVERRIDE: [decision] - Override agent decision")
        print(f"{'='*60}")
        
        while True:
            try:
                user_input = input("👤 Your response: ").strip()
                
                if not user_input:
                    print("❌ Please provide a response.")
                    continue
                
                if self._is_valid_response(user_input):
                    print(f"✅ Response recorded: {user_input}")
                    break
                else:
                    print("❌ Please start with: APPROVE, REJECT:, MODIFY:, or OVERRIDE:")
                    
            except KeyboardInterrupt:
                print("\n🛑 Using default APPROVE due to interruption")
                user_input = "APPROVE - Default approval"
                break
        
        self.decision_history.append({
            "prompt": prompt[:100] + "...",
            "response": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        return user_input
    
    def _is_valid_response(self, response):
        """Check if response starts with valid command"""
        valid_starts = ["APPROVE", "REJECT:", "MODIFY:", "OVERRIDE:"]
        return any(response.upper().startswith(start) for start in valid_starts)
    
    def get_decision_summary(self):
        """Get summary of human decisions"""
        return {
            "total_decisions": len(self.decision_history),
            "decision_types": {},
            "last_decision": self.decision_history[-1] if self.decision_history else None
        }
