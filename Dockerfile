FROM python:3.12-alpine
# copy requirements alone to speed up build time
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "theMoth.py"]
