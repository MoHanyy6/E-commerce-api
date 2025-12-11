from fastapi import APIRouter, BackgroundTasks
from app.send_email import send_email

router = APIRouter()

@router.post("/send-test-email")
async def send_test_email(background_tasks: BackgroundTasks):
    background_tasks.add_task(
        send_email,
        subject="Test Email",
        recipients=["MHany.Tech@ship-crew.com"],
        body="<h1>Hello! Your order is confirmed.</h1>"
    )
    return {"message": "Email sent in the background!"}
