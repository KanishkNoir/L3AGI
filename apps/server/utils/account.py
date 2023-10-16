from models.account import AccountModel
from typing import List
from typings.account import AccountOutput
from utils.type import convert_value_to_type

new_config = default_configs = {
    "info": {
        "logo": '',
        "welcomeMessage": "Welcome to L3AGI"
    },
    "naming": {
        "home": 'Home',
        "agent": "Agent",
        "team": "Team",
        "datasource": "Data sources",
        "models": "Models",
        "discovery": "Discovery"
    },
    "modules": {
        "home": {
            "welcome_message": "Build your ",
            "submodules": {
                "team": {
                    "operations": {
                        "create": True,
                        "list": True,
                        "edit": True,
                        "delete": True
                    }
                },
                "agent": False,
                "discovery": False,
            }
        },
        "chat" :{
            "active: True"
            "label": "Multi-Agent",
            "submodules": {
                "team": {
                    "operations": {
                        "create": True,
                        "list": True,
                        "edit": True
                    }
                },
                "agent": False,
                "session": {
                    "operations": True
                }
            }
        },
        "model" : {
            "active" : True,
            "label": "Models",
            "submodules": {
                "models": {
                    "operations": {
                        "create": True,
                        "list": True,
                        "edit": True
                    }
                },
                "fine-tuning": {
                    "operations": True
                }
            }
        },
        "toolkit": False, #True
        "datasource": False,
        "discovery": False,
        "Session": False
    },
}

default_configs = {
    "info": {
        "logo": '',
        "welcomeMessage": "Welcome to L3AGI"
    },
    "modules" : {
        "home": {
            "active" : True,
             "display" : {
              "showAgents": True,
              "showTeams": True ,  
              "showDiscoveryTeams": True,             
              "showDiscoveryAgents": True,          
            }                
        },
        "agent": {
            "active" : True,
            "name": "Team",
            "actions" : {
                "addAgent": True,
                "addTeam": True,
                "createTeamSession": True,
                "createAgentSession": True,
            },
            "display" : {
                "teams": True,
                "agents": True,
                "sessions": True                
            }           
        },
        "datasource": {
            "active" : True,
            "name": "Data sources"
        },
        "toolkit": {
            "active" : True,
            "name": "Toolkits"
        },
        "model" : {
            "active" : True,
            "name": "Models",
            "display": {
                "models": True,
                "fine-tuning": True
            }            
        },
        "contact": {
            "active" : False,
            "name": "Contact"
        },
        "group": {
            "active" : False,
            "name": "Group"
        },
        "schedule": {
            "active" : False,
            "name": "Campaign"
        },
        "discovery": {
            "active" : True,
            "name": "Discovery",
            "display" : {
                "team": True,
                "agents": True,             
            }        
            
        }
    }
}

def convert_model_to_response(account_model: AccountModel) -> AccountOutput:
    account_data = {}
    # if not account_model.configs:
    account_model.configs = default_configs
        
    # Extract attributes from AccountModel using annotations of Account
    for key in AccountOutput.__annotations__.keys():
        if hasattr(account_model, key):
            target_type = AccountOutput.__annotations__.get(key)
            account_data[key] = convert_value_to_type(
                value=getattr(account_model, key), target_type=target_type
            )
            
    return AccountOutput(**account_data)


def convert_accounts_to_account_list(
    accounts: List[AccountModel],
) -> List[AccountOutput]:
    return [convert_model_to_response(account_model) for account_model in accounts]
