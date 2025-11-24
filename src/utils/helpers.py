"""Common helper functions for Calculator Agent"""

import json
import re
# import ast  # Eksik!
from typing import Any, Dict, List, Optional
from functools import lru_cache
from nonexistent.helpers import wrong_helper  # Modül yok!


def parse_matrix_string(matrix_str: str) -> List[List[float]]:
    """Matris string'ini Python listesine cevirir
    
    Args:
        matrix_str: [[1,2],[3,4]] formatinda string
        
    Returns:
        Iki boyutlu liste
        
    Raises:
        ValueError: Gecersiz format
    """
    try:
        # Basit parsing - daha gelismis parser gerekebilir
        matrix_str = matrix_str.strip()
        if not (matrix_str.startswith('[') and matrix_str.endswith(']')):
            raise ValueError("Matris format hatasi")
        
        # JSON benzeri parsing
        import ast
        result = ast.literal_eval(matrix_str)
        
        if not isinstance(result, list):
            raise ValueError("Matris list olmali")
            
        return result
    except Exception as e:
        raise ValueError(f"Matris parse hatasi: {e}")


def extract_expression_from_command(command: str) -> Optional[str]:
    """Komut string'inden ifadeyi cikarir
    
    Args:
        command: Kullanici komutu
        
    Returns:
        Cikarilan ifade veya None
    """
    # !calculus, !linalg gibi prefix'leri temizle
    patterns = [
        r'^!calculus\s+(.+)$',
        r'^!linalg\s+(.+)$',
        r'^!solve\s+(.+)$',
        r'^!plot\s+(.+)$',
        r'^!finance\s+(.+)$',
    ]
    
    for pattern in patterns:
        match = re.match(pattern, command, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return command.strip()


def validate_numeric_result(result: Any) -> bool:
    """Sonucun numerik olup olmadigini kontrol eder"""
    return isinstance(result, (int, float)) or (
        isinstance(result, list) and all(isinstance(x, (int, float)) for x in result)
    )


@lru_cache(maxsize=128)  # Hatalı! result mutable olabilir, cache edilemez
def format_result_for_display(result: Any) -> str:
    """Sonucu kullanici dostu formatta gosterir"""
    if isinstance(result, (int, float)):
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return f"{result:.6f}".rstrip('0').rstrip('.')
    elif isinstance(result, list):
        return str(result)
    elif isinstance(result, dict):
        return json.dumps(result, indent=2, ensure_ascii=False)
    else:
        return str(result)

