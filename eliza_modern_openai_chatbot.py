from openai_chatbot import OpenAiChatbot

class AnyOpenAiChatbot(OpenAiChatbot):
    def __init__(self, chatbot_name, user_title, chatbot_title):
        prompt_name = chatbot_name + "_prompt"
        init_prompt = ""
        with open(f'prompts/{prompt_name}.txt', 'r') as f:
            init_prompt = f.read()
        log_path = "logs/" + chatbot_name + ".log"

        intro_line = "HI! I'M ELIZA. WHAT'S YOUR PROBLEM?"
        super().__init__("gpt-4o", init_prompt, intro_line, user_title, chatbot_title, log_path)
        
if __name__ == "__main__":

    # Change these to switch chatbot and titles
    CHATBOT_NAME = "eliza_modern"
    USER_TITLE = "human" # try "Human"
    CHATBOT_TITLE = "eliza" # also try name of chatbot.

    # Change the following line
    chat_bot = AnyOpenAiChatbot(CHATBOT_NAME, USER_TITLE, CHATBOT_TITLE)
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
            elif inp == "shut":
                print("O.K. IF YOU FEEL THAT WAY I'LL SHUT UP....")
                break
            answer = chat_bot.get_response(inp)
            print(answer)
    except KeyboardInterrupt:
        chat_bot.close()

