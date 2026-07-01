from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., gt=0, le=10000000)
    stock: int = Field(..., ge=0, le=10000)
    category: str = Field(..., min_length=3)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        name = value.strip()

        if not name:
            raise ValueError("El nombre no puede estar vacío")

        if name.lower() in ["test", "prueba", "producto"]:
            raise ValueError("El nombre del producto no está permitido")

        return name


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    price: Optional[float] = Field(None, gt=0, le=10000000)
    stock: Optional[int] = Field(None, ge=0, le=10000)
    category: Optional[str] = Field(None, min_length=3)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value is None:
            return value

        name = value.strip()

        if not name:
            raise ValueError("El nombre no puede estar vacío")

        if name.lower() in ["test", "prueba", "producto"]:
            raise ValueError("El nombre del producto no está permitido")

        return name


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
        