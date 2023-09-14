from sqlalchemy import Column, String, Boolean, UUID, func, or_, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from models.base_model import BaseModel
from sqlalchemy.dialects.postgresql import JSONB
import uuid
from exceptions import AccountException, AccountNotFoundException
from typings.account import AccountInput
from models.user_account import UserAccountModel

class AccountModel(BaseModel):
    """
    Represents an account entity.

    Attributes:
        id (UUID): Unique identifier of the account.
        user_id (UUID): ID of the user associated with the account.
        name (str): Name of the account.
        deleted (bool): Flag indicating if the account has been soft-deleted.
    """
    __tablename__ = 'account'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(100), default=None) 
    deleted = Column(Boolean, default=False)       
    
    created_by = Column(UUID, ForeignKey('user.id', name='fk_created_by'), nullable=True, index=True)
    modified_by = Column(UUID, ForeignKey('user.id', name='fk_modified_by'), nullable=True, index=True)
    creator = relationship("UserModel", foreign_keys=[created_by], cascade="all, delete", lazy='noload')
    
    
    # user_accounts = relationship("UserAccountModel", back_populates="account")
    # projects = relationship("WorkspaceModel", back_populates="account")
    
    def __repr__(self) -> str:
        return (
            f"Account(id={self.id}, "
            f"name='{self.name}', "
            f"deleted={self.deleted})"
        )

    @classmethod
    def create_account(cls, db, account, user):
        db_account = AccountModel(
                         created_by=user.id, 
                         )
        cls.update_model_from_input(db_account, account)
        db.session.add(db_account)
        db.session.flush()  # Flush pending changes to generate the account's ID
        db.session.commit()
        
        return db_account
       
    @classmethod
    def update_account(cls, db, id, account, user):
        old_account = cls.get_account_by_id(db=db, account_id=id)
        if not old_account:
            raise AccountNotFoundException("Account not found")
        db_account = cls.update_model_from_input(account_model=old_account, account_input=account)
        db_account.modified_by = user.id
        
        db.session.add(db_account)
        db.session.commit()
        
        return db_account
     
    @classmethod
    def update_model_from_input(cls, account_model: 'AccountModel', account_input: AccountInput):
        for field in AccountInput.__annotations__.keys():
            setattr(account_model, field, getattr(account_input, field))
        return account_model

    @classmethod
    def get_accounts(cls, db):
        accounts = (
            db.session.query(AccountModel)
            .filter(or_(or_(AccountModel.deleted == False, AccountModel.deleted is None), AccountModel.deleted is None))
            .all()
        )
        return accounts
    

    @classmethod
    def get_account_by_id(cls, db, account_id):
        accounts = (
            db.session.query(AccountModel)
            .filter(AccountModel.id == account_id, or_(or_(AccountModel.deleted == False, AccountModel.deleted is None), AccountModel.deleted is None))
            .first()
        )
        return accounts
    
    @classmethod
    def get_account_created_by(cls, db, user_id):
        accounts = (
            db.session.query(AccountModel)
            .filter(AccountModel.created_by == user_id, or_(or_(AccountModel.deleted == False, AccountModel.deleted is None), AccountModel.deleted is None))
            .first()
        )
        return accounts
    
    @classmethod
    def get_account_by_access(cls, db, user_id, account_id):
       
        accounts = (
             db.session.query(AccountModel)
            .join(UserAccountModel, AccountModel.id == UserAccountModel.account_id)
            .filter(UserAccountModel.account_id == account_id, or_(or_(AccountModel.deleted == False, AccountModel.deleted is None), AccountModel.deleted is None))
            # .options(joinedload(AgentModel.configs))  # if you have a relationship set up named "configs"
            .first()
        )
        return accounts

    @classmethod
    def delete_by_id(cls, db, account_id):
        db_account = db.session.query(AccountModel).filter(AccountModel.id == account_id).first()

        if not db_account or db_account.deleted:
            raise AccountNotFoundException("Account not found")

        db_account.deleted = True
        db.session.commit()
