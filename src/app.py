
import gradio as gr
import numpy as np
import pickle
from scipy.special import softmax
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig


# Requirements
model_path = "gr8testgad-1/sentiment_analysis"
tokenizer = AutoTokenizer.from_pretrained(model_path)
config = AutoConfig.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)


# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


def sent_analysis(text):
    text = preprocess(text)

    # PyTorch-based models
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores_ = output[0][0].detach().numpy()
    scores_ = softmax(scores_)

    # Format output dict of scores
    labels = {0: 'NEGATIVE', 1: 'NEUTRAL', 2: 'POSITIVE'}
    scores = {labels[i]: float(s) for i, s in enumerate(scores_)}
    return scores

demo = gr.Interface(
    fn=sent_analysis,
    inputs=gr.Textbox(placeholder="Share your thoughts on COVID vaccines..."),
    outputs="label",
    interpretation="default",
    examples=[
    ["I feel confident about covid vaccines"],
    ["Will you take the jab"],
    ["I like the covid vaccines"],
    ["The covid vaccines are effective"]
    ],
    title="COVID Vaccine Sentiment Analysis",
    description="An AI model that predicts sentiment about COVID vaccines, providing labels and probabilities for 'NEGATIVE', 'NEUTRAL', and 'POSITIVE' sentiments.",
    theme="default", 
    live=True 
)



if __name__ == "__main__":
    demo.launch(host="0.0.0.0",port=7860)
