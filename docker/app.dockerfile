FROM python:3.10.12-alpine
LABEL mainteiner="André Luzardo Porto <andreportol@gmail.com>"

# Copiar o conteúdo do projeto para o contêiner
COPY . /var/www
WORKDIR /var/www

# Atualizar pacotes e instalar dependências do sistema
RUN apk update && \
    apk add --no-cache \
    postgresql-dev \
    py3-pip \
    py3-setuptools

# Instalar as dependências do projeto
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Coletar arquivos estáticos do Django
RUN python manage.py collectstatic --noinput

# Definir o comando de entrada (ENTRYPOINT) fora do RUN
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "projeto_cacamba.wsgi"]

# Expor a porta 8000
EXPOSE 8000