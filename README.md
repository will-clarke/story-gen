# [ShortStories.lol](https://shortstories.lol)


This is basically an experiment to encourage me to learn how ML / AI actually works.
I generated these pretty rubbish models on my laptop(!) with 7b- & 13b-parameter Llama2 models.

- Ignore the awful stories & worse ratings. I need to fine-tune some models.
- Server stats generated from nginx logs: https://www.shortstories.lol/static/report.html
- From a Flask-perspective, I'm kinda proud of [how we filter categories via query parameters.](https://www.shortstories.lol/stories?categories=melancholic,reflective,sci-fi)
- I've recently been playing around with Google Colab and Kaggle and HuggingFace (GPU access is useful)

This repo is roughly split in two main bits:

1. A way to generate & rate short stories
2. A web app (Python / Flask) to display the stories

## Interesting files include:

- [generate_stories.py](stories_app/gen/generate_stories.py)
- [rate_stories.py](stories_app/gen/rate_stories.py)
- [scrape_reddit.py](stories_app/scripts/scrape_reddit.py)
- [colab-generate-story.py](colab-generate-story.py) - that runs on Google Colab and connects to a database.

## Made with the following:
- Flask
- Sqlalchemy
- HuggingFace
- Langchain


## Hosting
Hosted on a digital ocean droplet (which is really nice)

## TODOs:

- [-] IN PROGRESS - learn more about models (& fine-tune!)
    - [X] Fine-tune model to determine whether text is actually a story or not (eg. [huggingface fine-trained model](https://huggingface.co/will-clarke/km3p-5cou-dikk-0))
    - [X] Fine-tune model to determine whether story is good [Update: trained model (on reddit data) is useless. Need better data / better fine-tuning]
- [ ] improve prometheus metrics!
- [ ] allow human votes
- [ ] use own model?!
- [ ] log in / bot detection?
- [ ] Grafana???
- [ ] think of awesome monetisation ideas
- [X] SSL (surprisingly easy with certbot)
- [X] prometheus metrics or something
- [X] scrape reddit short stories / two sentence horror
- [X] tags
- [X] analytics!
- [X] sort by AI votes
- [X] get migrations working properly
- [X] make the website look half decent
- [X] stories page 
- [X] stories page with lots of search-param filters. eg. tones, themes, votes


## Dev tips

```
flask db check
flask db migrate -m 'message'
flask db upgrade
flask db history
```

### Migrations

```
alembic revision --autogenerate -m "init; create stories tables"
alembic upgrade head
```
