all: remove build run

rerun: stop remove build run

run-d: remove build run-detached

build:
	@docker compose build

run:
	@docker compose up --remove-orphans

rebuild:
	@docker compose up --force-recreate --build

run-detached:
	@docker compose up -d --remove-orphans

remove:
	@docker compose down
	@docker compose rm

stop:
	@docker compose down