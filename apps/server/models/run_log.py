from __future__ import annotations

import uuid

from sqlalchemy import UUID, Boolean, Column, ForeignKey, String
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql import or_

from models.base_model import BaseModel
from typings.run import RunLogInput, UpdateRunLogInput


class RunLogModel(BaseModel):
    """
    Model representing a log for run.

    Attributes:
        id (UUID): The primary key of the log.
        agent_id (UUID): The ID of the agent associated with the configuration.
        account_id (UUID): The ID of the account associated with the configuration.
        workspace_id (UUID): The ID of the project associated with the configuration.
        is_deleted (Boolean): Whether the tool configuration is deleted.
    """

    __tablename__ = "run_log"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)

    name = Column(String)
    input = Column(String)
    output = Column(String)
    type = Column(String)  # System, Tool, Final Answer

    run_id = Column(
        UUID, ForeignKey("run.id", ondelete="CASCADE"), nullable=True, index=True
    )

    agent_id = Column(
        UUID, ForeignKey("agent.id", ondelete="CASCADE"), nullable=True, index=True
    )

    team_id = Column(
        UUID, ForeignKey("team.id", ondelete="CASCADE"), nullable=True, index=True
    )

    chat_id = Column(
        UUID, ForeignKey("chat.id", ondelete="CASCADE"), nullable=True, index=True
    )

    account_id = Column(
        UUID, ForeignKey("account.id", ondelete="CASCADE"), nullable=True
    )
    workspace_id = Column(
        UUID, ForeignKey("workspace.id", ondelete="CASCADE"), nullable=True, index=True
    )

    session_id = Column(String, nullable=True, index=True)
    is_deleted = Column(Boolean, default=False, index=True)

    created_by = Column(
        UUID,
        ForeignKey("user.id", name="fk_created_by", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    modified_by = Column(
        UUID,
        ForeignKey("user.id", name="fk_modified_by", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    creator = relationship("UserModel", foreign_keys=[created_by], lazy="select")

    def __repr__(self) -> str:
        return (
            f"RunLog(id={self.id}, "
            f"is_deleted={self.is_deleted}, account_id={self.account_id})"
        )

    @classmethod
    def create_run_log(
        cls, session: Session, run: RunLogInput, user_id: UUID, account_id: UUID
    ):
        """
        Creates a new run log with the provided configuration.

        Args:
            db: The database object.
            config_with_config: The object containing the run and configuration details.

        Returns:
            Run: The created run.

        """
        db_run_log = RunLogModel(
            created_by=user_id,
            account_id=account_id,
        )

        cls.update_model_from_input(db_run_log, run)

        session.add(db_run_log)
        session.flush()  # Flush pending changes to generate the config's ID
        session.commit()

        return db_run_log

    @classmethod
    def update_latest_run_log(
        cls, session: Session, run_id: UUID, run: UpdateRunLogInput, user_id: UUID
    ):
        # Get the latest run log by the 'created_on' field
        old_run_log = (
            session.query(RunLogModel)
            .filter(RunLogModel.run_id == run_id)
            .order_by(RunLogModel.created_on.desc())
            .first()
        )

        # If the run log does not exist, raise an exception
        if not old_run_log:
            raise Exception("Run log not found")

        for field in UpdateRunLogInput.__annotations__.keys():
            setattr(old_run_log, field, getattr(run, field))

        old_run_log.modified_by = user_id

        # Commit the changes to the database
        session.add(old_run_log)
        session.commit()

        return old_run_log

    @classmethod
    def update_model_from_input(cls, run_model: RunLogModel, run_input: RunLogInput):
        for field in RunLogInput.__annotations__.keys():
            setattr(run_model, field, getattr(run_input, field))

        return run_model

    @classmethod
    def get_run_logs(cls, session: Session, run_id, account):
        run_logs = (
            session.query(RunLogModel)
            .filter(
                RunLogModel.run_id == run_id,
                RunLogModel.account_id == account.id,
                or_(
                    or_(
                        RunLogModel.is_deleted.is_(False),
                        RunLogModel.is_deleted is None,
                    ),
                    RunLogModel.is_deleted is None,
                ),
            )
            .order_by(RunLogModel.created_on.asc())
            .all()
        )
        return run_logs
