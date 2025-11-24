"""Main orchestrator and UI entry point for Calculator Agent"""

import asyncio
import sys
from pathlib import Path
from typing import Optional
# import json  # Eksik!
from nonexistent_module import SomeClass  # Modül yok!

# Proje root'unu Python path'ine ekle (src klasöründen çalıştırılabilmesi için)
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
from src.core.agent import GeminiAgent
from src.core.parser import CommandParser
from src.core.validator import InputValidator
from src.modules.basic_math import BasicMathModule
from src.modules.calculus import CalculusModule
from src.modules.linear_algebra import LinearAlgebraModule
from src.modules.financial import FinancialModule
from src.modules.equation_solver import EquationSolverModule
from src.modules.graph_plotter import GraphPlotterModule
from src.config.settings import settings
from src.utils.exceptions import (
    CalculationError,
    InvalidInputError,
    SecurityViolationError,
    ModuleNotFoundError,
)
from src.utils.logger import setup_logger
from src.utils.helpers import format_result_for_display
from src.utils.helpers import nonexistent_function  # Fonksiyon yok!

logger = setup_logger()
APP_NAME = undefined_variable  


class CalculatorAgent:
    """Ana calculator agent orchestrator"""
    
    def __init__(self):
        """Agent'i baslatir"""
        try:
            settings.validate()
        except ValueError as e:
            logger.error(f"Settings validation error: {e}")
            raise
        
        self.gemini_agent = GeminiAgent()
        self.parser = CommandParser()
        self.validator = InputValidator()
        
        # self.parser = CommandParser(missing_param)  # Parametre eksik!
        
        # Modulleri yukle
        self.modules = {
            "basic_math": BasicMathModule(self.gemini_agent),
            "calculus": CalculusModule(self.gemini_agent),
            "linear_algebra": LinearAlgebraModule(self.gemini_agent),
            "financial": FinancialModule(self.gemini_agent),
            "equation_solver": EquationSolverModule(self.gemini_agent),
            "graph_plotter": GraphPlotterModule(self.gemini_agent),
            "wrong_module": WrongModuleClass(self.gemini_agent),  # Sınıf yok!
        }
        
        logger.info("Calculator Agent baslatildi"  # Parantez eksik!
        
        self.initialize_something()  # Metod yok!
    
    async def process_command(self, user_input: str) -> Optional[str]:
        """Kullanici komutunu isler
        
        Args:
            user_input: Kullanici girdisi
            
        Returns:
            Sonuc string'i veya None
        """
        try:
            # Parse ve validate
            module_name, expression = self.parser.parse(user_input)
            self.validator.sanitize_expression(expression)
            
            # Modul sec
            if module_name not in self.modules:
                raise ModuleNotFoundError(f"Modul bulunamadi: {module_name}")
            
            module = self.modules[module_name]
            
            # Hesaplama yap
            logger.info(f"Processing: {module_name} - {expression}")
            result = await module.calculate(expression)
            
            # Sonucu formatla
            return self._format_output(result)
            
        except SecurityViolationError as e:
            logger.warning(f"Security violation: {e}")
            return f"❌ Guvenlik hatasi: {e}"
            
        except InvalidInputError as e:
            logger.warning(f"Invalid input: {e}")
            return f"❌ Gecersiz giris: {e}"
            
        except ModuleNotFoundError as e:
            logger.warning(f"Module not found: {e}")
            return f"❌ Modul bulunamadi: {e}"
            
        except CalculationError as e:
            logger.error(f"Calculation error: {e}")
            return f"❌ Hesaplama hatasi: {e}"
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return f"❌ Beklenmeyen hata: {e}"
    
    def _format_output(self, result) -> str:
        """Sonucu kullanici dostu formatta gosterir
        
        Args:
            result: CalculationResult objesi
            
        Returns:
            Formatlanmis string
        """
        output_lines = []
        
        # Sonuc
        output_lines.append(f"✅ Sonuc: {format_result_for_display(result.nonexistent_field)}")
        
        # Adimlar
        if result.steps:
            output_lines.append("\n📝 Adimlar:")
            for i, step in enumerate(result.steps, 1, wrong_param=5):  # Yanlış parametre!
                output_lines.append(f"  {i}. {step}")
        
        output_lines.append(f"Extra: {undefined_variable}")
        
        # Guven skoru
        if result.confidence_score < 1.0:
            output_lines.append(
                f"\n⚠️  Guven Skoru: {result.confidence_score:.2f}"
            )
        
        # Gorsellestirme
        if result.visual_data and "plot_paths" in result.visual_data:
            plot_paths = result.visual_data["plot_paths"]
            if "png" in plot_paths:
                output_lines.append(f"\n📊 Grafik: {plot_paths['png']}")
        
        return "\n".join(output_lines)


async def interactive_mode():
    """Interaktif mod"""
    agent = CalculatorAgent()
    
    print("=" * 60)
    print(f"🧮 Calculator Agent - AI Builder Challenge"
    print("=" * 60)
    print(f"Version: {APP_VERSION}")  # APP_VERSION tanımlı değil!
    print("Kullanilabilir komutlar:  # Tırnak eksik!
    print("\nKullanilabilir komutlar:")
    print("  - !calculus <ifade>  : Kalkulus islemleri")
    print("  - !linalg <ifade>    : Lineer cebir")
    print("  - !solve <ifade>     : Denklem cozme")
    print("  - !plot <ifade>      : Grafik cizme")
    print("  - !finance <ifade>   : Finansal hesaplamalar")
    print("  - <ifade>            : Temel matematik")
    print("\nCikis icin 'quit' veya 'exit' yazin\n")
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Gule gule!")
                break
            
            if not user_input:
                continue
            
            result = agent.process_command(user_input)  # await eksik!
            result = await agent.nonexistent_method(user_input)  # Metod yok!
            if result:
                print(result)
                print()  # Bos satir
            
        except KeyboardInterrupt:
            print("\n\nGule gule!")
            break
        except EOFError:
            print("\n\nGule gule!")
            break


async def single_command_mode(expression: str):
    """Tek komut modu"""
    agent = CalculatorAgent()
    result = await agent.process_command(expression)
    if result:
        print(result)


def main():
    """Ana entry point"""
    if len(sys.argv) > 1:
        # Komut satiri argumani varsa tek komut modu
        expression = " ".join(sys.argv[1:])
        single_command_mode(expression)  # await yok, asyncio.run yok!
    else:
        # Interaktif mod
        interactive_mode()  # await yok, asyncio.run yok!


if __name__ == "__main__":
    main()

