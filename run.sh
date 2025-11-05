#!/bin/bash
# Quick start script for KERN1 Invoice OCR Application

echo "🚀 Starting KERN1 Invoice OCR Application..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
fi

# Create directories
echo "Creating necessary directories..."
mkdir -p uploads exports

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✅ .env file created. Edit it to add your OpenAI API key (optional)"
fi

echo ""
echo "✅ Starting application..."
echo "🌐 The app will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run the app
streamlit run app.py
