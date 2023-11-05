from fastapi import HTTPException


class CommentAlreadyExists(HTTPException):
    def __init__(self):
        detail = "You have already left a comment on this ad. Multiple comments are not allowed."
        super().__init__(status_code=400, detail=detail)
