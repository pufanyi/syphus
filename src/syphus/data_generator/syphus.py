import os

from typing import Optional, Tuple, Iterable
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

import syphus.data_generator.gpt_manager as gpt_manager
import syphus.data_generator.response as syphus_response

from syphus import prompts
from syphus.data_generator.response import Response
from syphus.prompts.info import Info


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
        try:
            gpt_response = self.gpt_manager.query_gpt(messages)
            response = Response(gpt_response=gpt_response)
        except Exception as e:
            response = Response(gpt_error_messages=str(e))
        return response

    def query_all_infos(
        self, infos: Iterable[Info], *, num_threads: int = 8
    ) -> Iterable[Tuple[str, Optional[Response], Optional[str]]]:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            with tqdm(total=len(infos), desc="Querying GPT") as progress_bar:
                for id, response in executor.map(
                    lambda info: (info.id, self.query_single_info(info)), infos
                ):
                    yield id, response
                    progress_bar.update(1)

    def query_all_infos_and_save(
        self,
        infos: Iterable[Info],
        path,
        *,
        num_threads: int = 8,
        format: str = "json",
        response_file_name: str = "responses",
        error_message_file_name: str = "error_messages",
        full_response_file_name: str = "gpt_full_responses",
        output_type: str = "split",
    ):
        if output_type not in ["split", "combined"]:
            raise ValueError("Invalid output type")
        if format not in ["json", "yaml", "jsonl"]:
            raise ValueError("Invalid format, must be json, yaml, or jsonl")
        if output_type == "split":
            for id, response in self.query_all_infos(infos, num_threads=num_threads):
                response.save(
                    os.path.join(path, id),
                    format=format,
                    response_file_name=response_file_name,
                    error_message_file_name=error_message_file_name,
                    full_response_file_name=full_response_file_name,
                )
        elif output_type == "combined":
            data = {}
            for id, response in self.query_all_infos(infos, num_threads=num_threads):
                data[id] = response
            syphus_response.save_all(
                data,
                path,
                format=format,
                response_file_name=response_file_name,
                error_message_file_name=error_message_file_name,
                full_response_file_name=full_response_file_name,
            )
