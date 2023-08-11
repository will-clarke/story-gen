import db
import uuid
import random
from langchain.llms import CTransformers
from langchain.prompts.chat import (
    PromptTemplate,
    # ChatPromptTemplate,
    # SystemMessagePromptTemplate,
    # HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser


potential_genres = ["historical", "fantasy", "romantic", "suspense", "sci-fi", "noir", "adventure", "comedy", "mystery", "fantasy", "romance"]
potential_tones = ["eerie", "suspense", "joyful", "celebration", "melancholic", "reflective", "funny", "comedy", "tense"]

db.setup()
# db.load_fake_data()

cursor = db.cursor

rows = cursor.execute("SELECT * from stories").fetchall()
print(rows)
rows = cursor.execute("SELECT * from story_categories").fetchall()



def process(genres, tones, length):
    prompt = PromptTemplate.from_template("""
    I want you to write an interesting and absorbing short stort with the following genres: {genres}.

    It should have the following tone: {tones}.

    Make in interesting and fun and {length} words long.

    Start with the title on the first line then the story on the next line.
    """)
    f = prompt.format(genres=", ".join(genres), tones=", ".join(tones), length=length)
    print(f)

    model_name = "./models/llama-2-7b-chat-ggml.bin"
    llm = CTransformers(
        model=model_name,
        model_type="llama",
        # config=config,
# config = {'max_new_tokens': 256, 'repetition_penalty': 1.1}
        client=None
    )

    chain = LLMChain(
        llm=llm,
        prompt=prompt,
    )

    out = chain.run(genres=genres, tones=tones, length=length)
    print(out)

    u   = str(uuid.uuid4())
    cursor.execute("INSERT INTO stories VALUES ('%s', '%s', '%s', DATE('now'), DATE('now'))" %(u, out, f))

    for genre in genres:
        cursor.execute("INSERT INTO story_categories VALUES ('%s', 'genre', '%s' )" %(u, genre))
    for tone in tones:
        cursor.execute("INSERT INTO story_categories VALUES ('%s', 'tone', '%s' )" %(u, tone))
    db.connection.commit()


for i in range(0, 1000):
    genres = [random.choice(potential_genres) for _ in range(0, random.randint(1, 5))]
    genres = list(set(genres))
    tones = [random.choice(potential_tones) for _ in range(0, random.randint(1, 5))]
    tones = list(set(tones))
    length = random.choice(["10", "50", "100", "200", "500"])
    process(genres, tones, length)


db.close()
exit()
