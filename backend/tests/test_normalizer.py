from app.services.normalizer import fingerprint, normalize_message


def test_normalize_masks_volatile_tokens():
    msg = "User 12345 failed from 10.0.0.1 at 0xDEADBEEF"
    assert normalize_message(msg) == "user <num> failed from <ip> at <hex>"


def test_similar_messages_share_fingerprint():
    a = fingerprint("api", "Timeout connecting to db after 30 ms")
    b = fingerprint("api", "Timeout connecting to db after 45 ms")
    assert a == b


def test_different_services_differ():
    a = fingerprint("api", "connection refused")
    b = fingerprint("worker", "connection refused")
    assert a != b
