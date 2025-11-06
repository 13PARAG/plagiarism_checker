 """
 telegram_bot.py
 Place this file in: backend_api/telegram_bot.py
 """
 import os
 import logging
 import requests
 import tempfile
 from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
 from telegram.ext import (
 Application,
 CommandHandler,
 MessageHandler,
 CallbackQueryHandler,
 filters,
 ContextTypes
 )
 from dotenv import load_dotenv
 load_dotenv()
 # Configuration<a></a>
 TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
 BACKEND_API_URL = os.getenv('BACKEND_API_URL', 'http://localhost:5000')
 ALLOWED_FORMATS = ['.txt', '.pdf', '.docx']
 MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
 # Logging<a></a>
 logging.basicConfig(
 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 level=logging.INFO
 )
 logger = logging.getLogger(__name__)
 # User session storage (consider Redis for production)<a></a>
 user_sessions = {}
 class PlagiarismBot:
 """Telegram bot for plagiarism checking"""
 def __init__(self):
 self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
 self._register_handlers()
 def _register_handlers(self):
 """Register all command and message handlers"""
 # Command handlers
 self.application.add_handler(CommandHandler("start", self.start_command))
 self.application.add_handler(CommandHandler("help", self.help_command))
 self.application.add_handler(CommandHandler("check", self.check_command))
 self.application.add_handler(CommandHandler("status", self.status_command))
 self.application.add_handler(CommandHandler("cancel", self.cancel_command))
 # Message handlers
        self.application.add_handler(
            MessageHandler(filters.Document.ALL, self.handle_document)
        )
        self.application.add_handler(
            MessageHandler(filters.TEXT &amp; ~filters.COMMAND, self.handle_text)
        )
        
        # Callback query handler for inline buttons
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_message = (
            f" Hello {user.first_name}!\n\n"
            "Welcome to **Professional Plagiarism Checker Bot**\n\n"
            " **What I can do:**\n"
            "• Check documents for plagiarism (TXT, PDF, DOCX)\n"
            "• Analyze text snippets\n"
            "• Compare two documents\n"
            "• Provide detailed similarity reports\n\n"
            " **How to use:**\n"
            "1. Upload a document or send text\n"
            "2. Choose analysis type\n"
            "3. Receive plagiarism report\n\n"
            "Type /help for detailed instructions\n"
            "Type /check to start plagiarism check"
        )
        
        keyboard = [
            [InlineKeyboardButton(" Check Document", callback_data='check_doc')],
            [InlineKeyboardButton(" Check Text", callback_data='check_text')],
            [InlineKeyboardButton("ℹ  Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = (
            " **How to Use the Bot**\n\n"
            "**Commands:**\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/check - Begin plagiarism check\n"
            "/status - Check bot and API status\n"
            "/cancel - Cancel current operation\n\n"
            "**Checking Documents:**\n"
            "1. Upload your document (TXT, PDF, or DOCX)\n"
            "2. Bot will analyze it automatically\n"
            "3. Receive similarity score and report\n\n"
            "**Checking Text:**\n"
            "1. Type or paste your text\n"
            "2. Bot will analyze it\n"
            "3. Get instant results\n\n"
            "**Supported Formats:**\n"
            "• TXT (Plain text)\n"
            "• PDF (Portable Document Format)\n"
            "• DOCX (Microsoft Word)\n\n"
            "**File Size Limit:** 20MB\n\n"
            "Need assistance? Contact support."
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def check_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /check command"""
        keyboard = [
            [InlineKeyboardButton(" Upload Document", callback_data='upload_doc')],
            [InlineKeyboardButton("✍  Paste Text", callback_data='paste_text')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Choose how you want to check for plagiarism:",
            reply_markup=reply_markup
        )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check backend API status"""
        await update.message.reply_text(" Checking system status...")
        
        try:
            response = requests.get(
                f"{BACKEND_API_URL}/api/status",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                status_message = (
                    "✅ **System Status: Online**\n\n"
                    f"Backend API: {data.get('status', 'OK')}\n"
                    f"Google API: {data.get('google_api', 'Configured')}\n"
                    f"Response Time: {data.get('response_time', 'N/A')}ms"
                )
            else:
                status_message = "⚠  Backend API is experiencing issues"
        except Exception as e:
            logger.error(f"Status check failed: {e}")
            status_message = "❌ Could not connect to backend API"
        
        await update.message.reply_text(status_message, parse_mode='Markdown')
    
    async def cancel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel current operation"""
        user_id = update.effective_user.id
        if user_id in user_sessions:
            del user_sessions[user_id]
        
        await update.message.reply_text(
            "Operation cancelled. Type /start to begin again."
        )
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document uploads"""
        document = update.message.document
        user_id = update.effective_user.id
        
        # Validate file format
        file_name = document.file_name
        file_ext = os.path.splitext(file_name)[1].lower()
        
        if file_ext not in ALLOWED_FORMATS:
            await update.message.reply_text(
                f"❌ Unsupported file format: {file_ext}\n"
                f"Supported formats: {', '.join(ALLOWED_FORMATS)}"
            )
            return
        
        # Validate file size
        if document.file_size &gt; MAX_FILE_SIZE:
            await update.message.reply_text(
                f"❌ File too large ({document.file_size / 1024 / 1024:.2f}MB)\n"
                f"Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB"
            )
            return
        
        # Download file
        await update.message.reply_text(
            f" Downloading {file_name}...\n"
            "Please wait, this may take a moment."
        )
        
        try:
            file = await context.bot.get_file(document.file_id)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_ext
            ) as temp_file:
                await file.download_to_drive(temp_file.name)
                temp_file_path = temp_file.name
            
            # Process plagiarism check
            await self.process_plagiarism_check(
                update,
                temp_file_path,
                file_name
            )
            
            # Cleanup
            os.unlink(temp_file_path)
            
        except Exception as e:
            logger.error(f"Document handling error: {e}")
            await update.message.reply_text(
                "❌ Error processing document. Please try again."
            )
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        text = update.message.text
        user_id = update.effective_user.id
        
        # Validate text length
        if len(text) &lt; 50:
            await update.message.reply_text(
                "⚠  Text too short (minimum 50 characters)\n"
                "Please provide more content for accurate analysis."
            )
            return
        
        if len(text) &gt; 50000:
            await update.message.reply_text(
                "⚠  Text too long (maximum 50,000 characters)\n"
                "Please upload as a document instead."
            )
            return
        
        await update.message.reply_text(
            " Analyzing your text...\n"
            "Please wait while I check for plagiarism."
        )
        
        try:
            # Process text plagiarism check
            await self.process_text_check(update, text)
        except Exception as e:
            logger.error(f"Text handling error: {e}")
            await update.message.reply_text(
                "❌ Error processing text. Please try again."
            )
    
    async def process_plagiarism_check(
        self,
        update: Update,
        file_path: str,
        file_name: str
    ):
        """Send file to backend API for plagiarism check"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_name, f)}
                data = {'threshold': 50}  # Default threshold
                
                response = requests.post(
                    f"{BACKEND_API_URL}/api/check-document",
                    files=files,
                    data=data,
                    timeout=60
                )
            
            if response.status_code == 200:
                result = response.json()
                await self.send_results(update, result)
            else:
                await update.message.reply_text(
                    f"❌ API Error: {response.status_code}\n"
                    "Please try again later."
                )
        
        except requests.exceptions.Timeout:
            await update.message.reply_text(
                "  Request timed out. Document may be too large."
            )
        except Exception as e:
            logger.error(f"Plagiarism check error: {e}")
            await update.message.reply_text(
                "❌ Error during plagiarism check. Please try again."
            )
    
    async def process_text_check(self, update: Update, text: str):
        """Send text to backend API for plagiarism check"""
        try:
            data = {'text': text, 'threshold': 50}
            
            response = requests.post(
                f"{BACKEND_API_URL}/api/check-text",
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                await self.send_results(update, result)
            else:
                await update.message.reply_text(
                    f"❌ API Error: {response.status_code}"
                )
        
        except Exception as e:
            logger.error(f"Text check error: {e}")
            await update.message.reply_text(
                "❌ Error during text check. Please try again."
            )
    
    async def send_results(self, update: Update, result: dict):
        """Format and send plagiarism check results"""
        similarity = result.get('similarity_score', 0)
        status = result.get('status', 'Unknown')
        
        # Determine status emoji
        if similarity &lt; 30:
            status_emoji = "✅"
            status_text = "PASS"
        elif similarity &lt; 50:
            status_emoji = "⚠ "
            status_text = "MODERATE"
        else:
            status_emoji = "❌"
            status_text = "HIGH SIMILARITY"
        
        # Format results message
        results_message = (
            f"{status_emoji} **Plagiarism Check Results**\n\n"
            f"**Similarity Score:** {similarity:.1f}%\n"
            f"**Status:** {status_text}\n"
            f"**Analysis:** {result.get('analysis', 'Complete')}\n\n"
        )
        
        # Add matched sources if available
        if 'sources' in result and result['sources']:
            results_message += "**Top Similar Sources:**\n"
            for idx, source in enumerate(result['sources'][:3], 1):
                results_message += f"{idx}. {source.get('url', 'N/A')} ({source.get('similarity', 0):.1f}%)
        
        await update.message.reply_text(
            results_message,
            parse_mode='Markdown'
        )
        
        # Offer report download if available
        if 'report_url' in result:
            keyboard = [[
                InlineKeyboardButton(
                    " Download Full Report",
                    url=result['report_url']
                )
            ]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                " Detailed report available:",
                reply_markup=reply_markup
            )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'check_doc':
            await query.message.reply_text(
                " **Upload Document**\n\n"
                "Send me a document file (TXT, PDF, or DOCX) "
                "and I'll check it for plagiarism."
            )
        elif query.data == 'check_text':
            await query.message.reply_text(
                "✍  **Paste Text**\n\n"
                "Send me the text you want to check "
                "(minimum 50 characters)."
            )
        elif query.data == 'help':
            await self.help_command(update, context)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred. Please try again or contact support."
            )
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
 if __name__ == '__main__':
    bot = PlagiarismBot()
    bot.run()