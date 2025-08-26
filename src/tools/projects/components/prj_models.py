from dataclasses import dataclass
from typing import List, Optional, Literal, Dict, Any

Status = Literal["in_progress", "completed"]

@dataclass
class Wrapper:
    id: str
    name: str
    type: Literal["wrapper"]
    status: Status

@dataclass
class Project:
    id: str
    name: str
    type: Literal["project"]
    status: Status
    wrapper_id: Optional[str]
    owner: str
    start_date: str  # YYYY-MM-DD
    end_date: str    # YYYY-MM-DD
    notes: str = ""

@dataclass
class DataModel:
    wrappers: List[Wrapper]
    projects: List[Project]

    @staticmethod
    def from_json(obj: Dict[str, Any]) -> "DataModel":
        wrappers = [Wrapper(**w) for w in obj.get("wrappers", [])]
        projects = [Project(**p) for p in obj.get("projects", [])]
        return DataModel(wrappers, projects)

    def to_json(self) -> Dict[str, Any]:
        return {
            "wrappers": [w.__dict__ for w in self.wrappers],
            "projects": [p.__dict__ for p in self.projects],
        }
