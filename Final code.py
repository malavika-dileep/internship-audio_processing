import speech_recognition as sr
import wave
import os
import time

# Function to transcribe audio using PocketSphinx

def transcribe_audio_pocketsphinx(audio_path):
    intime=time.time()
    recognizer = sr.Recognizer()
    transcript = ""

    # Chunk the audio into smaller portions
    chunk_size_seconds = 30  # You can adjust the chunk size as needed

    with sr.AudioFile(audio_path) as source:
        total_duration = source.DURATION

    start_time = 0
    while start_time < total_duration:
        with sr.AudioFile(audio_path) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source, offset=start_time, duration=chunk_size_seconds)

        try:
            partial_transcript = recognizer.recognize_sphinx(audio)
            #print(partial_transcript)
            transcript += partial_transcript + " "
        except sr.UnknownValueError:
            print(f"Could not understand audio chunk starting at {start_time} seconds")
        except Exception as e:
            print(f"Error processing audio chunk at {start_time} seconds:", str(e))

        start_time += chunk_size_seconds

    outtime=time.time()
    print("Time taken by transcribing function : ",outtime-intime)

    return transcript


# Function to format time as MM:SS
def format_time(minutes, seconds):
    return f"{int(minutes):02d}:{int(seconds):02d}"
    

# Function to find the timestamp of the keyword in the transcript
def find_keyword_timestamp(transcript, keyword, total_duration, chunk_size_seconds=30):
    intime=time.time()
    # Calculate the timestamp for the keyword
    keyword_position = transcript.lower().find(keyword.lower())
    if keyword_position != -1:
        # Calculate the timestamp of the keyword
        keyword_timestamp = (keyword_position / len(transcript)) * total_duration

        # Convert to minutes and seconds
        minutes = int(keyword_timestamp) // 60
        seconds = int(keyword_timestamp) % 60
        outtime=time.time()
        print("Time taken to find keyword : ",outtime-intime)

        return format_time(minutes, seconds)
    else:
        outtime=time.time()
        print("Time taken to search for keyword : ",outtime-intime)
        return None



# Function to extract audio around the keyword and save it to a new file
def extract_audio_around_keyword(audio_path, minutes, seconds, output_audio_path, duration=4):
    intime=time.time()
    # Convert minutes and seconds to total seconds
    total_seconds = minutes * 60 + seconds

    with wave.open(audio_path, 'rb') as wav:
        # Get audio parameters
        sample_width = wav.getsampwidth()
        frame_rate = wav.getframerate()
        num_channels = wav.getnchannels()

        # Calculate start and end frames for the extraction
        start_frame = int((total_seconds - duration / 2) * frame_rate)
        end_frame = int((total_seconds + duration / 2) * frame_rate)

        # Read frames and extract audio
        wav.setpos(start_frame)
        frames = wav.readframes(end_frame - start_frame)

        # Save the extracted audio to a new file
        with wave.open(output_audio_path, 'wb') as output_wav:
            output_wav.setnchannels(num_channels)
            output_wav.setsampwidth(sample_width)
            output_wav.setframerate(frame_rate)
            output_wav.writeframes(frames)
        outtime=time.time()
        print("Time taken to extract and save : ",outtime-intime)

if __name__ == "__main__":
    input_audio = "D:\\Desktop folder\\Malavika Dileep\\Malu\\Quest internship\\Audio files\\audiofile3.wav"  # Path to the WAV audio file



    try:
        transcript = transcribe_audio_pocketsphinx(input_audio)
        print("Transcription:")
        print(transcript)
        with sr.AudioFile(input_audio) as source:
            total_duration = source.DURATION

        keyword = input("Enter the text you want to search for: ")

        if keyword in transcript:
            print("Keyword found")
            keyword_timestamp = find_keyword_timestamp(transcript, keyword, total_duration)
            if keyword_timestamp is not None:
                print("Keyword timestamp:", keyword_timestamp)

                # Extract 4 seconds around the keyword
                minutes, seconds = map(int, keyword_timestamp.split(':'))
                output_audio_path = "output_audio.wav"
                extract_audio_around_keyword(input_audio, minutes, seconds, output_audio_path)

                print("Audio around the keyword extracted and saved to", output_audio_path)
            else:
                print("Unable to determine the keyword timestamp.")
        else:
            print("Keyword not found")
    except Exception as e:
        print("Error:", str(e))


