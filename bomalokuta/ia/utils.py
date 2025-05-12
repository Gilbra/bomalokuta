from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True).half().cuda()
model.eval()

def get_response_json(user_text):
    prompt = f"""Analyse ce message et détermine s'il contient des signes de désinformation. 
Sois concis et donne une explication. Format :
{{
  "label": "vrai/faux/incertain",
  "explication": "...",
  "sources": ["...", "..."]
}}

Message : \"{user_text}\""""

    response, _ = model.chat(tokenizer, prompt, history=[])
    return response
