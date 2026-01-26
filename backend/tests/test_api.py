"""
API Integration Tests
Tests API endpoints and request/response handling
"""

import pytest
import json
from app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_endpoint(self, client):
        """Test health check returns 200"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'version' in data


class TestProcessTextEndpoint:
    """Test text processing endpoint"""
    
    def test_process_text_success(self, client):
        """Test successful text processing"""
        payload = {
            'text': 'Hello world. This is a test.'
        }
        response = client.post(
            '/api/process-text',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'words' in data
        assert 'orp_data' in data
        assert 'stats' in data
        assert len(data['words']) > 0
    
    def test_process_text_missing_field(self, client):
        """Test with missing text field"""
        payload = {}
        response = client.post(
            '/api/process-text',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_process_text_empty_string(self, client):
        """Test with empty text"""
        payload = {'text': ''}
        response = client.post(
            '/api/process-text',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_process_text_whitespace_only(self, client):
        """Test with whitespace only"""
        payload = {'text': '   '}
        response = client.post(
            '/api/process-text',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_process_text_long_text(self, client):
        """Test with long text"""
        payload = {'text': 'Hello world. ' * 100}  # Long text
        response = client.post(
            '/api/process-text',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['words']) > 100


class TestCalculateORPEndpoint:
    """Test ORP calculation endpoint"""
    
    def test_calculate_orp_success(self, client):
        """Test successful ORP calculation"""
        payload = {'word': 'reading'}
        response = client.post(
            '/api/calculate-orp',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert data['word'] == 'reading'
        assert data['before'] == 're'
        assert data['orp'] == 'a'
        assert data['after'] == 'ding'
        assert data['orp_position'] == 3
    
    def test_calculate_orp_missing_word(self, client):
        """Test with missing word field"""
        payload = {}
        response = client.post(
            '/api/calculate-orp',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400


class TestPlaceholderEndpoints:
    """Test placeholder endpoints for future features"""
    
    def test_extract_url_not_implemented(self, client):
        """Test URL extraction returns 501"""
        payload = {'url': 'https://example.com'}
        response = client.post(
            '/api/extract-url',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 501
        data = json.loads(response.data)
        assert 'Not implemented' in data['error'] or 'Not implemented' in data['message']
    
    def test_upload_pdf_not_implemented(self, client):
        """Test PDF upload returns 501"""
        response = client.post('/api/upload-pdf')
        
        assert response.status_code == 501


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 for non-existent endpoint"""
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_405_method_not_allowed(self, client):
        """Test 405 for wrong HTTP method"""
        response = client.get('/api/process-text')  # Should be POST
        assert response.status_code == 405


# Run tests with: pytest tests/test_api.py -v
