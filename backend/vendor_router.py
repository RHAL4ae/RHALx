from fastapi import APIRouter
from .nokia_adapter import NokiaAdapter
from .huawei_adapter import HuaweiAdapter
from .tuya_adapter import TuyaAdapter

router = APIRouter(prefix="/vendor", tags=["Vendor Integration"])

adapters = {
    "nokia": NokiaAdapter(),
    "huawei": HuaweiAdapter(),
    "tuya": TuyaAdapter()
}

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