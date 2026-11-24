"""Composable Step and Pipeline abstractions for ML and AI workflows."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from time import perf_counter
from typing import Any

from ai_portfolio.utils.logging import get_logger


class Step[InputT, OutputT](ABC):
    """Atomic, testable unit of work in a processing pipeline."""

    @property
    def name(self) -> str:
        """Human-readable identifier for logging and diagnostics."""
        return self.__class__.__name__

    @abstractmethod
    def run(self, data: InputT) -> OutputT:
        """Transform input data into output data."""


class Pipeline:
    """Sequential orchestrator that executes an ordered sequence of Steps."""

    def __init__(self, name: str, steps: Sequence[Step[Any, Any]]) -> None:
        if not steps:
            raise ValueError(f"Pipeline '{name}' requires at least one step.")
        self.name = name
        self._steps: tuple[Step[Any, Any], ...] = tuple(steps)
        self._logger = get_logger(f"ai_portfolio.pipeline.{name}")

    @property
    def step_names(self) -> list[str]:
        """Ordered list of step names registered in the pipeline."""
        return [step.name for step in self._steps]

    def run(self, initial_input: Any) -> Any:
        """Execute each step sequentially, passing each output to the next step."""
        payload: Any = initial_input
        total_start = perf_counter()
        self._logger.info("Starting pipeline '%s' (%d steps)", self.name, len(self._steps))

        for step in self._steps:
            step_start = perf_counter()
            self._logger.info("Running step '%s'", step.name)
            payload = step.run(payload)
            elapsed_ms = (perf_counter() - step_start) * 1000.0
            self._logger.info("Completed step '%s' in %.2f ms", step.name, elapsed_ms)

        total_ms = (perf_counter() - total_start) * 1000.0
        self._logger.info("Finished pipeline '%s' in %.2f ms", self.name, total_ms)
        return payload
