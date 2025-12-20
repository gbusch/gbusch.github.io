---
title: "Dynamic Traceability: Linking Pytest to Jira Tickets"
date: 2025-12-18T12:46:22+01:00
draft: false
tags: [ASPICE, python, pytest]
---

In automotive development with ASPICE, establishing bidirectional traceability between requirements and tests is a key objective. While techniques like tagging git commits or adding source code comments can fulfil this requirement, they are essentially passive documentation.

The major benefit of using markers is turning this metadata into executable selection logic. By tagging test cases with Jira ticket IDs, we can filter and run specific subsets of our test suite directly from the CLI based on requirements.

## The Approach

We use a custom pytest marker, `@pytest.mark.requirements`, to decorate our tests. This allows us to link a test case to one or more Jira tickets:

```python
@pytest.mark.requirements("PROJ-123")
def test_some_logic():
    ...

@pytest.mark.requirements("PROJ-123", "PROJ-456")
def test_some_other_logic():
    ...
```

## The Problem: Marker Registration

Pytest requires all markers to be registered in `pyproject.toml` to avoid `PytestUnknownMarkWarning`. Manually adding every new Jira ticket ID to a config file is not scalable. We need these IDs to act as dynamic markers so we can filter them via the `-m` flag.

## The Solution: Dynamic Registration

To solve this, we first register the base requirements marker in pyproject.toml:

```bash
[tool.pytest.ini_options]
markers = [
    "requirements(tickets): Link to Jira tickets with requirements covered by the test",
]
```

Then, we use a hook in `conftest.py` to intercept the collection process. This script reads the arguments passed to `@pytest.mark.requirements`, sanitizes them (replacing hyphens with underscores for CLI compatibility), and dynamically registers them as valid markers.

```python
import pytest

def pytest_collection_modifyitems(items, config):
    """
    Dynamically adds markers based on the arguments passed to @pytest.mark.requirements.
    This allows 'pytest -m PROJ_123' to work even if the ID is a string argument.
    """
    for item in items:
        for marker in item.iter_markers(name="requirements"):
            for arg in marker.args:
                # Sanitize ID: pytest markers cannot contain hyphens
                clean_id = arg.replace("-", "_")
                
                # Register the marker dynamically to silence warnings
                config.addinivalue_line(
                    "markers", f"{clean_id}: Link to Jira ticket {arg}"
                )
                
                # Add the sanitized marker to the test item
                item.add_marker(getattr(pytest.mark, clean_id))
```

## Usage

Now you can filter your test suite using the Jira ticket IDs directly. Note that due to the sanitization in our hook, hyphens in ticket IDs become underscores in the CLI command.

- Run tests for a specific requirement: `pytest -m "PROJ_123"`
- Run tests covering multiple requirements: `pytest -m "PROJ_123 or PROJ_456"`
- Exclude specific requirements: `pytest -m "PROJ_123 and not PROJ_456"`
