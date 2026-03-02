# 🏨 Smart Hotel Reservation Agent

Welcome to the **Smart Hotel Reservation Agent** – an AI-powered web application that helps users search for the best hotel deals across multiple booking sites and assists in completing hotel bookings conversationally. Built with Streamlit, powered by Gemini LLM via Google ADK, this project delivers an intelligent and user-friendly hotel booking experience.

## ✨ Features

- **🔍 Hotel Search Assistant**  
  Uses Google Search and AI to retrieve up to 15 hotel options based on user queries.
- **💰 Price Comparison Engine**  
  Simulates pricing from multiple platforms like Booking.com, Agoda, Trivago, etc., and presents the best deals.
- **🛏️ Conversational Booking Flow**  
  Interactive assistant to help users book a hotel via steps like selecting room type, choosing dates, entering guest info, and final confirmation.
- **📊 Summary View**  
  Displays a concise summary of search results including price ranges and total hotels found.
- **✅ Real-Time Booking Status Tracking**  
  Sidebar panel shows the current step and lets users cancel bookings if needed.

## 🚀 Technologies Used

- **Python 3.10+**: Core programming language
- **Streamlit**: Frontend web interface
- **Google ADK**: LLM-based agents + tool integration
- **Gemini-2.0-Flash**: Language model used for search and conversation
- **LiteLLM**: Lightweight LLM model wrapper
- **Pydantic**: Data validation for structured responses

## 📦 Installation

Make sure you have Python 3.10+ installed.

### Clone the Repository

```bash
git clone https://github.com/your-username/hotel-agent.git
cd hotel-agent
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Google API Key

Replace in the code or use environment variable:

```bash
export GOOGLE_API_KEY="your_google_api_key_here"
```

## 📂 File Structure

```text
.
├── hotel_agent_app.py # Main Streamlit application
├── requirements.txt   # Project dependencies
└── README.md          # This file
```

## 🧠 Agent Architecture

The app utilizes two custom LLM Agents:

1. **🔍 hotel_search_agent**  
   Searches for hotels via `google_search` tool. Returns structured hotel data in JSON format. Enriches hotel data with mock price comparison from 8 booking sites.
2. **📘 booking_agent**  
   Conversational flow for hotel booking. Handles room type selection, dates, guest info, and confirmation. Maintains multi-step booking state in memory.

## 💬 Sample Commands

Try the following prompts:

- `Find hotels in Goa under 10000`
- `Book The Leela Palace`
- `2 guests for 2 nights`
- `confirm booking`

## 🧪 Demo Walkthrough

1. Enter prompt like "Find hotels in Mumbai"
2. View hotel cards with best prices from multiple sites
3. Click "📋 Book" to begin booking
4. Select room type, dates, number of guests
5. Confirm your booking and receive booking ID
