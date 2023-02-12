import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .voltalis import Voltalis


USERNAME = os.getenv("VOLTALIS_USERNAME")
if USERNAME == None:
    raise ValueError("VOLTALIS_USERNAME env should be set")
PASSWORD = os.getenv("VOLTALIS_PASSWORD")
if PASSWORD == None:
    raise ValueError("VOLTALIS_PASSWORD env should be set")

app = FastAPI()
voltalis = Voltalis(USERNAME, PASSWORD)


class ChangeModeRequest(BaseModel):
    appliance: str
    mode: str


@app.get("/status")
def status():
    return


@app.get("/info")
def status():
    voltalis.set_appliances()
    return voltalis.appliances_info


@app.get("/mode")
def get_mode(appliance: str):
    voltalis.set_appliances()
    if appliance not in voltalis.appliances:
        raise HTTPException(status_code=404, detail="Appliance not found")
    return {"appliance": appliance, "mode": voltalis.appliances_info[appliance]["mode"]}


@app.post("/mode")
async def change_mode(req: ChangeModeRequest):
    return voltalis.change_applicance_mode(req.appliance, req.mode)
