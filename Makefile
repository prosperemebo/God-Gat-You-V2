postgres:
	docker run --name postgres16 -p 5432:5432 -e POSTGRES_USER=$(DATABASE_USER) -e POSTGRES_PASSWORD=$(DATABASE_PASSWORD) -d postgres:16-alpine
	
createdb:
	docker exec -it postgres16 createdb --username=$(DATABASE_USER) --owner=root $(DATABASE_NAME)

build:
	docker build -t godgatyou-app .

start:
	docker run -dp 5000:5000 -w /app -v "$(pwd):/app" godgatyou-app

dropdb:
	docker exec -it postgres16 dropdb $(DATABASE_NAME)

migrateup:
	migrate -path db/migration -database "postgresql://$(DATABASE_USER):$(DATABASE_PASSWORD)@localhost:5432/$(DATABASE_NAME)?sslmode=disable" -verbose up

migratedown:
	migrate -path db/migration -database "postgresql://$(DATABASE_USER):$(DATABASE_PASSWORD)@localhost:5432/$(DATABASE_NAME)?sslmode=disable" -verbose down