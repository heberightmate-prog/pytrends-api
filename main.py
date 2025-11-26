from fastapi import FastAPI
from pytrends.request import TrendReq

app = FastAPI()

@app.get("/trends")
def get_trends(keyword: str, geo: str = "AU", timeframe: str = "now 1-d"):
    pytrends = TrendReq(hl='en-AU', tz=600)
    pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)

    related_queries = pytrends.related_queries()
    interest_over_time = pytrends.interest_over_time()
    interest_by_region = pytrends.interest_by_region(resolution="city")

    top = related_queries[keyword]["top"].to_dict('records') if related_queries[keyword]["top"] is not None else []
    rising = related_queries[keyword]["rising"].to_dict('records') if related_queries[keyword]["rising"] is not None else []

    return {
        "keyword": keyword,
        "geo": geo,
        "timeframe": timeframe,
        "top": top,
        "rising": rising,
        "interest_over_time": interest_over_time.reset_index().to_dict("records"),
        "interest_by_region": interest_by_region.reset_index().to_dict("records")
    }
