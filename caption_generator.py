import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# 모델과 토크나이저 로드
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    token=hf_token,
    device_map="auto",  # GPU 자동 할당
    torch_dtype=torch.float16,
)

# 텍스트 생성 파이프라인 설정
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=300,
    temperature=0.7,
    top_p=0.95,
    repetition_penalty=1.1
)

def generate_caption(title, summary):
    prompt = f"""
You are a sports journalist creating short and engaging Instagram-style news posts.

Write a stylish short paragraph (in <100 words) based on the following:

Title: {title}
Summary: {summary}

Instagram Post:
"""
    outputs = generator(prompt, do_sample=True)
    return outputs[0]["generated_text"].split("Instagram Post:")[-1].strip()
