
from fastapi import FastAPI

import logging
from tuya_controller import TuyaController
# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from pydantic import BaseModel


# Tạo FastAPI app với lifecycle
app = FastAPI(
    title="API Tunnel",
    description="FastAPI tự động tạo tunnel khi khởi động",
)

class RequestTuya(BaseModel):
    device_id: str
    device_ip: str
    device_key: str
    device_version: float = 3.5

@app.get("/scan-devices")
async def scan_devices():
    result = await TuyaController.scan_devices()
    return result

@app.post("/status")
async def get_status(request: RequestTuya):
    result = await TuyaController.get_status(request.device_id, request.device_ip, request.device_key, request.device_version)
    return result

@app.post("/turn-on")
async def turn_on(request: RequestTuya):
    result = await TuyaController.turn_on(request.device_id, request.device_ip, request.device_key, request.device_version)
    return result

@app.post("/turn-off")
async def turn_off(request: RequestTuya):
    result = await TuyaController.turn_off(request.device_id, request.device_ip, request.device_key, request.device_version)
    return result

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    
    print("🌟 Đang khởi động FastAPI với Cloudflare Tunnel...")
    print("📝 Tunnel URL sẽ hiển thị trong log khi sẵn sàng")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )