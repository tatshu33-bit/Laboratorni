# Deployment Instructions

## Repository Branch Structure

As per the laboratory requirements, this REST API implementation should be deployed to the `lab.5` branch.

### Creating and Pushing to lab.5 Branch

To push this implementation to the lab.5 branch, execute the following commands:

```bash
# If you're on a different branch, first merge or cherry-pick the implementation
git checkout -b lab.5

# Or if lab.5 already exists:
git checkout lab.5
git merge copilot/develop-basic-rest-api

# Push to remote
git push origin lab.5
```

### Implementation Summary

This implementation includes:

1. **REST API with 6+ Endpoints**:
   - Root endpoint (`/`)
   - Health check (`/api/health`)
   - Get all items (`GET /api/items`)
   - Get item by ID (`GET /api/items/<id>`)
   - Create item (`POST /api/items`)
   - Update item (`PUT /api/items/<id>`)
   - Delete item (`DELETE /api/items/<id>`)

2. **API Documentation**:
   - Swagger/OpenAPI documentation via Flasgger
   - Interactive documentation UI at `/api/docs`
   - Complete request/response schemas
   - Usage examples for each endpoint

3. **Testing Resources**:
   - Postman collection with 11 test scenarios
   - Error handling tests (404, 400)
   - Success scenario tests
   - Category filtering test

4. **Error Handling**:
   - 400 Bad Request (invalid data, missing fields)
   - 404 Not Found (non-existent resources)
   - 500 Internal Server Error (unexpected errors)
   - Consistent JSON error response format

### Verification Checklist

Before considering deployment complete, verify:

- [ ] All endpoints respond correctly
- [ ] Error handling works as expected
- [ ] Swagger documentation is accessible at `/api/docs`
- [ ] Postman collection imports successfully
- [ ] All tests in Postman collection pass
- [ ] README.md contains setup and usage instructions
- [ ] requirements.txt includes all dependencies
- [ ] Code is pushed to lab.5 branch

### Running the API

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py

# Access documentation
# Open browser to: http://localhost:5000/api/docs
```

### Testing the API

1. **Using curl**:
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Using Postman**:
   - Import `Laboratorni_API_Collection.postman_collection.json`
   - Run the collection
   - View test results

3. **Using Swagger UI**:
   - Navigate to http://localhost:5000/api/docs
   - Test endpoints directly from the interface

## Notes

- The current implementation uses in-memory storage
- Data will reset when the server restarts
- For production deployment, consider integrating a database
- The server runs in debug mode by default (suitable for development only)
