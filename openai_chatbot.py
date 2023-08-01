import os
import openai
from os import path

openai.api_key = os.getenv("OPENAI_API_KEY")

#roles: system, user, or assistant
# user is the role that gives instructions or asks questions
# system is the role that responds. content contains description of that role (e.g. friendly assistant)
# assistant is the role that 

class OpenAiChatbot:
    def __init__(self, mname, init_prompt, intro_line, name1_label, name2_label, log_path):
        self.mname = mname
        self.init_prompt = init_prompt
        self.intro_line = intro_line
        self.name1_label = name1_label
        self.name2_label = name2_label
        self.log_start = 0
        self.messages = []
        self.init_chat_log(log_path)
        self.log_file = open(log_path, "a")
    
    def close(self):
        self.log_file.close()

    def get_intro_line(self):
        return self.intro_line

    def get_response(self, input):
        self.messages.append({"role": "user", "content": input})

        # completion = {
        #     "choices": [
        #         {
        #         "index": 0,
        #         "message": {
        #             "role": "assistant",
        #             "content": "Someries Castle, located in Bedfordshire, England, is a fortified manor house built in the 15th century by Sir John Wenlock. Though referred to as a castle, its structure does not fully meet the definition. The site was previously owned by William de Someries, from whom it derived its name. Wenlock began construction on the mansion in 1430 using brick, making it one of the earliest brick buildings in England. However, the house was never finished and was partially torn down in the 18th century. Today, only the gatehouse, including a chapel and lodge, remains intact, showcasing the original brickwork. The former manor house and the earlier Norman Castle exist as earthworks, outlining the plot where the house initially stood. Some bricks from the manor house were repurposed to construct neighboring farmhouses during the 17th century. Despite its controversial classification, Someries Castle remains a Scheduled Ancient Monument and a testament to medieval architecture."
        #         },
        #         }
        #     ]
        # }

        completion = openai.ChatCompletion.create(
            model=self.mname,
            #top_p=1.0,                # range 0 to 1.0, default 1.0, alternative to temp, 0.1 means only top 10% probability mass are considered
            #temperature=0.9,          # range: 0.0 to 2.0, default 0.8  Higher values like 0.8 make output more random, lower more deterministic
            max_tokens=120,            # maximum number of tokens to generate in the completion (gpt3: 2048, GPT3.5: 4096)
            #frequency_penalty=0.9,    # range: -2.0 to 2.0, default 0
            #n=1,                      # how many chat completion choices to generate for each input message
            messages=self.messages
            )

        #res = completion["choices"][0]["message"]["content"]
        res = completion.choices[0].message.content
        if "." in res:
            res = res.strip().rpartition('.')[0]            # strip white space and take up to last period.
            if len(res):
                res += '.'

        self.messages.append({"role": "assistant", "content": res})
        self.log_file.write("User: " + input + "\n")
        self.log_file.write("Assistant: " + res + "\n")
        return res

    def init_chat_log(self, log_path):
        if path.isfile(log_path):
            with open(log_path) as log_file:
                log_messages_str = log_file.read()
                message_strs = log_messages_str.split('\n')
                line_count = len(message_strs)
                self.log_start_message_index = line_count + 1
                index = 0
                while index < line_count:
                    split = message_strs[index].split(":")
                    role = split[0].lower().strip()
                    if role != "assistant" and role != "user" and role != "system":
                        print("warning: unknown role")
                    content = split[1]
                    index += 1
                    while index < line_count:    
                        if ":" in message_strs[index] and (message_strs[index].startswith("Assistant") 
                            or message_strs[index].startswith("User") or message_strs[index].startswith("System")):
                            break
                        else:
                            content += '\n' + message_strs[index]
                        index += 1

                    self.messages.append({"role": role, "content": content.lstrip()})
                    print(self.messages[-1])
        else:
            self.messages = [{"role": "system", "content" : self.init_prompt}]

    def get_log(self):
        log = ""
        end = len(self.messages)
        for index in range(self.log_start_message_index, end):
            msg = self.messages[index]
            if msg['role'] == 'user':
                log += f"{self.name1_label}: {msg['content']}\n"
            elif msg['role'] == 'assistant':              
                log += f"{self.name2_label}: {msg['content']}\n"
        return log
            
if __name__ == "__main__":
    f = open("conv_short.txt")
    data = f.read() 
    a = OpenAiChatbot("","","","","",data)
    