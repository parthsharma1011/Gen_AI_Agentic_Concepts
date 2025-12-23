import streamlit as st 
from agent import TravelAgent
import config


def main():
    st.set_page_config(page_title=" AI Travel Planner", page_icon=":airplane:")
    st.title("AI Travel Planner")
    
    agent = TravelAgent()
    
    if 'answers' not in st.session_state:
        st.session_state.answers = []
        st.session_state.current_q = 0 
        st.session_state.planning_done = False
        
    if not st.session_state.planning_done:
        current_q = st.session_state.current_q
        
        if current_q < len(config.QUESTIONS):
            st.subheader(f"Question {current_q + 1} of {len(config.QUESTIONS)}")
            st.write(config.QUESTIONS[current_q])
            
            if current_q == 0:
                col1, col2 = st.columns(2)
                with col1:
                    dest = st.text_input("Destination")
                with col2:
                    date = st.text_input("Date for eg(March 15, 2024)")
                answer = f"{dest} on {date}" if dest and date else ""
            
            elif current_q == 1:
                answer = str(st.number_input("Duration in days", min_value=1, value=5))
                
            elif current_q == 2:
                budget = st.number_input("Budget in USD", min_value=100, value=1000)
                answer = str(budget)
                
            elif current_q == 3:
                answer = st.text_input("Nationality")
                
            elif current_q == 4:

                col1, col2 = st.columns(2)
                with col1:
                    culture = st.checkbox("Cultural")
                    food = st.checkbox("Food")
                with col2:
                    nature = st.checkbox("Nature")
                    adventure = st.checkbox("Adventure")
                    
                custom_interests = st.text_input("type your own interest: eg: hiking, skiing, etc")
                
                selected = []
                if culture: selected.append('culture')
                if food: selected.append('food')
                if nature: selected.append('nature')
                if adventure: selected.append('adventure')
                
                if custom_interests: selected.append(custom_interests)
                
                answer = ", ".join(selected) if selected else ""
                
            if st.button("Next") and answer:
                st.session_state.answers.append(answer)
                st.session_state.current_q += 1
                st.rerun()
        else:
            with st.spinner("Planning your trip..."):
                itinerary = agent.plan_trip(st.session_state.answers)
                st.session_state.itinerary = itinerary
                st.session_state.planning_done = True
                st.rerun()
                
    else:
        st.success("Your itinerary is ready")
        st.markdown(st.session_state.itinerary)
        
        st.download_button(
            label="Download Itinerary",
            data=st.session_state.itinerary,
            file_name="itinerary.md",
            mime="text/markdown",
        )
        
        if st.button("Plan another trip"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
            
            
if __name__ == "__main__":
    main()
        
    
    