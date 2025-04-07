# Contributing to Rush Analytics

Thank you for considering contributing to Rush Analytics! We welcome contributions from the community to improve this project.

## How to Contribute

1. **Report Issues**: If you encounter a bug or have a feature request, please open an issue in the GitHub repository.
2. **Fork the Repository**: Create a personal fork of the repository and clone it to your local machine.
3. **Create a Branch**: Create a new branch for your changes (e.g., `feature/new-feature` or `bugfix/fix-issue`).
4. **Make Changes**: Implement your changes, ensuring that your code adheres to the project's coding standards.
5. **Write Tests**: Add tests for your changes to ensure they work as expected.
6. **Run Tests**: Run the test suite to verify that all tests pass.
7. **Submit a Pull Request**: Push your changes to your fork and open a pull request against the `main` branch of the repository.

## Code of Conduct

Please note that all contributors are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md).

## Development Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/CireSnave/rush-analytics.git
   ```
2. Install dependencies:
   ```bash
   uv sync
   ```
   (Note: We use uv as our package manager.  You can use pip, poetry, etc.)
3. Run tests:
   ```bash
   python -m unittest discover tests
   ```

## Style Guide

- Use `black` for code formatting.
- Use `flake8` for linting.
- Use `mypy` for type checking.

Thank you for contributing!