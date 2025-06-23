import panel as pn
import requests

pn.extension()

# Szövegbeviteli mező és gomb
input_text = pn.widgets.TextAreaInput(name='Szöveg', placeholder='Írd ide a mondatot...', height=150, width=500)
output = pn.pane.Markdown('', width=500)
button = pn.widgets.Button(name='Elemzés indítása', button_type='primary')

# Callback függvény
def analyze_sentiment(event):
    text = input_text.value
    if text.strip():
        try:
            res = requests.post("http://localhost:5000/sentiment", data=text)
            result = res.json().get('sentiment', 'nincs válasz')
            output.object = f"### Eredmény: **{result}**"
        except Exception as e:
            output.object = f"### Hiba történt: {e}"
    else:
        output.object = "### Kérlek adj meg szöveget!"

button.on_click(analyze_sentiment)

# Panel elrendezés
layout = pn.Column(
    "# Sentiment Elemző Panel",
    input_text,
    button,
    output
)

layout.servable()

