"""
Echo effect implementation for audio processing.

Provides an audio echo effect as a subclass of BaseEffect.
"""

import numpy as np

from effects.base_effect import BaseEffect


class EchoEffect(BaseEffect):
    """
    Echo effect class to apply echo audio effect.

    Inherits from BaseEffect.
    """

    def apply(self, audio_data, sample_rate, **kwargs):
        """
        Apply the echo effect to audio data.

        Args:
            audio_data (np.ndarray): Input audio data.
            sample_rate (int): Sample rate of the audio.
            **kwargs: Parameters for the echo effect.
                Expected keys:
                - delay (float): Delay time in seconds.
                - decay (float): Decay factor of the echo.

        Returns:
            np.ndarray: Processed audio data with echo effect.

        Raises:
            RuntimeError: If processing fails.
        """
        delay = kwargs.get('delay', 0.2)  # default delay 200 ms
        decay = kwargs.get('decay', 0.5)  # default decay

        try:
            delay_samples = int(delay * sample_rate)
            echo_signal = np.zeros(len(audio_data) + delay_samples)
            echo_signal[:len(audio_data)] = audio_data
            for i, sample in enumerate(audio_data):
                if i + delay_samples < len(echo_signal):
                    echo_signal[i + delay_samples] += decay * sample
            # Normalize to prevent clipping
            max_val = np.max(np.abs(echo_signal))
            if max_val > 1.0:
                echo_signal = echo_signal / max_val
            return echo_signal.astype(np.float32)
        except Exception as e:
            raise RuntimeError(f"Echo effect error: {str(e)}") from e
