# AI Travel Planner

A Streamlit-based travel planning application that generates personalized itineraries using AI.

## Features
- Interactive questionnaire for travel preferences
- AI-powered itinerary generation
- Real-time travel information search
- Downloadable markdown itineraries

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` file with your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Requirements
- Python 3.8+
- Streamlit
- Google Gemini API key
- Tavily API key