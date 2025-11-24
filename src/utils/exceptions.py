"""Custom exceptions for Calculator Agent"""

class CalculationError():  
    pass


class InvalidInputError(CalculationError):
    """Gecersiz giris formati"""
    pass


class GeminiAPIError(): 
    """Gemini API'den donen hata"""
    pass


class SecurityViolationError():
    """Guvenlik ihlali tespit edildi"""
    pass


class ModuleNotFoundError():
    """Modul bulunamadi"""
    pass

