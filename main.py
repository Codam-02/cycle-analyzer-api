from typing import Union

from fastapi import FastAPI

#import yfinance as yf
from openai import OpenAI

app = FastAPI()


"""
ticker_symbol = 'BTC-USD'
interval = '1wk'
ticker = yf.Ticker(ticker_symbol)
ticker_history = ticker.history(interval=interval, period='max')[['High', 'Low']]
ticker_history.to_csv('C:/Users/damco/Desktop/cycle-analyzer-api/data/s1.csv')
"""

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/run")
def chat_completion():
    client = OpenAI()

    file = client.files.create(
        file=open("data/s1.csv", "rb"),
        purpose="assistants"
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "developer", "content": "You are a helpful assistant."},
                  {"role": "user", "content": "Analyze the attached CSV file."}],
        file_ids=[file.id]
    )

    answer = completion.choices[0].message.content

    return {"answer" : answer}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}