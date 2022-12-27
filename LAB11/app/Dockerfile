FROM python:3.9-alpine
WORKDIR /home
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY hello.py .
COPY images ./images
COPY templates ./templates
CMD [ "python3", "hello.py" ]
