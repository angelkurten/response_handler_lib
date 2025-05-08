from typing import TypeVar, Generic, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict

T = TypeVar('T')

class SuccessData(BaseModel, Generic[T]):
    """
    Clase base para los datos de éxito.
    Esta clase puede ser extendida para definir tipos específicos de datos de éxito.
    """
    data: T
    metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(arbitrary_types_allowed=True) 