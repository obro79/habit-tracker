from fastapi import APIRouter, Response, Request
from twilio.twiml.messaging_response import MessagingResponse

from agent.agent import handle_message
from app.db import db

router = APIRouter()


@router.post("/sms")
async def receive_sms(request: Request):
    form = await request.form()
    phone_number = str(form.get("From", ""))
    message_body = str(form.get("Body", ""))

    # Look up user by phone number
    user = await db.user.find_first(where={"phoneNumber": phone_number})
    if not user:
        twiml = MessagingResponse()
        twiml.message("Sorry, I don't recognize this number.")
        return Response(content=str(twiml), media_type="application/xml")

    # Pass to agent
    reply = await handle_message(user_id=user.id, message=message_body)

    # Respond via Twilio
    twiml = MessagingResponse()
    twiml.message(reply)
    return Response(content=str(twiml), media_type="application/xml")
