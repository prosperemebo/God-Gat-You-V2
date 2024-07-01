postgres:
	docker run --name postgres16 -p 5432:5432 -e POSTGRES_USER=$(DATABASE_USER) -e POSTGRES_PASSWORD=$(DATABASE_PASSWORD) -d postgres:16-alpine
	
createdb:
	docker exec -it postgres16 createdb --username=$(DATABASE_USER) --owner=$(DATABASE_USER) $(DATABASE_NAME)

build:
	docker build -t godgatyou-app .

start:
	docker run -dp 8000:8000 -w /app -v "$(PWD):/app" godgatyou-app

dropdb:
	docker exec -it postgres16 dropdb $(DATABASE_NAME)

init-migrate:
	flask db init

migrate:
	flask db migrate

apply-migrate:
	flask db upgrade