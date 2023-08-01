import os
import openai
import tiktoken

openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAiApi:
    def __init__(self, model="gpt-3.5-turbo-16k"):
        self._model = model
        try:
            self._encoding = tiktoken.encoding_for_model(self._model)
        except KeyError:
            self._encoding = tiktoken.get_encoding("cl100k_base")

    def build_message(self, role, content):
        return {"role": role, "content": content}

    def get_response(self, messages):
        #print(messages)
        return openai.ChatCompletion.create(
            model=self._model,
            #top_p=1.0,                # range 0 to 1.0, default 1.0, alternative to temp, 0.1 means only top 10% probability mass are considered
            #temperature=0.9,          # range: 0.0 to 2.0, default 0.8  Higher values like 0.8 make output more random, lower more deterministic
            #max_tokens=2048,          # maximum number of tokens to generate in the completion (gpt3: 2048, GPT3.5: 4096)
            #frequency_penalty=0.9,    # range: -2.0 to 2.0, default 0
            #n=1,                      # how many chat completion choices to generate for each input message
            messages=messages
            )

#See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens
# 

    def find_nth_token_in_str(self, string: str, n: int):
        str_len = len(string)
        midpt = str_len / 2
        if midpt > 0:
            while string[midpt] != ' ' and string[midpt] != '.' and string[midpt] != "!":
                midpt += 1
            left_half = string[0:midpt]
            right_half = string[midpt : -1]
            c = self.num_tokens_from_str(left_half)
            if c <= n:
                return midpt - self.find_nth_token_in_str(left_half, n)
            elif c > n:
                return midpt + self.find_nth_token_in_str(right_half, n - c)
        else:
            return 0

    def num_tokens_from_str(self, string):
        return len(self._encoding.encode(string))
    
    def num_tokens_from_messages(self, messages):
        """Returns the number of tokens used by a list of messages."""
        if self._model.startswith("gpt"):  # note: future models may deviate from this
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(self._encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.""")
