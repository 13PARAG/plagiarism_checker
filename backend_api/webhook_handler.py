"""
 webhook_handler.py
 Advanced webhook handler for production deployment
 Place in: backend_api/webhook_handler.py
 """
 from flask import Flask, request, jsonify
 import os
 import logging
 from telegram import Update
 from telegram.ext import Application
 import asyncio
 logger = logging.getLogger(__name__)
 # Initialize Telegram Application<a></a>
 TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
 WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET_TOKEN')
 application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
 async def process_update(update_data):
    """Process incoming Telegram update"""
    try:
        update = Update.de_json(update_data, application.bot)
        await application.process_update(update)
    except Exception as e:
        logger.error(f"Update processing error: {e}")
 @app.route('/telegram-webhook', methods=['POST'])
 def telegram_webhook():
    """
    Webhook endpoint for Telegram
    Receives POST requests from Telegram servers
    """
    try:
        # Verify webhook secret token (security)
        token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
        if token != WEBHOOK_SECRET:
            logger.warning("Invalid webhook token")
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Get update data
        update_data = request.get_json()
        
        if not update_data:
            return jsonify({'error': 'No data'}), 400
        
        # Process update asynchronously
        asyncio.run(process_update(update_data))
        
        return jsonify({'status': 'ok'}), 200
    
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({'error': 'Internal error'}), 500
 def set_webhook(webhook_url):
    """
    Set webhook URL for Telegram bot
    Call this once during deployment
    """
    import requests

    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    data = {
        'url': webhook_url,
        'secret_token': WEBHOOK_SECRET,
        'allowed_updates': ['message', 'callback_query']
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        logger.info("Webhook set successfully")
        return True
    else:
        logger.error(f"Webhook setup failed: {response.text}")
        return False