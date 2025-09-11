from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_users():
    return {"message": "Hello World"}

# @router.get("/{user_id}")
# def get_user(user_id: int):
#     return {"message": f"Hello User {user_id}"}
