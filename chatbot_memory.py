from openai_api import OpenAiApi
import math
import argparse
from pathlib import Path

class ChatbotMemory:
  def __init__(self):
    self._summarize_prompt = "Summarize this transcript in at least {} words."
    self._messages = []
    self._openAiApi = OpenAiApi()
    self._fraction = 3.0

  def load_from_file(self, filename):
    with open(filename) as fd:
      line = fd.readline()
      try:
        role = line.partition(":")[0]
        role = role.lower()
      except:
        role = "user"
      
      content = fd.read()

      tokens_count = self._openAiApi.num_tokens_from_str(content) + 7
      print("total tokens of file: ", tokens_count)
      tokens_per_chunk = 0
      if tokens_count > 12288:
        self._fraction = tokens_count / 12288.0
        if self._fraction < 3.0:
          self._fraction = 3.0
        tokens_per_chunk = tokens_count /  self._fraction
        chunk_count = math.ceil(self._fraction)
        words_per_chunk = 0.75 * tokens_per_chunk
        chars_per_chunk = words_per_chunk * 5
        print("chunk count: ", chunk_count)
        print("tokens per chunk: ", tokens_per_chunk)

        for i in range(0,chunk_count):
          chunk = content[int(i * chars_per_chunk) : int((i+1)* chars_per_chunk)]
          self._messages.append(self._openAiApi.build_message(role, chunk))
      else:
          self._messages.append(self._openAiApi.build_message(role, content))

      for msg in self._messages:
        #print("chunk len: ", len(msg["content"]))
        print("chunk tokens: ", self._openAiApi.num_tokens_from_str(msg["content"]))

  def make_summaries(self):
    summaries = ""
    for msg in self._messages:
      to_submit = []
      request_output = int(self._openAiApi.num_tokens_from_messages([msg]) / self._fraction)
      to_submit.append(msg)
      msg_instruct = self._openAiApi.build_message("user", self._summarize_prompt.format(request_output))
      to_submit.append(msg_instruct)
      print(msg_instruct)
      response = self._openAiApi.get_response(to_submit)
      print(response)
      response_str = response['choices'][0]["message"]["content"]
      print("response len = ", len(response_str))
      summaries += response_str
    return summaries
      

def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(
        description="Summarize large doc/transcript using ChatGPT to a size suitable to fit in 16k.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
 
  parser.add_argument(
        "--input-file",
        type=str,
        help="Path of input file to summarize.",
    )
  
  parser.add_argument(
        "--append-to-file",
        type=argparse.FileType('a'),
        help="Chatlog file to append summary.",
    )
  
  args = parser.parse_args()
  return args

def main() -> None:
  args = parse_args()
  cbm = ChatbotMemory()
  cbm.load_from_file(args.input_file)
  summaries = "User:" + cbm.make_summaries()

  summaries_no_lfs = summaries.replace('\n',' ')

  if args.append_to_file:
    args.append_to_file.write(summaries_no_lfs)
    args.append_to_file.close()
  else:
    print(summaries)

if __name__ == '__main__':
  main()
