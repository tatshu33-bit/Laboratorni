#!/bin/bash
# Test script for Flask SQLite Application

set -e

echo "==================================="
echo "Flask SQLite Application Test Suite"
echo "==================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local method=$2
    local url=$3
    local data=$4
    local expected_code=$5
    
    echo -n "Testing $name... "
    
    if [ -n "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" -H "Content-Type: application/json" -d "$data")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" = "$expected_code" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (Expected HTTP $expected_code, got $http_code)"
        echo "Response: $body"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Wait for application to be ready
echo "Waiting for application to be ready..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:5000/health > /dev/null 2>&1; then
        echo -e "${GREEN}Application is ready!${NC}"
        echo ""
        break
    fi
    attempt=$((attempt + 1))
    sleep 1
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "${RED}Application failed to start within 30 seconds${NC}"
    exit 1
fi

# Run tests
echo "Running API tests..."
echo ""

# Test 1: Root endpoint
test_endpoint "Root endpoint" "GET" "http://localhost:5000/" "" "200"

# Test 2: Health check
test_endpoint "Health check" "GET" "http://localhost:5000/health" "" "200"

# Test 3: List items (empty)
test_endpoint "List items (initially empty)" "GET" "http://localhost:5000/items" "" "200"

# Test 4: Create item
test_endpoint "Create item 1" "POST" "http://localhost:5000/items" '{"name":"Item 1","description":"First test item"}' "201"

# Test 5: Create another item
test_endpoint "Create item 2" "POST" "http://localhost:5000/items" '{"name":"Item 2","description":"Second test item"}' "201"

# Test 6: List items (should have 2)
test_endpoint "List items (with data)" "GET" "http://localhost:5000/items" "" "200"

# Test 7: Get specific item
test_endpoint "Get item by ID" "GET" "http://localhost:5000/items/1" "" "200"

# Test 8: Update item
test_endpoint "Update item" "PUT" "http://localhost:5000/items/1" '{"name":"Updated Item","description":"Updated description"}' "200"

# Test 9: Get updated item
test_endpoint "Get updated item" "GET" "http://localhost:5000/items/1" "" "200"

# Test 10: Delete item
test_endpoint "Delete item" "DELETE" "http://localhost:5000/items/1" "" "200"

# Test 11: Try to get deleted item (should fail)
test_endpoint "Get deleted item (should fail)" "GET" "http://localhost:5000/items/1" "" "404"

# Test 12: Create item without name (should fail)
test_endpoint "Create item without name (should fail)" "POST" "http://localhost:5000/items" '{"description":"No name"}' "400"

echo ""
echo "==================================="
echo "Test Results"
echo "==================================="
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
fi
