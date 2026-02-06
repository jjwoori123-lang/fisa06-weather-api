import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# 로컬 테스트용 .env 로드 (GitHub Actions 환경에서는 무시됨)
load_dotenv()

# 환경 변수 설정
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Seoul"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# README 파일 경로
README_PATH = "README.md"

def get_weather():
    """OpenWeather API를 호출하여 서울의 날씨 데이터를 가져옴"""
    if not API_KEY:
        return "API 키가 설정되지 않았습니다."
    
    try:
        response = requests.get(URL)
        response.raise_for_status() # 에러 발생 시 예외 처리
        data = response.json()
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        return f"현재 날씨: **{weather}**, 온도: **{temp}°C**, 습도: **{humidity}%**"
    except Exception as e:
        return f"날씨 정보를 가져오는 데 실패했습니다. (에러: {e})"

def update_readme():
    """README.md 파일을 업데이트"""
    weather_info = get_weather()
    # 한국 시간(KST)을 고려한다면 시간을 조정할 수 있지만, 일단 UTC 기준으로 작성
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 문자열 앞의 들여쓰기를 제거한 깔끔한 포맷
    readme_content = f"""# Weather API Status

이 리포지토리는 OpenWeather API를 사용하여 서울의 날씨 정보를 자동으로 업데이트합니다.

## 📍 현재 서울 날씨
> {weather_info}

⏳ 마지막 업데이트: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)
    print(f"성공: {README_PATH} 파일이 업데이트되었습니다.")

if __name__ == "__main__":
    update_readme()