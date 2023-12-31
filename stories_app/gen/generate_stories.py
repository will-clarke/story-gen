from stories_app.db import db
import random
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from sqlalchemy.orm import Session
from stories_app.models import Story, StoryCategory, StoryRating
from stories_app.app import create_app


potential_genres = [
    "hisorical",
    "fantasy",
    "romantic",
    "suspense",
    "sci-fi",
    "noir",
    "adventure",
    "comedy",
    "mystery",
    "fantasy",
    "romance",
]
potential_tones = [
    "eerie",
    "suspense",
    "joyful",
    "celebration",
    "melancholic",
    "reflective",
    "funny",
    "comedy",
    "tense",
]


app = create_app()
app.app_context().push()

session = db.session

prompt = PromptTemplate.from_template(
    """
I want you to write an interesting and absorbing short story with the following genres: {genres}.

It should have the following tone: {tones}.

Make in interesting and fun and roughly maximum {length} words long.

Start with the title on the first line then the story on the next line.
"""
)

model_name = "TheBloke/Llama-2-13B-Chat-GGML"

llm = CTransformers(model=model_name, model_type="llama", client=None)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
)


def extract_title(text):
    lines = text.strip().split("\n")
    if len(lines) < 2:
        return "", text
    title = lines[0]
    story_text = "\n".join(lines[1:])
    title = title.strip()
    story_text = story_text.strip()
    title = title.replace("Title: ", "")
    title = title.replace("Example: ", "")
    return title, story_text


def process(genres, tones, length):
    f = prompt.format(genres=", ".join(genres), tones=", ".join(tones), length=length)
    out = chain.run(genres=genres, tones=tones, length=length)
    print(out)

    title, story_text = extract_title(out)
    if title == "":
        return

    categories = [StoryCategory(category_type="tones", category=t) for t in tones] + [
        StoryCategory(category_type="genres", category=g) for g in genres
    ]
    s = Story(
        title=title,
        text=story_text,
        prompt=f,
        categories=categories,
        model_name=model_name,
        length=length,
    )

    session.add(s)
    session.commit()


if __name__ == "__main__":
    for i in range(0, 100000):
        genres = [
            random.choice(potential_genres) for _ in range(0, random.randint(1, 3))
        ]
        genres = list(set(genres))
        tones = [random.choice(potential_tones) for _ in range(0, random.randint(1, 3))]
        tones = list(set(tones))
        length = random.choice(["10", "50", "100", "200", "500", "1000", "2000"])
        process(genres, tones, length)
