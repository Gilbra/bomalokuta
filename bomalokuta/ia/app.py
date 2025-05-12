# app.py (dans Hugging Face)
import gradio as gr
from utils import get_response_json

def predict(text):
    result = get_response_json(text)
    return result

iface = gr.Interface(fn=predict, inputs="text", outputs="text")
iface.launch()
