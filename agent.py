from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from tavily import TavilyClient
import config
from typing import TypedDict, Optional


#flagging
try:
    tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)
except Exception as e:
    print(f"Error initializing Tavily client: {e}")
    tavily_client = None
    
class TravelState(TypedDict):
    destination : Optional[str]
    dates : Optional[str]
    duration : Optional[int]
    budget : Optional[float]
    nationality : Optional[str]
    interests : Optional[str]
    current_question : int
    search_results : dict
    itinerary : Optional[str]
    
from prompts import (
    MAIN_PROMPT
    )
    
class TravelAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                                          temperature=0.7, 
                                          google_api_key=config.GEMINI_API_KEY,
                                          max_output_tokens=512)
        
    def search_info(self, state: TravelState):
        results = {}
        destination = state['destination']
        dates = state['dates']
        nationality = state['nationality']
        
        if destination and nationality and tavily_client:
            try:
                #visa requirements
                visa_query = f"Visa requirements for a {nationality} citizen traveling to {destination}."
                results['visa'] = tavily_client.search(visa_query, max_results=2)
                #weather 
                month = dates.strip().split()[0] if dates and dates.strip() else "March"
                weather_query = f"weather {destination} {month}"
                results['weather'] = tavily_client.search(weather_query, max_results=2)
                #Restaurants
                restaurant_query = f"Top restaurants in {destination}."
                results['restaurants'] = tavily_client.search(restaurant_query, max_results=2)
                #Travel advisories
                advisory_query = f"Current travel advisories for {destination}. for {nationality} citizens."
                results['advisories'] = tavily_client.search(advisory_query, max_results=2)
            except Exception as e:
                print(f"Error during Tavily search: {e}")
                
        state['search_results'] = results
        return state
    
    def generate_itinerary(self, state: TravelState):
        search_context = ""
        for category, data in state['search_results'].items():
            if data and 'results' in data:
                search_context += f"\n{category.upper()}:\n"
                for result in data['results']:
                    search_context += f"- {result['title']}: {result['content']}\n"
          
        prompt = MAIN_PROMPT.format(state['destination'],
                                    state['dates'],
                                    state['duration'],
                                    state['budget'],
                                    state['nationality'],
                                    state['interests'],
                                    search_context)         

        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        state['itinerary'] = response.content
        return state
    
    def plan_trip(self, answers: list):
        state = TravelState(
            destination=None,
            dates=None,
            duration=None,
            budget=None,
            nationality=None,
            interests=None,
            current_question=0,
            search_results={},
            itinerary=None
        )
        
        if len(answers) < 5:
            return "Error: Please answer all questions to generate itinerary."
            
        #parsing answers
        if len(answers)>=5:
            dest_date = answers[0].split(' in ')
            state['destination'] = dest_date[0].strip() if len(dest_date)>0 else answers[0]
            state['dates'] = dest_date[1].strip() if len(dest_date)>1 else "August 2025"
            
            try:
                state['duration'] = int(answers[1].split()[0])
            except (ValueError, IndexError):
                state['duration'] = 5
                
            try:
                state['budget'] = float(''.join(filter(str.isdigit, answers[2])))
            except (ValueError, IndexError):
                state['budget'] = 1000.0
                
            state['nationality'] = answers[3].strip()
            state['interests'] = answers[4].strip()
            
            state = self.search_info(state)
            state = self.generate_itinerary(state)
            
            return state['itinerary']
        
