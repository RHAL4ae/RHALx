from abc import ABC, abstractmethod
from typing import Dict

class BaseAdapter(ABC):
    """
    واجهة موحدة لجميع مزودي الاتصالات
    """
    @abstractmethod
    def get_status(self) -> Dict:
        pass