# DebiAI Vuejs Frontend
FROM node:16.13-alpine as build-stage
WORKDIR /frontend
COPY frontend/ .
RUN npm install
RUN npm run build

# DebiAI Python Backend
FROM python:3.10.12
WORKDIR /backend
COPY backend/ .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY --from=build-stage /frontend/dist dist
ENV FLASK_ENV production
CMD ["python", "websrv.py"]

