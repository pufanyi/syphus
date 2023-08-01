import openai
import time

from syphus import prompts


class GPTManager(object):
    def query_gpt(prompt: prompts.Prompts, *, openai_api, gpt_params):
        messages = prompt.get_messages()
        succuss = False
        while not succuss:
            try:
                response = openai.ChatCompletion.create(
                    engine=engine,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=3200,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None,
                )
                succuss = False
            except Exception as e:
                print(f"Error: {e}")
                if "have exceeded call rate limit" in str(e):
                    print("Sleeping for 3 seconds")
                    succuss = True
                    time.sleep(3)
                else:
                    succuss = False
                    response = {"error_message": str(e)}
        return response
