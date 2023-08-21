import os

from typing import Optional, Tuple, Iterable, Union, List
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

import syphus.data_generator.gpt_manager as gpt_manager
import syphus.data_generator.openai_settings as openai_settings
import syphus.data_generator.gpt_params_settings as gpt_params_settings
import syphus.data_generator.response as syphus_response
import syphus.prompts.prompts as syphus_prompts

from syphus.data_generator.response import Response
from syphus.prompts.info import Info


class Syphus(object):
    """
    A class for managing interactions with the OpenAI GPT-3 engine and querying prompts for responses.

    Attributes:
        gpt_manager (gpt_manager.GPTManager): An instance of GPTManager for managing GPT-3 interactions.
        prompts (syphus.prompts.prompts.Prompts): An instance of Prompts containing conversation prompts and messages.

    """

    def __init__(
        self,
        *,
        gpt_info_path: Optional[str] = None,
        openai_api: Optional[openai_settings.OpenAISettings] = None,
        gpt_params: Optional[gpt_params_settings.GPTParamsSettings] = None,
        prompts: Union[syphus_prompts.Prompts, str],
    ):
        """
        Initialize the Syphus instance.

        Args:
            gpt_info_path (str, optional): Path to a YAML file containing OpenAI API and GPT parameters settings.
            openai_api (gpt_manager.OpenAISettings, optional): An instance of OpenAISettings containing OpenAI API settings.
            gpt_params (gpt_manager.GPTParamsSettings, optional): An instance of GPTParamsSettings containing GPT-3 parameters settings.
            prompts (Union[prompts.Prompts, str]): Either an instance of Prompts or a path to a YAML file containing conversation prompts and messages.

        """
        self.gpt_manager = gpt_manager.GPTManager(
            gpt_info_path=gpt_info_path, openai_api=openai_api, gpt_params=gpt_params
        )
        if isinstance(prompts, str):
            self.prompts = syphus_prompts.read_yaml(prompts)
        elif isinstance(prompts, syphus_prompts.Prompts):
            self.prompts = prompts
        else:
            raise ValueError("Must provide either prompts yaml path or prompts object")

    def query_single_info(self, info: Info) -> Response:
        """
        Generate a response from the GPT-3 engine based on the provided Info object.

        Args:
            info (Info): An instance of Info containing information for generating the response.

        Returns:
            Response: An instance of Response containing the generated response or error messages.

        """
        messages = self.prompts.get_messages()
        messages.append({"role": "user", "content": info.content})
        try:
            gpt_response = self.gpt_manager.query_gpt(messages)
            response = Response(gpt_response=gpt_response)
        except Exception as e:
            response = Response(gpt_error_messages=str(e))
        return response

    def query_all_infos(
        self, infos: Iterable[Info], *, num_threads: int = 4
    ) -> Iterable[Tuple[str, Optional[Response], Optional[str]]]:
        """
        Generate responses for multiple Info objects using multiple threads.

        Args:
            infos (Iterable[Info]): An iterable containing Info objects to generate responses for.
            num_threads (int, optional): Number of threads to use for concurrent response generation.

        Yields:
            Tuple[str, Optional[Response], Optional[str]]: A tuple containing the Info ID, response, and error message (if any).

        """
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            with tqdm(total=len(infos), desc="Querying GPT") as progress_bar:
                for id, response in executor.map(
                    lambda info: (info.id, self.query_single_info(info)), infos
                ):
                    yield id, response
                    progress_bar.update(1)

    def query_all_infos_and_save(
        self,
        infos: List[Info],
        path,
        *,
        num_threads: int = 4,
        format: str = "json",
        response_file_name: str = "responses",
        error_message_file_name: str = "error_messages",
        full_response_file_name: str = "gpt_full_responses",
        split: bool = True,
    ):
        """
        Generate responses for multiple Info objects, save them to files, and manage different output formats.

        Args:
            infos (List[Info]): An iterable containing Info objects to generate responses for.
            path (str): Path to the directory where the response files will be saved.
            num_threads (int, optional): Number of threads to use for concurrent response generation.
            format (str, optional): Output file format (json, yaml, or jsonl).
            response_file_name (str, optional): Name of the response file.
            error_message_file_name (str, optional): Name of the error message file.
            full_response_file_name (str, optional): Name of the full response file.
            split (bool, optional): Whether to split the responses into separate files.

        Raises:
            ValueError: If an invalid output type or format is provided.

        """
        if format not in ["json", "yaml", "jsonl"]:
            raise ValueError("Invalid format, must be json, yaml, or jsonl")
        if split:
            for id, response in self.query_all_infos(infos, num_threads=num_threads):
                response.save(
                    os.path.join(path, id),
                    format=format,
                    response_file_name=response_file_name,
                    error_message_file_name=error_message_file_name,
                    full_response_file_name=full_response_file_name,
                )
        else:
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
