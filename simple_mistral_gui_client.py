import os
import sys
from dotenv import load_dotenv
import panel as pn
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage

pn.extension()
load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    print("Error: MISTRAL_API_KEY is not defined. Please set the API key in your environment.")
    sys.exit()

client = MistralAsyncClient(api_key=api_key)

# Model configuration options
available_models = [
    ("Open Mistral 7B", "open-mistral-7b"),
    ("BOFH Mistral", "ft:open-mistral-7b:c32c2392:20240613:ce61015d"),
    ("Open Mistral Mixtral-8x7B", "open-mixtral-8x7b"),
    ("Mistral Small", "mistral-small-latest"),
    ("Mistral Medium", "mistral-medium-latest"),
    ("Mistral Large", "mistral-large-latest")
]

model_selector = pn.widgets.Select(
    name='Select Model',
    options={name: api_id for name, api_id in available_models},
    value=available_models[0][1]
)

guardrails_select = pn.widgets.Select(name='Guardrails', options=[True, False], value=False)
temperature_slider = pn.widgets.FloatSlider(name='Temperature', start=0.0, end=1.0, step=0.01, value=0.7)
top_p_slider = pn.widgets.FloatSlider(name='Top P', start=0.0, end=1.0, step=0.1, value=1.0)
max_tokens_input = pn.widgets.IntInput(name='Max Tokens', value=None, placeholder='Optional')
random_seed_input = pn.widgets.IntInput(name='Random Seed', value=None, placeholder='Optional')

messages = []


async def process_user_message(contents: str, user: str, chat_instance: pn.chat.ChatInterface):
    """Process user message and generate model response."""
    global messages
    messages.append(ChatMessage(role="user", content=contents))

    model_api_id = model_selector.value
    safe_prompt = guardrails_select.value
    temperature = temperature_slider.value
    top_p = top_p_slider.value
    max_tokens = max_tokens_input.value
    random_seed = random_seed_input.value

    model_name = [name for name, api_id in available_models if api_id == model_api_id][0]
    chat_instance.callback_user = (
        f"{model_name.upper()}, guardrails: {safe_prompt}, temperature: {temperature}, "
        f"top_p: {top_p}, max_tokens: {max_tokens}, random_seed: {random_seed}"
    )

    accumulated_message = ""
    async for chunk in client.chat_stream(
            model=model_api_id,
            messages=messages,
            safe_prompt=safe_prompt,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            random_seed=random_seed
    ):
        part = chunk.choices[0].delta.content
        if part is not None:
            accumulated_message += part
            yield accumulated_message

    messages.append(ChatMessage(role="assistant", content=accumulated_message))


def create_chat_interface() -> pn.chat.ChatInterface:
    """Create the chat interface."""
    return pn.chat.ChatInterface(
        callback=process_user_message,
        callback_user="Mistral",
        show_undo=False,
        show_rerun=False,
        show_stop=True,
        widgets=pn.widgets.TextInput(placeholder="Talk to Mistral"),
    )


def create_model_config_column() -> pn.Column:
    """Create the model configuration column."""
    return pn.Column(
        model_selector,
        guardrails_select,
        temperature_slider,
        top_p_slider,
        max_tokens_input,
        random_seed_input
    )


def create_app_layout() -> pn.Column:
    """Create the main application layout."""
    chat_interface = create_chat_interface()
    chat_interface.send("Send a message to get a reply from the selected model!", user="System", respond=False)

    vertical_separator = pn.Spacer(width=3, sizing_mode='stretch_height', styles={'background': 'black'})
    model_config_column = create_model_config_column()

    app_header = pn.pane.Markdown(
        "# Mistral API Simple Client - [github](https://github.com/rogerkibbe/simple-mistral-api-client)",
        align="center"
    )

    return pn.Column(
        app_header,
        pn.Row(
            chat_interface,
            vertical_separator,
            model_config_column,
            sizing_mode='stretch_width'
        )
    )


app_layout = create_app_layout()
app_layout.servable()