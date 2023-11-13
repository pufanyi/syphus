import os
from .dataset import Dataset
from datasets import load_dataset
from tqdm import tqdm


class M3ITDataset(Dataset):
    def __init__(self, subset: str, cache_folder: str = "./cache"):
        dataset_name = f"M3IT_{subset.upper()}"
        super().__init__(dataset_name)
        self.cache_folder = cache_folder
        self.subset = subset
        hf_data = load_dataset("MMInstruction/M3IT", subset, cache_dir=cache_folder)

        for split, data in hf_data.items():
            for instruction in tqdm(data, desc=f"Loading {split}"):
                image_ids = []
                for image in instruction["image_base64_str"]:
                    image_ids.append(self.add_image_by_base64(image))
                instruction_sentence = instruction["instruction"]
                if instruction["inputs"]:
                    instruction_sentence += "\n" + instruction["inputs"]
                self.add_single_instruction(
                    {
                        "instruction": instruction_sentence,
                        "answer": instruction["outputs"],
                        "image_ids": image_ids,
                        "rel_ins_ids": [],
                    }
                )


def convert(
    subset: str,
    output_folder: str,
    cache_folder: str = "./cache",
    image_format: str = "parquet",
):
    dataset_name = f"M3IT_{subset.upper().replace('-', '')}"
    image_file = os.path.join(output_folder, f"{dataset_name}.json")
    ins_file = os.path.join(output_folder, f"{dataset_name}_instructions.json")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    dataset = M3ITDataset(subset, cache_folder)
    dataset.save_instructions(ins_file)
    dataset.save_images(image_file, format=image_format)
