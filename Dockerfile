FROM python:3.13-bookworm

WORKDIR /src

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# CHANGE ME: replace `wines.wsgi:application` with your project's WSGI module
# e.g. `school_proj.wsgi:application` or `publisher.wsgi:application`
CMD gunicorn --bind 0.0.0.0:8000 --workers 3 wines.wsgi:application
