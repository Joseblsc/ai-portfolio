"""Unit tests for Pipeline and Step abstractions."""

import pytest

from ai_portfolio.utils.pipelines import Pipeline, Step


class AddOneStep(Step[int, int]):
    """Simple test step that increments an integer."""

    def run(self, data: int) -> int:
        return data + 1


class DoubleStep(Step[int, int]):
    """Simple test step that doubles an integer."""

    def run(self, data: int) -> int:
        return data * 2


def test_pipeline_requires_at_least_one_step() -> None:
    """Pipeline initialization rejects an empty sequence of steps."""
    with pytest.raises(ValueError, match="requires at least one step"):
        Pipeline(name="empty", steps=[])


def test_pipeline_chaining_and_step_names() -> None:
    """Pipeline runs steps in order and exposes step class names."""
    pipeline = Pipeline(name="math", steps=[AddOneStep(), DoubleStep()])

    assert pipeline.step_names == ["AddOneStep", "DoubleStep"]
    assert pipeline.run(4) == 10
