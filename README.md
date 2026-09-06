# KIS 국장 초단기 자동매매봇 V0.2

거래비용과 슬리피지를 포함한 순기대값을 검증하기 위한 연구 우선 구조입니다.

## 안전 기본값

- `KIS_MODE=mock`
- `LIVE_TRADING_ENABLED=false`
- 실전 주문 어댑터는 잠금 상태
- `.env`와 비밀키는 커밋하지 않음
- 하루 손실 한도 1%, 거래당 위험 한도 0.30%

## 실행

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
pytest
```

현재 구현은 위험관리·수량계산·비용필터·상태·모의주문 기반입니다. KIS REST/WebSocket 실연결은 응답 스키마와 모의장 데이터 검증 후 별도 어댑터로 추가합니다.
