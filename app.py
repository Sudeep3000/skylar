from fastapi import FastAPI
from engine import assign_mission, urgent_reassignment

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Skylark Drone AI Agent Running"}


@app.get("/assign/{project_id}")
def assign(project_id: str):
    return assign_mission(project_id)


@app.get("/urgent/{project_id}")
def urgent(project_id: str):
    return urgent_reassignment(project_id)
