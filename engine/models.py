from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Point3D(BaseModel):
    x: float
    y: float
    z: float

class Metadata(BaseModel):
    engine_version: str
    sequence_type: str
    generation_bounds: Dict[str, Any]
    calculation_time_ms: float

class Data(BaseModel):
    sequence: List[str]
    points: Optional[List[Point3D]] = None

class SequenceResponse(BaseModel):
    metadata: Metadata
    data: Data
