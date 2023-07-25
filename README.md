Install all dependencies and libs using ```poetry install ```

It is important to run the browser with frontend.html without the CORS mechanism.

To do that on Linux with Chrome, use the following command:
```
google-chrome --disable-site-isolation-trials --disable-web-security --user-data-dir="/tmp"
```

For websocket html file it isn't required. Just run fast_api app open frontend_ws.html file . 
```python3 -m uvicorn main:app --reload```


I planned to but didn't make it in time:
- tests
- using aioredis instead of redis
- docker-compose for proxy and avoid cors issues for locally development
