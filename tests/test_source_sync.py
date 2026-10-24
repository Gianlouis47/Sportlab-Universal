from datetime import date, datetime, timezone

from sportlab.data.source_sync import collect, snapshot


def test_atp_tournament_never_becomes_individual_match():
    urls = []
    def fetch(url):
        urls.append(url)
        return {"events": [{"id": "123", "name": "Shanghai"}]}
    rows, errors = collect(["ATP"], [date(2026, 10, 15)], fetch=fetch)
    assert not errors and len(rows) == 1 and len(urls) == 1


def test_failed_provider_does_not_erase_successful_reads():
    def fetch(url):
        if "hockey" in url:
            raise OSError("HTTP 403")
        return {"events": []}
    rows, errors = collect(["NHL", "MLB"], [date(2026, 10, 15)], fetch=fetch)
    assert len(rows) == 1 and len(errors) == 1
    assert rows[0]["resource_key"].startswith("MLB/")


def test_payload_hash_ignores_json_key_order():
    now = datetime.now(timezone.utc)
    assert snapshot("k", "u", {"a": 1, "b": 2}, now)["payload_hash"] == snapshot("k", "u", {"b": 2, "a": 1}, now)["payload_hash"]
