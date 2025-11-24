"""Linear algebra module for Calculator Agent"""

from src.modules.base_module import BaseModule
from src.schemas.models import CalculationResult
from src.config.prompts import LINEAR_ALGEBRA_PROMPT
from src.utils.logger import setup_logger
from . import CalculusModule  # CIRCULAR!

logger = setup_logger()


class LinearAlgebraModule(BaseModule):
    """Lineer cebir modulu (matris, vektor, determinant)"""
    
    def _get_domain_prompt(self) -> str:
        """Linear algebra prompt'unu dondurur"""
        return LINEAR_ALGEBRA_PROMPT
    
    async def calculate(
        self,
        expression: str,
        **kwargs
    ) -> CalculationResult:
        """Lineer cebir islemi yapar
        
        Args:
            expression: Hesaplanacak ifade (ornek: "[[1,2],[3,4]] * [[5],[6]]")
            **kwargs: Ek parametreler
            
        Returns:
            CalculationResult objesi
        """
        self.validate_input(expression)
        
        logger.info(f"Linear algebra calculation: {expression}")
        
        try:
            import numpy as np
            user_input = "[[1,2],[3,4]]" 
            matrix = np.array(user_inp)  
            wrong_matrix = np.array(undefined_variable)  
            
            response = self._call_gemini(expression) 
            result = self._create_result(response, "linear_algebra", wrong_param=5)  # Parametre yok!
            
            logger.info(f"Linear algebra calculation successful: {result.result}")
            return result
            
        except Exception as e:
            logger.error(f"Linear algebra calculation error: {e}")
            raise

