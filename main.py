r"""
Healthcare AI — main.py (FINAL FIX)
"""
import os, sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Dict

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SERVICES_DIR = os.path.join(PROJECT_ROOT, "services")

if SERVICES_DIR not in sys.path:
    sys.path.insert(0, SERVICES_DIR)

# Routers Import
from services.diabetes_service.app.router import router as diabetes_router
from services.heart_service.app.router     import router as heart_router
from services.kidney_service.app.router    import router as kidney_router
from services.liver_service.app.router     import router as liver_router
from services.breast_cancer_service.app.router import router as breast_cancer_router
from services.parkinson_service.app.router import router as parkinson_router
from services.stroke_service.app.router    import router as stroke_router
from services.hypertension_service.app.router import router as hypertension_router
from services.bmi_risk_service.app.router   import router as bmi_risk_router
from services.blood_report_service.app.router import router as blood_report_router

app = FastAPI(title="Healthcare AI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ══════════════════════════════════════════════════════════════
# STATIC FILES (FRONTEND) FIX
# ══════════════════════════════════════════════════════════════
# Hum 'files' aur 'frontend' dono check karte hain
_fe_dir = None
for folder in ["files", "frontend"]:
    _path = os.path.join(PROJECT_ROOT, folder)
    if os.path.isdir(_path):
        _fe_dir = _path
        break

if _fe_dir:
    print(f"✅ Static folder found at: {_fe_dir}")
    app.mount("/ui", StaticFiles(directory=_fe_dir, html=True), name="ui")
else:
    print("❌ ERROR: Neither 'files' nor 'frontend' folder found!")

# ══════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════
@app.get("/")
async def root():
    return RedirectResponse(url="/ui")

app.include_router(diabetes_router,      prefix="/api/v1/diabetes",     tags=["Diabetes"])
app.include_router(heart_router,         prefix="/api/v1/heart",         tags=["Heart"])
app.include_router(kidney_router,        prefix="/api/v1/kidney",        tags=["Kidney"])
app.include_router(liver_router,         prefix="/api/v1/liver",         tags=["Liver"])
app.include_router(breast_cancer_router, prefix="/api/v1/breast-cancer", tags=["Cancer"])
app.include_router(parkinson_router,     prefix="/api/v1/parkinson",     tags=["Parkinson"])
app.include_router(stroke_router,        prefix="/api/v1/stroke",        tags=["Stroke"])
app.include_router(hypertension_router,  prefix="/api/v1/hypertension",  tags=["Hypertension"])
app.include_router(bmi_risk_router,      prefix="/api/v1/bmi-risk",      tags=["BMI"])
app.include_router(blood_report_router,  prefix="/api/v1/blood-report",  tags=["Blood"])

@app.get("/health")
def health(): return {"status": "healthy"}

@app.get("/api/v1/models")
def list_models():
    # Frontend toggle ke liye ye endpoint zaroori hai
    return {"models": []} # Aap purana _META wala code yahan daal sakte hain