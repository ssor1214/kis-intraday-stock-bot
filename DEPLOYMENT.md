# Separate bots

`paper_bot/start.bat` runs the mock-only WebSocket bot.

`live_bot/start.bat` is a separate live configuration entry point. It is deliberately locked: the current `LiveBroker` has no order implementation. It exits before sending any order even if credentials exist. Do not remove the lock until KIS order, fill, cancel, position-recovery, and kill-switch tests are complete.

Both modes now use the same `OrderIntent` validation. The paper adapter fills locally; the live adapter rejects while locked.
