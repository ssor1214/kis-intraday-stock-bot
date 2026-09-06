import pytest
from kis_bot.account_guard import ExposureManager
def test_account_exposure():
    a=ExposureManager(10_000_000); a.reserve('A',3_000_000); assert not a.can_open('B',3_000_000); a.release('A',3_000_000,3_030_000); assert a.cash==10_030_000
    with pytest.raises(ValueError): a.release('A',1,1)
