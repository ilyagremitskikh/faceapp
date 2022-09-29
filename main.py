import base64
from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, Header, HTTPException, UploadFile, status
from PIL import UnidentifiedImageError
from sqlalchemy.orm import Session

from app.classes.face_processor import FaceProcessor
from app.classes.index import Faiss
from app.models import crud, models
from app.models.database import SessionLocal, config, engine
from app.utils import exceptions

SIMILARITY_THRESHOLD = 60


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def verify_key(x_key: str = Header()):
    if x_key != config.api.secret_api_key:
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup_event():
    global faiss
    faiss = Faiss("euclidean", 128)
    if not Path("./Faiss.index").is_file():
        faiss.create()
        faiss.save()
    faiss.load()

    global fp
    fp = FaceProcessor()


@app.post(
    "/get_similar_pornstars/",
    response_model=List[models.PornstarModel],
    summary="Get similar pornstars",
    response_description="List of Similar Pornstars",
    responses={
        404: {"description": "Suitable results not found"},
        406: {"description": "Number of faces on given image is more than 1"},
        415: {"description": "Cannot identify image file"},
        422: {"description": "Can't find faces on image"},
    },
)
async def get_similar_pornstars(
    file: UploadFile, number_of_neighbors: int = 10, db: Session = Depends(get_db)
):
    """
    Get similar pornstars for uploaded human face photo
     - **file**: human face photo
     - **number_of_neighbors**: number of similar pornstars to return
    """
    image_file = file.file
    try:
        encoding = fp.get_encoding(image_file)
    except UnidentifiedImageError as error:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Cannot identify image file",
            headers={"X-Error": f"{error}"},
        )

    except exceptions.WrongNumberOfFacesError as error:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Wrong number of faces on photo",
            headers={"X-Error": f"{error}"},
        )

    except exceptions.NoFacesFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Can't find faces of photo",
            headers={"X-Error": f"{error}"},
        )

    neighbors, distances = faiss.get_neighbors(vector=encoding, n=number_of_neighbors)
    db_pornstars = crud.get_pornstars_by_ids(db, neighbors)
    pydantic_pornstars = [models.PornstarModel.from_orm(item) for item in db_pornstars]
    for index, model in enumerate(pydantic_pornstars):
        model.image = base64.b64encode(model.image)
        model.distance = distances[index]
        model.similarity = round((1 - distances[index]) * 100)
    result = [
        star for star in pydantic_pornstars if star.similarity > SIMILARITY_THRESHOLD
    ]
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Suitable results not found"
        )
    else:
        return result
