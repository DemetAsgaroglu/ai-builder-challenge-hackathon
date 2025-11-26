
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from src.modules.statistics import StatisticsModule
from src.schemas.models import CalculationResult

@pytest.mark.asyncio
async def test_statistics_mean():
    # Mock Gemini Agent
    mock_agent = MagicMock()
    mock_agent.generate_json_response = AsyncMock(return_value={
        "data": [1, 2, 3, 4, 5],
        "operation": "mean",
        "explanation": "Test mean"
    })
    
    module = StatisticsModule(mock_agent)
    result = await module.calculate("[1, 2, 3, 4, 5] ortalamasi")
    
    assert result.result == 3.0
    assert result.domain == "statistics"
    assert result.confidence_score == 1.0

@pytest.mark.asyncio
async def test_statistics_median():
    # Mock Gemini Agent
    mock_agent = MagicMock()
    mock_agent.generate_json_response = AsyncMock(return_value={
        "data": [1, 2, 3, 4, 5],
        "operation": "median",
        "explanation": "Test median"
    })
    
    module = StatisticsModule(mock_agent)
    result = await module.calculate("[1, 2, 3, 4, 5] medyani")
    
    assert result.result == 3.0

@pytest.mark.asyncio
async def test_statistics_std():
    # Mock Gemini Agent
    mock_agent = MagicMock()
    mock_agent.generate_json_response = AsyncMock(return_value={
        "data": [2, 4, 4, 4, 5, 5, 7, 9],
        "operation": "std",
        "explanation": "Test std"
    })
    
    module = StatisticsModule(mock_agent)
    result = await module.calculate("standart sapma")
    
    # std of [2, 4, 4, 4, 5, 5, 7, 9] is 2.0
    assert result.result == 2.0

if __name__ == "__main__":
    # Manual run for quick check
    async def run_manual():
        print("Running manual test...")
        mock_agent = MagicMock()
        mock_agent.generate_json_response = AsyncMock(return_value={
            "data": [10, 20, 30],
            "operation": "mean",
            "explanation": "Manual test"
        })
        module = StatisticsModule(mock_agent)
        res = await module.calculate("test")
        print(f"Result: {res.result}")
        
    asyncio.run(run_manual())
