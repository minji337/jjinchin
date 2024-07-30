from common import client, model
from characters import system_role
from pprint import pprint
import time

assistant = client.beta.assistants.create(
    name="내 찐친 고비", 
    instructions=system_role, 
    model=model.basic,
)

pprint(assistant.model_dump())

##############################################

#assistant = client.beta.assistants.retrieve(assistant_id = 'asst_5mvewDLvPyerdDBqr8OTq2co')
assistant = client.beta.assistants.retrieve(assistant_id = assistant.id)

##############################################

thread = client.beta.threads.create()
pprint(thread.model_dump())

#thread = client.beta.threads.retrieve(thread_id ='thread_PBQgV0UINj2UKyxSSBJ4k012')
thread = client.beta.threads.retrieve(thread_id = thread.id)

user_message = client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content="고비야 반가워! 잘 지냈지?"
        )
pprint(user_message.model_dump())	


thread_messages = [m for m in list(client.beta.threads.messages.list(thread_id=thread.id))]
print([user_message] == thread_messages)


run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
run_dict = run.model_dump()
keys_to_print = ['id', 'completed_at', 'required_action', 'status']
selected_run_dict = {key: run_dict[key] for key in keys_to_print}
pprint(selected_run_dict)	

start_time = time.time()

while(True):
    elapsed_time  = time.time() - start_time
    retrieved_run = client.beta.threads.runs.retrieve(
                        thread_id=thread.id,
                        run_id=run.id
                    )                
    print(f"run status: {retrieved_run.status}, 경과:{elapsed_time: .2f}초")
    if retrieved_run.status == "completed":
        break
    elif retrieved_run.status in ["failed", "cancelled", "expired"]:
        raise ValueError(f"run status: {retrieved_run.status}, {retrieved_run.last_error}")
    time.sleep(1)

thread_messages = [{"role": m.role, "content": m.content[0].text.value} 
                   for m in list(client.beta.threads.messages.list(thread_id=thread.id))]
thread_messages.reverse()                   
pprint(thread_messages)	
