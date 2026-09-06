# KIS 국장 초단기 자동매매봇 V0.2

거래비용과 슬리피지를 포함한 순기대값을 검증하기 위한 연구 우선 구조입니다.

## 안전 기본값

- `KIS_MODE=mock`
- `LIVE_TRADING_ENABLED=false`
- 실전 주문 어댑터는 잠금 상태
- `.env`와 비밀키는 커밋하지 않음
- 하루 손실 한도 1%, 거래당 위험 한도 0.30%
- 모의투자 종료일 `2026-09-24`

## 실행

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
pytest
```

## KIS 키 등록

번들 Python으로 `python scripts/setup_kis_env.py`를 실행해 모의 APP KEY/SECRET/계좌번호를 입력합니다. 선택적으로 실전 키도 입력할 수 있지만 `KIS_MODE=mock`, `LIVE_TRADING_ENABLED=false`가 기본값입니다. `.env`는 Git에 포함되지 않습니다. 실전 전환은 키 입력만으로 활성화되지 않으며, 별도 검증 후 두 설정을 명시적으로 변경해야 합니다.

## KIS 연결 검증

`python scripts/verify_kis.py`는 OAuth, 삼성전자(`005930`) 현재가, 잔고 조회만 실행합니다. 주문 API는 호출하지 않습니다. KIS 토큰 발급 제한으로 403이 발생하면 잠시 후 재시도하고, 모의 계좌가 한국투자증권 Open API 모의투자 서비스에 활성화되어 있는지 확인합니다.

구현된 연구 코어는 위험종목/유동성 필터, 자본구간별 총노출 및 성과 방어, Capital Fit 수량계산, Momentum Pullback 점수/트리거, 상태 전이, 비용계산, SL·모멘텀·시간청산, trailing stop, CSV 거래저널을 포함합니다. KIS REST/WebSocket 실연결은 응답 스키마와 모의장 데이터 검증 후 별도 어댑터로 추가합니다. 실전 주문은 계속 잠겨 있습니다.

## 구성 요소

- `safety.py`: 위험종목 hard filter와 유동성/spread 재검사
- `exposure.py`: 150만원 구간 100% 총노출, 자산 증가 및 성과 악화 방어
- `strategy.py`: 100점 Entry Score와 Momentum Pullback trigger
- `risk.py`: SL 기반 Risk/Capital/Cash 수량 제한
- `exits.py`: Hard SL, Momentum Failure, Time Stop, trailing
- `state.py`: 중복 주문 방지를 위한 허용 상태 전이
- `journal.py`: 거래별 비용·MAE/MFE·보유시간 CSV 기록
- `paper_engine.py`: 안전필터부터 모의 진입·청산·Net PnL 저널까지 연결

모의 사이클 확인:

```powershell
python scripts/run_paper_cycle.py
```

KIS 현재가 기반 모의 세션은 장중에 다음처럼 실행합니다. 기본 20회, 30초 간격이며 KIS 주문 API를 호출하지 않습니다.

```powershell
$env:PAPER_SYMBOL="005930"
$env:PAPER_INTERVAL_SECONDS="30"
$env:PAPER_MAX_TICKS="20"
python scripts/run_kis_paper_session.py
```
