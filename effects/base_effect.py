"""
Base class for audio effects.

Defines an abstract interface for all effects.
"""

class BaseEffect:
    """
    Abstract base class for audio effects.
    """

    def __init__(self):
        """
        Initialize the effect.
        """
        # No need for pass here since method is empty and required

    def apply(self, audio_data, sample_rate, **kwargs):
        """
        Apply effect to audio data.

        Args:
            audio_data (np.ndarray): The raw audio data.
            sample_rate (int): The sample rate of the audio.
            **kwargs: Additional parameters for effect.

        Returns:
            np.ndarray: Processed audio data.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_parameter_widgets(self):
        """
        Return parameters for the effect as Streamlit widgets.
        This method should be overridden by subclasses to provide UI controls.

        Returns:
            dict: Effect parameters from widgets.
        """
        return {}
