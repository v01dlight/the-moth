FROM python:3.9-bullseye

COPY . .
RUN pip install -r requirements.txt
CMD ["python", "theMoth.py"]
