# """
# Enhanced Flask Backend API with Internet Plagiarism Detection
# File: backend_api/app_enhanced.py

# Adds /check_internet endpoint for web-wide plagiarism detection
# """

# from file_handler import extract_text_from_file, validate_file
# from pdf_generator import generate_pdf_report
# from dotenv import load_dotenv; load_dotenv()
# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from utils import calculate_cosine_similarity, highlight_matching_text
# from google_search_integration import compare_with_internet_sources, validate_credentials
# import joblib
# import os
# import logging
# import traceback

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # Configuration
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# # Load ML model
# MODEL_PATH = "plagiarism_model.pkl"
# model = None

# def load_model():
#     """Load ML model on startup"""
#     global model
#     try:
#         if os.path.exists(MODEL_PATH):
#             model = joblib.load(MODEL_PATH)
#             logger.info(f"✅ Model loaded successfully")
#         else:
#             logger.warning(f"⚠️ Model file not found at {MODEL_PATH}")
#     except Exception as e:
#         logger.error(f"❌ Error loading model: {str(e)}")

# load_model()


# @app.route("/", methods=["GET"])
# def home():
#     """Health check endpoint"""
#     return jsonify({
#         "status": "running",
#         "message": "Enhanced Plagiarism Checker API",
#         "version": "2.0.0",
#         "endpoints": {
#             "GET /": "Health check",
#             "POST /check": "Compare two documents (local)",
#             "POST /check_internet": "Check plagiarism against internet",
#             "GET /config_status": "Check API configuration"
#         }
#     }), 200


# @app.route("/config_status", methods=["GET"])
# def config_status():
#     """Check if Google API is properly configured"""
#     is_configured = validate_credentials()
    
#     return jsonify({
#         "status": "configured" if is_configured else "not_configured",
#         "google_api_configured": is_configured,
#         "model_loaded": model is not None,
#         "message": "Ready for internet plagiarism detection" if is_configured else "Configure Google API credentials"
#     }), 200


# @app.route("/check", methods=["POST"])
# def check_plagiarism():
#     """
#     Original endpoint: Check plagiarism between two uploaded documents
    
#     Request:
#         - original: Original document file
#         - submission: Submission document file
    
#     Response:
#         - similarity_score, plagiarized, probability, highlighted texts
#     """
    
#     logger.info("📋 LOCAL DOCUMENT COMPARISON - REQUEST RECEIVED")
    
#     try:
#         # Validate model
#         if model is None:
#             logger.error("❌ Model not loaded")
#             return jsonify({
#                 "error": "Model not loaded. Please train the model first.",
#                 "status": "model_error"
#             }), 500
        
#         # Get files
#         if 'original' not in request.files or 'submission' not in request.files:
#             logger.warning("⚠️ Missing required files")
#             return jsonify({"error": "Both 'original' and 'submission' files required"}), 400
        
#         file1 = request.files['original']
#         file2 = request.files['submission']
        
#         # Read contents
#         try:
#             text1 = file1.read().decode('utf-8')
#             text2 = file2.read().decode('utf-8')
#         except UnicodeDecodeError:
#             logger.error("❌ File encoding error")
#             return jsonify({"error": "Files must be UTF-8 encoded"}), 400
        
#         # Validate non-empty
#         if not text1.strip() or not text2.strip():
#             logger.warning("⚠️ Empty file")
#             return jsonify({"error": "Files cannot be empty"}), 400
        
#         logger.info(f"✓ Files received: {file1.filename}, {file2.filename}")
        
#         # Calculate similarity
#         similarity = calculate_cosine_similarity(text1, text2)
        
#         # Predict
#         prediction = model.predict([[similarity]])[0]
#         probability = model.predict_proba([[similarity]])[0][1]
        
#         # Highlight
#         highlighted1, highlighted2 = highlight_matching_text(text1, text2)
        
#         response = {
#             "similarity_score": round(float(similarity), 4),
#             "plagiarized": bool(prediction),
#             "probability": round(float(probability), 4),
#             "highlighted_original": highlighted1,
#             "highlighted_submission": highlighted2
#         }
        
#         logger.info(f"✅ Comparison complete: {similarity:.4f}")
        
#         return jsonify(response), 200
    
#     except Exception as e:
#         logger.error(f"❌ Error: {str(e)}")
#         logger.error(traceback.format_exc())
#         return jsonify({"error": str(e)}), 500


# @app.route("/check_internet", methods=["POST"])
# def check_internet_plagiarism():
#     """
#     NEW ENDPOINT: Check plagiarism against internet sources
    
#     Request:
#         - submission: Document file to check
    
#     Response:
#         - internet_matches: Top-5 matches with URLs and similarity
#         - overall_verdict: PLAGIARIZED or LIKELY ORIGINAL
#     """
    
#     logger.info("\n" + "🌐 INTERNET PLAGIARISM CHECK - REQUEST RECEIVED".center(60))
    
#     try:
#         # Validate credentials
#         if not validate_credentials():
#             logger.error("❌ Google API not configured")
#             return jsonify({
#                 "error": "Google API not configured. Set GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables.",
#                 "status": "api_not_configured"
#             }), 500
        
#         # Get submission file
#         if 'submission' not in request.files:
#             logger.warning("⚠️ Missing submission file")
#             return jsonify({"error": "Missing 'submission' file"}), 400
        
#         submission_file = request.files['submission']
        
#         if submission_file.filename == '':
#             logger.warning("⚠️ Empty filename")
#             return jsonify({"error": "Submission file must be selected"}), 400
        
#         # Read file
#         try:
#             submission_text = submission_file.read().decode('utf-8')
#         except UnicodeDecodeError:
#             logger.error("❌ File encoding error")
#             return jsonify({"error": "File must be UTF-8 encoded text"}), 400
        
#         if not submission_text.strip():
#             logger.warning("⚠️ Empty submission text")
#             return jsonify({"error": "Submission file cannot be empty"}), 400
        
#         logger.info(f"✓ Submission received: {submission_file.filename}")
#         logger.info(f"  Size: {len(submission_text)} characters")
        
#         # Compare with internet sources
#         result = compare_with_internet_sources(submission_text)
        
#         if result.get('status') == 'error':
#             logger.error(f"❌ Error from plagiarism check: {result.get('message')}")
#             return jsonify(result), 500
        
#         # Add metadata to response
#         result['submission_filename'] = submission_file.filename
#         result['submission_size'] = len(submission_text)
        
#         logger.info("\n✅ INTERNET CHECK COMPLETE")
#         logger.info(f"   Matches found: {result.get('total_matches_found', 0)}")
#         logger.info(f"   Verdict: {result.get('overall_verdict', 'UNKNOWN')}\n")
        
#         return jsonify(result), 200
    
#     except Exception as e:
#         logger.error(f"❌ Error in internet check: {str(e)}")
#         logger.error(traceback.format_exc())
#         return jsonify({
#             "error": f"Error checking plagiarism: {str(e)}",
#             "status": "processing_error"
#         }), 500


# @app.errorhandler(413)
# def request_entity_too_large(error):
#     logger.warning("❌ File size exceeds limit")
#     return jsonify({"error": "File size too large. Maximum allowed: 16MB"}), 413


# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({
#         "error": "Endpoint not found",
#         "available_endpoints": [
#             "GET /",
#             "GET /config_status",
#             "POST /check",
#             "POST /check_internet"
#         ]
#     }), 404


# @app.errorhandler(500)
# def internal_error(error):
#     logger.error(f"❌ Internal error: {str(error)}")
#     return jsonify({"error": "Internal server error"}), 500


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
    
#     print("\n" + "=" * 70)
#     print("🚀 ENHANCED PLAGIARISM CHECKER API - STARTING")
#     print("=" * 70)
#     print(f"📍 Server: http://0.0.0.0:{port}")
#     print(f"🤖 Model: {'✓ Loaded' if model else '✗ Not loaded'}")
#     print(f"🌐 Google API: {'✓ Configured' if validate_credentials() else '✗ Not configured'}")
#     print("\n📡 ENDPOINTS:")
#     print(f"   GET  http://localhost:{port}/                 - Health check")
#     print(f"   GET  http://localhost:{port}/config_status   - API configuration status")
#     print(f"   POST http://localhost:{port}/check           - Compare two documents")
#     print(f"   POST http://localhost:{port}/check_internet - Search internet for plagiarism")
#     print("=" * 70 + "\n")
    
#     app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

























# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# from utils import calculate_cosine_similarity, highlight_matching_text
# from google_search_integration import compare_with_internet_sources, validate_credentials
# import joblib
# import os
# import logging
# import traceback
# import io
# from datetime import datetime

# # ============ STEP 3 ADDITIONS ============
# # Import file handler and PDF generator
# from file_handler import extract_text_from_file, validate_file, get_file_type_from_name
# from pdf_generator import generate_pdf_report

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # Configuration
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# # Load ML model
# MODEL_PATH = "plagiarism_model.pkl"
# model = None

# def load_model():
#     """Load ML model on startup"""
#     global model
#     try:
#         if os.path.exists(MODEL_PATH):
#             model = joblib.load(MODEL_PATH)
#             logger.info(f"✅ Model loaded successfully")
#         else:
#             logger.warning(f"⚠️ Model file not found at {MODEL_PATH}")
#     except Exception as e:
#         logger.error(f"❌ Error loading model: {str(e)}")

# load_model()


# @app.route("/", methods=["GET"])
# def home():
#     """Health check endpoint"""
#     return jsonify({
#         "status": "running",
#         "message": "Enhanced Plagiarism Checker API",
#         "version": "3.0.0",
#         "endpoints": {
#             "GET /": "Health check",
#             "POST /check": "Compare two documents (multi-format)",
#             "POST /check_internet": "Check plagiarism against internet",
#             "POST /generate_pdf": "Generate PDF report",
#             "GET /config_status": "Check API configuration"
#         }
#     }), 200


# @app.route("/config_status", methods=["GET"])
# def config_status():
#     """Check if Google API is properly configured"""
#     is_configured = validate_credentials()
    
#     return jsonify({
#         "status": "configured" if is_configured else "not_configured",
#         "google_api_configured": is_configured,
#         "model_loaded": model is not None,
#         "message": "Ready for internet plagiarism detection" if is_configured else "Configure Google API credentials"
#     }), 200


# @app.route("/check", methods=["POST"])
# def check_plagiarism():
#     """
#     ENHANCED: Check plagiarism between two uploaded documents
    
#     STEP 3 ADDITION: Now supports TXT, PDF, DOCX formats
    
#     Request:
#         - original: Original document file (TXT, PDF, DOCX)
#         - submission: Submission document file (TXT, PDF, DOCX)
    
#     Response:
#         - similarity_score, plagiarized, probability, highlighted texts
#     """
    
#     logger.info("📋 LOCAL DOCUMENT COMPARISON - REQUEST RECEIVED")
    
#     try:
#         # Validate model
#         if model is None:
#             logger.error("❌ Model not loaded")
#             return jsonify({
#                 "error": "Model not loaded. Please train the model first.",
#                 "status": "model_error"
#             }), 500
        
#         # Get files
#         if 'original' not in request.files or 'submission' not in request.files:
#             logger.warning("⚠️ Missing required files")
#             return jsonify({"error": "Both 'original' and 'submission' files required"}), 400
        
#         file1 = request.files['original']
#         file2 = request.files['submission']
        
#         # STEP 3: Validate files
#         try:
#             validate_file(file1, file1.filename)
#             validate_file(file2, file2.filename)
#             logger.info(f"✓ Files validated: {file1.filename}, {file2.filename}")
#         except ValueError as e:
#             logger.warning(f"⚠️ File validation error: {str(e)}")
#             return jsonify({"error": str(e)}), 400
        
#         # STEP 3: Extract text from files (supports TXT, PDF, DOCX)
#         try:
#             text1, type1 = extract_text_from_file(file1, file1.filename)
#             text2, type2 = extract_text_from_file(file2, file2.filename)
#             logger.info(f"✓ Text extracted: {type1} ({len(text1)} chars), {type2} ({len(text2)} chars)")
#         except Exception as e:
#             logger.error(f"❌ File processing error: {str(e)}")
#             return jsonify({"error": f"File processing error: {str(e)}"}), 400
        
#         # Validate non-empty
#         if not text1.strip() or not text2.strip():
#             logger.warning("⚠️ Empty file content")
#             return jsonify({"error": "Files cannot be empty"}), 400
        
#         # Calculate similarity
#         similarity = calculate_cosine_similarity(text1, text2)
        
#         # Predict
#         prediction = model.predict([[similarity]])[0]
#         probability = model.predict_proba([[similarity]])[0][1]
        
#         # Highlight
#         highlighted1, highlighted2 = highlight_matching_text(text1, text2)
        
#         response = {
#             "similarity_score": round(float(similarity), 4),
#             "plagiarized": bool(prediction),
#             "probability": round(float(probability), 4),
#             "highlighted_original": highlighted1,
#             "highlighted_submission": highlighted2,
#             "original_filename": file1.filename,
#             "original_type": type1,
#             "submission_filename": file2.filename,
#             "submission_type": type2
#         }
        
#         logger.info(f"✅ Comparison complete: {similarity:.4f}")
        
#         return jsonify(response), 200
    
#     except Exception as e:
#         logger.error(f"❌ Error: {str(e)}")
#         logger.error(traceback.format_exc())
#         return jsonify({"error": str(e)}), 500


# @app.route("/check_internet", methods=["POST"])
# def check_internet_plagiarism():
#     """
#     NEW ENDPOINT: Check plagiarism against internet sources
    
#     STEP 3 ADDITION: Now supports TXT, PDF, DOCX formats
    
#     Request:
#         - submission: Document file to check (TXT, PDF, DOCX)
    
#     Response:
#         - internet_matches: Top-5 matches with URLs and similarity
#         - overall_verdict: PLAGIARIZED or LIKELY ORIGINAL
#     """
    
#     logger.info("\n" + "🌐 INTERNET PLAGIARISM CHECK - REQUEST RECEIVED".center(60))
    
#     try:
#         # Validate credentials
#         if not validate_credentials():
#             logger.error("❌ Google API not configured")
#             return jsonify({
#                 "error": "Google API not configured. Set GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables.",
#                 "status": "api_not_configured"
#             }), 500
        
#         # Get submission file
#         if 'submission' not in request.files:
#             logger.warning("⚠️ Missing submission file")
#             return jsonify({"error": "Missing 'submission' file"}), 400
        
#         submission_file = request.files['submission']
        
#         if submission_file.filename == '':
#             logger.warning("⚠️ Empty filename")
#             return jsonify({"error": "Submission file must be selected"}), 400
        
#         # STEP 3: Validate file
#         try:
#             validate_file(submission_file, submission_file.filename)
#             logger.info(f"✓ File validated: {submission_file.filename}")
#         except ValueError as e:
#             logger.warning(f"⚠️ File validation error: {str(e)}")
#             return jsonify({"error": str(e)}), 400
        
#         # STEP 3: Extract text (supports TXT, PDF, DOCX)
#         try:
#             submission_text, file_type = extract_text_from_file(submission_file, submission_file.filename)
#             logger.info(f"✓ Text extracted: {file_type} ({len(submission_text)} characters)")
#         except Exception as e:
#             logger.error(f"❌ File processing error: {str(e)}")
#             return jsonify({"error": f"File processing error: {str(e)}"}), 400
        
#         if not submission_text.strip():
#             logger.warning("⚠️ Empty submission text")
#             return jsonify({"error": "Submission file cannot be empty"}), 400
        
#         logger.info(f"✓ Submission received: {submission_file.filename} ({file_type})")
#         logger.info(f"  Size: {len(submission_text)} characters")
        
#         # Compare with internet sources
#         result = compare_with_internet_sources(submission_text)
        
#         if result.get('status') == 'error':
#             logger.error(f"❌ Error from plagiarism check: {result.get('message')}")
#             return jsonify(result), 500
        
#         # Add metadata to response
#         result['submission_filename'] = submission_file.filename
#         result['submission_type'] = file_type
#         result['submission_size'] = len(submission_text)
        
#         logger.info("\n✅ INTERNET CHECK COMPLETE")
#         logger.info(f"   Matches found: {result.get('total_matches_found', 0)}")
#         logger.info(f"   Verdict: {result.get('overall_verdict', 'UNKNOWN')}\n")
        
#         return jsonify(result), 200
    
#     except Exception as e:
#         logger.error(f"❌ Error in internet check: {str(e)}")
#         logger.error(traceback.format_exc())
#         return jsonify({
#             "error": f"Error checking plagiarism: {str(e)}",
#             "status": "processing_error"
#         }), 500


# @app.route("/generate_pdf", methods=["POST"])
# def generate_pdf():
#     """
#     STEP 3 ADDITION: Generate PDF report from analysis results
    
#     Request (JSON):
#         - data: Analysis results from /check or /check_internet
#         - mode: "local" or "internet"
    
#     Response:
#         - PDF file download
#     """
    
#     logger.info("📄 PDF GENERATION - REQUEST RECEIVED")
    
#     try:
#         # Get request data
#         request_data = request.get_json()
        
#         if not request_data or 'data' not in request_data:
#             return jsonify({"error": "Missing analysis data"}), 400
        
#         data = request_data['data']
#         mode = request_data.get('mode', 'local')
        
#         logger.info(f"Generating PDF report (mode: {mode})")
        
#         # Generate PDF
#         pdf_content = generate_pdf_report(data, mode)
        
#         logger.info("✅ PDF generated successfully")
        
#         # Return PDF file
#         return send_file(
#             io.BytesIO(pdf_content),
#             mimetype='application/pdf',
#             as_attachment=True,
#             download_name=f"plagiarism_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#         )
    
#     except Exception as e:
#         logger.error(f"❌ Error generating PDF: {str(e)}")
#         logger.error(traceback.format_exc())
#         return jsonify({"error": f"PDF generation error: {str(e)}"}), 500


# @app.errorhandler(413)
# def request_entity_too_large(error):
#     logger.warning("❌ File size exceeds limit")
#     return jsonify({"error": "File size too large. Maximum allowed: 16MB"}), 413


# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({
#         "error": "Endpoint not found",
#         "available_endpoints": [
#             "GET /",
#             "GET /config_status",
#             "POST /check",
#             "POST /check_internet",
#             "POST /generate_pdf"
#         ]
#     }), 404


# @app.errorhandler(500)
# def internal_error(error):
#     logger.error(f"❌ Internal error: {str(error)}")
#     return jsonify({"error": "Internal server error"}), 500


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
    
#     print("\n" + "=" * 70)
#     print("🚀 ENHANCED PLAGIARISM CHECKER API - STARTING")
#     print("=" * 70)
#     print(f"📍 Server: http://0.0.0.0:{port}")
#     print(f"🤖 Model: {'✓ Loaded' if model else '✗ Not loaded'}")
#     print(f"🌐 Google API: {'✓ Configured' if validate_credentials() else '✗ Not configured'}")
#     print(f"📂 File Support: TXT, PDF, DOCX")
#     print(f"📄 PDF Generation: ✓ Enabled")
    
#     print("\n📡 ENDPOINTS:")
#     print(f"   GET  http://localhost:{port}/                 - Health check")
#     print(f"   GET  http://localhost:{port}/config_status   - API configuration")
#     print(f"   POST http://localhost:{port}/check           - Compare documents (STEP 3: Multi-format)")
#     print(f"   POST http://localhost:{port}/check_internet - Internet plagiarism search")
#     print(f"   POST http://localhost:{port}/generate_pdf   - Generate PDF report (NEW)")
#     print("=" * 70 + "\n")
    
#     app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)




















































# """
# FILE 2: backend_api/app_enhanced.py - COMPLETE UPDATED BACKEND
# This backend MUST send the highlighted_submission to PDF generator
# """

# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# from utils import calculate_cosine_similarity, highlight_matching_text
# from google_search_integration import compare_with_internet_sources, validate_credentials
# from file_handler import extract_text_from_file, validate_file
# from turnitin_style_pdf_generator import generate_turnitin_style_report
# import joblib
# import os
# import logging
# import traceback
# import io
# from datetime import datetime

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# app = Flask(__name__)
# CORS(app)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# MODEL_PATH = "plagiarism_model.pkl"
# model = None

# def load_model():
#     global model
#     try:
#         if os.path.exists(MODEL_PATH):
#             model = joblib.load(MODEL_PATH)
#             logger.info("✅ Model loaded successfully")
#         else:
#             logger.warning("⚠️ Model file not found")
#     except Exception as e:
#         logger.error(f"❌ Error loading model: {str(e)}")

# load_model()

# @app.route("/", methods=["GET"])
# def home():
#     return jsonify({
#         "status": "running",
#         "message": "Professional Plagiarism Checker API",
#         "version": "3.0.0 - Final Edition"
#     }), 200

# @app.route("/config_status", methods=["GET"])
# def config_status():
#     is_configured = validate_credentials()
#     return jsonify({
#         "status": "configured" if is_configured else "not_configured",
#         "google_api_configured": is_configured,
#         "model_loaded": model is not None
#     }), 200

# @app.route("/check", methods=["POST"])
# def check_plagiarism():
#     """Compare two documents"""
#     logger.info("📋 LOCAL DOCUMENT COMPARISON")
#     try:
#         if model is None:
#             return jsonify({"error": "Model not loaded"}), 500
        
#         if 'original' not in request.files or 'submission' not in request.files:
#             return jsonify({"error": "Both files required"}), 400
        
#         file1 = request.files['original']
#         file2 = request.files['submission']
        
#         try:
#             validate_file(file1, file1.filename)
#             validate_file(file2, file2.filename)
#         except ValueError as e:
#             return jsonify({"error": str(e)}), 400
        
#         try:
#             text1, type1 = extract_text_from_file(file1, file1.filename)
#             text2, type2 = extract_text_from_file(file2, file2.filename)
#         except Exception as e:
#             return jsonify({"error": f"File processing error: {str(e)}"}), 400
        
#         if not text1.strip() or not text2.strip():
#             return jsonify({"error": "Files cannot be empty"}), 400
        
#         similarity = calculate_cosine_similarity(text1, text2)
#         prediction = model.predict([[similarity]])[0]
#         probability = model.predict_proba([[similarity]])[0][1]
        
#         # GET HIGHLIGHTED TEXT - THIS IS CRITICAL
#         highlighted1, highlighted2 = highlight_matching_text(text1, text2)
        
#         response = {
#             "similarity_score": round(float(similarity), 4),
#             "plagiarized": bool(prediction),
#             "probability": round(float(probability), 4),
#             "highlighted_original": highlighted1,
#             "highlighted_submission": highlighted2,
#             "original_filename": file1.filename,
#             "original_type": type1,
#             "submission_filename": file2.filename,
#             "submission_type": type2,
#             "submission_size": len(text2),
#             "submission_text": text2  # INCLUDE RAW TEXT
#         }
        
#         logger.info(f"✅ Comparison complete: {similarity:.4f}")
#         return jsonify(response), 200
    
#     except Exception as e:
#         logger.error(f"❌ Error: {str(e)}")
#         logger.error(traceback.format_exc())
#         return jsonify({"error": str(e)}), 500

# @app.route("/check_internet", methods=["POST"])
# def check_internet_plagiarism():
#     """Check plagiarism against internet"""
#     logger.info("🌐 INTERNET PLAGIARISM CHECK")
#     try:
#         if not validate_credentials():
#             return jsonify({"error": "Google API not configured"}), 500
        
#         if 'submission' not in request.files:
#             return jsonify({"error": "Missing submission file"}), 400
        
#         submission_file = request.files['submission']
        
#         try:
#             validate_file(submission_file, submission_file.filename)
#             submission_text, file_type = extract_text_from_file(submission_file, submission_file.filename)
#         except Exception as e:
#             return jsonify({"error": str(e)}), 400
        
#         if not submission_text.strip():
#             return jsonify({"error": "File cannot be empty"}), 400
        
#         result = compare_with_internet_sources(submission_text)
        
#         if result.get('status') == 'error':
#             return jsonify(result), 500
        
#         # CREATE HIGHLIGHTED VERSION FOR INTERNET MODE
#         # This highlights the most plagiarized parts
#         highlighted_text = create_internet_highlighted_version(submission_text, result)
        
#         result['submission_filename'] = submission_file.filename
#         result['submission_type'] = file_type
#         result['submission_size'] = len(submission_text)
#         result['submission_text'] = submission_text  # INCLUDE RAW TEXT
#         result['highlighted_submission'] = highlighted_text  # HIGHLIGHTED VERSION
        
#         logger.info(f"✅ Internet check complete")
#         return jsonify(result), 200
    
#     except Exception as e:
#         logger.error(f"❌ Error: {str(e)}")
#         return jsonify({"error": str(e)}), 500

# def create_internet_highlighted_version(text, result):
#     """Create highlighted version for internet search results"""
#     try:
#         matches = result.get('internet_matches', [])
#         if not matches:
#             return f"<i>{text[:3000]}</i>"
        
#         # Get top match keywords
#         highlighted = text
        
#         # Highlight key phrases from snippets
#         for match in matches[:5]:
#             snippet = match.get('snippet', '')
#             similarity = match.get('similarity_score', 0)
            
#             if snippet and similarity > 0.1:
#                 # Extract keywords from snippet and highlight them in text
#                 words = snippet.split()[:10]  # First 10 words
#                 for word in words:
#                     if len(word) > 4 and word in highlighted:
#                         # Highlight this word
#                         highlighted = highlighted.replace(
#                             word,
#                             f'<span style="background-color: #FFFF00;"><b>{word}</b></span>'
#                         )
        
#         if highlighted == text:
#             # If no highlighting done, just return formatted text
#             return f"<font size='9'>{text[:5000]}</font>"
        
#         return f"<font size='9'>{highlighted[:5000]}</font>"
#     except:
#         return f"<font size='9'>{text[:5000]}</font>"

# @app.route("/generate_turnitin_pdf", methods=["POST"])
# def generate_turnitin_pdf():
#     """Generate professional Turnitin-style PDF"""
#     logger.info("📄 TURNITIN PDF GENERATION")
#     try:
#         request_data = request.get_json()
#         if not request_data or 'data' not in request_data:
#             return jsonify({"error": "Missing analysis data"}), 400
        
#         data = request_data['data']
#         mode = request_data.get('mode', 'local')
        
#         logger.info(f"Generating PDF - Mode: {mode}")
#         logger.info(f"Data keys: {data.keys()}")
        
#         # CRITICAL: Make sure highlighted_submission is present
#         if 'highlighted_submission' not in data:
#             logger.warning("⚠️ highlighted_submission missing, using raw text")
#             if 'submission_text' in data:
#                 # Fallback: wrap raw text
#                 data['highlighted_submission'] = f"<font size='9'>{data['submission_text'][:5000]}</font>"
        
#         pdf_content = generate_turnitin_style_report(data, mode)
        
#         logger.info("✅ PDF generated successfully")
        
#         return send_file(
#             io.BytesIO(pdf_content),
#             mimetype='application/pdf',
#             as_attachment=True,
#             download_name=f"plagiarism_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#         )
    
#     except Exception as e:
#         logger.error(f"❌ PDF generation error: {str(e)}")
#         logger.error(traceback.format_exc())
#         return jsonify({"error": f"PDF generation error: {str(e)}"}), 500

# @app.errorhandler(413)
# def request_entity_too_large(error):
#     return jsonify({"error": "File too large (max 16MB)"}), 413

# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({"error": "Endpoint not found"}), 404

# @app.errorhandler(500)
# def internal_error(error):
#     logger.error(f"❌ Internal error: {str(error)}")
#     return jsonify({"error": "Internal server error"}), 500

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     print("\n" + "=" * 90)
#     print("🚀 PROFESSIONAL PLAGIARISM CHECKER - FINAL VERSION")
#     print("=" * 90)
#     print(f"📍 Server: http://0.0.0.0:{port}")
#     print(f"🤖 ML Model: {'✓ Loaded' if model else '✗ Not loaded'}")
#     print(f"🌐 Google API: {'✓ Configured' if validate_credentials() else '✗ Not configured'}")
#     print(f"📂 File Support: TXT, PDF, DOCX (up to 16MB)")
#     print(f"📄 Report Style: Turnitin Professional (Full document with highlighting)\n")
#     print("📡 ENDPOINTS:")
#     print(f"   POST /{port}/check                    - Compare documents")
#     print(f"   POST /{port}/check_internet          - Internet search")
#     print(f"   POST /{port}/generate_turnitin_pdf  - Professional PDF report")
#     print("=" * 90 + "\n")
    
#     app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)







































# """
# Enhanced Flask Backend API with Internet Plagiarism Detection + Multi-Format Support
# File: backend_api/app_enhanced.py

# Adds /check_internet endpoint + PDF generation + multi-format file support
# """

# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# from utils import calculate_cosine_similarity, highlight_matching_text
# from google_search_integration import compare_with_internet_sources, validate_credentials
# import joblib
# import os
# import logging
# import traceback
# import io
# from datetime import datetime

# # ============ STEP 3 ADDITIONS ============
# # Import file handler and PDF generator
# from file_handler import extract_text_from_file, validate_file, get_file_type_from_name
# from pdf_generator import generate_pdf_report

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # Configuration
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# # Load ML model
# MODEL_PATH = "plagiarism_model.pkl"
# model = None

# def load_model():
#     """Load ML model on startup"""
#     global model
#     try:
#         if os.path.exists(MODEL_PATH):
#             model = joblib.load(MODEL_PATH)
#             logger.info(f"✅ Model loaded successfully")
#         else:
#             logger.warning(f"⚠️ Model file not found at {MODEL_PATH}")
#     except Exception as e:
#         logger.error(f"❌ Error loading model: {str(e)}")

# load_model()


# @app.route("/", methods=["GET"])
# def home():
#     """Health check endpoint"""
#     return jsonify({
#         "status": "running",
#         "message": "Enhanced Plagiarism Checker API",
#         "version": "3.0.0",
#         "endpoints": {
#             "GET /": "Health check",
#             "POST /check": "Compare two documents (multi-format)",
#             "POST /check_internet": "Check plagiarism against internet",
#             "POST /generate_pdf": "Generate PDF report",
#             "GET /config_status": "Check API configuration"
#         }
#     }), 200


# @app.route("/config_status", methods=["GET"])
# def config_status():
#     """Check if Google API is properly configured"""
#     is_configured = validate_credentials()
    
#     return jsonify({
#         "status": "configured" if is_configured else "not_configured",
#         "google_api_configured": is_configured,
#         "model_loaded": model is not None,
#         "message": "Ready for internet plagiarism detection" if is_configured else "Configure Google API credentials"
#     }), 200


# @app.route("/check", methods=["POST"])
# def check_plagiarism():
#     """
#     ENHANCED: Check plagiarism between two uploaded documents
    
#     STEP 3 ADDITION: Now supports TXT, PDF, DOCX formats
    
#     Request:
#         - original: Original document file (TXT, PDF, DOCX)
#         - submission: Submission document file (TXT, PDF, DOCX)
    
#     Response:
#         - similarity_score, plagiarized, probability, highlighted texts
#     """
    
#     logger.info("📋 LOCAL DOCUMENT COMPARISON - REQUEST RECEIVED")
    
#     try:
#         # Validate model
#         if model is None:
#             logger.error("❌ Model not loaded")
#             return jsonify({
#                 "error": "Model not loaded. Please train the model first.",
#                 "status": "model_error"
#             }), 500
        
#         # Get files
#         if 'original' not in request.files or 'submission' not in request.files:
#             logger.warning("⚠️ Missing required files")
#             return jsonify({"error": "Both 'original' and 'submission' files required"}), 400
        
#         file1 = request.files['original']
#         file2 = request.files['submission']
        
#         # STEP 3: Validate files
#         try:
#             validate_file(file1, file1.filename)
#             validate_file(file2, file2.filename)
#             logger.info(f"✓ Files validated: {file1.filename}, {file2.filename}")
#         except ValueError as e:
#             logger.warning(f"⚠️ File validation error: {str(e)}")
#             return jsonify({"error": str(e)}), 400
        
#         # STEP 3: Extract text from files (supports TXT, PDF, DOCX)
#         try:
#             text1, type1 = extract_text_from_file(file1, file1.filename)
#             text2, type2 = extract_text_from_file(file2, file2.filename)
#             logger.info(f"✓ Text extracted: {type1} ({len(text1)} chars), {type2} ({len(text2)} chars)")
#         except Exception as e:
#             logger.error(f"❌ File processing error: {str(e)}")
#             return jsonify({"error": f"File processing error: {str(e)}"}), 400
        
#         # Validate non-empty
#         if not text1.strip() or not text2.strip():
#             logger.warning("⚠️ Empty file content")
#             return jsonify({"error": "Files cannot be empty"}), 400
        
#         # Calculate similarity
#         similarity = calculate_cosine_similarity(text1, text2)
        
#         # Predict
#         prediction = model.predict([[similarity]])[0]
#         probability = model.predict_proba([[similarity]])[0][1]
        
#         # Highlight
#         highlighted1, highlighted2 = highlight_matching_text(text1, text2)
        
#         response = {
#             "similarity_score": round(float(similarity), 4),
#             "plagiarized": bool(prediction),
#             "probability": round(float(probability), 4),
#             "highlighted_original": highlighted1,
#             "highlighted_submission": highlighted2,
#             "original_filename": file1.filename,
#             "original_type": type1,
#             "submission_filename": file2.filename,
#             "submission_type": type2
#         }
        
#         logger.info(f"✅ Comparison complete: {similarity:.4f}")
        
#         return jsonify(response), 200
    
#     except Exception as e:
#         logger.error(f"❌ Error: {str(e)}")
#         logger.error(traceback.format_exc())
#         return jsonify({"error": str(e)}), 500


# @app.route("/check_internet", methods=["POST"])
# def check_internet_plagiarism():
#     """
#     NEW ENDPOINT: Check plagiarism against internet sources
    
#     STEP 3 ADDITION: Now supports TXT, PDF, DOCX formats
    
#     Request:
#         - submission: Document file to check (TXT, PDF, DOCX)
    
#     Response:
#         - internet_matches: Top-5 matches with URLs and similarity
#         - overall_verdict: PLAGIARIZED or LIKELY ORIGINAL
#     """
    
#     logger.info("\n" + "🌐 INTERNET PLAGIARISM CHECK - REQUEST RECEIVED".center(60))
    
#     try:
#         # Validate credentials
#         if not validate_credentials():
#             logger.error("❌ Google API not configured")
#             return jsonify({
#                 "error": "Google API not configured. Set GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables.",
#                 "status": "api_not_configured"
#             }), 500
        
#         # Get submission file
#         if 'submission' not in request.files:
#             logger.warning("⚠️ Missing submission file")
#             return jsonify({"error": "Missing 'submission' file"}), 400
        
#         submission_file = request.files['submission']
        
#         if submission_file.filename == '':
#             logger.warning("⚠️ Empty filename")
#             return jsonify({"error": "Submission file must be selected"}), 400
        
#         # STEP 3: Validate file
#         try:
#             validate_file(submission_file, submission_file.filename)
#             logger.info(f"✓ File validated: {submission_file.filename}")
#         except ValueError as e:
#             logger.warning(f"⚠️ File validation error: {str(e)}")
#             return jsonify({"error": str(e)}), 400
        
#         # STEP 3: Extract text (supports TXT, PDF, DOCX)
#         try:
#             submission_text, file_type = extract_text_from_file(submission_file, submission_file.filename)
#             logger.info(f"✓ Text extracted: {file_type} ({len(submission_text)} characters)")
#         except Exception as e:
#             logger.error(f"❌ File processing error: {str(e)}")
#             return jsonify({"error": f"File processing error: {str(e)}"}), 400
        
#         if not submission_text.strip():
#             logger.warning("⚠️ Empty submission text")
#             return jsonify({"error": "Submission file cannot be empty"}), 400
        
#         logger.info(f"✓ Submission received: {submission_file.filename} ({file_type})")
#         logger.info(f"  Size: {len(submission_text)} characters")
        
#         # Compare with internet sources
#         result = compare_with_internet_sources(submission_text)
        
#         if result.get('status') == 'error':
#             logger.error(f"❌ Error from plagiarism check: {result.get('message')}")
#             return jsonify(result), 500
        
#         # Add metadata to response
#         result['submission_filename'] = submission_file.filename
#         result['submission_type'] = file_type
#         result['submission_size'] = len(submission_text)
        
#         logger.info("\n✅ INTERNET CHECK COMPLETE")
#         logger.info(f"   Matches found: {result.get('total_matches_found', 0)}")
#         logger.info(f"   Verdict: {result.get('overall_verdict', 'UNKNOWN')}\n")
        
#         return jsonify(result), 200
    
#     except Exception as e:
#         logger.error(f"❌ Error in internet check: {str(e)}")
#         logger.error(traceback.format_exc())
#         return jsonify({
#             "error": f"Error checking plagiarism: {str(e)}",
#             "status": "processing_error"
#         }), 500


# @app.route("/generate_pdf", methods=["POST"])
# def generate_pdf():
#     """
#     STEP 3 ADDITION: Generate PDF report from analysis results
    
#     Request (JSON):
#         - data: Analysis results from /check or /check_internet
#         - mode: "local" or "internet"
    
#     Response:
#         - PDF file download
#     """
    
#     logger.info("📄 PDF GENERATION - REQUEST RECEIVED")
    
#     try:
#         # Get request data
#         request_data = request.get_json()
        
#         if not request_data or 'data' not in request_data:
#             return jsonify({"error": "Missing analysis data"}), 400
        
#         data = request_data['data']
#         mode = request_data.get('mode', 'local')
        
#         logger.info(f"Generating PDF report (mode: {mode})")
        
#         # Generate PDF
#         pdf_content = generate_pdf_report(data, mode)
        
#         logger.info("✅ PDF generated successfully")
        
#         # Return PDF file
#         return send_file(
#             io.BytesIO(pdf_content),
#             mimetype='application/pdf',
#             as_attachment=True,
#             download_name=f"plagiarism_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#         )
    
#     except Exception as e:
#         logger.error(f"❌ Error generating PDF: {str(e)}")
#         logger.error(traceback.format_exc())
#         return jsonify({"error": f"PDF generation error: {str(e)}"}), 500


# @app.errorhandler(413)
# def request_entity_too_large(error):
#     logger.warning("❌ File size exceeds limit")
#     return jsonify({"error": "File size too large. Maximum allowed: 16MB"}), 413


# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({
#         "error": "Endpoint not found",
#         "available_endpoints": [
#             "GET /",
#             "GET /config_status",
#             "POST /check",
#             "POST /check_internet",
#             "POST /generate_pdf"
#         ]
#     }), 404


# @app.errorhandler(500)
# def internal_error(error):
#     logger.error(f"❌ Internal error: {str(error)}")
#     return jsonify({"error": "Internal server error"}), 500


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
    
#     print("\n" + "=" * 70)
#     print("🚀 ENHANCED PLAGIARISM CHECKER API - STARTING")
#     print("=" * 70)
#     print(f"📍 Server: http://0.0.0.0:{port}")
#     print(f"🤖 Model: {'✓ Loaded' if model else '✗ Not loaded'}")
#     print(f"🌐 Google API: {'✓ Configured' if validate_credentials() else '✗ Not configured'}")
#     print(f"📂 File Support: TXT, PDF, DOCX")
#     print(f"📄 PDF Generation: ✓ Enabled")
    
#     print("\n📡 ENDPOINTS:")
#     print(f"   GET  http://localhost:{port}/                 - Health check")
#     print(f"   GET  http://localhost:{port}/config_status   - API configuration")
#     print(f"   POST http://localhost:{port}/check           - Compare documents (STEP 3: Multi-format)")
#     print(f"   POST http://localhost:{port}/check_internet - Internet plagiarism search")
#     print(f"   POST http://localhost:{port}/generate_pdf   - Generate PDF report (NEW)")
#     print("=" * 70 + "\n")
    
#     app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)










































print("==== APP ENHANCED.PY BOOTSTRAP OK ====")
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from utils import calculate_cosine_similarity, highlight_matching_text
from google_search_integration import compare_with_internet_sources, validate_credentials
from file_handler import extract_text_from_file, validate_file, get_file_type_from_name
from professional_pdf_generator import generate_professional_plagiarism_report
import joblib
import os
import logging
import traceback
import io
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

MODEL_PATH = "plagiarism_model.pkl"
model = None

def load_model():
    global model
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            logger.info("✅ Model loaded successfully")
        else:
            logger.warning("⚠️ Model file not found")
    except Exception as e:
        logger.error(f"❌ Error loading model: {str(e)}")

load_model()

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "Professional Plagiarism Checker API",
        "version": "3.0.0 - Professional Edition",
        "endpoints": {
            "GET /": "Health check",
            "POST /check": "Compare documents (multi-format)",
            "POST /check_internet": "Internet plagiarism search",
            "POST /generate_professional_pdf": "Generate professional report",
            "GET /config_status": "API status"
        }
    }), 200

@app.route("/config_status", methods=["GET"])
def config_status():
    is_configured = validate_credentials()
    return jsonify({
        "status": "configured" if is_configured else "not_configured",
        "google_api_configured": is_configured,
        "model_loaded": model is not None
    }), 200

@app.route("/check", methods=["POST"])
def check_plagiarism():
    logger.info("📋 LOCAL DOCUMENT COMPARISON")
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500
        
        if 'original' not in request.files or 'submission' not in request.files:
            return jsonify({"error": "Both files required"}), 400
        
        file1 = request.files['original']
        file2 = request.files['submission']
        
        try:
            validate_file(file1, file1.filename)
            validate_file(file2, file2.filename)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        try:
            text1, type1 = extract_text_from_file(file1, file1.filename)
            text2, type2 = extract_text_from_file(file2, file2.filename)
        except Exception as e:
            return jsonify({"error": f"File processing error: {str(e)}"}), 400
        
        if not text1.strip() or not text2.strip():
            return jsonify({"error": "Files cannot be empty"}), 400
        
        similarity = calculate_cosine_similarity(text1, text2)
        prediction = model.predict([[similarity]])[0]
        probability = model.predict_proba([[similarity]])[0][1]
        
        highlighted1, highlighted2 = highlight_matching_text(text1, text2)
        
        response = {
            "similarity_score": round(float(similarity), 4),
            "plagiarized": bool(prediction),
            "probability": round(float(probability), 4),
            "highlighted_original": highlighted1,
            "highlighted_submission": highlighted2,
            "original_filename": file1.filename,
            "original_type": type1,
            "submission_filename": file2.filename,
            "submission_type": type2
        }
        
        logger.info(f"✅ Comparison complete: {similarity:.4f}")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route("/check_internet", methods=["POST"])
def check_internet_plagiarism():
    logger.info("🌐 INTERNET PLAGIARISM CHECK")
    try:
        if not validate_credentials():
            return jsonify({"error": "Google API not configured", "status": "api_not_configured"}), 500
        
        if 'submission' not in request.files:
            return jsonify({"error": "Missing submission file"}), 400
        
        submission_file = request.files['submission']
        
        try:
            validate_file(submission_file, submission_file.filename)
            submission_text, file_type = extract_text_from_file(submission_file, submission_file.filename)
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
        if not submission_text.strip():
            return jsonify({"error": "File cannot be empty"}), 400
        
        result = compare_with_internet_sources(submission_text)
        
        if result.get('status') == 'error':
            return jsonify(result), 500
        
        result['submission_filename'] = submission_file.filename
        result['submission_type'] = file_type
        result['submission_size'] = len(submission_text)
        
        logger.info("✅ Internet check complete")
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e), "status": "processing_error"}), 500

@app.route("/generate_professional_pdf", methods=["POST"])
def generate_professional_pdf():
    logger.info("📄 PROFESSIONAL PDF GENERATION")
    try:
        request_data = request.get_json()
        if not request_data or 'data' not in request_data:
            return jsonify({"error": "Missing analysis data"}), 400
        
        data = request_data['data']
        mode = request_data.get('mode', 'local')
        
        pdf_content = generate_professional_plagiarism_report(data, mode)
        
        logger.info("✅ Professional PDF generated")
        
        return send_file(
            io.BytesIO(pdf_content),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"plagiarism_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
    except Exception as e:
        logger.error(f"❌ PDF generation error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": f"PDF generation error: {str(e)}"}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large (max 16MB)"}), 413

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"❌ Internal error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    
    print("\n" + "=" * 80)
    print("🚀 PROFESSIONAL PLAGIARISM CHECKER API - FINAL VERSION")
    print("=" * 80)
    print(f"📍 Server: http://0.0.0.0:{port}")
    print(f"🤖 Model: {'✓ Loaded' if model else '✗ Not loaded'}")
    print(f"🌐 Google API: {'✓ Configured' if validate_credentials() else '✗ Not configured'}")
    print(f"📂 File Support: TXT, PDF, DOCX (up to 16MB)")
    print(f"📄 Professional PDF: ✓ Enabled (Color-coded, Academic Format)\n")
    print("📡 ENDPOINTS:")
    print(f"   POST {port}/check                     - Compare documents")
    print(f"   POST {port}/check_internet           - Internet search")
    print(f"   POST {port}/generate_professional_pdf - Professional report ⭐")
    print("=" * 80 + "\n")
    
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
