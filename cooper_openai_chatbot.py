from openai_chatbot import OpenAiChatbot

class CooperOpenAiChatbot(OpenAiChatbot):
    def __init__(self):
        prompt_name ="cooper"
        init_prompt = ""
        prompt_messages = ""
        log_path = "C:/Users/jim/Desktop/Cooper/Windows/MetahumanChatbot/Saved/chat_log.txt"
        
        with open(f'prompts/{prompt_name}.txt', 'r') as f:
            init_prompt = f.read()
        
        intro_line = "In chat mode I can answer questions about myself. Say goodbye to end the chat. What can I answer for you today?"
        super().__init__("gpt-3.5-turbo-0125", init_prompt, intro_line, "user", "assistant", log_path)
        
if __name__ == "__main__":
    chat_bot = CooperOpenAiChatbot()
    inp = ""
    print(chat_bot.intro_line)
    try:
        while inp != "bye":
            print("> ",end='')
            inp = input()
            if inp == '':
                inp = "continue"
            elif inp == ".log":
                print(chat_bot.get_log())
                continue
            answer = chat_bot.get_response(inp)
            print(answer)
    except KeyboardInterrupt:
        chat_bot.close()
        