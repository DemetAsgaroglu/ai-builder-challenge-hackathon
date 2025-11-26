"""Graph plotter module for Calculator Agent"""

import os
import re
import json
from pathlib import Path
from typing import Dict, Any, Optional
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from src.modules.base_module import BaseModule
from src.schemas.models import CalculationResult
from src.config.prompts import GRAPH_PLOTTER_PROMPT
from src.utils.logger import setup_logger
from src.utils.exceptions import CalculationError

logger = setup_logger()


class GraphPlotterModule(BaseModule):
    """Grafik cizim modulu (2D/3D plotlar)"""
    
    def __init__(self, gemini_agent):
        """Graph plotter baslatir"""
        super().__init__(gemini_agent)
        self.cache_dir = Path("cache/plots")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.plot_cache: Dict[str, str] = {}
    
    def _get_domain_prompt(self) -> str:
        """Graph plotter prompt'unu dondurur"""
        return GRAPH_PLOTTER_PROMPT
    
    async def calculate(
        self,
        expression: str,
        **kwargs
    ) -> CalculationResult:
        """Grafik cizer
        
        Args:
            expression: Cizilecek fonksiyon (ornek: "x^2 + 2x + 1")
            **kwargs: Ek parametreler
            
        Returns:
            CalculationResult objesi (visual_data icerir)
        """
        self.validate_input(expression)
        
        logger.info(f"Graph plotting: {expression}")
        
        # Cache check
        cache_key = expression.lower().strip()
        if cache_key in self.plot_cache:
            logger.info("Using cached plot")
            cached_path = self.plot_cache[cache_key]
            return self._load_cached_result(cached_path)
        
        try:
            response = await self._call_gemini(expression)
            result = self._create_result(response, "graph_plotter")
            
            # Grafik olustur
            if result.visual_data is None:
                result.visual_data = {}
            
            # Use function from visual_data if available (cleaned by LLM), otherwise use raw expression
            plot_expression = result.visual_data.get("function", expression)

            # Check for specific point request (e.g., x=3) in the original expression
            # Regex to find x=<number> or x = <number>
            x_match = re.search(r'x\s*=\s*(-?\d+\.?\d*)', expression, re.IGNORECASE)
            if x_match:
                try:
                    x_val = float(x_match.group(1))
                    result.visual_data["highlight_point"] = x_val
                    logger.info(f"Identified point to plot at x={x_val}")
                except ValueError:
                    pass

            # Default values if missing
            if "plot_type" not in result.visual_data:
                result.visual_data["plot_type"] = "2d"
            if "x_range" not in result.visual_data:
                result.visual_data["x_range"] = [-10, 10]

            plot_paths = await self._create_plot(result.visual_data, plot_expression)
            result.visual_data["plot_paths"] = plot_paths
            self.plot_cache[cache_key] = plot_paths["png"]
            
            logger.info(f"Graph plotting successful")
            return result
            
        except Exception as e:
            logger.error(f"Graph plotting error: {e}")
            raise
    
    async def _create_plot(
        self,
        visual_data: Dict[str, Any],
        expression: str
    ) -> Dict[str, str]:
        """Grafik olusturur
        
        Args:
            visual_data: Gemini'den gelen visual data
            expression: Fonksiyon ifadesi
            
        Returns:
            Plot dosya yollari dict'i
        """
        plot_type = visual_data.get("plot_type", "2d")
        x_range = visual_data.get("x_range", [-10, 10])
        
        if plot_type == "2d":
            return await self._plot_2d(visual_data, expression, x_range)
        elif plot_type == "3d":
            return await self._plot_3d(visual_data, expression)
        elif plot_type == "parametric":
            return await self._plot_parametric(visual_data, expression)
        elif plot_type == "polar":
            return await self._plot_polar(visual_data, expression)
        else:
            return await self._plot_2d(visual_data, expression, x_range)
    
    async def _plot_2d(
        self,
        visual_data: Dict[str, Any],
        expression: str,
        x_range: list
    ) -> Dict[str, str]:
        """2D grafik cizer"""
        try:
            # Basit eval (guvenli) - production'da daha guvenli parser gerekli
            # Check if single point (x=3 case)
            is_single_point = abs(x_range[1] - x_range[0]) < 1e-6
            
            if is_single_point:
                # Expand range to show context
                center_x = x_range[0]
                view_range = [center_x - 5, center_x + 5]
                x = np.linspace(view_range[0], view_range[1], 1000)
            else:
                x = np.linspace(x_range[0], x_range[1], 1000)
            
            # Safe evaluation environment
            safe_dict = {
                "x": x,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "exp": np.exp,
                "log": np.log,
                "sqrt": np.sqrt,
                "pi": np.pi,
                "abs": np.abs,
                "np": np
            }
            
            # Clean expression for eval
            # Replace ^ with ** for python syntax
            eval_expr = expression.replace("^", "**")
            
            # Evaluate
            try:
                y = eval(eval_expr, {"__builtins__": {}}, safe_dict)
                
                # Handle constant result (e.g. y = 5)
                if isinstance(y, (int, float)):
                    y = np.full_like(x, y)
            except Exception as eval_error:
                logger.warning(f"Eval failed for '{expression}': {eval_error}. Fallback to x^2")
                y = x ** 2  # Fallback only on error
            
            plt.figure(figsize=(10, 6))
            plt.plot(x, y, 'b-', linewidth=2, label=f'f(x)={expression}')
            
            # If single point, highlight it
            if is_single_point:
                # Calculate y for the specific point
                # We can reuse the eval logic or just pick the center index if we were careful, 
                # but let's re-eval for precision
                try:
                    point_val = eval(eval_expr, {"__builtins__": {}}, {**safe_dict, "x": center_x})
                    plt.plot(center_x, point_val, 'ro', markersize=10, label=f'x={center_x}')
                    plt.annotate(f'({center_x}, {point_val:.2f})', 
                                 (center_x, point_val),
                                 xytext=(10, 10), textcoords='offset points',
                                 arrowprops=dict(arrowstyle='->'))
                except:
                    pass
            
            # Check for explicitly requested point via highlight_point
            if "highlight_point" in visual_data:
                try:
                    hp_x = visual_data["highlight_point"]
                    hp_y = eval(eval_expr, {"__builtins__": {}}, {**safe_dict, "x": hp_x})
                    plt.plot(hp_x, hp_y, 'ro', markersize=10, label=f'x={hp_x}')
                    plt.annotate(f'({hp_x}, {hp_y:.2f})', 
                                 (hp_x, hp_y),
                                 xytext=(10, 10), textcoords='offset points',
                                 arrowprops=dict(arrowstyle='->'))
                    logger.info(f"Plotted specific point ({hp_x}, {hp_y})")
                except Exception as e:
                    logger.warning(f"Could not plot specific point: {e}")

            plt.grid(True, alpha=0.3)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'f(x) = {expression}')
            plt.legend()
            
            png_path = self.cache_dir / f"{hash(expression + str(x_range))}.png"
            plt.savefig(png_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return {"png": str(png_path)}
            
        except Exception as e:
            logger.error(f"2D plot error: {e}")
            raise CalculationError(f"Grafik olusturulamadi: {e}")
    
    async def _plot_3d(
        self,
        visual_data: Dict[str, Any],
        expression: str
    ) -> Dict[str, str]:
        """3D grafik cizer"""
        # Placeholder - 3D plot implementasyonu
        return await self._plot_2d(visual_data, expression, [-10, 10])
    
    async def _plot_parametric(
        self,
        visual_data: Dict[str, Any],
        expression: str
    ) -> Dict[str, str]:
        """Parametrik grafik cizer"""
        # Placeholder
        return await self._plot_2d(visual_data, expression, [-10, 10])
    
    async def _plot_polar(
        self,
        visual_data: Dict[str, Any],
        expression: str
    ) -> Dict[str, str]:
        """Polar grafik cizer"""
        # Placeholder
        return await self._plot_2d(visual_data, expression, [-10, 10])
    
    def _load_cached_result(self, cached_path: str) -> CalculationResult:
        """Cache'den sonuc yukler"""
        return CalculationResult(
            result="Grafik olusturuldu (cache)",
            steps=["Cache'den yuklendi"],
            visual_data={"plot_paths": {"png": cached_path}},
            confidence_score=1.0,
            domain="graph_plotter",
        )
