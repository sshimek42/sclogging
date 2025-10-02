# Contributing to SCLogging

Thank you for your interest in contributing to SCLogging! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

Please review our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing. We are committed to providing a welcoming and inclusive environment for all contributors.

## Getting Started

SCLogging is a Python logging wrapper that simplifies configuration and provides convenient utilities like colorized output and timing helpers.

Before contributing, please:
1. Read the [README.md](README.md) to understand the project's purpose and API
2. Review the [full documentation](https://sclogging.readthedocs.io/en/latest/)
3. Check existing [issues](../../issues) and [pull requests](../../pulls) to avoid duplicating work

## Development Setup

### Prerequisites

- Python 3.13.7 (or compatible version)
- virtualenv (used as the package manager for this project)
- Git

### Setting Up Your Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/sclogging.git
   cd sclogging
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Unix/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development dependencies**
   ```bash
   pip install pytest pytest-cov
   ```

5. **Verify your setup**
   ```bash
   pytest tests/
   ```

## How to Contribute

### Types of Contributions Welcome

- **Bug fixes**: Fix issues identified in the issue tracker
- **Documentation improvements**: Clarify usage, add examples, fix typos
- **Configuration enhancements**: Add new configuration options or improve existing ones
- **Code quality improvements**: Refactoring, performance improvements, code cleanup
- **Feature requests**: Propose new features via issues first for discussion

### Getting Your Changes Merged

1. Create an issue describing your proposed change (unless it's a trivial fix)
2. Wait for feedback and approval from maintainers
3. Fork the repository and create a feature branch
4. Implement your changes
5. Submit a pull request

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines
- Use meaningful variable and function names
- Keep functions focused and modular
- Maximum line length: 88 characters (Black formatter default)

### Code Quality

- Write clear, self-documenting code with appropriate comments
- Add docstrings to all public functions, classes, and methods
- Use type hints where appropriate
- Maintain backwards compatibility whenever possible

### Example Docstring Format
```
python
def example_function(param1: str, param2: int = 10) -> bool:
    """Brief description of what the function does.
    
    More detailed explanation if needed.
    
    :param param1: Description of param1
    :type param1: str
    :param param2: Description of param2 (optional)
    :type param2: int
    :return: Description of return value
    :rtype: bool
    """
    pass
```
## Testing

### Running Tests
```
bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=sclogging tests/

# Run specific test file
pytest tests/test_specific_file.py
```
### Writing Tests

- Add tests for all new features and bug fixes
- Place test files in the `tests/` directory
- Name test files with the prefix `test_`
- Use descriptive test function names that explain what is being tested

### Test Coverage

- Aim for at least 80% code coverage for new code
- Ensure all public API functions have corresponding tests
- Include edge cases and error conditions in your tests

## Documentation

### Code Documentation

- Document all public APIs with clear docstrings
- Include usage examples in docstrings for complex functions
- Keep comments up-to-date when modifying code

### README and User Documentation

- Update README.md if your changes affect user-facing functionality
- Add examples for new features
- Update the documentation at `docs/` if substantial changes are made

### Documentation Style

- Use clear, concise language
- Include practical examples
- Focus on user needs and common use cases
- Avoid overly technical jargon unless necessary

## Pull Request Process

### Before Submitting

1. **Ensure your code passes all tests**
   ```bash
   pytest
   ```

2. **Format your code** (if using a formatter like Black)
   ```bash
   black sclogging/
   ```

3. **Update documentation** as needed

4. **Update CHANGELOG** (if applicable) with your changes

### Submitting Your PR

1. **Create a descriptive branch name**
   - Feature: `feature/description-of-feature`
   - Bug fix: `fix/description-of-bug`
   - Documentation: `docs/description-of-changes`

2. **Write a clear PR title and description**
   - Explain what changes you made and why
   - Reference any related issues (e.g., "Fixes #123")
   - Include examples or screenshots if relevant

3. **Keep PRs focused**
   - One PR should address one issue or feature
   - Avoid mixing unrelated changes

4. **Respond to feedback**
   - Be open to suggestions and constructive criticism
   - Update your PR based on reviewer comments
   - Ask for clarification if feedback is unclear

### PR Review Process

- Maintainers will review your PR as soon as possible
- You may be asked to make changes before approval
- Once approved and tests pass, your PR will be merged

## Issue Reporting

### Before Creating an Issue

- Search existing issues to avoid duplicates
- Verify the issue exists in the latest version
- Gather relevant information (error messages, logs, environment details)

### Creating a Good Issue

Include the following information:

1. **Clear title** that summarizes the issue
2. **Description** of the problem or feature request
3. **Steps to reproduce** (for bugs)
4. **Expected behavior**
5. **Actual behavior** (for bugs)
6. **Environment details**:
   - Python version
   - SCLogging version
   - Operating system
   - Any relevant dependencies

### Issue Templates

Use the following templates as a guide:

**Bug Report:**
```
markdown
**Description**
A clear description of the bug.

**Steps to Reproduce**
1. Step one
2. Step two
3. ...

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- Python version: X.X.X
- SCLogging version: X.X.X
- OS: [e.g., Windows 10, Ubuntu 20.04]

**Additional Context**
Any other relevant information.
```
**Feature Request:**
```
markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
Why this feature would be useful.

**Proposed Implementation** (optional)
Ideas on how this could be implemented.

**Alternatives Considered**
Other solutions you've thought about.
```
## Security Issues

**Do not report security vulnerabilities via public issues.**

Please see [SECURITY.md](SECURITY.md) for instructions on reporting security vulnerabilities privately.

## Questions?

If you have questions about contributing:
- Open an issue with the label "question"
- Check existing documentation and issues first
- Be clear and specific in your question

## License

By contributing to SCLogging, you agree that your contributions will be licensed under the project's MIT License.

---

Thank you for contributing to SCLogging! Your efforts help make this project better for everyone.
