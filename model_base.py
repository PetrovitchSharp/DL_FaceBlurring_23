from typing import Any

from pydantic import BaseModel

class BlurringModel(BaseModel):
    def __init__(self, model: Any) -> None:
        '''
        Blurring model initialization

        Args:
            model: Blurring model
        '''
        pass

    def blur_image(self, path_to_image: str) -> str:
        '''
        Blur input photo

        Args:
            path_to_image: Path to saved photo

        Returns:
            Path to blurred photo
        '''
        pass