sudo systemctl restart fastapi.service

pm2 restart nextjs

sudo systemctl restart nginx

pm2 status && sudo systemctl status nginx fastapi.service

cat /etc/systemd/system/fastapi.service 
cat /etc/nginx/sites-available/fastapi


# Integration tests
pytest tests/api/process_analysis/test_integration.py -v --log-cli-level=DEBUG

# Endpoint tests
pytest tests/api/process_analysis/test_endpoints.py -v --log-cli-level=DEBUG

# Pipeline tests
pytest tests/api/process_analysis/test_baseline.py -v --log-cli-level=DEBUG

# Monitoring tests
pytest tests/api/process_analysis/test_monitoring.py -v --log-cli-level=DEBUG

# Performance tests
pytest tests/api/process_analysis/test_performance.py -v --log-cli-level=DEBUG

# Scheduling tests
pytest tests/api/process_analysis/test_scheduling.py -v --log-cli-level=DEBUG

# Run all tests in the process_analysis directory
pytest tests/api/process_analysis/ -v --log-cli-level=DEBUG


# Run specific test functions:
# Test specific endpoint
pytest tests/api/process_analysis/test_endpoints.py::TestEndpoints::test_profitability_endpoint -v --log-cli-level=DEBUG
pytest tests/api/process_analysis/test_endpoints.py::TestEndpoints::test_capex_endpoint -v --log-cli-level=DEBUG
pytest tests/api/process_analysis/test_endpoints.py::TestEndpoints::test_opex_endpoint -v --log-cli-level=DEBUG

# Test specific integration test
# Test specific endpoint
pytest tests/api/process_analysis/test_endpoints.py::TestEndpoints::test_profitability_endpoint -v --log-cli-level=DEBUG
pytest tests/api/process_analysis/test_endpoints.py::TestEndpoints::test_capex_endpoint -v --log-cli-level=DEBUG
pytest tests/api/process_analysis/test_endpoints.py::TestEndpoints::test_opex_endpoint -v --log-cli-level=DEBUG


