import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Skylark Drone AI", layout="centered")

st.title("Skylark Drone Operations AI Agent")

st.markdown("Type commands like:")
st.markdown("- `assign M101`")
st.markdown("- `urgent M101`")
st.markdown("- `help`")


# Chat Memory

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# User Input
user_input = st.chat_input("Enter command...")

if user_input:

    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Process Command
    response_text = ""

    parts = user_input.strip().split()

    if parts[0].lower() == "assign" and len(parts) == 2:
        project_id = parts[1]
        response = requests.get(f"{API_URL}/assign/{project_id}")
        result = response.json()

        if "error" in result:
            response_text = f"❌ {result['error']}"
        else:
            response_text = f"""
### ✅ Assignment Recommendation

**Pilot:** {result['recommended_pilot']}  
**Drone:** {result['recommended_drone']}  
**Estimated Cost:** ₹ {result['estimated_cost']}

"""

            if result["warnings"]:
                response_text += "\n **Warnings:**\n"
                for w in result["warnings"]:
                    response_text += f"- {w}\n"

    elif parts[0].lower() == "urgent" and len(parts) == 2:
        project_id = parts[1]
        response = requests.get(f"{API_URL}/urgent/{project_id}")
        result = response.json()

        if "error" in result:
            response_text = f"❌ {result['error']}"
        else:
            response_text = f"""
**Urgent Reassignment Completed**

 Pilot: {result['recommended_pilot']}  
 Drone: {result['recommended_drone']}  
 Cost: ₹ {result['estimated_cost']}
"""

    elif parts[0].lower() == "help":
        response_text = """
### Available Commands

- `assign <project_id>` → Assign pilot & drone  
- `urgent <project_id>` → Trigger urgent reassignment  
- `help` → Show this menu
"""

    else:
        response_text = " Invalid command. Type `help` to see available options."

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response_text})

    with st.chat_message("assistant"):
        st.markdown(response_text)
