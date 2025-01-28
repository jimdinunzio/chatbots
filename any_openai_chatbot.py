from openai_chatbot import OpenAiChatbot

class AnyOpenAiChatbot(OpenAiChatbot):
    def __init__(self, chatbot_name, user_title, chatbot_title):
        prompt_name = chatbot_name + "_prompt"
        init_prompt = ""
        with open(f'prompts/{prompt_name}.txt', 'r') as f:
            init_prompt = f.read()
        
        try:
            with open(f'prompts/{prompt_name}_messages.txt', 'r') as f:
                prompt_messages = f.read()
        except:
            prompt_messages = ""
        
        intro_line = "In chat mode I can answer questions about myself. Say bye to end the chat. What can I answer for you today?"
        super().__init__("gpt-3.5-turbo-16k", init_prompt, intro_line, user_title, chatbot_title, prompt_messages)
        
if __name__ == "__main__":

    # Change these to switch chatbot and titles
    CHATBOT_NAME = "cooper"
    USER_TITLE = "user" # try "Human"
    CHATBOT_TITLE = "assistant" # also try name of chatbot.

    # Change the following line
    chat_bot = AnyOpenAiChatbot(CHATBOT_NAME, USER_TITLE, CHATBOT_TITLE)
    inp = ""
    print(chat_bot.intro_line)
    while inp != "bye":
        print("> ",end='')
        inp = input()
        if inp == ".log":
            print(chat_bot.get_log())
            continue
        answer = chat_bot.get_response(inp)
        chat_bot.add_to_chat_log(answer)
        print(answer)
        