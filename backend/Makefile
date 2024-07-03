postgres:
	docker run --name postgres16 -p 5432:5432 -e POSTGRES_USER=$(POSTGRES_USER) -e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) -d postgres:16-alpine
	
createdb:
	docker exec -it Godgatyou-postgres createdb --owner=$(POSTGRES_USER) $(POSTGRES_DB)

build:
	docker build -t godgatyou-app .

start:
	docker run -dp 8000:8000 -w /app -v "$(PWD):/app" godgatyou-app

dropdb:
	docker exec -it postgres16 dropdb $(POSTGRES_DB)

init-migrate:
	flask db init

migrate:
	flask db migrate

apply-migrate:
	flask db upgrade