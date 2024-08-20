import requests
from assistant import CustomAssistant



def repl(assistant: CustomAssistant):
    thread = assistant.new_thread()
    while True:
        print("\n> ", end="")
        prompt = input().strip("\n")
        if not prompt:
            data = assistant.run(thread.id)
            if data:
                print(data)
                resp = requests.post(url="http://localhost:5000/data", headers={"content-type": "application/json"}, json=data)
                if resp.status_code == 200:
                    print("inserted to database")

        else:
            assistant.add_message(thread=thread, prompt=prompt)
