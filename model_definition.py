from typing import List, Literal, Optional
from pydantic import BaseModel


class AnswerBase(BaseModel):
    answer: str | dict
    Replace: Optional[bool] = False
    Replace_way: Optional[int] = 0
    send_way: Optional[Literal["Text","Image","File","Gif","Url","Xml","Quote","Fav"]] = "Text"

class AnswerBaseList(BaseModel):
    answers: List[AnswerBase]
