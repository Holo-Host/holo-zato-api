SHELL = bash

.PHONY: all build test

all: build test

build:
	sudo docker build -t holo-zato-api-tests .

test:
	sudo docker run --env-file=./env holo-zato-api-tests apitest run /tests
