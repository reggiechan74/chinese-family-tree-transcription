"""
Factory for creating stage-specific model instances.
"""
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from models.model_interfaces import TranscriptionModel, ReviewModel, FinalStageModel

from models.stage_model import StageModel
from config.config import get_model_init_params

class ModelFactory:
    """Factory class for creating model instances for each stage."""
    
    @staticmethod
    def create_model(stage: int, model_num: int) -> Union['TranscriptionModel', 'ReviewModel', 'FinalStageModel']:
        """
        Create a model instance for a specific stage and model number.
        
        Each stage's models are completely independent and can use any provider/model.
        The factory ensures proper initialization based on stage requirements,
        but makes no assumptions about which provider/model should be used.
        
        Args:
            stage: Stage number (1-8)
            model_num: Model number within the stage (1-3 for stages 1-4, 1 for stages 5-8)
            
        Returns:
            Model instance appropriate for the stage
            
        Raises:
            ValueError: If stage or model number is invalid
        """
        # Get model configuration for this stage/number
        config = get_model_init_params(stage, model_num)
        
        # Create independent model instance
        # Each instance has its own client and makes its own API calls
        return StageModel(
            provider=config['provider'],
            model_name=config['name'],
            stage=stage,
            model_num=model_num
        )
