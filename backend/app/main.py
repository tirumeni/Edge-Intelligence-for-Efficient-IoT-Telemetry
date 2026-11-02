import os

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .api.huffman import router as huffman_router
from .api.algorithms import router as algorithms_router
from .api.encoder import router as encoder_router
from .api.telemetry import router as telemetry_router
from .api.codebook import router as codebook_router
from .services.telemetry_service import telemetry_service

app = FastAPI(
    title="Industrial IoT Telemetry Compression & Network Optimization Platform",
    description="Mathematical validation, algorithmic laboratory, and live network simulation for edge gateway telemetry.",
    version="1.0.0"
)

allowed_origins = [
    origin.strip().rstrip("/")
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:4173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(huffman_router)
app.include_router(algorithms_router)
app.include_router(encoder_router)
app.include_router(telemetry_router)
app.include_router(codebook_router)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Industrial IoT Telemetry Compression Platform",
        "version": "1.0.0",
        "network": {
            "capacity": "9.6 kbps",
            "message_rate": "40 msgs/sec",
            "sensors": 5000
        }
    }

@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await telemetry_service.register_websocket(websocket)
    try:
        while True:
            # Keep socket open and process incoming control commands from frontend if sent
            data = await websocket.receive_text()
            if data == "PING":
                await websocket.send_text("PONG")
    except WebSocketDisconnect:
        telemetry_service.unregister_websocket(websocket)
    except Exception:
        telemetry_service.unregister_websocket(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("DEBUG", "").lower() == "true",
    )

