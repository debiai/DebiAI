# DebiAI Vuejs Frontend
FROM node:16.13-alpine AS build-stage
WORKDIR /frontend
COPY frontend/ .
RUN npm install
RUN npm run build

# DebiAI Python debiaiServer
FROM python:3.10.12-slim-bullseye
WORKDIR /
COPY debiaiServer/ debiaiServer/
RUN pip install --trusted-host pypi.python.org -r debiaiServer/requirements.txt
COPY run_debiai_server_prod.py .
COPY --from=build-stage /frontend/dist debiaiServer/dist
CMD ["python", "run_debiai_server_prod.py"]

