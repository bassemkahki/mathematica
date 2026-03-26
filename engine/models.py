from pydantic import BaseModel
from typing import List, Dict, Any

class Metadata(BaseModel):
    engine_version: str
    sequence_type: str
    generation_bounds: Dict[str, Any]
    calculation_time_ms: float

class Data(BaseModel):
    sequence: List[str]

class SequenceResponse(BaseModel):
    metadata: Metadata
    data: Data
