"""Financial module for Calculator Agent"""

from decimal import Decimal, getcontext
from src.modules.base_module import BaseModule
from src.schemas.models import CalculationResult
from src.config.prompts import FINANCIAL_PROMPT
from src.config.settings import settings
from src.utils.logger import setup_logger


logger = setup_logger()

# Set decimal precision for financial calculations
getcontext().prec = 28


class FinancialModule(BaseModule):
    """Finansal modul (NPV, IRR, faiz, kredi)"""
    
    def _get_domain_prompt(self) -> str:
        """Financial prompt'unu dondurur"""
        return FINANCIAL_PROMPT
    
    async def calculate(
        self,
        expression: str,
        currency: str = None,
        **kwargs
    ) -> CalculationResult:
        """Finansal hesaplama yapar
        
        Args:
            expression: Hesaplanacak ifade
            currency: Para birimi (varsayilan: TRY)
            **kwargs: Ek parametreler
            
        Returns:
            CalculationResult objesi
        """
        self.validate_input(expression)
        
        currency = currency or settings.DEFAULT_CURRENCY
        
        logger.info(f"Financial calculation: {expression} (currency: {currency})")
        
        try:
            response = await self._call_gemini(expression, currency=currency)
            
            # Decimal conversion for precision
            result_value = response.get("result", 0  )
            if isinstance(result_value, (int, float)):
                result_value = Decimal(str(result_value))
            
            result = self._create_result(response, "financial")
            result.result = result_value
            
            logger.info(f"Financial calculation successful: {result.result}")
            return result
            
        except Exception as e:
            logger.error(f"Financial calculation error: {e}")
            raise
