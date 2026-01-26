"""
Global Error Handlers
Centralized error handling for the Flask application
"""

from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': str(error) if str(error) != '400 Bad Request: The browser (or proxy) sent a request that this server could not understand.' else 'The request was malformed or invalid',
            'status': 400
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found on this server',
            'status': 404
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'error': 'Method Not Allowed',
            'message': 'The method is not allowed for the requested URL',
            'status': 405
        }), 405
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            'error': 'Payload Too Large',
            'message': 'The request payload is too large. Maximum size is 16MB',
            'status': 413
        }), 413
    
    @app.errorhandler(415)
    def unsupported_media_type(error):
        return jsonify({
            'error': 'Unsupported Media Type',
            'message': 'The request media type is not supported. Use application/json',
            'status': 415
        }), 415
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred on the server',
            'status': 500
        }), 500
    
    @app.errorhandler(501)
    def not_implemented(error):
        return jsonify({
            'error': 'Not Implemented',
            'message': 'This feature is not yet implemented',
            'status': 501
        }), 501
    
    @app.errorhandler(503)
    def service_unavailable(error):
        return jsonify({
            'error': 'Service Unavailable',
            'message': 'The service is temporarily unavailable. Please try again later',
            'status': 503
        }), 503
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        # Log the error
        print(f"Unexpected error: {str(error)}")
        
        # Check if it's an HTTP exception
        if isinstance(error, HTTPException):
            return jsonify({
                'error': error.name,
                'message': error.description,
                'status': error.code
            }), error.code
        
        # Generic error response (don't expose internal details)
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status': 500
        }), 500


class ValidationError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ProcessingError(Exception):
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ResourceNotFoundError(Exception):
    def __init__(self, message, status_code=404):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
