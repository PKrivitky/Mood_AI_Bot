from openai import AsyncOpenAI
from amplitude import Amplitude, BaseEvent
from config import settings
import logging
from concurrent.futures import ThreadPoolExecutor

openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
amplitude_executor = ThreadPoolExecutor(max_workers=3)
logger = logging.getLogger(__name__)

async def analyze_mood_with_openai(image_base64: str) -> str:
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Определи эмоцию на фото. Ответь одним словом: счастье, грусть, злость, нейтрально, страх, удивление"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }],
            max_tokens=100
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        logger.error(f"OpenAI error: {str(e)}")
        return "неопределенно"

def send_amplitude_event(event_type: str, user_id: int, event_props: dict = None):
    def _send_event():
        try:
            amp = Amplitude(
                api_key=settings.AMPLITUDE_API_KEY,
                server_url=settings.AMPLITUDE_ENDPOINT,
                flush_interval_seconds=1  # Исправленное имя параметра
            )
            
            event = BaseEvent(
                event_type=event_type,
                user_id=str(user_id),
                event_properties=event_props if event_props else {}
            )
            
            amp.track(event)
            amp.flush()
            amp.shutdown()
            
        except Exception as e:
            logger.error(
                f"Amplitude error for event {event_type}: {str(e)}",
                extra={"user_id": user_id, "event_props": event_props}
            )
    
    amplitude_executor.submit(_send_event)