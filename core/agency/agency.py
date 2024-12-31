from agency_swarm import Agency
from DocuAgent import DocuAgent
from CEOAgent import CEOAgent
from GitAgent import GitAgent

def create_agency():
    return Agency(
        [CEOAgent, [CEOAgent, DocuAgent],
        [CEOAgent, GitAgent],
        [DocuAgent, GitAgent]],
        shared_instructions='./agency_manifesto.md',
        max_prompt_tokens=25000,
        temperature=0.5,
    )