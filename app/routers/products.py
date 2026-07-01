from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "/",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    # Verificar si ya existe un producto con el mismo nombre
    existing = crud.get_product_by_name(db, product.name)

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": {
                    "code": "PRODUCT_ALREADY_EXISTS",
                    "message": "Ya existe un producto con ese nombre"
                }
            }
        )

    return crud.create_product(db, product)


@router.get(
    "/",
    response_model=list[schemas.ProductResponse],
    status_code=status.HTTP_200_OK
)
def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@router.get(
    "/{product_id}",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_200_OK
)
def read_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = crud.get_product(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "PRODUCT_NOT_FOUND",
                    "message": "El producto solicitado no existe"
                }
            }
        )

    return product


@router.put(
    "/{product_id}",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_200_OK
)
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    # Validar que el JSON no venga vacío
    update_data = product.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "EMPTY_UPDATE_BODY",
                    "message": "Debe enviar al menos un campo para actualizar"
                }
            }
        )

    # Validar nombre duplicado
    if "name" in update_data:
        existing = crud.get_product_by_name(db, product.name)

        if existing and existing.id != product_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": {
                        "code": "PRODUCT_ALREADY_EXISTS",
                        "message": "Ya existe un producto con ese nombre"
                    }
                }
            )

    updated = crud.update_product(db, product_id, product)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "PRODUCT_NOT_FOUND",
                    "message": "El producto solicitado no existe"
                }
            }
        )

    return updated


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_product(db, product_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "PRODUCT_NOT_FOUND",
                    "message": "El producto solicitado no existe"
                }
            }
        )

    return