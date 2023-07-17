FROM  python:3.10.6     

WORKDIR /app

COPY . /app 

RUN pip install -r requirements.txt

EXPOSE  8000 

# ENTRYPOINT [ "uvicorn", "main:app" ]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

