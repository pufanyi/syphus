import openai
import time
import sys

from syphus import prompts
import syphus.data_generator.gpt_params_settings as gpt_params_settings
import syphus.data_generator.openai_settings as openai_settings

from typing import Optional


class GPTManager(object):
    def __init__(
        self,
        *,
        gpt_info_path: Optional[str] = None,
        openai_api: Optional[openai_settings.OpenAISettings] = None,
        gpt_params: Optional[gpt_params_settings.GPTParamsSettings] = None,
    ):
        if gpt_info_path:
            if openai_api or gpt_params:
                print(
                    "Warning: gpt_info_path overrides openai_api and gpt_params",
                    flush=True,
                    file=sys.stderr,
                )
            self.openai_api = openai_settings.read_yaml(gpt_info_path)
            self.gpt_params = gpt_params_settings.read_yaml(gpt_info_path)
        elif openai_api:
            self.openai_api = openai_api
            if gpt_params:
                self.gpt_params = gpt_params
            else:
                self.gpt_params = gpt_params_settings.GPTParamsSettings()
        else:
            raise ValueError("Must provide either gpt_info_path or openai_api")

    def set_gpt_params(self, gpt_params: gpt_params_settings.GPTParamsSettings):
        self.gpt_params = gpt_params

    def query_gpt(self, prompt: prompts.Prompts):
        succuss = False
        while not succuss:
            try:
                response = openai.ChatCompletion.create(
                    engine=self.openai_api.engine,
                    messages=prompt.get_messages(),
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
