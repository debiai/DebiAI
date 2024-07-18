# DebiAI Vuejs Frontend
FROM node:16.13-alpine as build-stage
WORKDIR /frontend
COPY frontend/ .
RUN npm install
RUN npm run build

# DebiAI Python debiaiServer (old backend dir)
FROM python:3.10.12-slim-bullseye
WORKDIR /
COPY debiaiServer/ debiaiServer/
RUN pip install --trusted-host pypi.python.org -r debiaiServer/requirements.txt
COPY run.py .
COPY --from=build-stage /frontend/dist debiaiServer/dist
ENV FLASK_ENV production
CMD ["python", "run.py"]

