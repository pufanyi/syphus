import base64
import io
import os
import pandas as pd
from PIL import Image
from .dataset import Dataset
from tqdm import tqdm


def decode_base64_to_image(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    return image


class MMBenchDataset(Dataset):
    def __init__(self, data_file, sys_prompt="There are several options:"):
        super().__init__("mmbench")

        df = pd.read_csv(data_file, sep="\t")
        data = {}

        def load_from_df(idx, key):
            if key in df.iloc[idx] and not pd.isna(df.iloc[idx][key]):
                return df.iloc[idx][key]
            else:
                return None

        for idx in tqdm(range(len(df))):
            index = self.convert_ins_id(df.iloc[idx]["index"])
            self.add_image_by_base64(df.iloc[idx]["image"])

            question = df.iloc[idx]["question"]
            answer = df.iloc[idx]["answer"] if "answer" in df.iloc[0].keys() else None

            option_candidate = ["A", "B", "C", "D", "E"]
            options = {
                cand: load_from_df(idx, cand)
                for cand in option_candidate
                if load_from_df(idx, cand) is not None
            }
            options_prompt = f"{sys_prompt}\n"
            for key, item in options.items():
                options_prompt += f"{key}. {item}\n"

            contexts = load_from_df(idx, "hint")

            final_question = (
                contexts + " " + question + " " + options_prompt
                if contexts is not None
                else question + " " + options_prompt
            )

            data[index] = {
                "instruction": final_question,
                "answer": answer,
                "image_ids": self.get_image_id(),
                "rel_ins_ids": [],
            }

        self.update_data(data)


def convert(datafile: str, output_folder: str, image_format: str = "parquet"):
    image_file = os.path.join(output_folder, "MMBENCH.json")
    ins_file = os.path.join(output_folder, "MMBENCH_instructions.json")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    dataset = MMBenchDataset(datafile)
    dataset.save_instructions(ins_file)
    dataset.save_images(image_file, format=image_format)
