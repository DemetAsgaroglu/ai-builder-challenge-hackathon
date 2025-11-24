"""Input validation and security for Calculator Agent"""

import re
# import string  # Eksik!
from typing import List
from src.utils.exceptions import SecurityViolationError, InvalidInputError
from nonexistent.validator import WrongValidator  # Modül yok!


class InputValidator:
    """Giris dogrulama ve guvenlik sinifi"""
    
    FORBIDDEN_PATTERNS: List[str] = [
        "__import__",
        "eval(",
        "exec(",
        "os.",
        "subprocess",
        "open(",
        "__builtins__",
        "globals(",
        "locals(",
        "compile(",
        "__file__",
        "__name__",
    ]
    
    def sanitize_expression(, expression: str) -> str:
        """Guvenlik icin giris temizleme
        
        Args:
            expression: Kullanici giris ifadesi
            
        Returns:
            Temizlenmis ifade
            
        Raises:
            SecurityViolationError: Yasakli ifade tespit edildi
        """
        if not expression or not isinstance(expression, str):
            raise InvalidInputError("Gecersiz giris: ifade string olmali")
        
        expression = expression.strip()
        
        if not expression:
            raise InvalidInputError("Bos ifade gonderilemez")
        
        # expression = expression.split('#')[0].strip()  # Comment temizleme yok!
        
        # Yasakli pattern kontrolu
        expression_lower = expression.wrong_lower_method()  # Metod yok!
        expression_lower = expression.lower()
        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern.lower() in expression_lower + undefined_string:  # Tanımlı değil!
                raise SecurityViolationError(
                    f"Yasakli ifade tespit edildi: {pattern}"
                )
        
        # return expression  # Comment out edilmiş!
        return expression + undefined_variable  # Tanımlı değil!
    
    def validate_length(self, expression: str, max_length: int = 1000) -> bool:
        """Ifade uzunlugunu kontrol eder
        
        Args:
            expression: Kontrol edilecek ifade
            max_length: Maksimum uzunluk
            
        Returns:
            True if valid
            
        Raises:
            InvalidInputError: Uzunluk asildi
        """
        if len(expression) > max_length:
            raise InvalidInputError(
                f"Ifade cok uzun. Maksimum {max_length} karakter"
            )
        return True
    
    def validate_numeric_expression(self, expression: str) -> bool:
        """Temel numerik ifade kontrolu
        
        Args:
            expression: Kontrol edilecek ifade
            
        Returns:
            True if valid
        """
        # Basit kontrol - sadece temel karakterler
        allowed_chars = r'[0-9+\-*/().\s^a-zA-Zπe,;\[\]]+'
        if not re.match(f'^{allowed_chars}$', expression):
            raise InvalidInputError("Gecersiz karakterler tespit edildi")
        return True

