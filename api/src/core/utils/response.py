from fastapi import HTTPException


def response_err(code,msg):
    raise HTTPException(status_code=code,detail={"msg":msg})