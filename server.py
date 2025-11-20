#!/usr/bin/env python3
"""
Server untuk menjalankan aplikasi PeduliGiziBalita v3.3 - Flask Edition
"""

import os
import sys
import subprocess

def run_flask_app():
    """Run Flask application with proper configuration"""
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_DEBUG'] = 'False'
    os.environ['SECRET_KEY'] = 'peduligizi-balita-secret-key-2024'
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run Flask application
    try:
        from app import app
        print(f"🚀 Starting PeduliGiziBalita v3.3 on port {port}")
        print(f"📱 Access the application at: http://localhost:{port}")
        print("=" * 60)
        
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            threaded=True
        )
        
    except ImportError:
        print("❌ Error: Could not import Flask app")
        print("Make sure app.py is in the same directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_flask_app()