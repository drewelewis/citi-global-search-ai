from pydantic import BaseModel

class ai_response(BaseModel):
    text: str
    errors: str