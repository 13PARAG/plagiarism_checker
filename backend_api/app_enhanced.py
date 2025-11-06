# print("==== APP ENHANCED.PY BOOTSTRAP OK ====")
# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# from utils import calculate_cosine_similarity, highlight_matching_text
# from google_search_integration import compare_with_internet_sources, validate_credentials
# from file_handler import extract_text_from_file, validate_file, get_file_type_from_name
# from professional_pdf_generator import generate_professional_plagiarism_report
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
#         "version": "3.0.0 - Professional Edition",
#         "endpoints": {
#             "GET /": "Health check",
#             "POST /check": "Compare documents (multi-format)",
#             "POST /check_internet": "Internet plagiarism search",
#             "POST /generate_professional_pdf": "Generate professional report",
#             "GET /config_status": "API status"
#         }
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
#     logger.info("🌐 INTERNET PLAGIARISM CHECK")
#     try:
#         if not validate_credentials():
#             return jsonify({"error": "Google API not configured", "status": "api_not_configured"}), 500
        
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
        
#         result['submission_filename'] = submission_file.filename
#         result['submission_type'] = file_type
#         result['submission_size'] = len(submission_text)
        
#         logger.info("✅ Internet check complete")
#         return jsonify(result), 200
    
#     except Exception as e:
#         logger.error(f"❌ Error: {str(e)}")
#         return jsonify({"error": str(e), "status": "processing_error"}), 500

# @app.route("/generate_professional_pdf", methods=["POST"])
# def generate_professional_pdf():
#     logger.info("📄 PROFESSIONAL PDF GENERATION")
#     try:
#         request_data = request.get_json()
#         if not request_data or 'data' not in request_data:
#             return jsonify({"error": "Missing analysis data"}), 400
        
#         data = request_data['data']
#         mode = request_data.get('mode', 'local')
        
#         pdf_content = generate_professional_plagiarism_report(data, mode)
        
#         logger.info("✅ Professional PDF generated")
        
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
    
#     print("\n" + "=" * 80)
#     print("🚀 PROFESSIONAL PLAGIARISM CHECKER API - FINAL VERSION")
#     print("=" * 80)
#     print(f"📍 Server: http://0.0.0.0:{port}")
#     print(f"🤖 Model: {'✓ Loaded' if model else '✗ Not loaded'}")
#     print(f"🌐 Google API: {'✓ Configured' if validate_credentials() else '✗ Not configured'}")
#     print(f"📂 File Support: TXT, PDF, DOCX (up to 16MB)")
#     print(f"📄 Professional PDF: ✓ Enabled (Color-coded, Academic Format)\n")
#     print("📡 ENDPOINTS:")
#     print(f"   POST {port}/check                     - Compare documents")
#     print(f"   POST {port}/check_internet           - Internet search")
#     print(f"   POST {port}/generate_professional_pdf - Professional report ⭐")
#     print("=" * 80 + "\n")
    
#     app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)







































print("==== APP ENHANCED.PY BOOTSTRAP OK ====")

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from utils import calculate_cosine_similarity, highlight_matching_text, check_plagiarism
from google_search_integration import compare_with_internet_sources, validate_credentials
from file_handler import extract_text_from_file, validate_file, get_file_type_from_name
from professional_pdf_generator import generate_professional_plagiarism_report
import requests
import joblib
import os
import logging
import traceback
import io
import tempfile
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB upload limit

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


@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json(force=True)
    if not data:
        return 'No data', 400

    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    send_url = f"https://api.telegram.org/bot{token}/sendMessage"
    chat_id = None
    reply = None

    if 'message' in data:
        chat_id = data['message']['chat']['id']

        # Document upload (file)
        if 'document' in data['message']:
            doc = data['message']['document']
            file_id = doc['file_id']
            resp = requests.get(f"https://api.telegram.org/bot{token}/getFile?file_id={file_id}")
            file_path = resp.json()['result']['file_path']
            file_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
            file_bytes = requests.get(file_url).content
            temp_ext = os.path.splitext(doc['file_name'])[1].lower()
            if temp_ext not in ['.txt', '.pdf', '.docx']:
                reply = "❌ Unsupported file format. Use TXT, PDF, or DOCX."
            elif len(file_bytes) > 16 * 1024 * 1024:
                reply = "❌ File too large (max 16MB)."
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=temp_ext) as temp_file:
                    temp_file.write(file_bytes)
                    temp_path = temp_file.name
                with open(temp_path, "rb") as f:
                    text, _ = extract_text_from_file(f, doc['file_name'])
                os.unlink(temp_path)
                # Support internet check for documents if caption says /check_internet
                if 'caption' in data['message'] and data['message']['caption'].strip().lower().startswith('/check_internet'):
                    result = compare_with_internet_sources(text)
                    if result.get("status") == "error":
                        reply = f"❌ Error: {result.get('error', 'Unknown')}"
                    else:
                        reply = (
                            f"🌐 Internet Similarity: {result.get('similarity_score')}%\n"
                            f"Top Match: {result.get('top_match_title', '')}\n"
                            f"Match URL: {result.get('top_match_url', '')}\n"
                            f"Status: {result.get('status')}"
                        )
                else:
                    similarity_score = check_plagiarism(text)
                    reply = (
                        f"🔍 Similarity: {similarity_score}%\n"
                        "Status: Complete\n"
                        "Document analyzed successfully"
                    )

        # Plain text message
        elif 'text' in data['message']:
            user_text = data['message']['text']
            if user_text.strip().lower() == '/start':
                reply = (
                    "👋 Welcome to Professional Plagiarism Checker Bot!\n"
                    "Send me a document (TXT/PDF/DOCX) or paste text to check for plagiarism."
                )
            elif len(user_text) < 50:
                reply = "⚠️ Text too short (minimum 50 characters required)."
            elif user_text.strip().lower().startswith('/check_internet'):
                text_to_search = user_text.replace('/check_internet', '').strip()
                if not text_to_search:
                    reply = "❗ Please provide text after /check_internet"
                else:
                    result = compare_with_internet_sources(text_to_search)
                    if result.get("status") == "error":
                        reply = f"❌ Error: {result.get('error', 'Unknown')}"
                    else:
                        reply = (
                            f"🌐 Internet Similarity: {result.get('similarity_score')}%\n"
                            f"Top Match: {result.get('top_match_title', '')}\n"
                            f"Match URL: {result.get('top_match_url', '')}\n"
                            f"Status: {result.get('status')}"
                        )
            else:
                similarity_score = check_plagiarism(user_text)
                reply = (
                    f"🔍 Similarity: {similarity_score}%\n"
                    "Status: Complete\n"
                    "Text analyzed successfully"
                )

    if chat_id and reply:
        requests.post(send_url, json={
            "chat_id": chat_id,
            "text": reply
        })

    return 'OK', 200


@app.route("/api/status", methods=["GET"])
def api_status():
    try:
        import time
        start_time = time.time()
        google_api_status = "Configured" if (
            os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_CSE_ID")
        ) else "Not Configured"
        response_time = int((time.time() - start_time) * 1000)
        return (
            jsonify(
                {
                    "status": "OK",
                    "timestamp": time.time(),
                    "google_api": google_api_status,
                    "response_time": response_time,
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return jsonify({"status": "Error", "message": str(e)}), 500


@app.route("/api/check-document", methods=["POST"])
def check_document():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400
        file = request.files["file"]
        threshold = int(request.form.get("threshold", 50))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as temp:
            file.save(temp.name)
            temp_path = temp.name
        with open(temp_path, "rb") as f:
            text, _ = extract_text_from_file(f, file.filename)
        similarity_score = check_plagiarism(text)  # Wrapper in utils.py
        result = {
            "similarity_score": similarity_score,
            "status": "Complete",
            "analysis": "Document analyzed successfully",
            "threshold": threshold,
            "filename": file.filename,
        }
        os.unlink(temp_path)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Document check error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/check-text", methods=["POST"])
def check_text():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "No text provided"}), 400
        text = data["text"]
        threshold = data.get("threshold", 50)
        similarity_score = check_plagiarism(text)  # Wrapper in utils.py
        result = {
            "similarity_score": similarity_score,
            "status": "Complete",
            "analysis": "Text analyzed successfully",
            "threshold": threshold,
        }
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Text check error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return (
        jsonify(
            {
                "status": "running",
                "message": "Professional Plagiarism Checker API",
                "version": "3.0.0 - Professional Edition",
                "endpoints": {
                    "GET /": "Health check",
                    "POST /check": "Compare documents (multi-format)",
                    "POST /check_internet": "Internet plagiarism search",
                    "POST /generate_professional_pdf": "Generate professional report",
                    "GET /config_status": "API status",
                },
            }
        ),
        200,
    )


@app.route("/config_status", methods=["GET"])
def config_status():
    is_configured = validate_credentials()
    return (
        jsonify(
            {
                "status": "configured" if is_configured else "not_configured",
                "google_api_configured": is_configured,
                "model_loaded": model is not None,
            }
        ),
        200,
    )


@app.route("/check", methods=["POST"])
def check_plagiarism_endpoint():
    logger.info("📋 LOCAL DOCUMENT COMPARISON")
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500
        if "original" not in request.files or "submission" not in request.files:
            return jsonify({"error": "Both files required"}), 400
        file1 = request.files["original"]
        file2 = request.files["submission"]
        validate_file(file1, file1.filename)
        validate_file(file2, file2.filename)
        text1, type1 = extract_text_from_file(file1, file1.filename)
        text2, type2 = extract_text_from_file(file2, file2.filename)
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
            "submission_type": type2,
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
            return jsonify(
                {"error": "Google API not configured", "status": "api_not_configured"}
            ), 500
        if "submission" not in request.files:
            return jsonify({"error": "Missing submission file"}), 400
        submission_file = request.files["submission"]
        validate_file(submission_file, submission_file.filename)
        submission_text, file_type = extract_text_from_file(
            submission_file, submission_file.filename
        )
        if not submission_text.strip():
            return jsonify({"error": "File cannot be empty"}), 400
        result = compare_with_internet_sources(submission_text)
        if result.get("status") == "error":
            return jsonify(result), 500
        result["submission_filename"] = submission_file.filename
        result["submission_type"] = file_type
        result["submission_size"] = len(submission_text)
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
        if not request_data or "data" not in request_data:
            return jsonify({"error": "Missing analysis data"}), 400
        data = request_data["data"]
        mode = request_data.get("mode", "local")
        pdf_content = generate_professional_plagiarism_report(data, mode)
        logger.info("✅ Professional PDF generated")
        return send_file(
            io.BytesIO(pdf_content),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"plagiarism_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
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
    print(
        f"🌐 Google API: {'✓ Configured' if validate_credentials() else '✗ Not configured'}"
    )
    print(f"📂 File Support: TXT, PDF, DOCX (up to 16MB)")
    print("📄 Professional PDF: ✓ Enabled (Color-coded, Academic Format)\n")
    print("📡 ENDPOINTS:")
    print(f"   POST {port}/check             - Compare documents")
    print(f"   POST {port}/check_internet      - Internet search")
    print(f"   POST {port}/generate_professional_pdf - Professional report ⭐")
    print("=" * 80 + "\n")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
