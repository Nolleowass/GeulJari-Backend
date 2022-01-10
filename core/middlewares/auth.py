from fastapi import Request
from fastapi.exceptions import HTTPException

class AuthProvider:
    async def __call__ (self, req :Request):
        authorization : str = req.headers.get('token')
        if not authorization:
            raise HTTPException(status_code=401)
        return authorization