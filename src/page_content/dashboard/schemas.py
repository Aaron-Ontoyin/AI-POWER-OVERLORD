from typing import List

from pydantic import BaseModel


class CoverageArea(BaseModel):
    id: str
    type: str
    name: str
    description: str
    sub_areas: List["CoverageArea"] = []

    @property
    def badge_color(self):
        type_ = self.type.lower()
        match type_:
            case "country":
                return "blue"
            case "province":
                return "indigo"
            case "district":
                return "teal"
            case "sub-district":
                return "cyan"
            case "village":
                return "gray"
            case _:
                return "gray"
