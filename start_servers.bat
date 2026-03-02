@echo off
echo Starting Blissful Abodes AI Hotel Platform...

:: Start the Flask backend on port 5000
echo Starting Backend Server (Flask)...
start "Flask Server" cmd /c "set PYTHONUTF8=1 && python app.py"

:: Delay for 2 seconds to let Flask start
timeout /t 2 /nobreak >nul

:: Start the Streamlit AI Agent on port 8501
echo Starting AI Chatbot Agent (Streamlit)...
start "AI Agent" cmd /c "streamlit run agent.py --server.port=8501 --server.headless=true"

echo.
echo Both servers have been started successfully!
echo The AI Hotel Platform is available at http://127.0.0.1:5000
echo The AI Agent is running silently in the background on port 8501.
echo.
pause
