all: dev

dev:
	flask run --debug

deploy:
	ssh -t will@161.35.40.10 "cd story-gen; git pull"

ssh:
	ssh -t will@161.35.40.10
