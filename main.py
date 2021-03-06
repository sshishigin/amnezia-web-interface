from fastapi import FastAPI

from services.configuration.openvpn import OpenVPNClientConfigurator

app = FastAPI()

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/openvpn/{client_name}")
async def get_new_config(client_name: str, platform: str):
    return OpenVPNClientConfigurator().generate_configuration(client_name, platform)
