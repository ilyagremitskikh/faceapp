from pathlib import Path

from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from app.classes.face_processor import FaceProcessor
from app.classes.index import Faiss
from app.models import models
from app.models import crud
from app.models.database import engine
from app.models.models import PornstarOrm
from app.utils import exceptions
from app.utils.base_logger import logger

Session = sessionmaker(bind=engine)

models.Base.metadata.create_all(bind=engine)


def main(root_folder_path: str):
    faiss = Faiss("euclidean", 128)
    faiss.create()
    fp = FaceProcessor()
    path = Path.cwd() / root_folder_path
    images_temp = path.rglob("*.jpg")
    images_length = len(list(images_temp))
    images = path.rglob("*.jpg")
    index = 0
    for image in tqdm(images, total=images_length):
        model_name = image.resolve().stem
        try:
            encoding = fp.get_encoding(image.resolve(), number_of_times_to_upsample=1)
        except exceptions.NoFacesFoundError:
            logger.error(f"No faces found for model: {model_name}")
            continue
        except exceptions.WrongNumberOfFacesError:
            logger.error(f"More than 1 faces found for model: {model_name}")
            continue
        except Exception as e:
            logger.error(e)
            continue
        image_file = open(image, "rb")
        pornstar = PornstarOrm(id=index, name=model_name, image=image_file.read())
        image_file.close()
        with Session.begin() as session:
            crud.save_pornstar(session, pornstar)
        faiss.add_vectors([encoding])
        index += 1
    faiss.save()


if __name__ == "__main__":
    main("../data")
