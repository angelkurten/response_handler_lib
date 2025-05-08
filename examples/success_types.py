from response_handler_lib.types import SuccessData
from response_handler_lib.either import Either, ErrorItem, Success
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

# Ejemplo de un modelo de datos específico
class User(BaseModel):
    id: str
    name: str
    email: str

# Ejemplo de un tipo de éxito específico para usuarios
class UserSuccessData(SuccessData[User]):
    """
    Tipo específico para respuestas exitosas relacionadas con usuarios.
    Incluye metadatos específicos para usuarios.
    """
    metadata: Optional[Dict[str, Any]] = {
        "user_type": "standard",
        "last_login": None
    }

# Ejemplo de uso con SuccessData y tipo explícito
def get_user_with_metadata(user_id: str) -> Either[ErrorItem, UserSuccessData]:
    # Simulación de obtención de usuario
    user = User(
        id=user_id,
        name="John Doe",
        email="john@example.com"
    )
    
    # Crear una respuesta exitosa con el tipo específico
    success_data = UserSuccessData(
        data=user,
        metadata={
            "user_type": "premium",
            "last_login": "2024-03-20T10:00:00Z"
        }
    )
    
    # Usando el método of solo con el tipo de éxito
    return Success.of[UserSuccessData](success_data)

# Ejemplo de uso directo con Success y tipo explícito
def get_user_simple(user_id: str) -> Either[ErrorItem, User]:
    # Simulación de obtención de usuario
    user = User(
        id=user_id,
        name="John Doe",
        email="john@example.com"
    )
    return Success.of[User](user)

# Ejemplo de uso con tipo genérico y SuccessData
def get_generic_data_with_metadata() -> Either[ErrorItem, SuccessData[str]]:
    return Success.of[SuccessData[str]](SuccessData(data="Hello, World!"))

# Ejemplo de uso directo con tipo genérico
def get_generic_data_simple() -> Either[ErrorItem, str]:
    return Success.of[str]("Hello, World!")

if __name__ == "__main__":
    # Ejemplo de uso con SuccessData
    user_result = get_user_with_metadata("123")
    if user_result.is_right:
        user_data = user_result.get_right()
        print(f"User with metadata: {user_data.data.name}")
        print(f"Metadata: {user_data.metadata}")
    
    # Ejemplo de uso directo
    user_simple = get_user_simple("123")
    if user_simple.is_right:
        user = user_simple.get_right()
        print(f"User simple: {user.name}")
    
    # Ejemplo de uso con tipo genérico y SuccessData
    generic_result = get_generic_data_with_metadata()
    if generic_result.is_right:
        generic_data = generic_result.get_right()
        print(f"Generic data with metadata: {generic_data.data}")
    
    # Ejemplo de uso directo con tipo genérico
    generic_simple = get_generic_data_simple()
    if generic_simple.is_right:
        data = generic_simple.get_right()
        print(f"Generic data simple: {data}") 