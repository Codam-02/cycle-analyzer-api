from typing import Union

from fastapi import FastAPI

#import yfinance as yf
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
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
    avgDuration: float

class CycleAnalysis(BaseModel):
    options: list[list[Cycle]]

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/run")
def chat_completion():
    client = OpenAI()

    client.files.create(
        file=open("data/s1.csv", "rb"),
        purpose="assistants"
    )

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{"role": "developer", "content": "You are an AI assistant designed to detect recurring cycles of roughly the same length in time series data. Your primary goal is to find the most regular arrangement of cycles at multiple levels, where a cycle starts at an opening low and ends at a closing low. The closing low must be a local low within its cycle, meaning no subsequent candle within that cycle should have a lower low, unless the cycle is a failed cycle. A failed cycle occurs when the price undercuts the cycle’s opening low at a later point, but such failures should not be encouraged—if shifting the cycle-low slightly to the right or left would prevent failure while maintaining cycle regularity, the assistant should prioritize that adjustment. The number of nested cycles within a larger cycle should also be consistent: if one instance of a large cycle contains a certain number of smaller cycles, then other instances of the same large cycle should contain approximately the same number of nested cycles. You must determine the most regular cycle arrangement, optimizing for consistent cycle lengths and a stable pattern of nested-cycle occurrences across multiple instances. Detect cycles until their length falls below approximately 30 days, at which point they are considered too short for meaningful analysis. Regularity is key: the best cycle structure is the one where cycle lengths and nesting patterns repeat as consistently as possible across different occurrences. All methods should be applied with the specific objective of finding the most regular cycles in terms of cycle duration consistency and nested cycle structure stability. Methods include Fourier Transform (FFT) to identify periodic components that suggest consistent cycle lengths, wavelet analysis to detect cycles that remain stable over time and filter out irregular fluctuations, peak detection to locate recurring highs and lows and measure their time intervals to find the most uniform cycle structures, autocorrelation and spectral analysis to quantify cycle regularity by measuring how well cycles repeat at consistent intervals, Hilbert-Huang Transform (HHT) to extract intrinsic mode functions that highlight cycles with the most stable frequencies, and optimization algorithms to compare different cycle structures and select the one with the highest regularity in terms of duration and nested cycle occurrences. Each cycle has a cycleLows attribute, which is a list of dates in the format 'yyyy-mm-dd' ordered from earliest to latest. These dates must be local lows within their respective cycles, except in cases of failed cycles. It also has an avgDuration attribute, which represents the average duration of its occurrences. This avgDuration is expressed in candles, meaning it depends on the timeframe of the input CSV (e.g., if the CSV contains daily candles, the avgDuration is in days; if it contains weekly candles, the avgDuration is in weeks). CycleAnalysis has an options attribute, which contains a list of ordered tuples of cycles. The first item in each tuple is the largest cycle, and the last item is the smallest nested cycle. Each tuple represents a cycle interpretation of the data. The list is ordered by accuracy, with the most reliable interpretation first. The assistant should not force interpretations—it should only detect those that form clear recurring patterns. At least one valid interpretation should be generated, if present."},
                  {"role": "user", "content": "the uploaded csv is in the format you're expecting, each row is a daily candle, with its appropriate day, that has 'High' and 'Low' values. The largest cycle that you must include in each interpretation of the analysis is the obvious 4-year cycle that has lows at the start of 2015, 2019 and 2023. Find these precise lows and then develop your interpretations for smaller nested cycles.",}
                  ],
        response_format= CycleAnalysis,
    )

    answer = completion.choices[0].message.parsed

    return {"answer" : answer}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}