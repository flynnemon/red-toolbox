FROM python:3.6-alpine
MAINTAINER Ryan Flynn <ryan@narwh.al>
ENV PS1="\[\e[0;33m\]|> kubesecret <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "

WORKDIR /src
COPY . /src
RUN pip install --no-cache-dir -r requirements.txt \
    && python setup.py install
WORKDIR /
ENTRYPOINT ["kubesecret"]
