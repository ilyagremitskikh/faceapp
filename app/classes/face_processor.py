from typing import Union

import face_recognition

from ..utils import exceptions
from ..utils.base_logger import logger


class FaceProcessor:
    @staticmethod
    def get_encoding(
        file, model: str = "large", number_of_times_to_upsample: int = 1
    ) -> Union[list, None]:
        """Returns 128-vector embedding of image file

        Args:
            :param file:
            :param model:
            :param number_of_times_to_upsample:

        Returns:
            list: 128-vector list

        """

        image = face_recognition.load_image_file(file)

        face_locations = face_recognition.face_locations(
            image, number_of_times_to_upsample=number_of_times_to_upsample
        )

        if len(face_locations) > 1:
            logger.error(f"Number of faces on photo {file} is more than 1")
            raise exceptions.WrongNumberOfFacesError(
                "Number of faces on given image is more than 1"
            )

        if len(face_locations) == 0:
            logger.error(f"No faces recognized on photo: {file}")
            raise exceptions.NoFacesFoundError("No faces recognized on given image")

        face_encoding = face_recognition.face_encodings(
            image, known_face_locations=face_locations, model=model
        )
        return face_encoding[0]


if __name__ == "__main__":
    encoding = FaceProcessor.get_encoding("./dataset/Анжелика.jpg")
    if encoding is not None:
        print(encoding[0])
