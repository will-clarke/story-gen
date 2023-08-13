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


# s = session.query(Story).limit(10).all()
# print(s)
# print("---------------------------")
# s = session.query(StoryCategory).limit(10).all()
# print(s)


rating_criteria= [
        "originality",
        "close to genres",
        "close to tones",
        "generally good",
        "interesting",
        ]
prompt = PromptTemplate.from_template("""
The following is a short story demarked with <<<<<< and >>>>>>s. 

The short story is called "{title}", and aims to have the following categories: {categories}.

Please rate how good you think it is on a scale of 1 to 100, where 1 is the worst and 100 is the best.
Output format should be the number out of 100, followed by a colon and a single sentence reason for the rating.

Examples:
34/100: The story is not coherent and the writing style is poor.
79/100: Interesting sci-fic concepts and some decent character development.

Take into account the following criteria:
- Originality
- Coherence
- Interest
- How well it fits the categories ({categories})
- General writing style
- Consistency

<<<<<<<
{story}
>>>>>>>


Rating:
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

def rate_story(story: Story):
    f = prompt.format(
        title=story.title,
        categories=", ".join([c.category for c in story.categories]),
        story=story.text
)

    out = chain.run(
        title=story.title,
        categories=", ".join([c.category for c in story.categories]),
        story=story.text
    )


    rating = out.split("\n")[-1]

    r = StoryRating(
        story_id=story.id,
        rating_type="overallv1",
        rating=rating,
        prompt=prompt,
        model_name=model_name,
        )

    story.ratings.append(r)
    session.add(r)
    session.commit()

if __name__ == "__main__":
    stories_with_no_ratings = session.query(Story).filter(~Story.ratings.any()).limit(1).all()
    for s in stories_with_no_ratings:
        rate_story(s)
