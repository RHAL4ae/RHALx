from fastapi import APIRouter
from .nokia_adapter import NokiaAdapter
from .huawei_adapter import HuaweiAdapter
from .tuya_adapter import TuyaAdapter
from .claude_adapter import ClaudeAdapter
from fastapi import Body
import os

router = APIRouter(prefix="/vendor", tags=["Vendor Integration"])

adapters = {
    "nokia": NokiaAdapter(),
    "huawei": HuaweiAdapter(),
    "tuya": TuyaAdapter()
}

claude_api_key = os.getenv("CLAUDE_API_KEY", "ضع_مفتاحك_هنا")
claude_adapter = ClaudeAdapter(api_key=claude_api_key)

@router.get("/{vendor}/status")
def get_vendor_status(vendor: str):
    if vendor not in adapters:
        return {"error": "Vendor not supported"}
    return adapters[vendor].get_status()

@router.post("/tuya/device/{device_id}/on")
def tuya_turn_on_device(device_id: str):
    """
    تشغيل جهاز Tuya ذكي عبر نقطة نهاية REST
    """
    return adapters["tuya"].turn_on_device(device_id)

@router.post("/tuya/device/{device_id}/off")
def tuya_turn_off_device(device_id: str):
    """
    إيقاف جهاز Tuya ذكي عبر نقطة نهاية REST
    """
    return adapters["tuya"].turn_off_device(device_id)

@router.post("/add_claude_vendor")
def add_claude_vendor(
    vendor_name: str = Body(...),
    vendor_type: str = Body(...),
    description: str = Body("")
):
    """
    إضافة vendor جديد ديناميكياً عبر Claude API
    """
    result = claude_adapter.add_vendor(vendor_name, vendor_type, description)
    return result