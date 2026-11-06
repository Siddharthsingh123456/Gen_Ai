# Contributing

Thank you for helping improve this GenAI learning repository.

## Before making changes

1. Choose the relevant assignment.
2. Read its README and understand its current structure.
3. Check whether a similar implementation already exists.
4. Keep changes scoped to the selected assignment unless a repository-wide change is necessary.

## Code standards

- Use descriptive names for files, variables, and functions.
- Follow PEP 8 for Python where practical.
- Keep functions focused and avoid unnecessary duplication.
- Add type hints to reusable or non-trivial functions where they improve clarity.
- Handle expected errors with useful messages; do not hide exceptions silently.
- Do not hardcode API keys, passwords, tokens, or private endpoints.
- Keep secrets in environment variables or a secret manager.
- Avoid committing generated caches, virtual environments, or large model files.

## Documentation

Each substantial project should document:

- What the project demonstrates
- Prerequisites and supported Python version
- Installation steps
- Required environment variables (names only, never real values)
- Exact run commands
- Dataset/model download instructions and licensing
- Example input/output or screenshots where useful
- Known limitations

## Validation

From the repository root, run:

```bash
python scripts/validate_repo.py
```

Also run the selected project's own tests and manually verify its documented run command when possible. Do not claim a project was tested unless it was actually executed.

## Pull request checklist

- [ ] Changes are limited to the intended project.
- [ ] No secrets or private data are included.
- [ ] Documentation matches the actual files and commands.
- [ ] Python files compile successfully.
- [ ] Notebook files contain valid JSON.
- [ ] Tests or manual checks were run and their results are described.
- [ ] Dataset and third-party asset attribution is preserved.
