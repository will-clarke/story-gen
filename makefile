all: dev


docker: docker-run

docker-run: docker-build
	docker run --publish 5000:5000 --rm --name omg omg 

docker-build:
	docker build -t omg .

install:
	pip install -r requirements.txt

script-scrape-reddit:
	python3 -m stories_app.scripts.scrape_reddit

script-reddit-to-csv:
	python3 -m stories_app.scripts.reddit_to_csv

script-download-reddit-csv:
	scp will@161.35.40.10:/home/will/story-gen/stories_app/data/data.csv reddit-data.csv

setup:
	source venv/bin/activate.fish
	pip install -r requirements.txt
	flask db upgrade

metrics:
	ssh will@161.35.40.10 'zcat -f /var/log/nginx/access.log*' | goaccess --log-format=COMBINED

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

copy-local-db-to-remote: psql-backup
	pg_dump --data-only --inserts -d stories > tmp.db
	scp tmp.db will@161.35.40.10:/home/will/tmp.db
	# ssh -t will@161.35.40.10 "psql -d stories -f tmp.db"

generate-stories-mac:
	caffeinate python3 -m stories_app.gen.generate_stories

rate-stories-mac:
	caffeinate python3 -m stories_app.gen.rate_stories
