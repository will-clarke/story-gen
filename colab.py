# !pip install ctransformers ctransformers[cuda]

from ctransformers import AutoModelForCausalLM

llm = AutoModelForCausalLM.from_pretrained("TheBloke/Llama-2-7B-GGML", gpu_layers=50)

llm("AI is going to")
