"""
tools/dispatcher.py - Dynamic Tool Selection and Dispatch System
Intelligently selects and executes tools based on task analysis
"""
import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class DynamicToolDispatcher:
    """
    Intelligently selects and calls appropriate tools based on task content
    This is the core dispatcher that analyzes tasks and routes to appropriate tools
    """
    
    def __init__(self):
        # Tool selection patterns for different domains
        self.tool_patterns = {
            'environmental_data': [
                r'pollution', r'environment', r'air quality', r'water quality',
                r'pm2\.5', r'pm10', r'carbon', r'emissions', r'climate', r'contamination'
            ],
            'web_search': [
                r'news', r'current', r'latest', r'recent', r'today', r'search',
                r'research', r'study', r'report', r'analysis', r'information'
            ],
            'market_data': [
                r'stock', r'market', r'price', r'finance', r'economy',
                r'business', r'revenue', r'profit', r'sales', r'trading'
            ],
            'weather_data': [
                r'weather', r'temperature', r'rain', r'storm', r'forecast',
                r'humidity', r'wind', r'precipitation'
            ],
            'data_analysis': [
                r'analyze', r'analysis', r'compare', r'comparison', r'evaluate',
                r'assess', r'calculate', r'measure', r'statistics'
            ]
        }
        
        # Location patterns for geographic extraction
        self.location_patterns = [
            r'in ([A-Za-z\s]+)', r'for ([A-Za-z\s]+)', 
            r'from ([A-Za-z\s]+)', r'([A-Za-z\s]+) pollution',
            r'([A-Za-z\s]+) environment', r'([A-Za-z\s]+) data'
        ]
        
        # Time comparison patterns
        self.time_patterns = [
            r'last year', r'previous year', r'2023', r'2024', r'2025',
            r'compared to', r'vs', r'versus', r'difference', r'change from'
        ]
    
    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """
        Main method: Analyze task and determine which tools to use
        
        Args:
            task_description (str): The task to analyze
            
        Returns:
            Dict: Tool selection and parameters
        """
        task_lower = task_description.lower()
        selected_tools = []
        parameters = {}
        
        # Extract context information
        location = self._extract_location(task_description)
        has_comparison = self._detect_time_comparison(task_lower)
        complexity = self._assess_complexity(task_description)
        
        # Select appropriate tools based on patterns
        for tool_type, patterns in self.tool_patterns.items():
            if any(re.search(pattern, task_lower) for pattern in patterns):
                selected_tools.append(tool_type)
                parameters[tool_type] = self._get_tool_parameters(
                    tool_type, task_description, location, has_comparison
                )
        
        # Ensure at least one tool is selected
        if not selected_tools:
            selected_tools.append('web_search')
            parameters['web_search'] = {
                'query': task_description,
                'date_filter': 'recent' if has_comparison else 'all'
            }
        
        # Add analysis tool if multiple data sources
        if len(selected_tools) > 1 and 'data_analysis' not in selected_tools:
            selected_tools.append('data_analysis')
            parameters['data_analysis'] = {'analysis_type': 'comparative'}
        
        return {
            'tools': selected_tools,
            'parameters': parameters,
            'task_complexity': complexity,
            'execution_strategy': self._determine_execution_strategy(selected_tools),
            'extracted_context': {
                'location': location,
                'has_comparison': has_comparison,
                'task_type': self._classify_task_type(task_lower)
            }
        }
    
    def _extract_location(self, task_description: str) -> str:
        """Extract geographic location from task description"""
        for pattern in self.location_patterns:
            match = re.search(pattern, task_description, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                # Filter out common non-location words
                if location.lower() not in ['data', 'information', 'analysis', 'report']:
                    return location
        return "global"
    
    def _detect_time_comparison(self, task_text: str) -> bool:
        """Detect if task requires time-based comparison"""
        return any(re.search(pattern, task_text) for pattern in self.time_patterns)
    
    def _classify_task_type(self, task_text: str) -> str:
        """Classify the type of task being requested"""
        if any(word in task_text for word in ['pollution', 'environment', 'climate']):
            return 'environmental'
        elif any(word in task_text for word in ['market', 'stock', 'finance']):
            return 'financial'
        elif any(word in task_text for word in ['weather', 'temperature', 'forecast']):
            return 'weather'
        elif any(word in task_text for word in ['analyze', 'compare', 'evaluate']):
            return 'analytical'
        else:
            return 'general'
    
    def _get_tool_parameters(self, tool_type: str, task: str, location: str, has_comparison: bool) -> Dict[str, Any]:
        """Generate tool-specific parameters based on context"""
        base_params = {
            'task_context': task,
            'location': location,
            'timestamp': datetime.now().isoformat()
        }
        
        if tool_type == 'environmental_data':
            return {
                **base_params,
                'include_comparison': has_comparison,
                'metrics': self._extract_pollution_metrics(task.lower()),
                'data_source': 'real_time_monitoring'
            }
        elif tool_type == 'web_search':
            return {
                **base_params,
                'query': task,
                'date_filter': 'recent' if has_comparison else 'all',
                'result_limit': 10
            }
        elif tool_type == 'data_analysis':
            return {
                **base_params,
                'analysis_type': 'comparative' if has_comparison else 'descriptive',
                'include_visualization': True
            }
        elif tool_type == 'weather_data':
            return {
                **base_params,
                'include_forecast': True,
                'historical_data': has_comparison
            }
        else:
            return base_params
    
    def _extract_pollution_metrics(self, task_text: str) -> List[str]:
        """Extract specific pollution metrics mentioned in task"""
        metrics = []
        metric_patterns = {
            'pm2.5': r'pm2\.5|particulate matter 2\.5',
            'pm10': r'pm10|particulate matter 10|dust',
            'no2': r'no2|nitrogen dioxide',
            'so2': r'so2|sulfur dioxide',
            'co': r'\bco\b|carbon monoxide',
            'o3': r'o3|ozone',
            'aqi': r'aqi|air quality index'
        }
        
        for metric, pattern in metric_patterns.items():
            if re.search(pattern, task_text, re.IGNORECASE):
                metrics.append(metric)
        
        return metrics if metrics else ['pm2.5', 'pm10', 'no2']  # default metrics
    
    def _assess_complexity(self, task: str) -> str:
        """Assess task complexity for execution planning"""
        word_count = len(task.split())
        complexity_indicators = ['compare', 'analyze', 'evaluate', 'assessment', 'comprehensive', 'detailed']
        
        has_complex_words = any(indicator in task.lower() for indicator in complexity_indicators)
        
        if word_count > 15 or has_complex_words:
            return 'high'
        elif word_count > 8:
            return 'medium'
        return 'low'
    
    def _determine_execution_strategy(self, tools: List[str]) -> str:
        """Determine how tools should be executed"""
        if len(tools) > 2:
            return 'parallel'  # Execute multiple tools simultaneously
        elif len(tools) == 2:
            return 'sequential'  # Execute one after another
        return 'single'  # Single tool execution
    
    def get_tool_execution_order(self, tools: List[str]) -> List[str]:
        """Determine optimal tool execution order"""
        # Priority order for tool execution
        priority_order = ['environmental_data', 'web_search', 'weather_data', 'market_data', 'data_analysis']
        
        ordered_tools = []
        for tool in priority_order:
            if tool in tools:
                ordered_tools.append(tool)
        
        # Add any remaining tools not in priority list
        for tool in tools:
            if tool not in ordered_tools:
                ordered_tools.append(tool)
        
        return ordered_tools

# Factory function for easy instantiation
def create_tool_dispatcher() -> DynamicToolDispatcher:
    """Factory function to create and return DynamicToolDispatcher instance"""
    return DynamicToolDispatcher()
