"""KIS domestic stock websocket adapter (market data only)."""
import json
import requests
import websocket
from .config import Settings

WS_MOCK = 'ws://ops.koreainvestment.com:31000'
WS_LIVE = 'ws://ops.koreainvestment.com:21000'

class KisMarketStream:
    def __init__(self, settings: Settings, symbols: list[str], on_message, timeout: float = 10):
        self.settings, self.symbols, self.on_message, self.timeout = settings, symbols, on_message, timeout
        self.ws = None

    def approval_key(self) -> str:
        self.settings.validate()
        base = 'https://openapivts.koreainvestment.com:29443' if self.settings.mode == 'mock' else 'https://openapi.koreainvestment.com:9443'
        r = requests.post(base + '/oauth2/Approval', json={
            'grant_type': 'client_credentials', 'appkey': self.settings.app_key,
            'secretkey': self.settings.app_secret}, timeout=self.timeout)
        if not r.ok: raise RuntimeError(f'KIS websocket approval HTTP {r.status_code}: {r.text[:300]}')
        key = r.json().get('approval_key')
        if not key: raise RuntimeError('KIS websocket approval_key missing')
        return key

    def connect(self) -> None:
        self.ws = websocket.create_connection(WS_MOCK if self.settings.mode == 'mock' else WS_LIVE, timeout=self.timeout)
        key = self.approval_key()
        for symbol in self.symbols:
            for tr_id in ('H0STCNT0', 'H0STASP0'):
                self.ws.send(json.dumps({'header': {'approval_key': key, 'custtype': 'P', 'tr_type': '1', 'content-type': 'utf-8'},
                    'body': {'input': {'tr_id': tr_id, 'tr_key': 'J' + symbol}}}))

    def run_once(self) -> dict:
        if self.ws is None: self.connect()
        raw = self.ws.recv()
        if isinstance(raw, bytes): raw = raw.decode('utf-8', errors='replace')
        if raw.startswith('0|'):
            self.on_message(raw)
            return {'raw': raw}
        try: payload = json.loads(raw)
        except json.JSONDecodeError: return {'raw': raw}
        self.on_message(payload)
        return payload

    def close(self) -> None:
        if self.ws: self.ws.close(); self.ws = None
