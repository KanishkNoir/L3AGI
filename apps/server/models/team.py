from __future__ import annotations
from typing import List, Optional
import uuid

from sqlalchemy import Column, String, Boolean, UUID, func, or_, ForeignKey, Integer, and_
from sqlalchemy.orm import relationship, joinedload
from models.base_model import BaseModel
from typings.team import TeamInput
from exceptions import TeamNotFoundException
from models.team_agent import TeamAgentModel
from models.agent import AgentModel
from models.user import UserModel

class TeamModel(BaseModel):
    """
    Represents an team entity.

    Attributes:
        id (UUID): Unique identifier of the team.
        name (str): Name of the team.

    """
    __tablename__ = 'team'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    team_type = Column(String) #todo replace as enum (Debates, Plan_Execute, Authoritarian_Speaker, Decentralized_speaker)
    description = Column(String, nullable=True) 
    is_deleted = Column(Boolean, default=False, index=True)
    is_public = Column(Boolean, default=False, index=True)
    is_template = Column(Boolean, default=False, index=True)
    workspace_id = Column(UUID, ForeignKey('workspace.id'), nullable=True, index=True) 
    account_id = Column(UUID, ForeignKey('account.id'), nullable=True, index=True)
    
    account = relationship("AccountModel", cascade="all, delete")
    team_agents = relationship("TeamAgentModel", back_populates="team")
    chat_messages = relationship("ChatMessage", back_populates="team", cascade="all, delete")
    configs = relationship("ConfigModel", cascade="all, delete")
    
        
    created_by = Column(UUID, ForeignKey('user.id', name='fk_created_by'), nullable=True, index=True)
    modified_by = Column(UUID, ForeignKey('user.id', name='fk_modified_by'), nullable=True, index=True)
    creator = relationship("UserModel", foreign_keys=[created_by], cascade="all, delete", lazy='noload')
    
    def __repr__(self) -> str:
        return (
            f"Team(id={self.id}, "
            f"name='{self.name}', type='{self.team_type}', description='{self.description}', "
            f"is_deleted={self.is_deleted}, is_public={self.is_public}, is_template={self.is_template}, "
            f"workspace_id={self.workspace_id}, account_id={self.account_id})"
        )

    @classmethod
    def create_team(cls, db, team: TeamInput, user, account) -> TeamModel:
        """
        Creates a new team with the provided configuration.

        Args:
            db: The database object.
            team_with_config: The object containing the team and configuration details.

        Returns:
            Team: The created team.

        """
        db_team = TeamModel(
                         created_by=user.id, 
                         account_id=account.id,
                         )
        cls.update_model_from_input(db_team, team)
        db.session.add(db_team)
        db.session.flush()  # Flush pending changes to generate the team's ID
        db.session.commit()
        
        return db_team
       
    @classmethod
    def update_team(cls, db, id, team: TeamInput, user, account):
        """
        Creates a new team with the provided configuration.

        Args:
            db: The database object.
            team_with_config: The object containing the team and configuration details.

        Returns:
            Team: The created team.

        """
        old_team = cls.get_team_by_id(db=db, team_id=id, account=account)
        if not old_team:
            raise TeamNotFoundException("Team not found")
        db_team = cls.update_model_from_input(team_model=old_team, team_input=team)
        db_team.modified_by = user.id
        
        db.session.add(db_team)
        db.session.commit()

        return db_team
     
    @classmethod
    def update_model_from_input(cls, team_model: TeamModel, team_input: TeamInput):
        for field in TeamInput.__annotations__.keys():
            setattr(team_model, field, getattr(team_input, field))
        return team_model  

    @classmethod
    def get_teams(cls, db, account):
        teams = (
            db.session.query(TeamModel)
            .filter(TeamModel.account_id == account.id, or_(or_(TeamModel.is_deleted == False, TeamModel.is_deleted is None), TeamModel.is_deleted is None))
            .options(joinedload(TeamModel.team_agents).joinedload(TeamAgentModel.agent).joinedload(AgentModel.configs))
            .all()
        )
        return teams
    
    
    @classmethod
    def get_team_with_agents(cls, db, account, id: str):
        #todo later need to filter by account_id        
        # filter_conditions = [TeamModel.account_id == account.id, or_(or_(TeamModel.is_deleted == False, TeamModel.is_deleted is None), TeamModel.is_deleted is None)]
        filter_conditions = [or_(or_(TeamModel.is_deleted == False, TeamModel.is_deleted is None), TeamModel.is_deleted is None)]

        filter_conditions.append(TeamModel.id == id)
                
        teams = (
            db.session.query(TeamModel)
            .options(joinedload(TeamModel.team_agents).joinedload(TeamAgentModel.agent).joinedload(AgentModel.configs))
            .filter(and_(*filter_conditions))
            .first()
        )
        return teams
    

    @classmethod
    def get_team_by_id(cls, db, team_id, account):
        """
            Get Team from team_id

            Args:
                session: The database session.
                team_id(int) : Unique identifier of an Team.

            Returns:
                Team: Team object is returned.
        """
        # return db.session.query(TeamModel).filter(TeamModel.account_id == account.id, or_(or_(TeamModel.is_deleted == False, TeamModel.is_deleted is None), TeamModel.is_deleted is None)).all()
        teams = (
            db.session.query(TeamModel)
            .filter(TeamModel.id == team_id, or_(or_(TeamModel.is_deleted == False, TeamModel.is_deleted is None), TeamModel.is_deleted is None))
            .first()
        )
        return teams

    @classmethod
    def delete_by_id(cls, db, team_id, account):
        db_team = db.session.query(TeamModel).filter(TeamModel.id == team_id, TeamModel.account_id==account.id).first()

        if not db_team or db_team.is_deleted:
            raise TeamNotFoundException("Team not found")

        db_team.is_deleted = True
        db.session.commit()
        
    @classmethod        
    def get_template_agents(cls, db):
        agents = (
            db.session.query(TeamModel) 
            .filter(or_(TeamModel.is_deleted == False, TeamModel.is_deleted.is_(None)),
                    TeamModel.is_template == True)
            .options(joinedload(TeamModel.creator))
            .all()
        )
        return agents  

    @classmethod
    def get_public_agents(cls, db):
        agents = (
            db.session.query(TeamModel)
            # .join(AgentConfigModel, TeamModel.id == AgentConfigModel.agent_id)
            .join(UserModel, TeamModel.created_by == TeamModel.id)           
            .filter(or_(TeamModel.is_deleted == False, TeamModel.is_deleted.is_(None)),
                    TeamModel.is_public == True)
            .options(joinedload(TeamModel.creator))
            # .options(joinedload(TeamModel.configs))  # if you have a relationship set up named "configs"
            # .options(joinedload(TeamModel.agents))
            .all()
        )
        return agents  

    
