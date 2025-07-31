#!/usr/bin/env python3
"""
Coaching RAG Agent Launcher

A simple launcher script for the coaching voice agent.
This script provides an easy way to start the voice server.
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Launch the voice server."""
    print("🎤 Starting Coaching RAG Voice Agent...")
    print("=" * 50)
    
    # Get the directory of this script
    script_dir = Path(__file__).parent
    voice_server_path = script_dir / "voice_server.py"
    
    if not voice_server_path.exists():
        print("❌ Error: voice_server.py not found!")
        sys.exit(1)
    
    try:
        # Run the voice server
        subprocess.run([sys.executable, str(voice_server_path)], check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down voice agent...")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running voice server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
