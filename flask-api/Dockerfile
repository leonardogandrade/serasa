FROM python:3.13

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# RUN export JWT_SECRET_KEY="serasa2025"

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]