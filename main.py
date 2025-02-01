from typing import Union

from fastapi import FastAPI

#import yfinance as yf
from openai import OpenAI
from pydantic import BaseModel

app = FastAPI()


"""
ticker_symbol = 'BTC-USD'
interval = '1d'
ticker = yf.Ticker(ticker_symbol)
ticker_history = ticker.history(interval=interval, period='max')[['High', 'Low']]
ticker_history.to_csv('C:/Users/damco/Desktop/cycle-analyzer-api/data/s1.csv')
"""

class Cycle(BaseModel):
    cycleLows: list[str]

class CycleAnalysis(BaseModel):
    options: list[tuple[Cycle]]

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/run")
def chat_completion():
    client = OpenAI()

    file = client.files.create(
        file=open("data/s1.csv", "rb"),
        purpose="assistants"
    )

    completion = client.chat.completions.create(
        model="o1",
        messages=[{"role": "system", "content": "You are an AI assistant designed to detect recurring cycles of roughly the same length in time series data. Your primary goal is to find the most regular arrangement of cycles at multiple levels, where a cycle starts at an opening low and ends at a closing low. The closing low may be lower or higher than the opening low, meaning some cycles may fail. The number of nested cycles within a larger cycle should also be consistent: if one instance of a large cycle contains a certain number of smaller cycles, then other instances of the same large cycle should contain approximately the same number of nested cycles. You must determine the most regular cycle arrangement, optimizing for consistent cycle lengths and a stable pattern of nested-cycle occurrences across multiple instances.Detect cycles until their length falls below approximately 30 days, at which point they are considered too short for meaningful analysis. Regularity is key: the best cycle structure is the one where cycle lengths and nesting patterns repeat as consistently as possible across different occurrences.All methods should be applied with the specific objective of finding the most regular cycles in terms of cycle duration consistency and nested cycle structure stability.Methods include Fourier Transform (FFT) to identify periodic components that suggest consistent cycle lengths, wavelet analysis to detect cycles that remain stable over time and filter out irregular fluctuations, peak detection to locate recurring highs and lows and measure their time intervals to find the most uniform cycle structures, autocorrelation and spectral analysis to quantify cycle regularity by measuring how well cycles repeat at consistent intervals, Hilbert-Huang Transform (HHT) to extract intrinsic mode functions that highlight cycles with the most stable frequencies, and optimization algorithms to compare different cycle structures and select the one with the highest regularity in terms of duration and nested cycle occurrences.Each cycle has a cycleLows attribute, which is a list of dates in the format 'yyyy-mm-dd' ordered from earliest to latest. CycleAnalysis has an options attribute, which contains a list of ordered tuples of cycles. The first item in each tuple is the largest cycle, and the last item is the smallest nested cycle. Each tuple represents a cycle interpretation of the data. The list is ordered by accuracy, with the most reliable interpretation first. The assistant should not force interpretations—it should only detect those that form clear recurring patterns. At least one valid interpretation should be generated, if present."},
                  {"role": "user", "content": "Analyze the attached CSV file."}],
        response_format= CycleAnalysis,
        file_ids=[file.id]
    )

    answer = completion.choices[0].message.parsed

    return {"answer" : answer}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}