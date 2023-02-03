FROM python:3.7-slim
WORKDIR /app/Plan/
COPY ./ /app
RUN pip install -r /app/requirements.txt
RUN python3 -m pip install --upgrade Pillow
CMD ["gunicorn", "Plan.wsgi:application", "--bind", "0:8000" ] 