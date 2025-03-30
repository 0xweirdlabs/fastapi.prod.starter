# Testing Specifications

This document outlines the testing strategy and specifications for the FastAPI Production Standard Template.

## Testing Levels

### 1. Unit Tests

Unit tests focus on testing individual components in isolation.

#### Repository Tests
- Test CRUD operations for each repository
- Verify query filters work correctly
- Test edge cases like empty results or invalid inputs
- Use an in-memory SQLite database for testing

#### Service Tests
- Test business logic in isolation
- Mock repository dependencies
- Verify error handling and edge cases
- Test service-specific validation

#### Schema Tests
- Validate schema validation rules
- Test serialization/deserialization
- Verify schema inheritance works correctly

### 2. Integration Tests

Integration tests verify that components work together correctly.

#### API Endpoint Tests
- Test each endpoint's HTTP methods
- Verify correct status codes for success/failure scenarios
- Test authentication and authorization
- Validate response formats
- Test query parameters and pagination

#### Database Integration Tests
- Test transactions and rollbacks
- Verify migrations work correctly
- Test complex queries across related tables
- Use a dedicated test PostgreSQL instance

#### External Service Integration Tests
- Test resilience patterns against flaky services
- Verify timeout handling
- Test circuit breaker functionality
- Use mock servers that simulate real services

### 3. End-to-End Tests

End-to-end tests verify the entire application works together.

#### Application Flow Tests
- Test common user flows from start to finish
- Verify monitoring and metrics collection
- Test environment configuration loading

## Test Directories Structure

```
tests/
├── conftest.py                 # Test fixtures and configuration
├── unit/
│   ├── repositories/
│   │   ├── test_user_repository.py
│   │   └── ...
│   ├── services/
│   │   ├── test_user_service.py     # Tests for user service methods
│   │   └── ...
│   └── schemas/
│       ├── test_user_schema.py
│       └── ...
├── integration/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── test_users_api.py
│   │   │   ├── test_auth_api.py     # Tests for authentication endpoints
│   │   │   └── ...
│   ├── db/
│   │   ├── test_migrations.py
│   │   └── test_transactions.py
│   └── external/
│       ├── test_external_client.py
│       └── ...
└── e2e/
    ├── test_user_flows.py
    ├── test_monitoring.py
    └── ...
```

## Testing Tools and Frameworks

- **pytest**: Primary testing framework
- **pytest-cov**: Test coverage
- **pytest-asyncio**: Testing async code
- **httpx**: Testing HTTP endpoints
- **pytest-mock**: Mocking dependencies
- **factory_boy**: Test data generation
- **testcontainers**: Spin up test databases in containers

## Mocking Strategy

- Use pytest-mock for general mocking
- Use unittest.mock.patch for system functions
- Use httpx.MockResponse for external HTTP calls
- Use SQLAlchemy in-memory databases for repository tests

## Test Database Strategy

- Unit tests: Use SQLite in-memory database
- Integration/E2E tests: Use testcontainers to spin up a PostgreSQL instance
- Ensure each test run starts with a clean database
- Run migrations before tests to ensure schema is current

## CI/CD Integration

- Run unit tests on every commit
- Run integration tests on PRs and main branch commits
- Run E2E tests nightly and before releases
- Enforce minimum test coverage thresholds (85% for core modules)

## Best Practices

1. **Test Isolation**: Each test should be independent and not affect other tests
2. **Descriptive Names**: Use clear test names that describe the expected behavior
3. **Arrange-Act-Assert**: Structure tests with setup, action, and verification phases
4. **Avoid Test Duplication**: Use fixtures and parameterization for similar tests
5. **Don't Mock What You Don't Own**: Prefer integration tests for external dependencies
6. **Test Behavior, Not Implementation**: Focus on what components do, not how they do it
7. **Use Test-Driven Development**: Write tests before implementation when possible

## Resilience Testing

- Test retry logic with deliberately flaky mock services
- Verify circuit breaker patterns prevent cascading failures
- Simulate network issues to test timeout handling
- Test monitoring alerts with threshold violations

## Performance Testing

- Create baseline performance tests for key API endpoints
- Measure response times under various load conditions
- Test database query performance with large datasets
- Verify connection pooling works under load

## Running Tests Locally

### Setup

Before running tests, you need to install the test dependencies using UV:

```bash
# Install the project with test dependencies using UV
uv pip install -e ".[dev]"
```

### Running Tests

This project comes with several example tests that demonstrate different testing patterns:

1. **User Service Tests** - Shows how to test business logic with mocked repositories
2. **Authentication API Tests** - Shows how to test API endpoints with a test client

You can run these tests using the provided test script:

```bash
# Run all tests with coverage report
uv run scripts/test.py

# Run only unit tests
uv run scripts/test.py tests/unit

# Run the example user service tests
uv run scripts/test.py tests/unit/services/test_user_service.py

# Run the example authentication API tests
uv run scripts/test.py tests/integration/api/v1/test_auth_api.py

# Run with specific pytest options
uv run scripts/test.py -v --no-cov tests/unit
```

### Test Configuration

The `conftest.py` file contains fixtures for:
- Setting up a SQLite in-memory database for tests
- Creating a test DB session
- Configuring a test client with DB dependency overrides

You can extend these fixtures for your specific testing needs.

## Test Documentation

Each test file should include docstrings explaining:
- What functionality is being tested
- Any special setup required
- Assumptions made in the tests

Test functions should have descriptive names following the pattern:
`test_<function_name>_<expected_behavior>_<conditions>`

Example: `test_create_user_raises_error_when_email_exists()`
