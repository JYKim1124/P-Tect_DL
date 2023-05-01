import cv2
import torch
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from io import BytesIO
from MGFN.models.mgfn import mgfn as Model

# 스트리밍 모듈 import
from cv_stream import get_stream_video

# MGFN 모델 불러오기
with torch.no_grad():
    model=Model()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    model = model.to(device)
    model_dict = model.load_state_dict({k.replace('module.', ''): v for k, v in torch.load('C:/Users/nancy/capston/MGFN/mgfn_ucf.pkl', map_location=device).items()})
    model.eval()

app = FastAPI()
#templates = Jinja2Templates(directory="templates")

# 웹캠 스트리밍
def webcam_stream():
    return get_stream_video()

# 이상 점수 예측
def predict_abnormality(frame):
    # 프레임 전처리
    frame = cv2.resize(frame, (64, 2048), interpolation=cv2.INTER_LINEAR)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = torch.tensor(frame, dtype=torch.float).permute(1, 2, 0).unsqueeze(0)


    # 이상 점수 예측
    with torch.no_grad():
        scores, _, _, _, _ = model(frame)

    return scores.item()

# 이상 점수 REST API 노출
@app.get("/score_abnormal")
async def get_score_abnormal():
    return predict_abnormality(cv2.VideoCapture(0).read()[1])




# 웹캠 스트리밍 REST API 노출
@app.get("/")
async def home():
    # StringResponse함수를 return하고,
    # 인자로 OpenCV에서 가져온 "바이트"이미지와 type을 명시
    return StreamingResponse(webcam_stream(), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)