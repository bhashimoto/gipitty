from assistant import CustomAssistant



def repl(assistant: CustomAssistant):
    thread = assistant.new_thread()
    while True:
        print("\n> ", end="")
        prompt = input().strip("\n")
        if not prompt:
            assistant.run(thread.id)
        else:
            assistant.add_message(thread=thread, prompt=prompt)
