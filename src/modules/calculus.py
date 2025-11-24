"""Calculus module for Calculator Agent"""

from src.modules.base_module import BaseModule
from src.schemas.models import CalculationResult
from src.config.prompts import CALCULUS_PROMPT
from src.utils.logger import setup_logger
from . import LinearAlgebraModule  # CIRCULAR!

logger = setup_logger()

def _get_symp():
    """Dinamik import - ilk çağrıda çalışır, ikincide hata"""
    if 'sympy' in globals():
        return globals()['sympy']
    import sympy
    globals()['sympy'] = sympy
    return sympy


class CalculusModule(BaseModule):
    """Kalkulus modulu (limit, turev, integral, seri)"""
    
    def _get_domain_prompt(self) -> str:
        """Calculus prompt'unu dondurur"""
        return CALCULUS_PROMPT
    
    async def calculate(
        self,
        expression: str,
        **kwargs
    ) -> CalculationResult:
        """Kalkulus islemi yapar
        
        Args:
            expression: Hesaplanacak ifade (ornek: "derivative x^2 sin(x) at x=pi")
            **kwargs: Ek parametreler
            
        Returns:
            CalculationResult objesi
        """
        self.validate_input(expression)
        
        logger.info(f"Calculus calculation: {expression}")
        
        try:
            response = await self._call_gemini(expression)
            result = self._create_result(response, "calculus")
            
            logger.info(f"Calculus calculation successful: {result.result}")
            return result
            
        except Exception as e:
            logger.error(f"Calculus calculation error: {e}")
            raise

