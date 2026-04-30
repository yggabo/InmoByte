from app.core.extensions import db
from app.api.agents.models import Agent


def get_all_agents(status_filter=None):
    query = Agent.query
    if status_filter is not None:
        query = query.filter(Agent.status == status_filter)
    return query.all()


def get_agent_by_id(agent_id):
    return Agent.query.filter(
        Agent.id == agent_id
    ).first()


def get_agent_by_userProfileId(userProfileId):
    return Agent.query.filter(
        Agent.userProfileId == userProfileId
    ).first()


def create_agent(userProfileId):
    agent = Agent(
        userProfileId=userProfileId,
        status=True
    )
    db.session.add(agent)
    db.session.commit()
    return agent


def delete_agent(agent_id):
    agent = db.session.get(Agent, agent_id)
    if not agent:
        return None
    
    agent.status = False
    db.session.commit()
    return agent