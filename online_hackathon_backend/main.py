from fastapi import FastAPI
app = FastAPI()

from fastapi.responses import FileResponse


# uvicorn main:app --reload
# 이거 복사해서 사용
@app.get("/") 
def hello():
    return 'hello'

