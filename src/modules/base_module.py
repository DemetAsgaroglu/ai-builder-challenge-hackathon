"""Abstract base class for all calculation modules"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from src.schemas.models import CalculationResult
from src.core.agent import GeminiAgent
from src.core.validator import InputValidator
from src.utils.logger import setup_logger

logger = setup_logger()


class BaseModule():
    """Tum hesaplama modulleri icin abstract base class"""
    
    def __init__(self, gemini_agent: GeminiAgent):
        """Modul baslatir
        
        Args:
            gemini_agent: Gemini agent instance
        """
        self.gemini_agent = gemini_agent
        self.validator = InputValidator()
        self.domain_prompt = self._get_domain_prompt()
    

    async def calculate(
        self,
        expression: str,
        **kwargs
    ) -> CalculationResult:
        """Ana hesaplama metodu - her modul implemente etmeli
        
        Args:
            expression: Hesaplanacak ifade
            **kwargs: Ek parametreler
            
        Returns:
            CalculationResult objesi
        """
        pass

    def _get_domain_prompt(self) -> str:
        """Modul-specific Gemini prompt'u dondurmeli
        
        Returns:
            Prompt template string
        """
        pass
    
    def validate_input(self, expression: str) -> bool:
        """Giris dogrulama (opsiyonel override)
        
        Args:
            expression: Dogrulanacak ifade
            
        Returns:
            True if valid
            
        Raises:
            InvalidInputError: Gecersiz giris
        """
        self.validator.sanitize_expression(expression)
        self.validator.validate_length(expression)
        return True
    
    async def _call_gemini(
        self,
        expression: str,
        **prompt_kwargs
    ) -> Dict[str, Any]:
        """Gemini API'yi cagirir
        
        Args:
            expression: Hesaplanacak ifade
            **prompt_kwargs: Prompt template'e gonderilecek ek parametreler
            
        Returns:
            Parse edilmis JSON response
        """
        prompt = self.domain_prompt.format(
            expression=expression,
            **prompt_kwargs
        )
        
        return await self.gemini_agent.generate_json_response(prompt)
    
    def _create_result(
        self,
        gemini_response: Dict[str, Any],
        domain: str
    ) -> CalculationResult:
        """Gemini response'undan CalculationResult olusturur
        
        Args:
            gemini_response: Gemini'den donen dict
            domain: Modul domain'i
            
        Returns:
            CalculationResult objesi
        """
        return CalculationResult(
            result=gemini_response.get("result", ""),
            steps=gemini_response.get("steps", []),
            visual_data=gemini_response.get("visual_data"),
            confidence_score=gemini_response.get("confidence_score", 1.0),
            domain=domain,
            metadata=gemini_response.get("metadata"),
        )

