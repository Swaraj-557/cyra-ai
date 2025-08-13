"""
Cyra Advanced - Troubleshooting Guide
=====================================

🔧 COMMON ISSUES AND SOLUTIONS:

1. JAVASCRIPT ERRORS
   Error: "Uncaught ReferenceError: function is not defined"
   Solution: 
   - Check for syntax errors in regex patterns
   - Ensure all JavaScript functions are properly defined
   - Clear browser cache and reload

2. PORT CONFLICTS
   Error: "[Errno 10048] only one usage of each socket address is permitted"
   Solutions:
   - Kill existing Python processes: taskkill /f /im python.exe
   - Use a different port in the uvicorn.run() call
   - Check for other applications using the same port

3. FAVICON NOT FOUND
   Error: "Failed to load resource: favicon.ico:1 404 (Not Found)"
   Solution: This is cosmetic - create a favicon.ico file or ignore

4. VOICE FEATURES NOT WORKING
   Issues: Microphone not working, speech recognition fails
   Solutions:
   - Allow microphone permissions in browser
   - Use Chrome/Edge for best compatibility
   - Check browser support for Web Speech API
   - Ensure HTTPS for production (required for microphone access)

5. AZURE OPENAI CONNECTION ISSUES
   Error: "API key not found" or connection failures
   Solutions:
   - Check .env file has correct AZURE_OPENAI_API_KEY
   - Verify AZURE_OPENAI_ENDPOINT is correct
   - Ensure Azure subscription is active
   - Check deployment name matches AZURE_OPENAI_DEPLOYMENT

6. WEBSOCKET DISCONNECTIONS
   Issue: Real-time chat not working
   Solutions:
   - Check network connectivity
   - Refresh the page to reconnect
   - Ensure no firewall blocking WebSocket connections

🚀 QUICK FIXES:

1. RESTART APPLICATION:
   taskkill /f /im python.exe
   python cyra_advanced.py

2. CLEAR BROWSER CACHE:
   - Ctrl+Shift+R (hard refresh)
   - Or F12 -> Application -> Storage -> Clear site data

3. CHECK BROWSER CONSOLE:
   - F12 -> Console tab
   - Look for red error messages
   - Common issues show there first

4. VERIFY DEPENDENCIES:
   pip install -r requirements.txt

5. TEST API ENDPOINTS:
   - Health: http://localhost:8003/health
   - Docs: http://localhost:8003/docs

📱 BROWSER COMPATIBILITY:

✅ FULLY SUPPORTED:
- Chrome 90+
- Edge 90+
- Firefox 85+
- Safari 14+

⚠️  PARTIAL SUPPORT:
- Older browsers may have limited voice features
- Internet Explorer not supported

🎤 VOICE FEATURES REQUIREMENTS:

1. HTTPS (for production)
2. Microphone permissions
3. Modern browser with Web Speech API
4. Good internet connection for best results

💡 PERFORMANCE TIPS:

1. Use modern browsers for best performance
2. Close unnecessary tabs to free memory
3. Ensure stable internet connection
4. Allow microphone permissions on first use
5. Use headphones to prevent audio feedback

🔐 SECURITY CONSIDERATIONS:

1. Never expose API keys in client-side code
2. Use environment variables for sensitive data
3. Enable HTTPS for production deployment
4. Regularly update dependencies
5. Monitor Azure usage for cost control

🏗️ DEPLOYMENT NOTES:

For production deployment:
1. Use HTTPS (required for microphone access)
2. Set proper CORS headers
3. Use environment variables for secrets
4. Configure proper logging
5. Set up health monitoring
6. Use a reverse proxy (nginx/apache)

📞 NEED HELP?

If you encounter issues not covered here:
1. Check the browser console (F12)
2. Look at server logs for errors
3. Verify all environment variables are set
4. Test with a different browser
5. Restart the application

Remember: Most issues are resolved by restarting the application and clearing browser cache!
"""
