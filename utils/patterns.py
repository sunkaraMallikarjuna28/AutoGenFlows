"""
Pattern matching and utility functions
Common patterns and helpers used across the system
"""
import re
from typing import List, Dict, Any, Optional

def extract_location_patterns(text: str) -> Optional[str]:
    """Extract location patterns from text"""
    patterns = [
        r'in ([A-Za-z\s]+)',
        r'from ([A-Za-z\s]+)', 
        r'at ([A-Za-z\s]+)',
        r'([A-Za-z\s]+) region',
        r'([A-Za-z\s]+) area'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            location = match.group(1).strip()
            # Filter out common non-location words
            if location.lower() not in ['data', 'information', 'analysis', 'report', 'study']:
                return location
    return None

def extract_time_patterns(text: str) -> Dict[str, Any]:
    """Extract time-related patterns from text"""
    time_info = {
        'has_comparison': False,
        'specific_years': [],
        'time_references': []
    }
    
    # Comparison patterns
    comparison_patterns = [
        r'compared to', r'vs', r'versus', r'than last year',
        r'from last year', r'year over year', r'annually'
    ]
    
    time_info['has_comparison'] = any(
        re.search(pattern, text, re.IGNORECASE) 
        for pattern in comparison_patterns
    )
    
    # Extract years
    year_pattern = r'\b(20\d{2})\b'
    years = re.findall(year_pattern, text)
    time_info['specific_years'] = list(set(years))
    
    # Time reference patterns
    time_patterns = [
        r'last year', r'this year', r'previous year',
        r'recently', r'current', r'latest'
    ]
    
    for pattern in time_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            time_info['time_references'].append(pattern.replace(r'\b', ''))
    
    return time_info

def extract_metric_patterns(text: str) -> List[str]:
    """Extract pollution/environmental metrics from text"""
    metrics = []
    metric_patterns = {
        'pm2.5': [r'pm2\.5', r'pm 2\.5', r'particulate matter 2\.5'],
        'pm10': [r'pm10', r'pm 10', r'particulate matter 10'],
        'no2': [r'no2', r'nitrogen dioxide'],
        'so2': [r'so2', r'sulfur dioxide', r'sulphur dioxide'],
        'co': [r'\bco\b', r'carbon monoxide'],
        'o3': [r'o3', r'ozone'],
        'aqi': [r'aqi', r'air quality index']
    }
    
    for metric, patterns in metric_patterns.items():
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
            metrics.append(metric)
    
    return metrics if metrics else ['pm2.5', 'pm10', 'no2']  # Default

def validate_tool_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and clean tool parameters"""
    validated = {}
    
    # Location validation
    if 'location' in params:
        location = str(params['location']).strip()
        if location and location.lower() != 'none':
            validated['location'] = location
        else:
            validated['location'] = 'global'
    
    # Boolean validations
    boolean_fields = ['include_comparison', 'has_comparison']
    for field in boolean_fields:
        if field in params:
            validated[field] = bool(params[field])
    
    # List validations
    if 'metrics' in params:
        if isinstance(params['metrics'], list):
            validated['metrics'] = [str(m).lower() for m in params['metrics']]
        else:
            validated['metrics'] = ['pm2.5', 'pm10', 'no2']
    
    # String validations
    string_fields = ['query', 'analysis_type', 'report_type']
    for field in string_fields:
        if field in params:
            validated[field] = str(params[field]).strip()
    
    return validated

def format_tool_response(response: str, tool_name: str) -> Dict[str, Any]:
    """Format tool responses consistently"""
    return {
        'tool_name': tool_name,
        'response_data': response,
        'timestamp': '2024-08-06T21:07:00Z',
        'status': 'success' if 'error' not in response.lower() else 'error',
        'data_size': len(response)
    }

def extract_key_insights(text: str) -> List[str]:
    """Extract key insights from text content"""
    insights = []
    
    # Look for improvement indicators
    improvement_patterns = [
        r'improved by (\d+\.?\d*%)', r'decreased by (\d+\.?\d*%)',
        r'reduced by (\d+\.?\d*%)', r'better than'
    ]
    
    for pattern in improvement_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            insights.append(f"Improvement detected: {match}")
    
    # Look for concerning trends
    concern_patterns = [
        r'increased by (\d+\.?\d*%)', r'worsened by (\d+\.?\d*%)',
        r'higher than', r'exceeded.*limit'
    ]
    
    for pattern in concern_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            insights.append(f"Concern identified: {match}")
    
    return insights[:5]  # Limit to top 5 insights

def classify_urgency(content: str) -> str:
    """Classify urgency level based on content"""
    urgent_keywords = ['urgent', 'critical', 'immediate', 'emergency', 'hazardous']
    high_keywords = ['important', 'significant', 'major', 'concerning']
    
    content_lower = content.lower()
    
    if any(keyword in content_lower for keyword in urgent_keywords):
        return 'urgent'
    elif any(keyword in content_lower for keyword in high_keywords):
        return 'high'
    else:
        return 'normal'
