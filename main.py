from dotenv import load_dotenv
from openai import OpenAI

from assistant import CustomAssistant
from repl import repl



def main():
    load_dotenv()
    client = OpenAI()
    assistant = client.beta.assistants.retrieve("asst_kwFJQ9FwmLxoOq8niwmCDPZV")
    custom_assistant = CustomAssistant(assistant=assistant, client=client)
    repl(custom_assistant)

if __name__ == "__main__":
    main()

