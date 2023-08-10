import syphus.data_generator.gpt_manager as gpt_manager

from syphus import prompts
from syphus.data_generator.response import Response
from syphus.prompts.info import Info

from typing import Optional, List, Tuple, Iterable
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


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
        messages.append({"role": "user", "content": info.content})
        gpt_response = self.gpt_manager.query_gpt(messages)
        response = Response(gpt_response)
        return response

    def query_single_info_with_error_management(
        self, info: Info
    ) -> Tuple[str, Optional[Response], Optional[str]]:
        try:
            return info.id, self.query_single_info(info), None
        except Exception as e:
            return info.id, None, str(e)

    def query_all_infos(
        self, infos: Iterable[Info], *, num_threads: int = 8
    ) -> Iterable[Tuple[str, Optional[Response], Optional[str]]]:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            with tqdm(total=len(infos), desc="Querying GPT") as progress_bar:
                for id, response, error_message in executor.map(
                    self.query_single_info_with_error_management, infos
                ):
                    progress_bar.update(1)
                    yield id, response, error_message
