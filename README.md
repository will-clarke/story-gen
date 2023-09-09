# ShortStories.lol

## In progress:

- [ ] scrape reddit short stories / two sentence horror
- [ ] learn more about models
- [ ] SSL

## TODOs:

- [ ] improve prometheus metrics!
- [ ] allow human votes
- [ ] fine-tune?!
- [ ] use own model?!
- [ ] log in / bot detection?
- [ ] Grafana???
- [ ] think of awesome monetisation ideas
- [X] prometheus metrics or something
- [X] tags
- [X] analytics!
- [X] sort by AI votes
- [X] get migrations working properly
- [X] make the website look half decent
- [X] stories page 
- [X] stories page with lots of search-param filters. eg. tones, themes, votes

## Stuff I should do at some point

## Dev tips

```
flask db check
flask db migrate -m 'message'
flask db upgrade
flask db history
```

### Cool models:

- TheBloke/Llama-2-7B-Chat-GGML
Maybe try 13B parameter model?

Migrations:

```
alembic revision --autogenerate -m "init; create stories tables"
alembic upgrade head
```
