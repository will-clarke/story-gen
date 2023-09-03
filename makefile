all: dev

dev:
	flask run --debug

shell:
	flask shell

deploy:
	ssh -t will@161.35.40.10 "cd story-gen; git pull"

ssh:
	ssh -t will@161.35.40.10

generate-stories:
	python3 -m stories_app.gen.generate_stories

rate-stories:
	python3 -m stories_app.gen.rate_stories

# generate-stories-mac:
# 	caffeinate -i "python3 -m stories_app.gen.generate_stories"

# rate-stories-mac:
# 	caffeinate -i "python3 -m stories_app.gen.rate_stories"
