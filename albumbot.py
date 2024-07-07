# CHATBOT practice for an album store!

# Setup
import os
import openai
from dotenv import load_dotenv, find_dotenv 
import panel as pn # GUI

_ = load_dotenv('.venv/.env') # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

# I don't use this, but for reference
# def get_completion(prompt, model="gpt-3.5-turbo"):
#     messages = [{"role": "user", "content": "prompt"}]
#     response = client.chat.completions.create(model = model,
#     messages = messages,
#     temperature = 0) # degree of randomness
#     return response.choices[0].message.content

# I use this instead, however since I am exceeding my current quota I will use a mock function
def get_completion_from_messages(messages, model = "gpt-3.5-turbo", temperature = 0):
    # (OpenAI.ChatCompletion.) 
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = temperature, # degree of randomness
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

# MOCK FUNCTION for testing

# def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature = 0):
#     # Mock response based on the messages
#     last_user_message = messages[-1]['content']
#     mock_responses = {
#         "Hi": "Hello! How can I assist you today?",
#         "I'd like to order a BTS album.": "Sure! Which version would you like to order? We have BTS Love Yourself: Her L, O, V, and E.",
#         "I'd like to order BTS Love Yourself: Her L.": "Great choice! That will be $20. Would you like to add anything else to your order?",
#         "No, that's all.": "Would you like this order for pickup or delivery?",
#     }
#     return mock_responses.get(last_user_message, "Last Message")

# OrderBot
def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role': 'user', 'content': f"{prompt}"})
    response = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width = 600))
    )
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width = 600))
    )
    return pn.Column(*panels)

pn.extension()

panels = [] # collect display

context = [ {'role': 'system', 'content': """
    You are OrderBot, an automated service to collect orders for an album shop. 
             
    You first greet the customer, then collect their order, and clarify the price of each album.
    Wait to collect the entire order.
    Ask if it is for pickup or delivery.
        If there a delivery, ask for an address. If it is pickup, state our address (123 Sample Address)
    After collecting the entire order, then summarize it and do a final check if the customer wants to add anything else.
    Collect payment. 
             
    Make sure to clarify all versions of an album to uniquely identify the item from the catalog. 
    You should respond in a short, conversational friendly style.
             
    When summarizing the order it should be in this format:
        <pickup or delivery>
        1 - <album name> , <price>
        ...
        N - <album name> , <price>
             
    The menu includes 
    BTS Love Yourself: Her L , Price: 40.0  
    BTS Love Yourself: Her O , Price: 40.0 
    BTS Love Yourself: Her V , Price: 40.0 
    BTS Love Yourself: Her E, , Price: 40.0 
    SZA SOS , Price: 30.0
    SZA Ctrl, Price: 30.0
    Ariana Grande eternal sunshine , Price: 35.0
    Ariana Grande positions , Price: 30.0
    """ }] # context will accumulate

# Setup text box and button
inp = pn.widgets.TextInput(value = "Hi", placeholder = 'How may I help you?')
button_conversation = pn.widgets.Button(name = "Chat!")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column (
    inp, 
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator = True, height = 300),
)

# Display dashboard in a web browser
pn.serve(dashboard, start = True)

messages = context.copy()
messages.append(
    {'role': 'system', 'content': 'Create a json summary of the previous album order. Itemize the price for each item \
     The fields should be 1) album, include version 2) pickup or delivery 3) total price'}
)

response = get_completion_from_messages(messages, temperature = 0)
print(response) 