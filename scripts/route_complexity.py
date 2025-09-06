#!/usr/bin/env python3
"""
Central Complexity Router for Claude Code Configuration System

Provides centralized complexity scoring, agent selection, and validation routing
with consistent behavior across all commands.
"""

import argparse
import json
import os
import sys
import time
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple, Any

from schemas import (
    ComplexityMapConfiguration, FrontMatterMetadata, RoutingResult,
    ComplexityScore, AxisScore, SelectedAgents, ValidationChecks,
    AuditTrailEntry, TelemetryEntry, ComplexityLevel
)

__version__ = "1.0.0"


class ComplexityRouter:
    """Central router for complexity scoring and agent selection."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize router with configuration."""
        self.config_path = config_path or self._find_config_path()
        self.config = self._load_config()
        self.logs_dir = Path(".logs")
        self.logs_dir.mkdir(exist_ok=True)
        
    def _find_config_path(self) -> str:
        """Find the complexity-map.yaml configuration file."""
        possible_paths = [
            "config/complexity-map.yaml",
            ".claude/config/complexity-map.yaml",
            os.path.expanduser("~/.claude/config/complexity-map.yaml")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        raise FileNotFoundError(
            f"Could not find complexity-map.yaml in any of: {possible_paths}"
        )
    
    def _load_config(self) -> ComplexityMapConfiguration:
        """Load and validate configuration."""
        try:
            with open(self.config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            return ComplexityMapConfiguration(**config_data)
        except Exception as e:
            raise RuntimeError(f"Failed to load config from {self.config_path}: {e}")
    
    def parse_complexity_metadata(self, file_paths: List[str]) -> Dict[str, FrontMatterMetadata]:
        """Parse YAML front-matter from multiple files with precedence handling."""
        metadata = {}
        
        for file_path in file_paths:
            try:
                content = self._read_file_with_frontmatter(file_path)
                if content:
                    metadata[file_path] = FrontMatterMetadata(**content)
            except Exception as e:
                print(f"Warning: Failed to parse metadata from {file_path}: {e}", 
                      file=sys.stderr)
                
        return metadata
    
    def _read_file_with_frontmatter(self, file_path: str) -> Optional[Dict]:
        """Read YAML front-matter from a markdown file."""
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return None
        
        # Look for YAML front-matter between --- markers
        if not content.startswith('---\n'):
            return None
        
        try:
            end_marker = content.find('\n---\n', 4)
            if end_marker == -1:
                return None
            
            yaml_content = content[4:end_marker]
            return yaml.safe_load(yaml_content)
        except Exception:
            return None
    
    def score_complexity(self, metadata: Dict[str, FrontMatterMetadata]) -> ComplexityScore:
        """Compute complexity score using the scoring rubric."""
        # Resolve metadata using precedence rules
        resolved_metadata = self._resolve_metadata_precedence(metadata)
        
        # Calculate per-axis scores
        axis_scores = {}
        for axis_name, axis_config in self.config.axes.items():
            axis_score = self._calculate_axis_score(resolved_metadata, axis_config)
            axis_scores[axis_name] = axis_score
        
        # Calculate total score using main formula
        total_score = self._calculate_total_score(resolved_metadata)
        computed_level = self._score_to_complexity_level(total_score)
        
        # Determine dominant axis (highest scoring axis)
        dominant_axis = max(axis_scores.keys(), 
                          key=lambda k: axis_scores[k].weighted_score)
        
        return ComplexityScore(
            total_score=total_score,
            computed_level=computed_level,
            axis_scores=axis_scores,
            dominant_axis=dominant_axis
        )
    
    def _resolve_metadata_precedence(self, metadata: Dict[str, FrontMatterMetadata]) -> FrontMatterMetadata:
        """Resolve metadata conflicts using precedence rules."""
        if not metadata:
            return self.config.defaults
        
        # Sort files by precedence (task > spec > prd > repo-config)
        precedence_order = self.config.precedence.order
        sorted_sources = []
        
        for source_type in precedence_order:
            for file_path, meta in metadata.items():
                if self._matches_source_type(file_path, source_type):
                    sorted_sources.append((file_path, meta))
                    break
        
        # Merge metadata with precedence
        resolved = FrontMatterMetadata()
        
        # Start with defaults and apply in reverse precedence order
        for file_path, meta in reversed(sorted_sources):
            resolved = self._merge_metadata(resolved, meta)
        
        return resolved
    
    def _matches_source_type(self, file_path: str, source_type: str) -> bool:
        """Check if file path matches the source type."""
        filename = os.path.basename(file_path).lower()
        
        if source_type == "task_metadata":
            return filename.startswith("task") and filename.endswith(".md")
        elif source_type == "spec_metadata":
            return filename.startswith("spec") or "spec" in filename
        elif source_type == "prd_metadata":
            return filename.startswith("prd") or "prd" in filename
        elif source_type == "repo_config":
            return "config" in file_path.lower()
        
        return False
    
    def _merge_metadata(self, base: FrontMatterMetadata, override: FrontMatterMetadata) -> FrontMatterMetadata:
        """Merge two metadata objects with override precedence."""
        # Simple field-level override for now
        # In production, this would handle complex merge strategies
        merged_dict = base.model_dump()
        override_dict = override.model_dump()
        
        # Update non-None values from override
        for key, value in override_dict.items():
            if value is not None and value != {}:
                merged_dict[key] = value
        
        return FrontMatterMetadata(**merged_dict)
    
    def _calculate_axis_score(self, metadata: FrontMatterMetadata, axis_config) -> AxisScore:
        """Calculate score for a specific complexity axis."""
        factor_scores = {}
        weighted_sum = 0.0
        
        for i, factor in enumerate(axis_config.factors):
            factor_value = self._get_factor_value(metadata, factor)
            ordinal_score = self._get_ordinal_score(factor, factor_value)
            weight = axis_config.weights[i]
            
            factor_scores[factor] = factor_value
            weighted_sum += ordinal_score * weight
        
        # Determine axis complexity level
        axis_level = self._score_to_complexity_level(int(weighted_sum))
        
        return AxisScore(
            name="axis",
            factors=factor_scores,
            weighted_score=weighted_sum,
            level=axis_level
        )
    
    def _calculate_total_score(self, metadata: FrontMatterMetadata) -> int:
        """Calculate total complexity score using the main formula."""
        scoring = self.config.scoring
        
        # Extract factor values
        blast_radius = metadata.risk.blast_radius.value
        data_sensitivity = metadata.nonfunctional.data_sensitivity.value
        backward_compat = metadata.nonfunctional.backward_compat_required
        migration = metadata.risk.migration
        external_api_change = metadata.risk.external_api_change
        
        # Handle performance budget
        perf_budget_ms = metadata.nonfunctional.perf_budget_ms_p95
        perf_budget_key = self._perf_budget_to_key(perf_budget_ms)
        
        # Get ordinal scores
        blast_ordinal = scoring.ordinals.blast_radius[blast_radius]
        data_ordinal = scoring.ordinals.data_sensitivity[data_sensitivity]
        compat_ordinal = scoring.ordinals.backward_compat[str(backward_compat).lower()]
        migration_ordinal = scoring.ordinals.migration[str(migration).lower()]
        api_ordinal = scoring.ordinals.external_api_change[str(external_api_change).lower()]
        perf_ordinal = scoring.ordinals.perf_budget_ms[perf_budget_key]
        
        # Apply weights and calculate total
        total = (
            blast_ordinal * scoring.weights.blast_radius +
            data_ordinal * scoring.weights.data_sensitivity +
            compat_ordinal * scoring.weights.backward_compat +
            migration_ordinal * scoring.weights.migration +
            api_ordinal * scoring.weights.external_api_change +
            perf_ordinal * scoring.weights.perf_budget_ms
        )
        
        return total
    
    def _get_factor_value(self, metadata: FrontMatterMetadata, factor: str) -> Union[str, int, bool]:
        """Extract factor value from metadata."""
        if factor == "blast_radius":
            return metadata.risk.blast_radius.value
        elif factor == "data_sensitivity":
            return metadata.nonfunctional.data_sensitivity.value
        elif factor == "perf_budget_ms":
            return metadata.nonfunctional.perf_budget_ms_p95 or 0
        elif factor == "backward_compat":
            return metadata.nonfunctional.backward_compat_required
        elif factor == "migration":
            return metadata.risk.migration
        elif factor == "external_api_change":
            return metadata.risk.external_api_change
        else:
            return None
    
    def _get_ordinal_score(self, factor: str, value: Union[str, int, bool]) -> int:
        """Get ordinal score for a factor value."""
        ordinals = self.config.scoring.ordinals
        
        if factor == "perf_budget_ms":
            key = self._perf_budget_to_key(value)
            return ordinals.perf_budget_ms[key]
        elif factor in ["backward_compat", "migration", "external_api_change"]:
            return getattr(ordinals, factor)[str(value).lower()]
        else:
            return getattr(ordinals, factor)[str(value)]
    
    def _perf_budget_to_key(self, perf_budget_ms: Optional[int]) -> str:
        """Convert performance budget to ordinal key."""
        if perf_budget_ms is None:
            return "none"
        elif perf_budget_ms <= 100:
            return "<=100"
        elif perf_budget_ms <= 200:
            return "101-200"
        elif perf_budget_ms <= 300:
            return "201-300"
        else:
            return ">300"
    
    def _score_to_complexity_level(self, score: int) -> ComplexityLevel:
        """Convert numeric score to complexity level."""
        thresholds = self.config.scoring.thresholds
        
        if thresholds.minimum[0] <= score <= thresholds.minimum[1]:
            return ComplexityLevel.MINIMUM
        elif thresholds.basic[0] <= score <= thresholds.basic[1]:
            return ComplexityLevel.BASIC
        elif thresholds.moderate[0] <= score <= thresholds.moderate[1]:
            return ComplexityLevel.MODERATE
        else:  # complex level
            return ComplexityLevel.COMPLEX
    
    def select_agents(self, complexity_level: ComplexityLevel, 
                     metadata: Optional[FrontMatterMetadata] = None) -> SelectedAgents:
        """Select appropriate agents based on complexity level."""
        level_agents = getattr(self.config.agents, complexity_level.value)
        
        # Check for explicit agent overrides
        if metadata and metadata.agents:
            developer = (metadata.agents.developer if metadata.agents.developer != "auto" 
                        else level_agents["developer"])
            reviewer = (metadata.agents.reviewer if metadata.agents.reviewer != "auto"
                       else level_agents["quality_reviewer"])
            selection_method = "explicit" if (metadata.agents.developer != "auto" or 
                                            metadata.agents.reviewer != "auto") else "auto"
        else:
            developer = level_agents["developer"]
            reviewer = level_agents["quality_reviewer"]
            selection_method = "auto"
        
        return SelectedAgents(
            developer=developer,
            quality_reviewer=reviewer,
            selection_method=selection_method
        )
    
    def get_validation_requirements(self, complexity_level: ComplexityLevel) -> ValidationChecks:
        """Get validation requirements for complexity level."""
        level_validation = getattr(self.config.validation, complexity_level.value)
        
        return ValidationChecks(
            required_checks=level_validation.required_checks,
            testing_depth=level_validation.testing_depth,
            performance_checks=level_validation.performance_checks,
            security_scan=level_validation.security_scan
        )
    
    def resolve_complexity(self, file_paths: List[str], 
                          dry_run: bool = False,
                          strict: bool = False,
                          audit_detail: str = "minimal") -> RoutingResult:
        """Complete complexity resolution pipeline."""
        start_time = time.time()
        
        # Parse metadata from all input files
        metadata_dict = self.parse_complexity_metadata(file_paths)
        
        # Score complexity
        complexity_score = self.score_complexity(metadata_dict)
        
        # Get resolved metadata for agent selection
        resolved_metadata = self._resolve_metadata_precedence(metadata_dict)
        
        # Select agents
        selected_agents = self.select_agents(complexity_score.computed_level, resolved_metadata)
        
        # Get validation requirements
        validation_reqs = self.get_validation_requirements(complexity_score.computed_level)
        
        # Build audit trail
        audit_trail = self._build_audit_trail(metadata_dict, audit_detail)
        
        # Check for overrides
        override_applied = (resolved_metadata.complexity != "auto" and 
                          resolved_metadata.complexity != complexity_score.computed_level)
        override_reason = resolved_metadata.routing.override_reason if override_applied else None
        
        # Validate overrides if strict mode
        if strict and override_applied and not override_reason:
            raise ValueError("Override reason required in strict mode")
        
        result = RoutingResult(
            input_sources=file_paths,
            computed_complexity=complexity_score,
            selected_agents=selected_agents,
            validation_requirements=validation_reqs,
            audit_trail=audit_trail,
            override_applied=override_applied,
            override_reason=override_reason,
            timestamp=datetime.now().isoformat(),
            router_version=__version__
        )
        
        # Log telemetry if not dry run
        if not dry_run:
            self._log_telemetry(result, time.time() - start_time)
        
        return result
    
    def _build_audit_trail(self, metadata_dict: Dict[str, FrontMatterMetadata], 
                          detail_level: str) -> List[AuditTrailEntry]:
        """Build audit trail showing metadata resolution."""
        audit_trail = []
        
        if detail_level == "minimal":
            return audit_trail
        
        # Add entries for each resolved field
        for i, (file_path, metadata) in enumerate(metadata_dict.items()):
            audit_trail.append(AuditTrailEntry(
                field="complexity",
                source=file_path,
                value=metadata.complexity,
                precedence_rank=i
            ))
        
        return audit_trail
    
    def _log_telemetry(self, result: RoutingResult, processing_time: float):
        """Log telemetry data for analysis."""
        telemetry = TelemetryEntry(
            timestamp=result.timestamp,
            command=os.environ.get('COMMAND_NAME', 'unknown'),
            input_files=result.input_sources,
            computed_level=result.computed_complexity.computed_level,
            override_applied=result.override_applied,
            override_reason=result.override_reason,
            selected_agents={
                "developer": result.selected_agents.developer,
                "quality_reviewer": result.selected_agents.quality_reviewer
            },
            dominant_axis=result.computed_complexity.dominant_axis,
            conflicts_count=len(result.conflicts_resolved),
            processing_time_ms=processing_time * 1000
        )
        
        # Write to telemetry log
        telemetry_file = self.logs_dir / "complexity-routing.jsonl"
        with open(telemetry_file, 'a') as f:
            f.write(telemetry.model_dump_json() + '\n')


def main():
    """Command-line interface for complexity router."""
    parser = argparse.ArgumentParser(
        description="Central complexity router for Claude Code configuration"
    )
    parser.add_argument('files', nargs='*', help='Input files to analyze')
    parser.add_argument('--input', help='Input file paths (comma-separated)')
    parser.add_argument('--stdin', action='store_true', help='Read file paths from stdin')
    parser.add_argument('--config', help='Path to complexity-map.yaml')
    parser.add_argument('--dry-run', action='store_true', help='Do not log telemetry')
    parser.add_argument('--strict', action='store_true', help='Strict validation mode')
    parser.add_argument('--audit-detail', choices=['minimal', 'full'], default='minimal',
                       help='Audit trail detail level')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    # Collect input files
    input_files = []
    if args.files:
        input_files.extend(args.files)
    if args.input:
        input_files.extend(args.input.split(','))
    if args.stdin:
        input_files.extend(line.strip() for line in sys.stdin if line.strip())
    
    if not input_files:
        parser.error("No input files specified")
    
    try:
        router = ComplexityRouter(args.config)
        result = router.resolve_complexity(
            input_files,
            dry_run=args.dry_run,
            strict=args.strict,
            audit_detail=args.audit_detail
        )
        
        # Output JSON result
        print(result.model_dump_json(indent=2))
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())