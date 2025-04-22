from fastapi import APIRouter, WebSocket
import asyncio

router = APIRouter(prefix="/alerts", tags=["RealTime Alerts"])

# قائمة الاتصالات النشطة عبر WebSocket
active_connections = []

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # هنا يمكن معالجة الرسائل الواردة من العميل إذا لزم الأمر
    except Exception:
        pass
    finally:
        active_connections.remove(websocket)

# دالة لإرسال تنبيه لجميع العملاء المتصلين
async def broadcast_alert(message: str):
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception:
            pass

# --- دعم MQTT (هيكل أولي فقط) ---
try:
    import paho.mqtt.client as mqtt
    mqtt_available = True
except ImportError:
    mqtt_available = False

mqtt_client = None

def setup_mqtt(broker_url: str, topic: str):
    global mqtt_client
    if not mqtt_available:
        raise RuntimeError("paho-mqtt غير مثبت")
    mqtt_client = mqtt.Client()
    mqtt_client.connect(broker_url)
    mqtt_client.subscribe(topic)
    mqtt_client.on_message = on_mqtt_message
    mqtt_client.loop_start()

def on_mqtt_message(client, userdata, msg):
    # عند استقبال رسالة MQTT، يمكن بثها عبر WebSocket
    message = msg.payload.decode()
    asyncio.create_task(broadcast_alert(message))