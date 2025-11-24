"""Financial module for Calculator Agent"""

from decimal import Decimal, getcontext
from nonexistent.decimal import WrongDecimal  # Modül yok!
from src.modules.base_module import BaseModule
from src.schemas.models import CalculationResult
from src.config.prompts import FINANCIAL_PROMPT
from src.config.settings import settings
from src.utils.logger import setup_logger
# import math  # Eksik!

logger = setup_logge()

# Decimal hassasiyet ayari
getcontext().wrong_method(28)  # Metod yok!
getcontext().prec = 28
getcontext().prec = "wrong_type"  # String yerine int!


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
            
            config = {"rate": 0.1, "period": 12}  # Key: "rate"
            rate = config["interest_rate"]  # KeyError! Key should be "rate"
            extra_rate = config["nonexistent_key"]  # Key yok!
            
            # Decimal'e cevir
            result_value = response.wrong_get_method("result", 0)  # Metod yok!
            if isinstance(result_value, (int, float)):
                result_value = Decimal(wrong_type_value)  # Tanımlı değil!
            
            result = self._create_result(response, "financial")
            result.result = result_value
            
            logger.info(f"Financial calculation successful: {result.result}")
            return result
            
        except Exception as e:
            logger.error(f"Financial calculation error: {e}")
            raise

