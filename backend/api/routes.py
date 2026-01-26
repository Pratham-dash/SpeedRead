

from flask import Blueprint, request, jsonify
from services.text_processor import TextProcessor
from services.orp_calculator import ORPCalculator
from services.word_preprocessor import WordPreprocessor
from utils.validators import Validator

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/process-text', methods=['POST'])
def process_text():
    try:
        # Validate request
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing text field',
                'message': 'Request body must contain "text" field'
            }), 400
        
        text = data['text']
        detect_headings = data.get('detect_headings', True)  # New option
        
        # Validate input
        is_valid, error = Validator.validate_text_input(text)
        if not is_valid:
            return jsonify({
                'error': 'Invalid input',
                'message': error
            }), 400
        
        # Initialize services
        processor = TextProcessor()
        preprocessor = WordPreprocessor()
        orp_calc = ORPCalculator()
        
        # Step 1: Split text into words with heading detection
        if detect_headings:
            # Use heading-aware processing
            words_with_meta = processor.split_words_with_metadata(text)
            processed_word_objects = preprocessor.preprocess_with_headings(words_with_meta)
            
            # Extract words list and build ORP data
            processed_words = []
            orp_data = []
            
            for word_obj in processed_word_objects:
                word = word_obj['word']
                multiplier = word_obj['display_multiplier']
                is_heading = word_obj['is_heading']
                
                # Repeat word based on multiplier
                for _ in range(multiplier):
                    processed_words.append(word)
                    
                    if word.strip():  # Skip blank pauses
                        orp_info = orp_calc.split_word(word)
                        orp_data.append({
                            'word': word,
                            'before': orp_info['before'],
                            'orp': orp_info['orp'],
                            'after': orp_info['after'],
                            'position': orp_info['orp_position'],
                            'is_heading': is_heading
                        })
                    else:
                        # Blank pause for pacing
                        orp_data.append({
                            'word': '',
                            'before': '',
                            'orp': '',
                            'after': '',
                            'position': 0,
                            'is_heading': False
                        })
            
            # For stats, count original words
            original_words = [w for w, _ in words_with_meta]
        else:
            # Use original processing without heading detection
            normalized = processor.normalize(text)
            words = processor.split_words(normalized)
            processed_words = preprocessor.preprocess(words)
            
            orp_data = []
            for word in processed_words:
                if word.strip():
                    orp_info = orp_calc.split_word(word)
                    orp_data.append({
                        'word': word,
                        'before': orp_info['before'],
                        'orp': orp_info['orp'],
                        'after': orp_info['after'],
                        'position': orp_info['orp_position'],
                        'is_heading': False
                    })
                else:
                    orp_data.append({
                        'word': '',
                        'before': '',
                        'orp': '',
                        'after': '',
                        'position': 0,
                        'is_heading': False
                    })
            original_words = words
        
        # Step 4: Calculate statistics
        stats = {
            'original_count': len(original_words),
            'processed_count': len(processed_words),
            'estimated_time_300wpm': round(preprocessor.estimate_reading_time(len(processed_words), 300), 1),
            'estimated_time_500wpm': round(preprocessor.estimate_reading_time(len(processed_words), 500), 1)
        }
        
        return jsonify({
            'success': True,
            'words': processed_words,
            'orp_data': orp_data,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Processing failed',
            'message': str(e)
        }), 500


@api_blueprint.route('/calculate-orp', methods=['POST'])
def calculate_orp():
    try:
        data = request.get_json()
        word = data.get('word', '') if data else ''
        
        if not word:
            return jsonify({
                'error': 'Missing word field',
                'message': 'Request body must contain "word" field'
            }), 400
        
        # Calculate ORP
        orp_calc = ORPCalculator()
        result = orp_calc.split_word(word)
        
        return jsonify({
            'success': True,
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Calculation failed',
            'message': str(e)
        }), 500


@api_blueprint.route('/extract-url', methods=['POST'])
def extract_url():
    return jsonify({
        'error': 'Not implemented',
        'message': 'URL extraction will be added in a future version',
        'status': 501
    }), 501


@api_blueprint.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    return jsonify({
        'error': 'Not implemented',
        'message': 'PDF upload will be added in a future version',
        'status': 501
    }), 501


@api_blueprint.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({
        'success': True,
        'message': 'API is working correctly',
        'endpoints': {
            'process_text': '/api/process-text (POST)',
            'calculate_orp': '/api/calculate-orp (POST)',
            'extract_url': '/api/extract-url (POST) - Not implemented',
            'upload_pdf': '/api/upload-pdf (POST) - Not implemented'
        }
    }), 200
