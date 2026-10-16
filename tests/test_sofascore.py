import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import pytest

from sportlab.data.sofascore import SofaScoreClient, SofaScoreUnavailable, threshold_history


def rows(values):
    return [{"event_id": i, "start_utc": f"2026-10-{i+1:02d}T12:00:00Z", "status": "completed",
             "event_key": "soccer:match:corners:90min", "value": v} for i, v in enumerate(values)]


def trend(values, **kwargs):
    return threshold_history(rows(values), event_key="soccer:match:corners:90min", line=7.5,
                             direction="over", as_of="2026-10-16T00:00:00Z", **kwargs)


def test_eight_of_ten_is_observed_frequency():
    result = trend([8]*8+[6, 7])
    assert (result["wins"], result["observed"], result["observed_hit_rate"]) == (8, 10, .8)


def test_missing_keeps_window_and_is_not_zero():
    result = trend([9]*10+[None], window=10)
    assert result["observed"] == 9
    assert result["missing_event_ids"] == [10]


def test_cutoff_retirement_duplicates_and_push():
    records = rows([8, 9, 7])
    records.append(records[0].copy())
    records[1]["status"] = "decided_without_play"
    result = threshold_history(records, event_key=records[0]["event_key"], line=8,
                               direction="over", as_of="2026-10-03T00:00:00Z")
    assert (result["observed"], result["pushes"], result["wins"]) == (1, 1, 0)


def test_mixed_markets_and_conflicting_duplicates_rejected():
    records = rows([8])
    records.append({**records[0], "value": 9})
    with pytest.raises(ValueError, match="Conflicting"):
        threshold_history(records, event_key=records[0]["event_key"], line=7.5,
                          direction="over", as_of="2026-10-16T00:00:00Z")
    with pytest.raises(ValueError, match="Mixed"):
        threshold_history(rows([8]), event_key="different", line=7.5,
                          direction="over", as_of="2026-10-16T00:00:00Z")


def test_empty_is_unknown():
    assert trend([])["observed_hit_rate"] is None


def test_api_over_http_pagination_statistics_and_error():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            assert self.headers.get("Authorization") == "Bearer test-token"
            if "statistics" in self.path:
                data = {"data": {"state": "ok", "has_payload": True, "payload": {"statistics": []}}}
            elif "cursor=next" in self.path:
                data = {"data": [{"id": 2}], "page": {"next_cursor": None}}
            else:
                data = {"data": [{"id": 1}], "page": {"next_cursor": "next"}}
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        client = SofaScoreClient(f"http://127.0.0.1:{server.server_port}", "test-token")
        assert [e["id"] for e in client.events("NHL")["events"]] == [1, 2]
        assert client.events("NHL", max_pages=1)["truncated"]
        assert client.statistics(1)["state"] == "ok"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
    with pytest.raises(SofaScoreUnavailable):
        client.get("health")


def test_stale_statistics_not_accepted(monkeypatch):
    client = SofaScoreClient()
    monkeypatch.setattr(client, "get", lambda *a, **k: {"data": {"state": "error", "has_payload": True}})
    with pytest.raises(SofaScoreUnavailable):
        client.statistics(1)


def test_remote_http_credentials_rejected():
    with pytest.raises(ValueError):
        SofaScoreClient("http://example.com")
    with pytest.raises(ValueError):
        SofaScoreClient("https://user:secret@example.com")
