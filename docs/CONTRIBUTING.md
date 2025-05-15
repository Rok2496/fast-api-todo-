# Contributing to FAST TODO API

Thank you for considering contributing to the FAST TODO API project! This document provides guidelines for contributing to the project.

## Code Style and Standards

This project follows these coding standards:

1. **Python Code Style**
   - Follow PEP 8 guidelines
   - Use 4 spaces for indentation
   - Maximum line length of 88 characters (Black formatter compatible)
   - Docstrings for all classes and functions

2. **Naming Conventions**
   - Functions and variables: snake_case
   - Classes: PascalCase
   - Constants: UPPER_CASE
   - Private functions/variables: _leading_underscore

3. **Type Hinting**
   - Use Python type hints for all function parameters and return values
   - Example:
     ```python
     def get_user_by_id(user_id: int) -> Optional[User]:
         # Function body
     ```

## Project Structure

When adding new features, follow the existing project structure:

- **API Endpoints**: Add to appropriate files in `app/api/`
- **Database Models**: Add to `app/db/models.py`
- **Database Operations**: Add to `app/db/crud.py`
- **Schema Validation**: Add to `app/schemas/schemas.py`
- **Core Functionality**: Add to appropriate files in `app/core/`
- **External Services**: Add to appropriate files in `app/services/`

## Development Workflow

1. **Set Up Development Environment**
   - Create a virtual environment
   - Install dependencies with `pip install -r requirements.txt`
   - Create a local `.env` file based on `.env.example`

2. **Run the Development Server**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Testing**
   - Write tests for new features
   - Run tests with pytest:
     ```bash
     pytest
     ```

## Pull Request Process

1. **Create a Feature Branch**
   - Branch from `main` for features: `feature/your-feature-name`
   - Branch from `main` for bugfixes: `fix/issue-description`

2. **Make Your Changes**
   - Follow the code style guidelines
   - Keep changes focused on a single issue

3. **Write or Update Tests**
   - Add tests for new functionality
   - Make sure all tests pass

4. **Update Documentation**
   - Update the README.md if necessary
   - Update API documentation for new endpoints
   - Add docstrings to new functions/classes

5. **Submit a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Wait for code review

## Commit Messages

Follow these guidelines for commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with a type:
  - feat: (new feature)
  - fix: (bug fix)
  - docs: (documentation changes)
  - style: (formatting, missing semicolons, etc; no code change)
  - refactor: (refactoring production code)
  - test: (adding missing tests, refactoring tests)
  - chore: (updating build tasks, package manager configs, etc)

## License

By contributing to this project, you agree that your contributions will be licensed under the project's license. 