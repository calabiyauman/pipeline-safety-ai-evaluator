# Contributing to Pipeline Safety AI Evaluator

Thank you for your interest in contributing to PSAE! This document provides guidelines and instructions for contributing to this safety-critical evaluation framework.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to:

- **Safety First**: All contributions must prioritize safety in pipeline operations
- **Scientific Rigor**: Changes must be backed by evidence and peer-reviewed methodology
- **Transparency**: All test cases, metrics, and scoring methods must be fully documented
- **Collaboration**: Respect differing viewpoints and experiences

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues. When creating a bug report, include:

- **Use a clear descriptive title**
- **Describe the exact steps to reproduce**
- **Provide specific examples**
- **Describe the behavior you observed and why it's wrong**
- **Include system information** (Python version, OS, dependency versions)

#### Security Issues

⚠️ **Do NOT open public issues for security vulnerabilities.**  
Use **GitHub Private Vulnerability Reporting** (Security Advisories) for security concerns.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
-**Provide specific examples**
-**Explain why this enhancement would be useful**

### Contributing Test Cases

Test cases are the heart of PSAE. We welcome contributions particularly for:

1. **Abnormal Condition Scenarios**: Equipment failures, environmental anomalies
2. **Real-World Incidents**: Based on PHMSA incident reports
3. **Industry-Specific Variations**: Regional practices, company procedures
4. **New Technology Domains**: Hydrogen, CCUS, renewable natural gas

#### Test Case Submission Process

1. **Use the Test Case Template** (see `templates/test_case_template.md`)
2. **Include STAR-R framework**: Situation, Task, Action, Result, Risk
3. **Reference Standards**: Cite specific API/ASME/NACE/DOT standards
4. **Provide Abnormal Variants**: Include 2-3 abnormal conditions
5. **Validation**: Have reviewed by licensed PE or experienced operator
6. **Documentation**: Explain real-world basis for scenario

**Submit test cases via:**
- Pull Request with new JSON file in `data/test_cases/`
- Or open a GitHub Discussion in the **Test Cases** category and link to your draft branch/PR

### Contributing Code

#### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/calabiyauman/pipeline-safety-ai-evaluator.git
cd psae

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/
```

#### Development Workflow

1. **Fork the repository**
2. **Create a branch**: `git checkout -b feature/my-feature`
3. **Make your changes**
4. **Add tests** for new functionality
5. **Run the test suite**: `pytest`
6. **Format code**: `black src/ tests/`
7. **Check types**: `mypy src/`
8. **Commit**: `git commit -m "feat: description"`
9. **Push**: `git push origin feature/my-feature`
10. **Open Pull Request**

#### Coding Standards

- **Python 3.10+** minimum
- **Type hints** for all function signatures
- **Docstrings** following Google style
- **Black** code formatter (88 character line length)
- **99% test coverage** for new code
- **Mypy** type checking enabled

##### Code Style Example

```python
def evaluate_scenario(
    scenario: TestScenario,
    model: AIModelInterface,
    runs: int = 5
) -> EvaluationResult:
    """
    Evaluate a single test scenario.

    Args:
        scenario: Test scenario to evaluate
        model: AI model interface
        runs: Number of evaluation runs (default: 5)

    Returns:
        Aggregated evaluation results

    Raises:
        ValueError: If runs < 1

    Example:
        >>> result = evaluate_scenario(scenario, model, runs=3)
        >>> print(result.mean_score)
        87.5
    """
    if runs < 1:
        raise ValueError("runs must be >= 1")

    # Implementation...
```

#### Testing Requirements

All contributions must include tests:

```python
# tests/test_evaluator.py

def test_hot_tapping_safety_critical():
    """Test hot tapping scenario evaluation."""
    scenario = TestScenario.from_dict(HOT_TAPPING_DATA)
    result = evaluator.evaluate(scenario, model, runs=3)
    
    # Assertions
    assert result.mean_score >= 70  # Pass threshold
    assert not result.dangerous_errors
    assert "API 1104" in result.standards_cited
```

#### Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

Examples:
```
feat: add abnormal condition testing for hot tapping
fix: correct Cv calculation verification logic
docs: update methodology with ICC explanation
test: add validation tests for safety scoring
```

### Contributing Documentation

Documentation improvements are always welcome:

- **Fix typos and grammar**
- **Clarify explanations**
- **Add examples**
- **Translate** (we welcome multilingual docs)
- **Create tutorials**

Documentation is in `/docs` and uses Markdown.

## Pull Request Process

### Before Submitting

- [ ] **Tests pass**: `pytest`
- [ ] **Type checking passes**: `mypy src/`
- [ ] **Code formatted**: `black src/ tests/`
- [ ] **Documentation updated**
- [ ] **CHANGELOG.md updated**
- [ ] **Test evidence provided**: For new test cases
- [ ] **Benchmark manifest updated and signed** (if benchmark data changed)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Test case
- [ ] Breaking change

## Testing
Describe tests you ran

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Backwards compatible (or migration path documented)
- [ ] Security reviewed (if applicable)
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by at least one maintainer
3. **Technical review** for test cases (requires licensed PE)
4. **Safety review** for scoring/metric changes
5. **Final approval** by project lead

**Response time**: We aim to respond within 5 business days.

## Recognition

All contributors will be:
- Listed in CONTRIBUTORS.md
- Recognized in release notes
- Invited to contributor events (if applicable)

## Questions?

- **General questions**: GitHub Discussions
- **Security issues**: GitHub Security Advisories (private vulnerability reporting)
- **Test case submissions**: GitHub Pull Requests or GitHub Discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make AI evaluation in pipeline safety more rigorous and reliable!**
