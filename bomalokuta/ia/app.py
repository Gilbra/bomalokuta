import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer

# Chargement du modèle optimisé
model_name = "THUDM/chatglm3-6b"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",  # Répartition sur CPU/GPU
    torch_dtype="float16",  # Réduction de la consommation mémoire
    low_cpu_mem_usage=True,  # Chargement efficace
    trust_remote_code=True  # Autoriser le code personnalisé
)

# Fonction d'inférence optimisée
def analyze_fake_news(text):
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_length=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Interface Gradio
iface = gr.Interface(
    fn=analyze_fake_news,  # Utilisation de la fonction optimisée
    inputs="text",
    outputs="text",
    title="Détection de Fake News",
    description="Entrez un texte et l’IA analysera s'il s'agit d'une fake news."
)

iface.launch()
