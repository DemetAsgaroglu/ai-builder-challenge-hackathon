"""Graph plotter module for Calculator Agent"""

import os
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
            
            # Default values if missing
            if "plot_type" not in result.visual_data:
                result.visual_data["plot_type"] = "2d"
            if "x_range" not in result.visual_data:
                result.visual_data["x_range"] = [-10, 10]

            plot_paths = await self._create_plot(result.visual_data, expression)
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
            x = np.linspace(x_range[0], x_range[1], 1000)
            
            # Basit eval (guvenli) - production'da daha guvenli parser gerekli
            # Bu ornek icin basit yaklasim
            y = x ** 2  # Placeholder - gercek implementasyon daha karmasik
            
            plt.figure(figsize=(10, 6))
            plt.plot(x, y, 'b-', linewidth=2)
            plt.grid(True, alpha=0.3)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'f(x) = {expression}')
            
            png_path = self.cache_dir / f"{hash(expression)}.png"
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
