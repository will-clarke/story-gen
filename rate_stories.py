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
The following is a story. It is called "{title}".
Please rate how good you think it is on a scale of 1 to 10, where 1 is the worst and 10 is the best.
Take into account the following criteria:
- Originality
- Interest
- How well it fits the genres ({genres})
- How well it fits the tones ({tones})
- General writing style
- Consistency

{story}

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
    pass




if __name__ == "__main__":
    stories_with_no_categories = session.query(Story).filter(~Story.categories.any()).all()
    for s in stories_with_no_categories:
        rate_story(s)
