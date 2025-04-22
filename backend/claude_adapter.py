import os
import requests
from typing import Dict, Any

class ClaudeAdapter:
    """
    طبقة وسيطة تعتمد على Claude API لإضافة أي vendor جديد (اتصالات أو IoT)
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY", "")
        self.base_url = "https://api.anthropic.com/v1/messages"  # مثال لمسار Claude API
        self.vendors = {}  # تخزين ديناميكي للـvendors المضافة

    def add_vendor(self, vendor_name: str, vendor_type: str, description: str = "") -> Dict[str, Any]:
        """
        إضافة vendor جديد ديناميكياً عبر Claude API
        :param vendor_name: اسم المزود
        :param vendor_type: نوع المزود (اتصالات/IoT)
        :param description: وصف اختياري
        :return: نتيجة العملية
        """
        # مثال على استخدام Claude API لتوليد كود adapter أو توصيفه
        prompt = f"""
        أنشئ كود Adapter بايثون لمزود جديد اسمه {vendor_name} من نوع {vendor_type}.
        الوصف: {description}
        يجب أن يرث الكلاس من BaseAdapter ويحتوي على دالة get_status.
        """
        headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json"
        }
        data = {
            "model": "claude-3-opus-20240229",  # يمكن تعديله حسب المتاح
            "max_tokens": 512,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            # حفظ معلومات vendor الجديد
            self.vendors[vendor_name] = {
                "type": vendor_type,
                "description": description,
                "adapter_code": result.get("content", "")
            }
            return {"result": "success", "vendor": vendor_name, "adapter_code": result.get("content", "")}
        except Exception as e:
            return {"result": "error", "error": str(e)}

    def get_vendor_adapter(self, vendor_name: str) -> Dict[str, Any]:
        """
        استرجاع كود adapter لمزود معين
        """
        return self.vendors.get(vendor_name, {"error": "Vendor not found"})
