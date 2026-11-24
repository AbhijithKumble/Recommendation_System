import os
import zipfile
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
import pandas as pd


class DataIngestor(ABC):
    @abstractmethod
    def ingest(self, file_path: str) -> pd.DataFrame:
        pass


class ZipFileIngestor(DataIngestor):

    def ingest(self, file_path: str) -> List[pd.DataFrame]:
        """
           Extracts a zipfile and returns and pandas DataFrame
        """

        if not file_path.endswith('.zip'):
            raise ValueError("The provided file is not a zip file")

        date_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_path = f'../extracted_data/data_{date_str}'
        os.makedirs(output_path, exist_ok=True)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_path)

        extracted_files = os.listdir(output_path)
        csv_files = [f for f in extracted_files if f.endswith(".csv")]

        if len(csv_files) == 0:
            raise ValueError("No csv files found")
        if len(csv_files) > 3:
            raise ValueError("Too many csv files found")

        if "anime_data.csv" in csv_files:
            anime_df = pd.read_csv(os.path.join(output_path, "anime_data.csv"))
            return [anime_df]
        else:
            return [None]
