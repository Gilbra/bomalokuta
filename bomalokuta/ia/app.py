import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer

# ✅ Modification : passage à ChatGLM2-6B
model_name = "THUDM/chatglm2-6b"  
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",  # Répartition sur CPU/GPU
    torch_dtype="float16",  # Optimisation mémoire
    low_cpu_mem_usage=True,  # Chargement efficace
    trust_remote_code=True  # Autoriser le code personnalisé
)

# ✅ Ajout de `use_cache=False` pour éviter les erreurs liées à `past_key_values`
def analyze_fake_news(text):
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_length=512, use_cache=False)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Interface Gradio
iface = gr.Interface(
    fn=analyze_fake_news,
    inputs="text",
    outputs="text",
    title="Détection de Fake News",
    description="Entrez un texte et l’IA analysera."
)

# ✅ Vérification des paramètres serveur
iface.launch(server_name="0.0.0.0", server_port=7860)
