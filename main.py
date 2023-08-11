from posixpath import split
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
#from vietTTS.synthesizer import * 
from starlette.responses import RedirectResponse
from pydantic import BaseModel
import re
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os
from pydub import AudioSegment
import io
from fastapi.responses import StreamingResponse
from pydub import AudioSegment
from pydub.playback import play

def amplify_audio(input_path, output_path, amplification_factor):
    audio = AudioSegment.from_file(input_path)
    amplified_audio = audio + (audio * (amplification_factor - 1))
    amplified_audio.export(output_path, format="wav")

APP_DESC = "text-to-speech HHP"

app = FastAPI(title='Text to speech Demo', description=APP_DESC)
app.mount("/output", StaticFiles(directory="output"), name="output")

origins = [
    "http://localhost",
    "http://localhost:3001",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")

class TTSRequest(BaseModel):
    text: str
    voice_id: int
    # volume: int
    #model: str
    
class TTSResponse(BaseModel):
    audio_path : str

def check_len_text(text):
    num_of_char = 1200
    temp = text
    count = 0 
    i = 0
    split_text = []
    while count+num_of_char < len(text):
        x = temp[count:count+num_of_char].rindex(".")
        split_text.append(temp[count:count+x+1])
        #print('------------------------------------')
        count = count + x + 1
        i +=1
    left = temp[count:len(text)]
    split_text.append(left)
    
    return split_text

def change_text(text):
    text = text.lower().strip()
    with open ('dict.txt', 'r') as dic:
        lines = dic.readlines()
        for line in lines:
            x = line.split('|')
            #print(x)
            text = re.sub(x[0],x[1][:-1], text)
    text = text.replace('+', 'cộng ')
    text = text.replace('(', ',(')
    
    return text.strip()


@app.post("/tts")
def TTS(request: TTSRequest):
    voice_id = request.voice_id
    text = change_text(request.text)
    # volume = request.volume
    split_text = check_len_text(text)
    counter = 0
    audio_list = []
    now = datetime.now()
    date_time = now.strftime("%Y_%m_%d_%H_%M_%S_")
    for text in split_text:
        audio_output = 'output/' + date_time + str(counter) + '.wav'
        os.system(
            f'python3 -m vietTTS.synthesizer --text "{text}" --output "{audio_output}" --silence-duration 0.20 --voice-id {voice_id}')
        audio = AudioSegment.from_file(audio_output, format="wav")
        print(audio)
        # Chuẩn hóa mức độ âm lượng
        # normalized_audio = audio.normalize()

        # Tăng âm lượng sau khi đã chuẩn hóa
        if voice_id == 1:
            louder_audio = audio + 9
        elif voice_id ==3:
            louder_audio = audio + 15
        elif voice_id == 4:
            louder_audio = audio +0
        else:
            louder_audio = audio + 7
        print("=================================")
        print(louder_audio)
        # Lưu tệp âm thanh sau khi đã tăng âm lượng
        louder_audio.export(audio_output, format="wav")

        counter += 1
        audio_list.append(audio_output)

    wavs = [AudioSegment.from_wav(wav) for wav in audio_list]
    combined = wavs[0]
    for wav in wavs[1:]:
        combined = combined.append(wav)

    output_buffer = io.BytesIO()
    combined.export(output_buffer, format="wav", parameters=["-ar", "16000"])

    return StreamingResponse(io.BytesIO(output_buffer.getvalue()), media_type="audio/wav")

if __name__ == "__main__":
    uvicorn.run(app, port = 5000, host='0.0.0.0')
#uvicorn main:app --reload
# /mnt/g/download/tts