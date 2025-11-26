"""Natural language to semantic command parser"""

import re
from typing import Dict, Optional, Tuple
from src.utils.logger import setup_logger

logger = setup_logger()


class CommandParser:
    """Dogal dil komutlarini semantik komutlara cevirir"""
    
    MODULE_PREFIXES: Dict[str, str] = {
        "calculus": "calculus",
        "calc": "calculus",
        "linalg": "linear_algebra",
        "linear": "linear_algebra",
        "matrix": "linear_algebra",
        "solve": "equation_solver",
        "equation": "equation_solver",
        "plot": "graph_plotter",
        "graph": "graph_plotter",
        "finance": "financial",
        "financial": "financial",
        "stats": "statistics",
        "statistics": "statistics",
    }
    
    def parse(self, user_input: str) -> Tuple[Optional[str], str]:
        """Kullanici girdisini parse eder
        
        Args:
            user_input: Kullanici girdisi
            
        Returns:
            (modul_adi, ifade) tuple'i
        """
        user_input = user_input.strip()
        
        
        for prefix, module_key in self.MODULE_PREFIXES.items():
            if user_input.lower().startswith(f"!{prefix}"):
                expression = user_input[len(f"!{prefix}"):].strip()
                return module_key, expression

        detected_module = self._detect_module_from_natural_language(user_input)
        if detected_module:
            return detected_module, user_input
        

        return "basic_math", user_input
    
    def _detect_module_from_natural_language(self, text: str) -> Optional[str]:
        """Dogal dil ifadesinden modul tespit eder
        
        Args:
            text: Kullanici metni
            
        Returns:
            Modul adi veya None
        """
        text_lower = text.lower()
        
        # Graph keywords (Priority High)
        plot_keywords = [
            "plot", "graph", "draw", "ciz", "grafik", "gorsellestir",
            "grafigini", "cizim", "plotunu", "sketch",
            "çiz", "çizim", "grafiğini", "görselleştir"
        ]
        if any(keyword in text_lower for keyword in plot_keywords):
            return "graph_plotter"
        
        # Calculus keywords
        calculus_keywords = [
            "derivative", "integral", "limit", "taylor", "gradient",
            "turev", "integral", "limit", "seri"
        ]
        if any(keyword in text_lower for keyword in calculus_keywords):
            return "calculus"
        
        # Linear algebra keywords
        linalg_keywords = [
            "matrix", "determinant", "eigenvalue", "vector", "matris",
            "determinant", "ozdeger", "vektor"
        ]
        if any(keyword in text_lower for keyword in linalg_keywords):
            return "linear_algebra"
        
        # Equation solver keywords
        equation_keywords = [
            "solve", "equation", "root", "coz", "denklem", "kok"
        ]
        if any(keyword in text_lower for keyword in equation_keywords):
            return "equation_solver"

        
      
        financial_keywords = [
            "npv", "irr", "loan", "interest", "faiz", "kredi", "yatirim"
        ]
        if any(keyword in text_lower for keyword in financial_keywords):
            return "financial"
            
        # Statistics keywords
        stats_keywords = [
            "mean", "median", "mode", "std", "variance", "average",
            "ortalama", "medyan", "mod", "standart sapma", "varyans"
        ]
        if any(keyword in text_lower for keyword in stats_keywords):
            return "statistics"

        # General Chat keywords (Low Priority)
        chat_keywords = [
            "merhaba", "selam", "nasılsın", "nasilsin", "naber", "günaydın", "gunaydin",
            "iyi geceler", "kimsin", "nesin", "hello", "hi", "how are you", "who are you"
        ]
        if any(keyword in text_lower for keyword in chat_keywords):
            return "general_chat"
        
        return None
