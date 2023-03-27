from collatz_activity import collatz
import pytest


@pytest.mark.asyncio
async def test_collatz():
    result = await collatz(6)
    assert result == ([3, 10, 5, 16, 8, 4, 2, 1], 8)
    result = await collatz(3)
    assert result == ([10, 5, 16, 8, 4, 2, 1], 7)
