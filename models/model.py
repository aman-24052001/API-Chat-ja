from pydantic import BaseModel, Field
from typing import List, Optional

class CampaignRequest(BaseModel):
    user_input: str 

class ContinueChatRequest(BaseModel):
    chatId: str = Field(..., min_length=1, max_length=100)
    user_response: str = Field(..., min_length=1, max_length=1000)

class WorkflowChatMessage(BaseModel):
    question: str
    response: Optional[str] = None

class WorkflowChat(BaseModel):
    id: str
    workflowid: str
    messages: List[WorkflowChatMessage]
    collected_info: dict
    is_completed: Optional[bool] = False
    json_filename: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "123456789",
                "workflowid": "987654321",
                "messages": [
                    {
                        "question": "What is your name?",
                        "response": "John Doe"
                    }
                ],
                "collected_info": {
                    "CampaignType": "Welcome Series"
                }
            }
        }