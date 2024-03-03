build:
	docker-compose -f docker-compose.yaml up --no-start --build

start:
	docker-compose -f docker-compose.yaml up -d

stop:
	docker-compose -f docker-compose.yaml down -v

PHONY: build start stop
