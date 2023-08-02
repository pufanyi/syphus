import openai
import time

from syphus import prompts
from syphus.data_generator.gpt_params_settings import GPTParamsSettings
from syphus.data_generator.openai_settings import OpenAISettings

from typing import Optional


class GPTManager(object):
    def __init__(
        self,
        openai_api: OpenAISettings,
        *,
        gpt_params: Optional[GPTParamsSettings] = None,
    ):
        self.openai_api = openai_api
        if gpt_params:
            self.gpt_params = gpt_params
        else:
            self.gpt_params = GPTParamsSettings()

    def set_gpt_params(self, gpt_params: GPTParamsSettings):
        self.gpt_params = gpt_params

    def query_gpt(self, prompt: prompts.Prompts):
        messages = prompt.get_messages()
        succuss = False
        while not succuss:
            try:
                response = openai.ChatCompletion.create(
                    engine=self.openai_api.engine,
                    messages=messages,
                    temperature=self.gpt_params.temperature,
                    max_tokens=self.max_tokens,
                    top_p=self.gpt_params.top_p,
                    frequency_penalty=self.gpt_params.frequency_penalty,
                    presence_penalty=self.gpt_params.presence_penalty,
                    stop=self.gpt_params.stop,
                )
                succuss = True
            except Exception as e:
                print(f"Error: {e}")
                if "have exceeded call rate limit" in str(e):
                    print("Sleeping for 3 seconds")
                    succuss = True
                    time.sleep(3)
                else:
                    succuss = True
                    response = {"error_message": str(e)}
        return response
