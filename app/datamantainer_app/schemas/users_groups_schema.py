from typing import List, Optional
from pydantic import BaseModel


class UserAssignGroup(BaseModel):
    user_id: int
    group_id: int
