import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "THUDM/chatglm2-6b"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# Fix padding issue
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype="float16",
    low_cpu_mem_usage=True,
    trust_remote_code=True
)

def analyze_fake_news(text):
    inputs = tokenizer(text, return_tensors="pt", padding=False).to(model.device)
    outputs = model.generate(**inputs, max_length=512, use_cache=False)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

iface = gr.Interface(
    fn=analyze_fake_news,
    inputs="text",
    outputs="text",
    title="Détection de Fake News",
    description="Entrez un texte et l’IA analysera."
)

iface.launch(server_name="0.0.0.0", server_port=7860)