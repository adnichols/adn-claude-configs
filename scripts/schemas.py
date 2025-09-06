#!/usr/bin/env python3
"""
Pydantic models for complexity inheritance system schema validation.
"""

from typing import Dict, List, Optional, Union, Literal
from enum import Enum
from pydantic import BaseModel, Field, validator


class ComplexityLevel(str, Enum):
    MINIMUM = "minimum"
    BASIC = "basic"
    MODERATE = "moderate"
    COMPLEX = "complex"


class BlastRadius(str, Enum):
    FILE = "file"
    PACKAGE = "package"
    SERVICE = "service"
    ORG = "org"


class DataSensitivity(str, Enum):
    NONE = "none"
    PII = "pii"
    REGULATED = "regulated"


class AgentSelection(str, Enum):
    AUTO = "auto"
    EXPLICIT = "explicit"


# Front-matter schema models
class RiskParameters(BaseModel):
    blast_radius: BlastRadius = BlastRadius.PACKAGE
    external_api_change: bool = False
    migration: bool = False


class NonfunctionalRequirements(BaseModel):
    perf_budget_ms_p95: Optional[int] = Field(None, gt=0)
    data_sensitivity: DataSensitivity = DataSensitivity.NONE
    backward_compat_required: bool = False


class AgentConfiguration(BaseModel):
    developer: Union[AgentSelection, str] = AgentSelection.AUTO
    reviewer: Union[AgentSelection, str] = AgentSelection.AUTO


class RoutingConfiguration(BaseModel):
    allow_override: bool = True
    override_reason: Optional[str] = None
    strict_validation: bool = False


class FrontMatterMetadata(BaseModel):
    version: int = Field(1, ge=1)
    complexity: Union[ComplexityLevel, Literal["auto"]] = "auto"
    agents: AgentConfiguration = Field(default_factory=AgentConfiguration)
    risk: RiskParameters = Field(default_factory=RiskParameters)
    nonfunctional: NonfunctionalRequirements = Field(default_factory=NonfunctionalRequirements)
    routing: RoutingConfiguration = Field(default_factory=RoutingConfiguration)

    @validator('complexity')
    def validate_complexity_override_reason(cls, v, values):
        """Require override reason for explicit complexity downgrades."""
        routing = values.get('routing')
        if routing and v != "auto" and not routing.override_reason:
            # This validation is context-dependent and would need computed complexity
            # Will be handled by the router logic
            pass
        return v


# Configuration schema models
class OrdinalMapping(BaseModel):
    """Ordinal value mappings for complexity scoring factors."""
    blast_radius: Dict[str, int]
    data_sensitivity: Dict[str, int]
    perf_budget_ms: Dict[str, int]
    backward_compat: Dict[str, int]
    migration: Dict[str, int]
    external_api_change: Dict[str, int]


class ScoringWeights(BaseModel):
    """Weights for complexity scoring formula."""
    blast_radius: int = 2
    data_sensitivity: int = 2
    backward_compat: int = 1
    perf_budget_ms: int = 1
    migration: int = 2
    external_api_change: int = 1


class ComplexityThresholds(BaseModel):
    """Score ranges for each complexity level."""
    minimum: List[int] = Field([0, 2], min_items=2, max_items=2)
    basic: List[int] = Field([3, 4], min_items=2, max_items=2)
    moderate: List[int] = Field([5, 7], min_items=2, max_items=2)
    complex: List[int] = Field([8, 999], min_items=2, max_items=2)


class ScoringConfiguration(BaseModel):
    """Complete scoring configuration."""
    ordinals: OrdinalMapping
    weights: ScoringWeights = Field(default_factory=ScoringWeights)
    thresholds: ComplexityThresholds = Field(default_factory=ComplexityThresholds)


class AgentMappings(BaseModel):
    """Agent mappings for each complexity level."""
    minimum: Dict[str, str]
    basic: Dict[str, str]
    moderate: Dict[str, str]
    complex: Dict[str, str]


class ValidationRequirements(BaseModel):
    """Validation requirements for a complexity level."""
    required_checks: List[str]
    testing_depth: str
    performance_checks: bool
    security_scan: str


class ValidationConfiguration(BaseModel):
    """Validation requirements by complexity level."""
    minimum: ValidationRequirements
    basic: ValidationRequirements
    moderate: ValidationRequirements
    complex: ValidationRequirements


class PrecedenceConfiguration(BaseModel):
    """Precedence rules for metadata resolution."""
    order: List[str]
    resolution: Dict[str, str]


class DefaultValues(BaseModel):
    """Default values when no metadata is found."""
    complexity: ComplexityLevel = ComplexityLevel.BASIC
    agents: AgentConfiguration = Field(default_factory=AgentConfiguration)
    risk: RiskParameters = Field(default_factory=RiskParameters)
    nonfunctional: NonfunctionalRequirements = Field(default_factory=NonfunctionalRequirements)
    routing: RoutingConfiguration = Field(default_factory=RoutingConfiguration)


class AxisConfiguration(BaseModel):
    """Per-axis complexity tracking configuration."""
    factors: List[str]
    weights: List[int]

    @validator('weights')
    def weights_match_factors(cls, v, values):
        factors = values.get('factors', [])
        if len(v) != len(factors):
            raise ValueError("Weights must match number of factors")
        return v


class OverrideRules(BaseModel):
    """Override validation rules."""
    require_reason_for: List[str]
    auto_approve: List[str]
    audit_trail_required: bool = True


class ComplexityMapConfiguration(BaseModel):
    """Complete complexity mapping configuration."""
    version: int = Field(1, ge=1)
    scoring: ScoringConfiguration
    agents: AgentMappings
    validation: ValidationConfiguration
    precedence: PrecedenceConfiguration
    defaults: DefaultValues = Field(default_factory=DefaultValues)
    axes: Dict[str, AxisConfiguration] = Field(default_factory=dict)
    overrides: OverrideRules = Field(default_factory=OverrideRules)


# Router output models
class AxisScore(BaseModel):
    """Score for a specific complexity axis."""
    name: str
    factors: Dict[str, Union[int, str]]
    weighted_score: float
    level: ComplexityLevel


class ComplexityScore(BaseModel):
    """Complete complexity scoring result."""
    total_score: int
    computed_level: ComplexityLevel
    axis_scores: Dict[str, AxisScore]
    dominant_axis: str


class SelectedAgents(BaseModel):
    """Selected agents for the complexity level."""
    developer: str
    quality_reviewer: str
    selection_method: str  # "auto" or "explicit"


class ValidationChecks(BaseModel):
    """Validation checks required for the complexity level."""
    required_checks: List[str]
    testing_depth: str
    performance_checks: bool
    security_scan: str


class AuditTrailEntry(BaseModel):
    """Single entry in the audit trail."""
    field: str
    source: str
    value: Union[str, int, bool, dict]
    precedence_rank: int


class RoutingResult(BaseModel):
    """Complete routing result from the complexity router."""
    version: int = 1
    input_sources: List[str]
    computed_complexity: ComplexityScore
    selected_agents: SelectedAgents
    validation_requirements: ValidationChecks
    audit_trail: List[AuditTrailEntry]
    conflicts_resolved: List[str] = Field(default_factory=list)
    override_applied: bool = False
    override_reason: Optional[str] = None
    timestamp: str
    router_version: str


# Telemetry models
class TelemetryEntry(BaseModel):
    """Telemetry logging entry."""
    timestamp: str
    command: str
    input_files: List[str]
    computed_level: ComplexityLevel
    override_applied: bool
    override_reason: Optional[str]
    selected_agents: Dict[str, str]
    dominant_axis: str
    conflicts_count: int
    processing_time_ms: float