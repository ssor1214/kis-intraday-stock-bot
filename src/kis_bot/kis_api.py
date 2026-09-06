"""Small, mock-first KIS REST adapter. It never submits an order implicitly."""
from dataclasses import dataclass
import time
import requests
from .config import Settings

MOCK_BASE = 'https://openapivts.koreainvestment.com:29443'
LIVE_BASE = 'https://openapi.koreainvestment.com:9443'

@dataclass
class KisClient:
    settings: Settings
    timeout: float = 10.0
    token: str | None = None
    token_expires_at: float = 0

    @property
    def base_url(self) -> str:
        return MOCK_BASE if self.settings.mode == 'mock' else LIVE_BASE

    def authenticate(self) -> str:
        self.settings.validate()
        response = requests.post(self.base_url + '/oauth2/tokenP', json={
            'grant_type': 'client_credentials',
            'appkey': self.settings.app_key,
            'appsecret': self.settings.app_secret,
        }, timeout=self.timeout)
        if not response.ok:
            raise RuntimeError(f'KIS OAuth HTTP {response.status_code}: {response.text[:500]}')
        payload = response.json()
        token = payload.get('access_token')
        if not token:
            raise RuntimeError(f'KIS token response missing access_token: {payload}')
        self.token = token
        self.token_expires_at = time.time() + int(payload.get('expires_in', 86400)) - 60
        return token

    def _headers(self, tr_id: str) -> dict[str, str]:
        if not self.token or time.time() >= self.token_expires_at:
            self.authenticate()
        return {'authorization': f'Bearer {self.token}', 'appkey': self.settings.app_key,
                'appsecret': self.settings.app_secret, 'tr_id': tr_id,
                'content-type': 'application/json; charset=utf-8'}

    def quote(self, symbol: str) -> dict:
        r = requests.get(self.base_url + '/uapi/domestic-stock/v1/quotations/inquire-price',
                         headers=self._headers('FHKST01010100'),
                         params={'FID_COND_MRKT_DIV_CODE':'J', 'FID_INPUT_ISCD':symbol}, timeout=self.timeout)
        return self._json_or_error(r)

    def balance(self) -> dict:
        r = requests.get(self.base_url + '/uapi/domestic-stock/v1/trading/inquire-balance',
                         headers=self._headers('VTTC8434R' if self.settings.mode == 'mock' else 'TTTC8434R'),
                         params={'CANO':self.settings.account_no[:8], 'ACNT_PRDT_CD':'01',
                                 'AFHR_FLPR_YN':'N', 'OFL_YN':'', 'INQR_DVSN':'01',
                                 'UNPR_DVSN':'01', 'FUND_STTL_ICLD_YN':'N', 'FNCG_AMT_AUTO_RDPT_YN':'N',
                                 'PRCS_DVSN':'00', 'CTX_AREA_FK100':'', 'CTX_AREA_NK100':''}, timeout=self.timeout)
        return self._json_or_error(r)

    @staticmethod
    def _json_or_error(response: requests.Response) -> dict:
        if not response.ok:
            raise RuntimeError(f'KIS HTTP {response.status_code}: {response.text[:500]}')
        payload = response.json()
        if payload.get('rt_cd') not in (None, '0'):
            raise RuntimeError(f"KIS API error {payload.get('msg_cd')}: {payload.get('msg1')}")
        return payload

    def submit_order(self, symbol: str, side: str, quantity: int, price: int, *, confirm: bool = False) -> dict:
        if not confirm or self.settings.mode != 'mock' or not self.settings.live_trading_enabled:
            raise PermissionError('order submission is locked; verification only')
        raise NotImplementedError('order submission remains disabled until execution review')
