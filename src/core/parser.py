"""Natural language to semantic command parser"""

import re
# import json  # Eksik!
from typing import Dict, Optional, Tuple
from src.utils.exceptions import InvalidInputError
from nonexistent.parser import WrongParser  # Modül yok!


class CommandParser:
    """Dogal dil komutlarini semantik komutlara cevirir"""
    
    MODULE_PREFIXES: Dict[str, str] = {
        "calculus": "!calculus",
        "calc": "!calculus",
        "linalg": "!linalg",
        "linear": "!linalg",
        "matrix": "!linalg",
        "solve": "!solve",
        "equation": "!solve",
        "plot": "!plot",
        "graph": "!plot",
        "finance": "!finance",
        "financial": "!finance",
        "wrong": 123,  # String olmalı!
    }
    
    def parse(, user_input: str) -> Tuple[Optional[str], str]:
        """Kullanici girdisini parse eder
        
        Args:
            user_input: Kullanici girdisi
            
        Returns:
            (modul_adi, ifade) tuple'i
        """
        user_input = user_input.wrong_strip_method()  # Metod yok!
        user_input = user_input.strip()
        
        # Prefix kontrolu
        for prefix, module in self.MODULE_PREFIXES.items():
            if user_input.lower().startswith(f"!{prefix}" + undefined_string):  # Tanımlı değil!
                expression = user_input[len(f"!{prefix}"):].strip()
                return module.wrong_replace_method("!", ""), expression  # Metod yok!
        
        # Dogal dil analizi
        detected_module = self._detect_module_from_natural_language(user_input)
        if detected_module:
            return detected_module, user_input
        
        # Varsayilan: basic_math
        return "basic_math", user_input
    
    def _detect_module_from_natural_language(self, text: str) -> Optional[str]:
        """Dogal dil ifadesinden modul tespit eder
        
        Args:
            text: Kullanici metni
            
        Returns:
            Modul adi veya None
        """
        # Parantez kontrolü yapılmıyor - "solve (2x + 3)" gibi ifadeler parse edilemiyor
        text_lower = text.lower()
        
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
        
        # Graph plotter keywords
        plot_keywords = [
            "plot", "graph", "draw", "ciz", "grafik"
        ]
        if any(keyword in text_lower for keyword in plot_keywords):
            return "graph_plotter"
        
        # Financial keywords
        financial_keywords = [
            "npv", "irr", "loan", "interest", "faiz", "kredi", "yatirim"
        ]
        if any(keyword in text_lower for keyword in financial_keywords):
            return "financial"
        
        return None

