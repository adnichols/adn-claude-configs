#!/usr/bin/env python3
"""
Agent Generation Script for Claude Code Configuration System

Generates agent files from Jinja2 templates with complexity-specific configurations.
"""

import os
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from typing import Dict, List


class AgentGenerator:
    """Generator for complexity-aware agent files."""
    
    def __init__(self, templates_dir: str = "agents/templates", output_dir: str = "agents"):
        """Initialize generator with template and output directories."""
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Agent configurations by complexity level
        self.agent_configs = {
            "developer": {
                "minimum": {
                    "agent_description": "Implements specs with basic testing - prototype quality",
                    "complexity_level": "minimum"
                },
                "basic": {
                    "agent_description": "Implements specs with comprehensive testing - production ready",
                    "complexity_level": "basic"
                },
                "moderate": {
                    "agent_description": "Implements specs with full validation - enterprise grade",
                    "complexity_level": "moderate"
                },
                "complex": {
                    "agent_description": "Implements specs with complete compliance - mission critical",
                    "complexity_level": "complex"
                }
            },
            "quality-reviewer": {
                "minimum": {
                    "agent_description": "Reviews code for basic production issues - prototype validation",
                    "complexity_level": "minimum"
                },
                "basic": {
                    "agent_description": "Reviews code for production issues - standard validation",
                    "complexity_level": "basic"
                },
                "moderate": {
                    "agent_description": "Reviews code for advanced production issues - comprehensive validation",
                    "complexity_level": "moderate"
                },
                "complex": {
                    "agent_description": "Reviews code for enterprise production issues - complete audit",
                    "complexity_level": "complex"
                }
            }
        }
    
    def generate_all_agents(self) -> Dict[str, List[str]]:
        """Generate all agent files from templates."""
        results = {"generated": [], "errors": []}
        
        for agent_type in self.agent_configs.keys():
            template_file = f"{agent_type}.j2"
            
            if not (self.templates_dir / template_file).exists():
                results["errors"].append(f"Template not found: {template_file}")
                continue
            
            try:
                template = self.env.get_template(template_file)
            except Exception as e:
                results["errors"].append(f"Failed to load template {template_file}: {e}")
                continue
            
            # Generate agent for each complexity level
            for complexity_level, config in self.agent_configs[agent_type].items():
                try:
                    output_file = f"{agent_type}-{complexity_level}.md"
                    output_path = self.output_dir / output_file
                    
                    # Render template with configuration
                    rendered_content = template.render(**config)
                    
                    # Write to output file
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(rendered_content)
                    
                    results["generated"].append(str(output_path))
                    print(f"Generated: {output_path}")
                    
                except Exception as e:
                    error_msg = f"Failed to generate {output_file}: {e}"
                    results["errors"].append(error_msg)
                    print(f"Error: {error_msg}", file=sys.stderr)
        
        return results
    
    def validate_generated_agents(self) -> Dict[str, List[str]]:
        """Validate that generated agents have required complexity-specific content."""
        validation_results = {"passed": [], "failed": []}
        
        # Validation rules by complexity level
        validation_rules = {
            "minimum": [
                "Basic smoke tests",
                "Simple unit tests",
                "Basic error handling",
                "prototype-level quality"
            ],
            "basic": [
                "Unit tests for all core logic",
                "Integration tests",
                "Production-ready code quality",
                "Comprehensive error handling"
            ],
            "moderate": [
                "Comprehensive unit test coverage",
                "Performance smoke tests",
                "Security validation tests",
                "Enterprise-grade code quality"
            ],
            "complex": [
                "Comprehensive unit test coverage (>90%)",
                "End-to-end tests",
                "Performance benchmark tests",
                "Mission-critical code quality",
                "Compliance with industry standards"
            ]
        }
        
        for agent_type in self.agent_configs.keys():
            for complexity_level in self.agent_configs[agent_type].keys():
                agent_file = self.output_dir / f"{agent_type}-{complexity_level}.md"
                
                if not agent_file.exists():
                    validation_results["failed"].append(f"Missing file: {agent_file}")
                    continue
                
                try:
                    with open(agent_file, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                    
                    # Check for required content based on complexity level
                    rules = validation_rules.get(complexity_level, [])
                    missing_rules = []
                    
                    for rule in rules:
                        # Simple keyword matching (could be enhanced)
                        if not any(keyword.lower() in content for keyword in rule.split()):
                            missing_rules.append(rule)
                    
                    if missing_rules:
                        validation_results["failed"].append(
                            f"{agent_file}: Missing requirements: {missing_rules}"
                        )
                    else:
                        validation_results["passed"].append(str(agent_file))
                
                except Exception as e:
                    validation_results["failed"].append(f"Error validating {agent_file}: {e}")
        
        return validation_results
    
    def clean_old_agents(self, backup: bool = True) -> List[str]:
        """Remove old manually-maintained agent files."""
        # List of manually maintained agents that should be replaced
        old_agents = [
            "developer.md",
            "quality-reviewer.md",
            "quality-reviewer-opus.md"  # Special case - keep this one for now
        ]
        
        removed_files = []
        
        for old_agent in old_agents:
            old_path = self.output_dir / old_agent
            
            if old_path.exists():
                if backup:
                    backup_path = self.output_dir / f"{old_agent}.backup"
                    try:
                        old_path.rename(backup_path)
                        print(f"Backed up: {old_path} → {backup_path}")
                    except Exception as e:
                        print(f"Warning: Failed to backup {old_path}: {e}")
                        continue
                else:
                    old_path.unlink()
                
                removed_files.append(str(old_path))
        
        return removed_files


def main():
    """Command-line interface for agent generation."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate complexity-aware agent files from templates"
    )
    parser.add_argument('--templates-dir', default='agents/templates',
                       help='Directory containing Jinja2 templates')
    parser.add_argument('--output-dir', default='agents',
                       help='Directory for generated agent files')
    parser.add_argument('--validate', action='store_true',
                       help='Validate generated agents after creation')
    parser.add_argument('--clean-old', action='store_true',
                       help='Remove old manually-maintained agent files')
    parser.add_argument('--no-backup', action='store_true',
                       help='Skip backing up old files when cleaning')
    
    args = parser.parse_args()
    
    try:
        generator = AgentGenerator(args.templates_dir, args.output_dir)
        
        # Generate all agents
        print("Generating agents from templates...")
        results = generator.generate_all_agents()
        
        if results["generated"]:
            print(f"\nSuccessfully generated {len(results['generated'])} agents:")
            for agent_file in results["generated"]:
                print(f"  - {agent_file}")
        
        if results["errors"]:
            print(f"\nErrors during generation:")
            for error in results["errors"]:
                print(f"  - {error}")
        
        # Validate if requested
        if args.validate:
            print("\nValidating generated agents...")
            validation_results = generator.validate_generated_agents()
            
            if validation_results["passed"]:
                print(f"Validation passed for {len(validation_results['passed'])} agents")
            
            if validation_results["failed"]:
                print(f"Validation failed for {len(validation_results['failed'])} agents:")
                for failure in validation_results["failed"]:
                    print(f"  - {failure}")
        
        # Clean old agents if requested
        if args.clean_old:
            print("\nCleaning old manually-maintained agents...")
            removed_files = generator.clean_old_agents(backup=not args.no_backup)
            
            if removed_files:
                print(f"Removed {len(removed_files)} old agent files:")
                for removed_file in removed_files:
                    print(f"  - {removed_file}")
            else:
                print("No old agent files found to remove")
        
        # Summary
        if results["errors"]:
            print(f"\nCompleted with {len(results['errors'])} errors")
            return 1
        else:
            print(f"\nSuccessfully generated all {len(results['generated'])} agents")
            return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())