from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# model_name = "TheBloke/Llama-2-7B-Chat-GGML"
model_name = "./models/llama-2-7b-chat-ggml.bin"

config = {'max_new_tokens': 256, 'repetition_penalty': 1.1}

llm = CTransformers(model=model_name, model_type="llama", config=config, client=None)

prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
prompt.format(product="colorful socks")


chain = LLMChain(
    llm=llm,
    prompt=prompt,
    # output_parser=CommaSeparatedListOutputParser()
)

out = chain.run(product="socks")

print(out)

