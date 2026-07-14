from fastapi import FastAPI

app = FastAPI(
    title="AI Research Assistant",
    description="Chat with your research papers using AI",
    version="0.1.0",
)

@app.get("/")
def root():
    return {
        "message": "Welcome to AI Research Assistant 🚀"
    }