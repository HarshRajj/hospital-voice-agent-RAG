import asyncio
import logging
from livekit import agents
from livekit.agents import AgentSession, RoomInputOptions
from livekit.plugins import openai, cartesia, deepgram, silero, elevenlabs

from src.core.config import load_config, get_project_dirs
from src.core.indexing import load_or_create_index
from src.agents.voice_agent import Assistant

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

async def entrypoint(ctx: agents.JobContext):
    try:
        # Load configuration and index
        config = load_config()
        dirs = get_project_dirs()
        
        # Load or create index with error handling
        try:
            index = load_or_create_index(dirs["persist_dir"], dirs["data_dir"])
            logging.info(f"Index loaded in main.py with vector store: {type(index.vector_store)}")
        except Exception as e:
            logging.error(f"Failed to load or create index: {str(e)}")
            return

        # Connect to LiveKit
        await ctx.connect()

        # Initialize session with error handling
        try:
            session = AgentSession(
                stt=deepgram.STT(model="nova-3", language="multi"),
                llm=openai.LLM(model="gpt-4o"),
                tts=elevenlabs.TTS(
                    voice_id="Xb7hH8MSUJpSbSDYk0k2",
                    # voice_id="pzxut4zZz4GImZNlqQ3H",
                    model="eleven_multilingual_v2"
                ),
                vad=silero.VAD.load(),
                
            )
        except Exception as e:
            logging.error(f"Failed to initialize session: {str(e)}")
            return

        # Initialize agent with error handling
        try:
            agent = Assistant(session=session, index=index)
        except Exception as e:
            logging.error(f"Failed to initialize Assistant: {str(e)}")
            return

        # Start session with error handling
        try:
            await session.start(
                room=ctx.room,
                agent=agent,
                room_input_options=RoomInputOptions(),
            )
        except Exception as e:
            logging.error(f"Failed to start session: {str(e)}")
            return

        # Initial greeting
        await session.generate_reply(
        instructions="Hello, welcome to [Hospital Name]. How may I assist you today?"
        )

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
    except Exception as e:
        logging.error(f"Failed to run LiveKit worker: {str(e)}")