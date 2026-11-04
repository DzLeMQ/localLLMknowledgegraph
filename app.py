import streamlit as st
import json
import pandas as pd
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# ==========================================
# PAGE CONFIGURATION & UI STYLING
# ==========================================
st.set_page_config(page_title="Local AI Wealth Planner", page_icon="📊", layout="wide")

st.title("📊 Local AI Wealth Planner & Visualizer")
st.caption("Powered by Llama 3.1 & LangChain — Running 100% Locally with Interactive Graphics")

# Sidebar Configuration
st.sidebar.header("🛠️ Local Environment Settings")
selected_model = st.sidebar.selectbox("Select Model", ["llama3.1", "llama3.2"], index=0)
temperature = st.sidebar.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.0, step=0.1)

# ==========================================
# 1. VISUALIZATION-READY CALCULATION ENGINE
# ==========================================
@tool
def calculate_financial_plan(
    starting_principal: float,
    years_to_grow: int,
    annual_growth_rate: float,
    withdrawal_rate: float = 4.0
) -> str:
    """
    Calculates future portfolio value, sustainable monthly income, and outputs data for chart plotting.
    Use this tool whenever the user asks to calculate growth, future value, or monthly income.
    """
    r = annual_growth_rate / 100.0
    swr = withdrawal_rate / 100.0
    n = 12
    
    # Calculate yearly values for data visualization tracking
    yearly_data = []
    current_value = starting_principal
    
    # Year 0 Baseline
    yearly_data.append({"Year": 0, "Portfolio Value": round(current_value, 2)})
    
    for year in range(1, years_to_grow + 1):
        # Compound monthly for 1 year
        current_value = current_value * ((1 + r/n) ** n)
        yearly_data.append({"Year": year, "Portfolio Value": round(current_value, 2)})
        
    future_value = current_value
    annual_income_target = future_value * swr
    monthly_income = annual_income_target / 12
    
    # Package text analysis alongside raw chart data points inside a JSON envelope
    result_payload = {
        "text_summary": (
            f"• Initial Principal: ${starting_principal:,.2f}\n"
            f"• Growth Period: {years_to_grow} years at {annual_growth_rate}% annual return\n"
            f"• Projected Portfolio Value: ${future_value:,.2f}\n"
            f"• Estimated Stable Monthly Income (at {withdrawal_rate}% SWR): ${monthly_income:,.2f}/month"
        ),
        "chart_points": yearly_data
    }
    
    return json.dumps(result_payload)

# ==========================================
# 2. INITIALIZE AGENT & SESSION STATE
# ==========================================
if "agent_executor" not in st.session_state:
    llm = ChatOllama(model=selected_model, temperature=temperature)
    tools = [calculate_financial_plan]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert AI Financial Planning Assistant running locally. Your job is to help users map out "
            "how to grow their money (like their $200k) into a stable monthly income.\n\n"
            "CRITICAL RULE 1: You must never calculate compounding math manually. Always use the tools.\n"
            "CRITICAL RULE 2: When you receive output from your tool, it will be in raw JSON format. "
            "Extract the 'text_summary' field to answer the user. DO NOT output the raw 'chart_points' array to the user. "
            "Always include a brief disclaimer that this is educational content only and not financial advice."
        )),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}\n\n{agent_scratchpad}"),
    ])
    
    agent = create_structured_chat_agent(llm, tools, prompt)
    st.session_state.agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True
    )

# Manage Chat & Visual History State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Hello! I can help you model your $200k wealth allocation strategy. Tell me your investment timeline and growth targets!",
            "chart_data": None
        }
    ]

# Display history (handling chat bubbles and charts)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("chart_data"):
            df = pd.DataFrame(message["chart_data"])
            st.line_chart(df.set_index("Year"))

# ==========================================
# 3. INTERACTIVE CHAT & INTERCEPTING RESULTS
# ==========================================
if user_query := st.chat_input("e.g., Run my $200k for 10 years at 7% growth and 4% SWR."):
    
    st.session_state.messages.append({"role": "user", "content": user_query, "chart_data": None})
    with st.chat_message("user"):
        st.markdown(user_query)
        
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        chart_placeholder = st.empty()
        
        with st.spinner("Llama is computing figures and rendering chart arrays..."):
            try:
                # Capture agent intermediate steps to extract chart data directly from the tool call
                response = st.session_state.agent_executor.invoke(
                    {"input": user_query},
                    return_only_outputs=False # Retain intermediate steps tracking data
                )
                
                output_text = response["output"]
                chart_points = None
                
                # Check if our specific tool was called during execution
                for step in response.get("intermediate_steps", []):
                    if step[0].tool == "calculate_financial_plan":
                        raw_tool_output = step[1]
                        try:
                            # Parse JSON data package returned by backend function
                            parsed_payload = json.loads(raw_tool_output)
                            chart_points = parsed_payload.get("chart_points")
                        except Exception:
                            pass # Fallback if JSON format parsing fails
                
                # Render components if chart data points are present
                response_placeholder.markdown(output_text)
                if chart_points:
                    df = pd.DataFrame(chart_points)
                    chart_placeholder.line_chart(df.set_index("Year"))
                
                # Append to session state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": output_text, 
                    "chart_data": chart_points
                })
                
            except Exception as e:
                error_msg = f"An error occurred during local model inference: {str(e)}"
                response_placeholder.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg, "chart_data": None})