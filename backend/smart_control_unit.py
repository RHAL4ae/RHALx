from typing import Dict, Any
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/smart", tags=["Smart Control Unit"])

# قاعدة بيانات مؤقتة للأجهزة والحالات والسياسات (للتجربة فقط)
devices_state = {}
rules = {}
events = []

# --- تنفيذ أوامر على أجهزة IoT (حالياً Tuya فقط) ---
@router.post("/device/{vendor}/{device_id}/command")
def execute_command(vendor: str, device_id: str, command: str, params: Dict[str, Any] = {}):
    if vendor == "tuya":
        # من المفترض استدعاء adapter حقيقي هنا
        if command == "on":
            devices_state[device_id] = "on"
            return {"result": "success", "device_id": device_id, "action": "on"}
        elif command == "off":
            devices_state[device_id] = "off"
            return {"result": "success", "device_id": device_id, "action": "off"}
        else:
            raise HTTPException(status_code=400, detail="Unknown command")
    else:
        raise HTTPException(status_code=400, detail="Vendor not supported yet")

# --- استقبال الأحداث (Events) ---
@router.post("/event")
def receive_event(event: Dict[str, Any]):
    events.append(event)
    return {"result": "event received", "event": event}

# --- إدارة السياسات (Rules) ---
@router.post("/rule")
def add_rule(rule: Dict[str, Any]):
    rule_id = str(len(rules) + 1)
    rules[rule_id] = rule
    return {"result": "rule added", "rule_id": rule_id}

@router.get("/rule/{rule_id}")
def get_rule(rule_id: str):
    rule = rules.get(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule

@router.delete("/rule/{rule_id}")
def delete_rule(rule_id: str):
    if rule_id in rules:
        del rules[rule_id]
        return {"result": "rule deleted"}
    else:
        raise HTTPException(status_code=404, detail="Rule not found")

# --- نقطة نهاية لتشغيل/تعطيل جهاز حسب السياسات ---
@router.post("/apply-rules")
def apply_rules():
    # منطق بسيط لتطبيق السياسات على الأجهزة
    for rule_id, rule in rules.items():
        device_id = rule.get("device_id")
        action = rule.get("action")
        if device_id and action:
            devices_state[device_id] = action
    return {"result": "rules applied", "devices_state": devices_state}