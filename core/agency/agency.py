from agency_swarm import Agency
from .DocuAgent.docuAgent import DocuAgent
from .CEOAgent.CEOAgent import CEOAgent
from .GitAgent.gitAgent import GitAgent
from .ReviewAgent.reviewAgent import ReviewAgent
from .settings.settings import AGENT_SETTINGS
import os

def create_agency():
    # Initialize the agents first
    ceo_agent = CEOAgent()
    docu_agent = DocuAgent()
    git_agent = GitAgent()
    review_agent = ReviewAgent()

    # Create agency with proper communication paths
    return Agency(
        [
            ceo_agent,  # First agent is the main coordinator
            [ceo_agent, docu_agent],  # Connection between CEO and DocuAgent
            [ceo_agent, git_agent],   # Connection between CEO and GitAgent
            [ceo_agent, review_agent], # Connection between CEO and ReviewAgent
            [docu_agent, review_agent], # Connection for documentation review
            [review_agent, docu_agent], # Connection for feedback implementation
            [review_agent, git_agent]   # Connection for committing approved docs
        ],
        shared_instructions=os.path.join(os.path.dirname(__file__), 'agency-manifesto.md'),
        max_prompt_tokens=AGENT_SETTINGS.get("max_prompt_tokens", 25000),
        temperature=AGENT_SETTINGS.get("temperature", 0.5),
    )