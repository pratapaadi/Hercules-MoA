import google.generativeai as genai
from typing import Dict
import json

class PromptTemplates:
    CODE_ANALYSIS = """
    Technical Analysis Required:
    - Architecture considerations
    - Code implementation details
    - Best practices and patterns
    - Performance implications
    - Security considerations
    """
    
    BUSINESS_ANALYSIS = """
    Business Context Required:
    - Use case analysis
    - Stakeholder considerations
    - Business requirements
    - ROI implications
    - Market factors
    """
    
    IMPLEMENTATION_GUIDE = """
    Implementation Details Required:
    - Step-by-step guide
    - Code examples
    - Testing strategies
    - Deployment considerations
    - Maintenance guidelines
    """

class GeminiAgent:
    def __init__(self, api_key: str, agent_id: str, role: str, expertise: str, specializations: list):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.agent_id = agent_id
        self.role = role
        self.expertise = expertise
        self.specializations = specializations
        self.prompt_templates = PromptTemplates()
        
    def get_context_prompt(self, prompt: str) -> str:
        context_prompt = f"""
        Analyze this prompt and determine the primary context required:
        {prompt}
        
        Identify if this requires:
        1. Technical analysis and code implementation
        2. Business analysis and strategy
        3. Implementation guidance and examples
        
        Return the most relevant context number.
        """
        try:
            response = self.model.generate_content(context_prompt)
            return response.text.strip()
        except:
            return "1"
        
    async def process(self, prompt: str) -> str:
        context_type = self.get_context_prompt(prompt)
        
        additional_context = ""
        if context_type == "1":
            additional_context = self.prompt_templates.CODE_ANALYSIS
        elif context_type == "2":
            additional_context = self.prompt_templates.BUSINESS_ANALYSIS
        else:
            additional_context = self.prompt_templates.IMPLEMENTATION_GUIDE
            
        enhanced_prompt = f"""
        Role: {self.role}
        Expertise: {self.expertise}
        Specializations: {', '.join(self.specializations)}
        
        You are an advanced AI agent specialized in {self.expertise} with deep knowledge in {', '.join(self.specializations)}.
        
        Original Question/Task: {prompt}
        
        {additional_context}
        
        Approach the analysis using these steps:
        
        1. Initial Assessment:
           - Problem classification
           - Key requirements
           - Technical/business constraints
           - Potential challenges
        
        2. Detailed Analysis:
           - Architecture/design considerations
           - Technical feasibility
           - Implementation approach
           - Best practices
        
        3. Code and Implementation (if applicable):
           - Provide relevant code examples
           - Include implementation details
           - Consider different programming languages/frameworks
           - Address error handling
        
        4. Business Impact (if applicable):
           - Scalability considerations
           - Maintenance implications
           - Resource requirements
           - Risk assessment
        
        5. Recommendations:
           - Concrete solutions
           - Alternative approaches
           - Trade-offs analysis
           - Next steps
        
        Format your response with clear sections and include code examples in markdown format when applicable.
        """
        
        try:
            response = self.model.generate_content(enhanced_prompt)
            return response.text
        except Exception as e:
            return f"Error from {self.role} ({self.agent_id}): {str(e)}"

class AggregatorAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def aggregate(self, responses: Dict[str, str], original_prompt: str) -> str:
        aggregation_prompt = f"""
        You are an advanced synthesis engine responsible for creating a comprehensive solution from multiple expert perspectives.
        
        Original Question/Task: {original_prompt}
        
        Expert Responses:
        {json.dumps(responses, indent=2)}
        
        Synthesize a solution following these steps:
        
        1. Executive Summary:
           - Key findings
           - Main recommendations
           - Critical insights
        
        2. Technical Analysis:
           - Architecture overview
           - Implementation approach
           - Code examples and patterns
           - Technical considerations
        
        3. Business Perspective:
           - Strategic alignment
           - Resource implications
           - Risk assessment
           - ROI considerations
        
        4. Implementation Guide:
           - Step-by-step approach
           - Best practices
           - Testing strategy
           - Deployment considerations
        
        5. Synthesis of Expert Insights:
           - Common patterns
           - Unique perspectives
           - Conflicting viewpoints resolution
           - Enhanced solutions
        
        Format the response with clear sections and include code examples in markdown format where relevant.
        """
        
        try:
            response = self.model.generate_content(aggregation_prompt)
            return response.text
        except Exception as e:
            return f"Aggregation Error: {str(e)}"