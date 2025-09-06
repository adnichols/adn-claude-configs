---
description: Refine a research specification by removing unnecessary requirements based on complexity level
argument-hint: [spec-file-path] [complexity-level: minimum|basic|moderate|complex]
---

# Rule: Refine Research Specification Based on Complexity Level

## Goal

To review and refine an existing research specification document by removing or simplifying requirements that don't match the specified complexity level. This ensures the specification is appropriately scoped and doesn't include unnecessary enterprise features, testing requirements, or architectural complexity.

## Input

1. **Specification File Path:** Path to existing research specification (typically in `/tasks/` directory)
2. **Complexity Level:** One of four levels:
   - `minimum`: Only functional requirements, no additional considerations
   - `basic`: Functional + basic testing and security, no performance/backward compatibility  
   - `moderate`: Focused scope with reliability, security, and performance recommendations
   - `complex`: Full enterprise requirements including backward compatibility and robustness

## Complexity Level Definitions

### Minimum Level
**Scope:** Only the necessary functional requirements
**Remove:**
- All testing sections beyond basic validation
- Security considerations beyond data validation
- Performance and scalability sections
- Industry analysis and competitive research
- Detailed implementation phases
- Risk analysis and mitigation
- Advanced architecture considerations

**Keep:**
- Executive summary (simplified)
- Core problem and solution
- Basic technical approach
- Essential user interface needs
- Immediate next steps

### Basic Level  
**Scope:** Core functionality with essential quality measures
**Remove:**
- Performance optimization strategies
- Backward compatibility requirements
- Industry standards and compliance
- Advanced security measures
- Scalability planning
- Enterprise deployment considerations

**Keep:**
- Basic testing approach
- Essential security considerations (input validation, basic auth)
- Core technical design
- Simple error handling
- Basic user experience requirements

### Moderate Level
**Scope:** Production-ready feature with appropriate quality measures
**Remove:**
- Enterprise compliance requirements
- Complex backward compatibility strategies
- Advanced performance optimization
- Industry competitive analysis
- Complex deployment architectures

**Keep:**
- Comprehensive testing strategy
- Security best practices
- Performance considerations
- Reliability and error handling
- User experience optimization
- Basic monitoring and observability

### Complex Level
**Scope:** Enterprise-grade implementation with full robustness
**Keep All Sections Including:**
- Backward compatibility analysis
- Enterprise security and compliance
- Performance and scalability planning
- Industry standards alignment
- Complex deployment strategies
- Comprehensive risk analysis
- Advanced monitoring and observability

## Process

1. **Validate Input:** Ensure specification file exists and complexity level is valid
2. **Parse Specification:** Read and analyze existing specification structure
3. **Apply Filtering Rules:** Remove or simplify sections based on complexity level
4. **Refine Content:** Adjust remaining sections to match complexity scope
5. **Generate Output:** Create refined specification with appropriate detail level
6. **Save Result:** Output to `refined-spec-[complexity]-[original-name].md` in same directory

## Filtering Rules by Section

### Executive Summary
- **Minimum:** Basic problem and solution only
- **Basic:** Add core technical approach
- **Moderate:** Include success criteria and key benefits
- **Complex:** Full context including strategic implications

### Technical Design
- **Minimum:** Simple implementation approach only
- **Basic:** Add basic integration patterns
- **Moderate:** Include architecture considerations and data design
- **Complex:** Full technical architecture with scalability planning

### Testing Approach
- **Minimum:** Remove entirely or minimal validation only
- **Basic:** Unit testing and basic integration tests
- **Moderate:** Comprehensive testing strategy with automation
- **Complex:** Full testing pyramid including performance and security testing

### Security Considerations
- **Minimum:** Remove entirely or basic input validation
- **Basic:** Essential security (authentication, input sanitization)
- **Moderate:** Security best practices and threat modeling
- **Complex:** Full security analysis with compliance considerations

### Performance & Scalability
- **Minimum:** Remove entirely
- **Basic:** Remove entirely
- **Moderate:** Basic performance considerations
- **Complex:** Full performance and scalability analysis

### Implementation Plan
- **Minimum:** Single phase implementation
- **Basic:** Simple MVP approach
- **Moderate:** Phased approach with quality gates
- **Complex:** Detailed project plan with risk management

## Output Format

The refined specification follows the same structure as the input but with sections filtered/simplified according to complexity level:

```markdown
# [Original Title] - Refined Specification (Complexity: [LEVEL])

*This specification has been refined for [COMPLEXITY] level implementation*

## 🎯 Executive Summary
[Filtered content based on complexity level]

## [Additional sections filtered according to complexity rules]

---
## 📋 Refinement Summary

**Original Complexity:** [Detected from original spec]
**Target Complexity:** [Specified level]
**Sections Removed:** [List of removed sections]
**Sections Simplified:** [List of simplified sections]
**Key Changes:** [Summary of major modifications]
```

## Key Principles

1. **Preserve Core Functionality:** Never remove essential functional requirements
2. **Match Complexity Level:** Ensure output aligns with specified complexity
3. **Maintain Coherence:** Ensure remaining sections work together logically  
4. **Clear Documentation:** Document what was changed and why
5. **Implementation Ready:** Refined spec should still support execution planning

## Error Handling

- **Invalid file path:** Display error and request valid specification file
- **Invalid complexity level:** Show available options and request correction
- **Malformed specification:** Attempt parsing but warn about potential issues
- **Missing required sections:** Proceed with available sections, note limitations

## Success Indicators

A well-refined specification should:
- Match the specified complexity level exactly
- Remove unnecessary enterprise features for simpler levels
- Maintain implementation feasibility at the target complexity
- Provide clear documentation of changes made
- Support seamless transition to execution planning