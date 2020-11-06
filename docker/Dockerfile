FROM arm32v7/python:3.7.9-buster
WORKDIR /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-m", "pip", "list"]
