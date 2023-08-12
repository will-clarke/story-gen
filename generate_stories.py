import db
import random
from langchain.llms import CTransformers
from langchain.prompts import  PromptTemplate
from langchain.chains import LLMChain
from sqlalchemy.orm import Session
from models import Story, StoryCategory, StoryRating

potential_genres = ["hisorical", "fantasy", "romantic", "suspense", "sci-fi", "noir", "adventure", "comedy", "mystery", "fantasy", "romance"]
potential_tones = ["eerie", "suspense", "joyful", "celebration", "melancholic", "reflective", "funny", "comedy", "tense"]

engine = db.setup()
session = Session(engine)

prompt = PromptTemplate.from_template("""
I want you to write an interesting and absorbing short story with the following genres: {genres}.

It should have the following tone: {tones}.

Make in interesting and fun and roughly maximum {length} words long.

Start with the title on the first line then the story on the next line.
""")

model_name = "./models/llama-2-7b-chat-ggml.bin"
model_name = "TheBloke/Llama-2-7B-Chat-GGML"

llm = CTransformers(
    model=model_name,
    model_type="llama",
    client=None
)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
)

def process(genres, tones, length):
    f = prompt.format(genres=", ".join(genres), tones=", ".join(tones), length=length)
    print(f)

    out = chain.run(genres=genres, tones=tones, length=length)
    print(out)

    categories=[StoryCategory(category_type="tones", category=t) for t in tones] + [
            StoryCategory(category_type="genres", category=g) for g in genres]
    s = Story(
        text=out,
        prompt=f,
        categories=categories,
        model_name=model_name,
        length=length,
    )

    session.add(s)
    session.commit()


for i in range(0, 100000):
    genres = [random.choice(potential_genres) for _ in range(0, random.randint(1, 5))]
    genres = list(set(genres))
    tones = [random.choice(potential_tones) for _ in range(0, random.randint(1, 5))]
    tones = list(set(tones))
    length = random.choice(["10", "50", "100", "200", "500"])
    process(genres, tones, length)
