## Short stories

TODOs
- [ ]  SSL
- [ ] improve prometheus metrics!
- [ ] analytics!
- [ ] stories page with lots of search-param filters. eg. tones, themes, votes
- [ ] tags
- [ ] allow human votes
- [ ] scrape reddit short stories / two sentence horror
- [ ] fine-tune?!
- [ ] use own model?!
- [ ] learn more about models
- [ ] log in / bot detection?
- [ ] Grafana???
- [ ] think of awesome monetisation ideas
- [X] prometheus metrics or something
- [X] sort by AI votes
- [X] get migrations working properly
- [X] make the website look half decent
- [X] stories page 

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
