from langchain.llms import CTransformers


model_name = "TheBloke/Llama-2-7B-Chat-GGML"

config = {'max_new_tokens': 256, 'repetition_penalty': 1.1}

llm = CTransformers(model=model_name, config=config)

print(llm('AI is going to'))

