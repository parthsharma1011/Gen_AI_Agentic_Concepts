MAIN_PROMPT = """
        Act like a senior travel and tour guide and provide a very professional travel itinerary:
        
        Destination: {0}
        Dates: {1}
        Duration: {2} 
        Budget: {3}
        Nationality: {4}
        Interests: {5}

        Research Info : {6}
        
        Create a markdown itinerary with:
        1. Visa requirements
        2. Budget breakdown
        3. Day-by-day activities (morning, afternoon, evening)
        4. Recommended restaurants
        5. Useful links to visit
        
        Make it a very practical and a very budget conscious itinerary.
        Make sure the details are accurate and up-to-date.
        Avoid generic suggestions and *DO NOT HALLUCINATE*
        Self-Critique your output for any mistakes before finalizing.

        Itinerary:
        """