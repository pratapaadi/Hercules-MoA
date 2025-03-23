from typing import Dict
import asyncio
from .base_agent import GeminiAgent, AggregatorAgent

class MixtureOfAgents:
    def __init__(self, api_key: str):
        self.agents = [
            GeminiAgent(
                api_key=api_key,
                agent_id="Agent_1",
                role="System Architect",
                expertise="software architecture and system design",
                specializations=[
                    "distributed systems",
                    "scalable architectures",
                    "design patterns",
                    "system integration",
                    "API design"
                ]
            ),
            GeminiAgent(
                api_key=api_key,
                agent_id="Agent_2",
                role="Technical Implementation Specialist",
                expertise="code implementation and best practices",
                specializations=[
                    "algorithm optimization",
                    "code quality",
                    "testing strategies",
                    "performance tuning",
                    "security practices"
                ]
            ),
            GeminiAgent(
                api_key=api_key,
                agent_id="Agent_3",
                role="Business Analysis Expert",
                expertise="business requirements and solution strategy",
                specializations=[
                    "requirement analysis",
                    "cost-benefit analysis",
                    "risk assessment",
                    "stakeholder management",
                    "market analysis"
                ]
            ),
            GeminiAgent(
                api_key=api_key,
                agent_id="Agent_4",
                role="Integration & DevOps Specialist",
                expertise="system integration and deployment",
                specializations=[
                    "CI/CD pipelines",
                    "cloud infrastructure",
                    "monitoring solutions",
                    "deployment strategies",
                    "automation frameworks"
                ]
            )
        ]
        self.aggregator = AggregatorAgent(api_key)
    
    async def process_prompt(self, prompt: str) -> Dict:
        tasks = [agent.process(prompt) for agent in self.agents]
        responses = await asyncio.gather(*tasks)
        
        response_dict = {
            f"{agent.role} ({agent.agent_id})\nExpertise: {agent.expertise}": response 
            for agent, response in zip(self.agents, responses)
        }
        
        final_response = await self.aggregator.aggregate(response_dict, prompt)
        
        return {
            "individual_responses": response_dict,
            "aggregated_response": final_response
        }