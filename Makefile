.PHONY: tests clean tide-install-git tide-install-pip  build upload local-dev docker-dev pylint docker-dev-server

define DOCKER_COMPOSE
cd ./plugins && git clean -f && git checkout .
docker-compose -f ./tests/docker/docker-compose-test.yml build
docker-compose -f ./tests/docker/docker-compose-test.yml run --rm --service-ports
endef

tests:
	$(DOCKER_COMPOSE) test-vim ./run-tests

clean:
	rm -rf ./plugins
	rm -rf ./autoload/tide

tide-install-git:
	$(MAKE) clean
	git clone https://github.com/wilvk/tide.git ./autoload/tide
	git clone https://github.com/wilvk/tide-plugins.git ./plugins
	cd ./autoload/tide && \
	  git checkout master && \
	  git pull && \
	  $(MAKE) git-install

tide-install-pip:
	$(MAKE) clean
	git clone https://github.com/wilvk/tide.git ./autoload/tide
	pip install --target=$(shell pwd)/autoload/tide tide

docker-dev:
	$(DOCKER_COMPOSE) test-vim sh

docker-dev-up:
	docker-compose -f ./tests/docker/docker-compose-dev.yml down
	docker-compose -f ./tests/docker/docker-compose-dev.yml build
	docker-compose -f ./tests/docker/docker-compose-dev.yml up --build --force-recreate dev-server
