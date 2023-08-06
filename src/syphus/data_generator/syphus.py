import syphus.data_generator.gpt_manager as gpt_manager

from syphus import prompts

from typing import Optional


class Syphus(object):
    def __init__(
        self,
        *,
        gpt_info_path: Optional[str] = None,
        openai_api: Optional[gpt_manager.OpenAISettings] = None,
        gpt_params: Optional[gpt_manager.GPTParamsSettings] = None,
        prompts: prompts.Prompts | str,
    ):
        self.gpt_manager = gpt_manager.GPTManager(
            gpt_info_path=gpt_info_path, openai_api=openai_api, gpt_params=gpt_params
        )
        if isinstance(prompts, str):
            self.prompts = prompts.Prompts.from_yaml(prompts)
        elif isinstance(prompts, prompts.Prompts):
            self.prompts = prompts
        else:
            raise ValueError("Must provide either prompts yaml path or prompts object")

    def query_gpt(self, info: str):
        messages = self.prompts.get_messages()
        messages.append({"role": "user", "content": info})
        response = self.gpt_manager.query_gpt(messages)
        # TODO: Parse response
        return response
