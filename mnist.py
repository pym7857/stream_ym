import cv2
from tensorflow.keras.models import load_model
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np

@st.cache(allow_output_mutation=True) # streamlit이 웹페이지를 최신상태로 계속 갱신(ReRun)하는 것을 막아줍니다.
def load():
    return load_model('model.h5')
model = load()

st.write('# MNIST Recognizer')

CANVAS_SIZE = 192 # preview이미지 크기(192 x 192)

# 왼쪽 컬럼에는 Canvas가 들어가고, 오른쪽 컬럼에는 Preview(도트 이미지)가 들어갑니다.
col1, col2 = st.beta_columns(2) 

with col1:
    canvas = st_canvas( # canvas 설정하는 곳
        fill_color='#000000',
        stroke_width=20,
        stroke_color='#FFFFFF',
        background_color='#000000',
        width=CANVAS_SIZE,
        height=CANVAS_SIZE,
        drawing_mode='freedraw',
        key='canvas'
    )

if canvas.image_data is not None:
    img = canvas.image_data.astype(np.uint8) # 이미지 데이터 형태로 바꿔줍니다.
    img = cv2.resize(img, dsize=(28, 28)) # mnist데이터 사이즈(28x28)로 바꾸어 줍니다.
    preview_img = cv2.resize(img, dsize=(CANVAS_SIZE, CANVAS_SIZE), interpolation=cv2.INTER_NEAREST) # preview이미지를 다시 192x192로 키워줍니다.

    col2.image(preview_img) # 두번째 컬럼에 preview_img를 넣어줍니다.

    # 모델의 input들을 만드는 과정입니다.
    x = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x = x.reshape((-1, 28, 28, 1))
    y = model.predict(x).squeeze() # 예측을 실행합니다.

    st.write('## Result: %d' % np.argmax(y)) # argmax를 이용해 y를 정수값으로 나타내줍니다.
    st.bar_chart(y) # 막대그래프를 그립니다.