all: dev

script-scrape-reddit:
	python3 -m stories_app.scripts.scrape_reddit

setup:
	source venv/bin/activate.fish
	pip install -r requirements.txt
	flask db upgrade

dev:
	flask run --debug

psql:
	psql postgresql://will@161.35.40.10:5432/stories

psql-backup:
	pg_dump postgresql://will@161.35.40.10:5432/stories > stories.db.bak

shell:
	flask shell

deploy:
	ssh -t will@161.35.40.10 "cd story-gen; git pull"
	ssh -t will@161.35.40.10 "cd story-gen; pip install -r requirements.txt"
	ssh -t will@161.35.40.10 "sudo systemctl restart stories"

ssh:
	ssh -t will@161.35.40.10

generate-stories:
	python3 -m stories_app.gen.generate_stories

rate-stories:
	python3 -m stories_app.gen.rate_stories

copy-db: psql-backup
	pg_dump --data-only --inserts -d stories > tmp.db
	scp tmp.db will@161.35.40.10:/home/will/tmp.db
	ssh -t will@161.35.40.10 "psql -d stories -f tmp.db"
	# may want to delete the data in the dbs first

generate-stories-mac:
	caffeinate python3 -m stories_app.gen.generate_stories

rate-stories-mac:
	caffeinate python3 -m stories_app.gen.rate_stories
