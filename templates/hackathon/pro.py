import gradio as gr
import pandas as pd
import requests
import tldextract
import re

# Scam keyword dataset
data = {
    "keyword": [
        "registration fee",
        "security deposit",
        "training fee",
        "pay before joining",
        "limited slots",
        "urgent hiring",
        "instant selection",
        "no interview"
    ],
    "score": [20,20,20,30,10,10,15,15]
}

df = pd.DataFrame(data)

free_email_domains = ["gmail.com","yahoo.com","outlook.com","hotmail.com"]

suspicious_domains = ["xyz","tk","ml","cf"]

def analyze(description,url):

    score = 0
    flags = []

    text = description.lower()

    # -------------------------
    # Keyword analysis
    # -------------------------
    for i in range(len(df)):
        if df["keyword"][i] in text:
            score += df["score"][i]
            flags.append("Scam phrase: " + df["keyword"][i])

    # -------------------------
    # Money detection
    # -------------------------
    money = re.findall(r'₹\d+|\d+\s?rs|\d+\s?rupees',text)

    if money:
        score += 25
        flags.append("Money/payment request detected")

    # -------------------------
    # Phone / WhatsApp detection
    # -------------------------
    phones = re.findall(r'\+?\d{10,13}',text)

    if phones:
        score += 10
        flags.append("Phone/WhatsApp contact detected")

    if "telegram" in text:
        score += 15
        flags.append("Telegram communication detected")

    # -------------------------
    # Email detection
    # -------------------------
    emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',text)

    for email in emails:
        domain = email.split("@")[1]

        if domain in free_email_domains:
            score += 10
            flags.append("Recruiter using free email domain")

    # -------------------------
    # URL domain analysis
    # -------------------------
    try:

        ext = tldextract.extract(url)
        domain = ext.domain
        suffix = ext.suffix

        if suffix in suspicious_domains:
            score += 15
            flags.append("Suspicious domain extension")

        if "-" in domain:
            score += 5
            flags.append("Unusual domain structure")

    except:
        flags.append("Invalid URL")

    # -------------------------
    # Website check
    # -------------------------
    try:

        response = requests.get(url,timeout=5)

        if response.status_code != 200:
            score += 10
            flags.append("Website not responding correctly")

        if len(response.text) < 500:
            score += 10
            flags.append("Website content looks suspicious")

    except:
        score += 10
        flags.append("Website unreachable")

    # -------------------------
    # Risk classification
    # -------------------------

    if score < 30:
        risk = "SAFE"
        color = "green"

    elif score < 60:
        risk = "SUSPICIOUS"
        color = "orange"

    else:
        risk = "HIGH RISK"
        color = "red"

    html = f"""
    <div style='padding:20px;border:3px solid {color};border-radius:10px'>
    <h2>Risk Score: {score}/100</h2>
    <h3 style='color:{color}'>Risk Level: {risk}</h3>
    </div>
    """

    flag_text = "\n".join(flags) if flags else "No strong scam indicators found."

    return html,flag_text


with gr.Blocks() as demo:

    gr.Markdown("# InternShield AI - Internship Scam Detector")

    description = gr.Textbox(lines=8,label="Internship Message")

    url = gr.Textbox(label="Company Website")

    btn = gr.Button("Analyze Internship")

    result = gr.HTML()

    flags = gr.Textbox(label="Detected Red Flags")

    btn.click(analyze,[description,url],[result,flags])

demo.launch()