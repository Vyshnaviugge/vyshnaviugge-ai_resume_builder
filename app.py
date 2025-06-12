import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load DialoGPT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

chat_history_ids = None

def chatbot(input_text, history=[]):
    global chat_history_ids

    # Encode user input and add end of string token
    new_input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors='pt')

    # Append input to chat history
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if history else new_input_ids

    # Generate response
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7
    )

    # Decode last output tokens from bot
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    history.append((input_text, response))
    return history, history

# Create Gradio interface
chat_interface = gr.ChatInterface(fn=chatbot, title="🎓 Career Chatbot", theme="soft")

# Launch app
if __name__ == "__main__":
    chat_interface.launch()
