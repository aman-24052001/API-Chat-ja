from fastapi import APIRouter, HTTPException, Request
from controllers.dripify_controller import trigger_workflow_chat, continue_workflow_chat
from models.model import CampaignRequest, ContinueChatRequest, WorkflowChat
import uuid

router = APIRouter()

@router.post("/start-chat")
def start_chat():
    workflowId = str(uuid.uuid4())
    return trigger_workflow_chat(workflowId)

@router.post("/continue-chat", response_model=WorkflowChat)
def continue_chat(request: ContinueChatRequest):
    return continue_workflow_chat(request, request.chatId, request.user_response)