import streamlit as st
import os
#import streamlit_app as sa
from openai.types.chat.chat_completion import ChatCompletionMessage, ChatCompletion
# from openai.types.chat.chat_completion import ChatCompletionMessageParam, ChatCompletionMessageParam
from openai import OpenAI
import json
from dotenv import load_dotenv, find_dotenv





# Set the page title
st.set_page_config(page_title="Custom Page Title")
st.write("# Call to API to get data")


_ : bool = load_dotenv(find_dotenv()) # read local .env file
load_dotenv()

client : OpenAI = OpenAI()

ctd_cost = 2000
project_budget = 8000
project_funded_value = 10000

def compute_percent_complete(ctd_cost=None, project_budget=None):
    try:
        if project_budget is None or project_budget <= 0:
            raise ValueError("I can compute the project percent compute if in your question below you provide me with project cost and project budget greater tha zero")
        
        percent_complete = ctd_cost / project_budget
        if percent_complete <= 0:
            percent_complete = 0
        elif percent_complete <= 1:
            percent_complete = percent_complete * 100
        elif percent_complete > 1:
            percent_complete = 100
    except ZeroDivisionError:
        st.warning("Error: Enter a value greater than zero for the budget")
        percent_complete = 0  # Set a default value or handle it appropriately
    except ValueError as e:
        st.warning(str(e))
        percent_complete = 0  # Set a default value or handle it appropriately
    
    return str(percent_complete)
 

percent_complete = compute_percent_complete()  
 
    
def run_conversation(main_request: str)->str:
    # Step 1: send the conversation and available functions to the model
    messages = [{"role": "user", "content": main_request}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "compute_percent_complete",
                "description": "Compute the percent complete of a project",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ITD_Cost": {
                            "type": "number",
                            "description": "The project's inception to date actual cost to date",
                        },
                        "project_budget": {"type": "number", "description": "The project's budget"},
                    },
                    "required": ["ITD_Cost", "project_budget"],                },
            },
        }
    ]

    # First Request
    response: ChatCompletion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message: ChatCompletionMessage = response.choices[0].message
    print("* First Response: ", dict(response_message))

    tool_calls = response_message.tool_calls
    print("* First Response Tool Calls: ", list(tool_calls))

    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "compute_percent_complete": compute_percent_complete,
        }  # only one function in this example, but you can have multiple
        
        messages.append(response_message)  # extend conversation with assistant's reply
        
        # Step 4: send the info for each function call and function response to the model
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            ctd_cost=function_args.get("ITD_Cost"),  # Fix the argument names
            project_budget=function_args.get("project_budget"),
        )
        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response

        print("* Second Request Messages: ", list(messages))
        second_response: ChatCompletion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )  # get a new response from the model where it can see the function response
        print("* Second Response: ", dict(second_response))
        return second_response.choices[0].message.content
    
#st.text("Percent Complete: " + str(percent_complete))
user_question = st.text_input("Enter your question here")
if st.button('Calculate Percent Complete'):
    response = run_conversation(user_question)
    st.text("Response: " + response)
