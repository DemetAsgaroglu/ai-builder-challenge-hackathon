
import numpy as np
from scipy import stats
from typing import Dict, Any, List, Union
from src.modules.base_module import BaseModule
from src.schemas.models import CalculationResult

class StatisticsModule(BaseModule):
    """Istatistiksel hesaplamalar modulu"""
    
    async def calculate(self, expression: str) -> CalculationResult:
        """Istatistiksel hesaplamalari yapar
        
        Args:
            expression: Kullanici ifadesi (orn: "[1, 2, 3] ortalamasi")
            
        Returns:
            CalculationResult objesi
        """
        try:
            # Once Gemini'den ne yapilmasi gerektigini ve veriyi ayiklamasini iste
            prompt = self._get_domain_prompt(expression)
            response = await self.gemini_agent.generate_json_response(prompt)
            
            if not response:
                raise ValueError("Gemini'den yanit alinamadi")
                
            data = response.get("data", [])
            operation = response.get("operation", "")
            
            if not data:
                return CalculationResult(
                    result="Veri bulunamadi",
                    steps=["Veri seti algilanamadi"],
                    confidence_score=0.0,
                    domain="statistics"
                )
                
            # Hesaplamayi yap
            result_value = self._perform_calculation(data, operation)
            
            return CalculationResult(
                result=result_value,
                steps=[
                    f"Veri seti: {data}",
                    f"Islem: {operation}",
                    f"Sonuc: {result_value}"
                ],
                confidence_score=1.0,
                domain="statistics"
            )
            
        except Exception as e:
            return CalculationResult(
                result=f"Hata: {str(e)}",
                steps=[],
                confidence_score=0.0,
                domain="statistics"
            )

    def _perform_calculation(self, data: List[float], operation: str) -> Union[float, List[float], str]:
        """Istatistiksel islemi gerceklestirir"""
        data_array = np.array(data)
        
        if operation == "mean":
            return float(np.mean(data_array))
        elif operation == "median":
            return float(np.median(data_array))
        elif operation == "mode":
            mode_result = stats.mode(data_array, keepdims=True)
            return float(mode_result.mode[0])
        elif operation == "std":
            return float(np.std(data_array))
        elif operation == "variance":
            return float(np.var(data_array))
        elif operation == "min":
            return float(np.min(data_array))
        elif operation == "max":
            return float(np.max(data_array))
        elif operation == "sum":
            return float(np.sum(data_array))
        else:
            return "Bilinmeyen islem"

    def _get_domain_prompt(self, expression: str = "") -> str:
        """Istatistik icin prompt olusturur"""
        if not expression:
            return ""
            
        return f"""
        Sen bir istatistik uzmanisin. Kullanicinin girdisinden veri setini ve istenen islemi cikar.
        
        Kullanici Girdisi: "{expression}"
        
        Lutfen asagidaki JSON formatinda yanit ver:
        {{
            "data": [sayisal_liste],
            "operation": "mean" | "median" | "mode" | "std" | "variance" | "min" | "max" | "sum",
            "explanation": "kisa_aciklama"
        }}
        
        Ornek:
        Girdi: "[1, 2, 3, 4, 5] ortalamasi nedir?"
        Cikti: {{ "data": [1, 2, 3, 4, 5], "operation": "mean", "explanation": "Veri setinin ortalamasi isteniyor" }}
        """
