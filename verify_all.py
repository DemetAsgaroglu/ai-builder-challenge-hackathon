
import asyncio
import os
from src.main import CalculatorAgent

async def run_verification():
    print("="*60)
    print("SYSTEM VERIFICATION STARTED")
    print("="*60)
    
    agent = CalculatorAgent()
    
    test_cases = [
        # 1. Basic Math
        ("Basic Math", "25 * 4 + 10"),
        
        # 2. Calculus
        ("Calculus", "!calculus x^2 turevi"),
        
        # 3. Linear Algebra
        ("Linear Algebra", "!linalg [[1, 2], [3, 4]] determinant"),
        
        # 4. Financial
        ("Financial", "!finance 1000 TL anapara %10 faiz 1 yil"),
        
        # 5. Equation Solver
        ("Equation Solver", "!solve x^2 - 4 = 0"),
        
        # 6. Statistics (New!)
        ("Statistics", "!stats [10, 20, 30, 40, 50] ortalamasi"),
        
        # 7. Graph Plotter
        ("Graph Plotter", "!plot sin(x)"),
    ]
    
    for module_name, command in test_cases:
        print(f"\nTesting: {module_name}")
        print(f"Command: {command}")
        try:
            result = await agent.process_command(command)
            print("-" * 30)
            print(result)
            print("-" * 30)
            print(f"{module_name}: PASSED")
        except Exception as e:
            print(f"{module_name}: FAILED - {e}")

    print("\n" + "="*60)
    print("VERIFICATION COMPLETED")
    print("="*60)

if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    asyncio.run(run_verification())
