FROM animcogn/face_recognition:cpu-latest

WORKDIR /faceapp

COPY ./requirements.txt /faceapp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /faceapp/requirements.txt

COPY . /faceapp/


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
