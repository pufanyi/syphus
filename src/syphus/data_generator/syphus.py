import syphus.data_generator.gpt_manager as gpt_manager

from syphus import prompts
from syphus.data_generator.response import Response
from syphus.data_generator.info import Info

from typing import Optional, List, Tuple


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

    def query_single_info(self, info: Info) -> Response:
        messages = self.prompts.get_messages()
        messages.append({"role": "user", "content": info.get_info()})
        gpt_response = self.gpt_manager.query_gpt(messages)
        response = Response(gpt_response)
        return response

    def query_all_infos(self, infos: List[Info]) -> Tuple[List[Response], List[str]]:
        responses = {}
        error_messages = {}
        for info in infos:
            try:
                responses[info.id] = self.query_single_info(info)
            except Exception as e:
                error_messages[info.id] = str(e)
        return responses, error_messages
