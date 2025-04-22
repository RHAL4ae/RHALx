from fastapi import FastAPI
from typing import List
from .vendor_router import router as vendor_router

app = FastAPI(
    title="RHALX 5G Integration Platform",
    description="منصة رحّال إكس لتكامل مزودي الاتصالات 5G مع دعم تعدد الشركات (Nokia, Huawei, وغيرها)",
    version="1.0.0"
)

app.include_router(vendor_router)

@app.get("/vendors", tags=["Vendors"])
def list_vendors() -> List[str]:
    """
    إرجاع قائمة بمزودي الخدمة المدعومين
    """
    return ["nokia", "huawei"]

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}