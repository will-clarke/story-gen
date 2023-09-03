## Short stories

TODOs
- [ ] analytics!
- [ ] get migrations working properly
- [ ] make the website look half decent
- [ ] stories page 
- [ ] stories page with lots of search-param filters. eg. tones, themes, votes
- [ ] sort by AI votes
- [ ] tags
- [ ] allow human votes
- [ ] scrape reddit short stories / two sentence horror
- [ ] fine-tune?!
- [ ] use own model?!
- [ ] learn more about models
- [ ] log in / bot detection?
- [ ] prometheus metrics or something. Grafana?!?!
- [ ] think of awesome monetisation ideas

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
