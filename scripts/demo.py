import uvicorn
from fastapi import FastAPI

app = FastAPI()


if __name__ == "__main__":
    # 这里可以自定义配置，甚至可以通过环境变量读取配置
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")