## Dev tips

### Cool models:

- TheBloke/Llama-2-7B-Chat-GGML
Maybe try 13B parameter model?

Migrations:

```
alembic revision --autogenerate -m "init; create stories tables"
alembic upgrade head
```
