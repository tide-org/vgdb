.PHONY: tests clean tide-install-git tide-install-pip  build upload local-dev docker-dev pylint docker-dev-server

define DOCKER_COMPOSE
cd ./plugins && git clean -f && git checkout .
docker-compose -f ./tests/docker/docker-compose-test.yml build
docker-compose -f ./tests/docker/docker-compose-test.yml run --rm --service-ports
endef

tests:
	$(DOCKER_COMPOSE) test-vim ./tests/scripts/run-tests

clean:
	rm -rf ./plugins
	rm -rf ./autoload/tide
	rm -rf ./tests/docker_volume_files/vader.vim

tide-install-git:
	$(MAKE) clean
	git clone git@github.com:wilvk/tide.git ./autoload/tide
	git clone git@github.com:wilvk/vader.vim.git ./tests/docker_volume_files/vader.vim
	git clone git@github.com:wilvk/tide-plugins.git ./plugins
	cd ./autoload/tide && \
	  git checkout master && \
	  git pull && \
	  $(MAKE) git-install

tide-install-pip:
	pip install --target=$(shell pwd).autoload/tide tide

docker-dev:
	$(DOCKER_COMPOSE) test-vim sh

docker-dev-up:
	docker-compose -f ./tests/docker/docker-compose-dev.yml down
	docker-compose -f ./tests/docker/docker-compose-dev.yml build
	docker-compose -f ./tests/docker/docker-compose-dev.yml up --build --force-recreate dev-server
