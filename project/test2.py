import asyncio
import sounddevice
import threading

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

class MyEventHandler(TranscriptResultStreamHandler):
    def __init__(self):
        self.final_transcript = ""
        self.stop_event = threading.Event()  # Event to signal when to stop transcription

    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        for result in results:
            if not result.is_partial:
                for alt in result.alternatives:
                    self.final_transcript += alt.transcript + " "
            else:
                for alt in result.alternatives:
                    print(alt.transcript)

        if self.stop_event.is_set():
            await transcript_event.stream.close()


def key_listener():
    while True:
        key_press = input()
        if key_press.lower() == 'q':
            my_event_handler.stop_event.set()
            break
    print("Recording stopped")


async def mic_stream():
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()

    def callback(indata, frame_count, time_info, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))

    stream = sounddevice.RawInputStream(
        channels=1,
        samplerate=16000,
        callback=callback,
        blocksize=1024 * 2,
        dtype="int16",  # PCM encoded
    )
    with stream:
        key_listener_thread = threading.Thread(target=key_listener, daemon=True)
        key_listener_thread.start()
        while True:
            if my_event_handler.stop_event.is_set():
                break
            indata, status = await input_queue.get()
            yield indata, status


async def write_chunks(stream):
    async for chunk, status in mic_stream():
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
        if my_event_handler.stop_event.is_set():
            break
    await stream.input_stream.end_stream()


async def basic_transcribe():
    global my_event_handler
    my_event_handler = MyEventHandler()
    
    client = TranscribeStreamingClient(region="us-east-1")
    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=16000,
        media_encoding="pcm",
    )
    
    await asyncio.gather(write_chunks(stream), my_event_handler.handle_transcript_event(stream))


loop = asyncio.get_event_loop()
loop.run_until_complete(basic_transcribe())
loop.close()

print("Final Transcript:", my_event_handler.final_transcript)
