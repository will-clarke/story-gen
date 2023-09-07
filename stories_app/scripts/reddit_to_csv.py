import pandas as pd
from stories_app.app import create_app
from stories_app.models import DataReddit
from stories_app.db import db

app = create_app()
app.app_context().push()
session = db.session

# all datareddit instances
allDataReddit = session.query(DataReddit).all()

allDataRedditVars = list(map(vars, allDataReddit))


df = pd.DataFrame(allDataRedditVars)
df = df.drop(columns=["_sa_instance_state"])
df.to_csv("stories_app/data/data.csv", index=False)

print(df.head())
