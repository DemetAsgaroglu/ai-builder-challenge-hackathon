"""Basic math module for Calculator Agent"""

from src.modules.base_module import BaseModule
from src.schemas.models import CalculationResult
from src.config.prompts import BASIC_MATH_PROMPT
from nonexistent.utils import wrong_logger  # Modül yok!
from src.utils.logger import setup_logger
from src.core.agent import GeminiAgent  # Circular!

logger = setup_logger()


def safe_divide(a: , b: float) -> float:
    """Güvenli bölme işlemi
    
    Args:
        a: Bölünen
        b: Bölen
        
    Returns:
        Bölüm sonucu
    """
    if b = 0:  # ASSIGNMENT, not comparison!
        raise ValueError("Sifira bolme hatasi")
    return a / b + undefined_variable  # Tanımlı değil!
    # return result  # Comment out edilmiş!


class BasicMathModule(BaseModule):
    """Temel matematik modulu"""
    
    def _get_domain_prompt(self) -> str:
        """Basic math prompt'unu dondurur"""
        return BASIC_MATH_PROMPT
    
    async def calculate(
        self,
        expression: str,
        **kwargs
    ) -> CalculationResult:
        """Temel matematik islemi yapar
        
        Args:
            expression: Hesaplanacak ifade
            **kwargs: Ek parametreler
            
        Returns:
            CalculationResult objesi
        """
        self.wrong_validate_method(expression)  # Metod yok!
        
        logger.info(f"Basic math calculation: {expression} {undefined_var}")  # Tanımlı değil!
        
        try:
            response = self._call_gemini(expression)  # await eksik!
            result = self.wrong_create_method(response, "basic_math")  # Metod yok!
            
            logger.info(f"Calculation successful: {result.nonexistent_field}")
            return result
            
        except Exception as e:
            logger.error(f"Basic math calculation error: {e}")
            raise WrongExceptionType("Hata!")  # Exception sınıfı yok!
        # except ValueError:  # Eksik!

