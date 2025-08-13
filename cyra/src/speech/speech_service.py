"""
Speech Service - Handle text-to-speech and speech-to-text using Azure Speech Services
"""
import asyncio
import logging
import tempfile
import wave
from typing import Optional, AsyncGenerator

try:
    import azure.cognitiveservices.speech as speechsdk
    AZURE_SPEECH_AVAILABLE = True
except (ImportError, FileNotFoundError, OSError) as e:
    speechsdk = None
    AZURE_SPEECH_AVAILABLE = False
    import logging
    logging.getLogger(__name__).warning(f"Azure Speech SDK not available: {e}")

from src.core.config import get_settings

logger = logging.getLogger(__name__)


class SpeechService:
    """Handle speech-to-text and text-to-speech operations"""
    
    def __init__(self):
        self.settings = get_settings()
        
        if not AZURE_SPEECH_AVAILABLE:
            logger.warning("Azure Speech Services not available. Speech features will be disabled.")
            self.speech_config = None
            return
        
        try:
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.settings.azure_speech_key,
                region=self.settings.azure_speech_region
            )
            
            # Configure voice settings for a professional, friendly female voice
            self.speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"
            self.speech_config.speech_recognition_language = "en-US"
            
            # Configure for high quality audio
            self.speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
            )
        except Exception as e:
            logger.error(f"Failed to initialize speech config: {e}")
            self.speech_config = None
    
    async def text_to_speech(self, text: str) -> Optional[bytes]:
        """
        Convert text to speech and return audio bytes
        """
        if not AZURE_SPEECH_AVAILABLE or not self.speech_config:
            logger.warning("Speech synthesis not available")
            return None
            
        try:
            # Create a synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
            
            # Use SSML for better voice control
            ssml_text = f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
                <voice name="en-US-AriaNeural">
                    <prosody rate="0.9" pitch="+2Hz">
                        {text}
                    </prosody>
                </voice>
            </speak>
            """
            
            # Synthesize speech
            result = synthesizer.speak_ssml_async(ssml_text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info("Speech synthesis completed successfully")
                return result.audio_data
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                logger.error(f"Speech synthesis canceled: {cancellation_details.reason}")
                if cancellation_details.error_details:
                    logger.error(f"Error details: {cancellation_details.error_details}")
                return None
            
        except Exception as e:
            logger.error(f"Error in text-to-speech: {str(e)}")
            return None
    
    async def speech_to_text_continuous(self) -> AsyncGenerator[str, None]:
        """
        Continuous speech recognition that yields recognized text
        """
        try:
            # Configure audio input
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config, 
                audio_config=audio_config
            )
            
            # Event handlers for continuous recognition
            done = False
            results = []
            
            def handle_final_result(evt):
                if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    results.append(evt.result.text)
                    logger.info(f"Recognized: {evt.result.text}")
            
            def handle_canceled(evt):
                nonlocal done
                logger.info(f"Recognition canceled: {evt.result.cancellation_details.reason}")
                done = True
            
            def handle_stopped(evt):
                nonlocal done
                logger.info("Recognition stopped")
                done = True
            
            # Connect event handlers
            speech_recognizer.recognized.connect(handle_final_result)
            speech_recognizer.canceled.connect(handle_canceled)
            speech_recognizer.session_stopped.connect(handle_stopped)
            
            # Start continuous recognition
            speech_recognizer.start_continuous_recognition_async()
            
            # Keep yielding results until stopped
            while not done:
                await asyncio.sleep(0.1)
                if results:
                    yield results.pop(0)
            
            # Stop recognition
            speech_recognizer.stop_continuous_recognition_async()
            
        except Exception as e:
            logger.error(f"Error in continuous speech recognition: {str(e)}")
            yield f"Error: {str(e)}"
    
    async def speech_to_text_single(self) -> Optional[str]:
        """
        Single shot speech recognition
        """
        try:
            # Configure audio input
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config, 
                audio_config=audio_config
            )
            
            logger.info("Listening for speech...")
            result = speech_recognizer.recognize_once_async().get()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                logger.info(f"Recognized: {result.text}")
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                logger.warning("No speech could be recognized")
                return None
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                logger.error(f"Speech recognition canceled: {cancellation_details.reason}")
                if cancellation_details.error_details:
                    logger.error(f"Error details: {cancellation_details.error_details}")
                return None
                
        except Exception as e:
            logger.error(f"Error in speech recognition: {str(e)}")
            return None
    
    def get_available_voices(self) -> list:
        """
        Get list of available voices for synthesis
        """
        try:
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
            result = synthesizer.get_voices_async().get()
            
            if result.reason == speechsdk.ResultReason.VoicesListRetrieved:
                voices = []
                for voice in result.voices:
                    voices.append({
                        "name": voice.name,
                        "display_name": voice.display_name,
                        "gender": voice.gender.name,
                        "locale": voice.locale
                    })
                return voices
            else:
                logger.error("Failed to retrieve voices list")
                return []
                
        except Exception as e:
            logger.error(f"Error getting available voices: {str(e)}")
            return []
    
    async def save_audio_to_file(self, audio_data: bytes, filename: str) -> bool:
        """
        Save audio data to a file
        """
        try:
            with open(filename, 'wb') as audio_file:
                audio_file.write(audio_data)
            logger.info(f"Audio saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving audio to file: {str(e)}")
            return False
