docker network create django-app
docker run --name RecrAppDB --network django-app -p 5432:5432 -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=RecrAppDB -d postgres:17.5-alpine3.22
docker run -d --name DjangoApp --network django-app -p 8001:8000 -v ${PWD}:/app python:3.13-alpine3.22 sleep inf