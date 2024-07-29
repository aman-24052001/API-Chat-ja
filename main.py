from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from routes.dripify_routes import router as dripify_router
import uuid
from controllers.dripify_controller import trigger_workflow_chat, continue_workflow_chat
from pydantic import BaseModel

app = FastAPI()

@app.on_event("startup")
def startup_event():
    print("Starting up...")

app.include_router(dripify_router, prefix="/api/v1")

class Req(BaseModel):
    user_input: str
@app.post("/start-chat")
async def start_chat(u_input:Req):
    print(u_input.user_input, "Hello")
    workflowId = str(uuid.uuid4())
    return trigger_workflow_chat( workflowId)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)