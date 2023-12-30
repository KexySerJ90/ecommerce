FROM python:3.11-alpine3.19

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /ecommerce

COPY requirements.txt /temp/requirements.txt
COPY ecommerce /ecommerce

RUN apk add postgresql-client build-base postgresql-dev libffi-dev
RUN pip install -r /temp/requirements.txt
RUN adduser --disabled-password ecommerce-user
USER ecommerce-user


#SHELL ["/bin/sh","-c"]
#
#
#
#RUN pip install --upgrade pip
#
#RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
#    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim
## Создание пользователя yt и установка прав доступа к определенным директориям
#RUN useradd -rms /bin/sh yt && chmod 777 /opt /run
#
#
#
#RUN mkdir /yt/static && mkdir /yt/media && chown -R yt:yt /yt && chmod 755 /yt
##RUN chown -R yt:yt /yt && chmod 755 /yt
#COPY --chown=yt:yt ecommerce .
#
#
#
#USER yt
#
#CMD ["gunicorn", "-b", "0.0.0.0:8001", "ecommerce.wsgi:application"]