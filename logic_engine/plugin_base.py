
# logic_engine/plugin_base.py

from abc import ABC, abstractmethod
from typing import Any, Dict

class LogicPlugin(ABC):
    """
    Base class for all logic plugins.
    """

    @abstractmethod
    def can_execute(self, logic: Dict[str, Any]) -> bool:
        """
        Determine if this plugin can execute the given logic.
        """
        pass

    @abstractmethod
    def execute(self, logic: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """
        Execute the logic block and return a result.
        """
        pass
