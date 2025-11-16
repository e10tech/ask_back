from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + uv!"}


# #実際につなげるときのサンプルコード
# # main.py
# from fastapi import FastAPI
#
# from app.api import router as user_router
# from app.database import Base, engine
#
# # DBテーブル作成（MVPなら自動作成でもOK）
# Base.metadata.create_all(bind=engine)
#
# app = FastAPI()
#
# app.include_router(user_router)
#
#
# @app.get("/")
# def read_root():
#     return {"message": "Hello from FastAPI + uv + SQLAlchemy!"}
