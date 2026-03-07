# ///////////////////////////////////////////////////////////////
# SERVICES.BOOTSTRAP.SEQUENCE - Initialization sequence orchestrator
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Explicit step-by-step initialization sequence with status tracking."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from collections.abc import Callable

# Local imports
from ...domain.errors import EzQtError
from ...domain.results import InitResult, InitStepResult
from ...domain.results.result_error import ResultError
from ...utils.printer import get_printer
from .contracts.options import InitOptions
from .contracts.steps import InitStep, StepStatus


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class InitializationSequence:
    """Orchestrates the ordered initialization steps for EzQt_App.

    Each step is registered with a name, description, callable and a
    *required* flag.  If a required step fails the sequence stops
    immediately; non-required steps are allowed to fail silently.
    """

    def __init__(self, options: InitOptions | None = None) -> None:
        self.options = (options or InitOptions()).resolve()
        self.steps: list[InitStep] = []
        self.current_step: InitStep | None = None
        self.printer = get_printer(self.options.verbose)
        self._setup_steps()

    # ------------------------------------------------------------------
    # Error code
    # ------------------------------------------------------------------

    def _error_code_for_step(self, step_name: str) -> str:
        """Return a normalized error code for a failed step."""
        slug = step_name.strip().lower().replace(" ", "_")
        return f"bootstrap.step.{slug}.failed"

    # ------------------------------------------------------------------
    # Default steps
    # ------------------------------------------------------------------

    def _setup_steps(self) -> None:
        """Register the default EzQt_App boot steps."""
        from ..application.app_service import AppService
        from ..application.file_service import FileService
        from .startup_config import StartupConfig

        options = self.options

        self.add_step(
            name="Configure Startup",
            description="Configure UTF-8 encoding, locale, and environment variables",
            function=lambda: StartupConfig().configure(options.project_root),
            required=True,
        )
        self.add_step(
            name="Create Directories",
            description="Create necessary directories for assets, config, and modules",
            function=lambda: FileService(
                base_path=options.project_root,
                bin_path=options.bin_path,
                overwrite_policy=options.overwrite_policy.value,
            ).make_assets_binaries(),
            required=True,
        )
        self.add_step(
            name="Copy Configurations",
            description="Copy package configuration files to project bin/config directory",
            function=lambda: AppService.copy_package_configs_to_project(),
            required=False,
        )
        self.add_step(
            name="Check Requirements",
            description="Verify that all required assets and dependencies are available",
            function=lambda: (
                AppService.check_assets_requirements(
                    base_path=options.project_root,
                    bin_path=options.bin_path,
                    overwrite_policy=options.overwrite_policy.value,
                )
                if options.build_resources
                else None
            ),
            required=True,
        )
        self.add_step(
            name="Generate Files",
            description="Generate required configuration and resource files",
            function=lambda: AppService.make_required_files(
                mk_theme=options.mk_theme,
                mk_config=options.mk_config,
                mk_translations=options.mk_translations,
                base_path=options.project_root,
                bin_path=options.bin_path,
                overwrite_policy=options.overwrite_policy.value,
            ),
            required=True,
        )

    # ------------------------------------------------------------------
    # Step management
    # ------------------------------------------------------------------

    def add_step(
        self,
        name: str,
        description: str,
        function: Callable[[], None],
        required: bool = True,
    ) -> None:
        """Append a new step to the sequence."""
        self.steps.append(
            InitStep(
                name=name, description=description, function=function, required=required
            )
        )

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(self, verbose: bool = True) -> InitResult:
        """Run all registered steps in order.

        Returns
        -------
        InitResult
            Typed aggregate result with step-level execution details.
        """
        import time

        if verbose:
            self.printer.custom_print(
                "~ [Initializer] Starting EzQt_App Initialization Sequence",
                color="MAGENTA",
            )
            self.printer.raw_print("...")

        start_time = time.time()
        successful_steps = 0
        failed_steps = 0
        skipped_steps = 0
        first_error: Exception | None = None
        first_failed_step: str | None = None

        for step in self.steps:
            self.current_step = step
            step_start = time.time()
            step.status = StepStatus.RUNNING

            try:
                step.function()
                step.status = StepStatus.SUCCESS
                step.duration = time.time() - step_start
                successful_steps += 1
            except Exception as e:
                step.status = StepStatus.FAILED
                step.error_message = str(e)
                step.duration = time.time() - step_start
                failed_steps += 1
                if first_error is None:
                    first_error = e
                    first_failed_step = step.name

                if verbose:
                    self.printer.error(
                        f"[Initializer] Step failed ({step.duration:.2f}s): {e}"
                    )

                if step.required:
                    if verbose:
                        self.printer.error(
                            f"[Initializer] Initialization failed at required step: {step.name}"
                        )
                    break

        total_time = time.time() - start_time
        summary = InitResult(
            success=(failed_steps == 0),
            total_steps=len(self.steps),
            successful=successful_steps,
            failed=failed_steps,
            skipped=skipped_steps,
            total_time=total_time,
            steps=[
                InitStepResult(
                    name=step.name,
                    description=step.description,
                    required=step.required,
                    status=step.status.value,
                    error_message=step.error_message,
                    duration=step.duration,
                )
                for step in self.steps
            ],
        )

        if first_error is not None and first_failed_step is not None:
            if isinstance(first_error, EzQtError):
                summary.error = ResultError(
                    code=first_error.code,
                    message=first_error.message,
                    context=first_error.context,
                )
            else:
                summary.error = ResultError(
                    code=self._error_code_for_step(first_failed_step),
                    message=str(first_error),
                    context={
                        "step": first_failed_step,
                        "error_type": type(first_error).__name__,
                    },
                )

        if verbose:
            self._print_summary(summary)

        return summary

    def _print_summary(self, summary: InitResult) -> None:
        self.printer.raw_print("...")
        if summary.success:
            self.printer.custom_print(
                "~ [Initializer] Initialization completed successfully!",
                color="MAGENTA",
            )
        else:
            self.printer.custom_print(
                "~ [Initializer] Initialization failed!", color="MAGENTA"
            )

    # ------------------------------------------------------------------
    # Introspection helpers
    # ------------------------------------------------------------------

    def get_step_status(self, step_name: str) -> StepStatus | None:
        for step in self.steps:
            if step.name == step_name:
                return step.status
        return None

    def get_failed_steps(self) -> list[InitStep]:
        return [s for s in self.steps if s.status == StepStatus.FAILED]

    def get_successful_steps(self) -> list[InitStep]:
        return [s for s in self.steps if s.status == StepStatus.SUCCESS]

    def reset(self) -> None:
        for step in self.steps:
            step.status = StepStatus.PENDING
            step.error_message = None
            step.duration = None
        self.current_step = None
