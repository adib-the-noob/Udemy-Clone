from fastapi import FastAPI, staticfiles
from routers import auth


app = FastAPI()

app.mount("/media", staticfiles.StaticFiles(directory="media"), name="media")

# routers
app.include_router(auth.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
