from openai.types.beta import Assistant, Thread
from typing_extensions import override
from openai import AssistantEventHandler, Client


class CustomAssistant():
    def __init__(self, assistant:Assistant, client:Client):
        self.client = client
        self.assistant = assistant
        self.thread = [self.client.beta.threads.create()]

    def new_thread(self):
        thread = self.client.beta.threads.create()
        self.thread.append(thread)
        return thread

    def add_message(self, thread:Thread, prompt:str):
        message = self.client.beta.threads.messages.create(
          thread_id=thread.id,
          role="user",
          content=prompt
        )
        return message

    def run(self, thread_id:str):
        with self.client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=self.assistant.id,
            instructions="Por favor, responda às chamadas.",
            event_handler=EventHandler(self.assistant.name),
        ) as stream:
            stream.until_done()


class EventHandler(AssistantEventHandler):    
    def __init__(self, assistant_name:str="assistant"):
        super().__init__()
        self.assistant_name = assistant_name

    @override
    def on_text_created(self, text) -> None:
        print(f"\n{self.assistant_name} > ", end="", flush=True)
    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\n{self.assistant_name} > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
        if delta.code_interpreter.outputs:
            print(f"\n\noutput >", flush=True)
            for output in delta.code_interpreter.outputs:
                if output.type == "logs":
                    print(f"\n{output.logs}", flush=True)
