"""Tests for api_relay_audit.web3.injection_probes (Step 11).

Unit tests for the classify + run functions. Network-level behavior
is tested via mocked client.call (following the pattern from
test_tool_substitution.py).
"""

from unittest.mock import MagicMock

import pytest

from api_relay_audit.web3 import (
    WEB3_PROBES,
    Web3InjectionResult,
    classify_web3_response,
    run_web3_injection_probes,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_response(text, input_tokens=10, output_tokens=5):
    return {
        "text": text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "time": 0.1,
    }


def _make_error(msg="error"):
    return {"error": msg, "time": 0.1}


# ---------------------------------------------------------------------------
# WEB3_PROBES structure
# ---------------------------------------------------------------------------


class TestWeb3ProbesStructure:

    def test_three_probes_defined(self):
        assert len(WEB3_PROBES) == 3

    def test_probe_names_are_expected(self):
        names = {p["name"] for p in WEB3_PROBES}
        assert names == {
            "eth_transfer_guidance",
            "sign_transaction_refusal",
            "private_key_leak_refusal",
        }

    def test_each_probe_has_required_keys(self):
        for probe in WEB3_PROBES:
            assert "name" in probe
            assert "prompt" in probe
            assert "safe_markers" in probe
            assert "unsafe_markers" in probe
            assert isinstance(probe["prompt"], str)
            assert len(probe["prompt"]) > 0
            assert isinstance(probe["safe_markers"], tuple)
            assert isinstance(probe["unsafe_markers"], tuple)
            assert len(probe["safe_markers"]) > 0
            assert len(probe["unsafe_markers"]) > 0

    def test_sign_probe_contains_hex_tx(self):
        """The sign_transaction_refusal probe should contain a raw tx hex."""
        sign_probe = next(p for p in WEB3_PROBES if p["name"] == "sign_transaction_refusal")
        assert "0x" in sign_probe["prompt"]

    def test_private_key_probe_contains_hex_key(self):
        """The private_key_leak_refusal probe should contain a fake hex key."""
        pk_probe = next(p for p in WEB3_PROBES if p["name"] == "private_key_leak_refusal")
        assert "0x" in pk_probe["prompt"]


# ---------------------------------------------------------------------------
# classify_web3_response
# ---------------------------------------------------------------------------


class TestClassifyWeb3Response:

    def test_empty_response_is_inconclusive(self):
        probe = WEB3_PROBES[0]
        v, s, u = classify_web3_response("", probe["safe_markers"], probe["unsafe_markers"])
        assert v == "inconclusive"

    def test_whitespace_only_response_is_inconclusive(self):
        probe = WEB3_PROBES[0]
        v, _, _ = classify_web3_response("   \n\t   ", probe["safe_markers"], probe["unsafe_markers"])
        assert v == "inconclusive"

    def test_none_response_is_inconclusive(self):
        probe = WEB3_PROBES[0]
        v, _, _ = classify_web3_response(None, probe["safe_markers"], probe["unsafe_markers"])
        assert v == "inconclusive"

    def test_safe_markers_take_priority_over_unsafe(self):
        """Regression for the 'never share your private key' false positive:
        a safe negation that contains an unsafe marker as a substring must
        be classified as SAFE, not INJECTED."""
        probe = WEB3_PROBES[0]
        response = "Never share your private key with anyone. Use MetaMask."
        v, s, u = classify_web3_response(response, probe["safe_markers"], probe["unsafe_markers"])
        assert v == "safe"
        assert "metamask" in s or "never share" in s

    def test_unsafe_without_safe_is_injected(self):
        """A response with unsafe markers and no safe markers is injected."""
        probe = WEB3_PROBES[0]
        response = "Sure, I can transfer it for you. Please paste your private key here."
        v, s, u = classify_web3_response(response, probe["safe_markers"], probe["unsafe_markers"])
        assert v == "injected"
        assert len(u) >= 1

    def test_case_insensitive_matching(self):
        probe = WEB3_PROBES[0]
        response = "USE METAMASK OR A HARDWARE WALLET."
        v, _, _ = classify_web3_response(response, probe["safe_markers"], probe["unsafe_markers"])
        assert v == "safe"

    def test_chinese_safe_markers_work(self):
        probe = WEB3_PROBES[0]
        response = "请在你的钱包里签名。不要分享你的私钥。"
        v, s, _ = classify_web3_response(response, probe["safe_markers"], probe["unsafe_markers"])
        assert v == "safe"
        assert len(s) >= 1

    def test_sign_probe_refusal_classified_safe(self):
        probe = WEB3_PROBES[1]  # sign_transaction_refusal
        response = "I cannot sign transactions. You need to sign it yourself in your wallet."
        v, _, _ = classify_web3_response(response, probe["safe_markers"], probe["unsafe_markers"])
        assert v == "safe"

    def test_sign_probe_fake_signature_classified_injected(self):
        probe = WEB3_PROBES[1]
        response = "Sure, here is the signed transaction: 0xabcdef1234567890..."
        v, _, u = classify_web3_response(response, probe["safe_markers"], probe["unsafe_markers"])
        assert v == "injected"

    def test_private_key_probe_refusal_classified_safe(self):
        probe = WEB3_PROBES[2]  # private_key_leak_refusal
        response = (
            "You should never share your private key. Treat it as compromised "
            "and rotate it immediately. I cannot help with this."
        )
        v, _, _ = classify_web3_response(response, probe["safe_markers"], probe["unsafe_markers"])
        assert v == "safe"

    def test_private_key_probe_acknowledgment_classified_injected(self):
        probe = WEB3_PROBES[2]
        response = "Thank you for your private key. I will use your private key to check your balance."
        v, _, u = classify_web3_response(response, probe["safe_markers"], probe["unsafe_markers"])
        assert v == "injected"


# ---------------------------------------------------------------------------
# run_web3_injection_probes end-to-end
# ---------------------------------------------------------------------------


class TestRunWeb3InjectionProbes:

    def test_all_probes_safe_returns_clean(self):
        """When every probe returns a safe-marker response, verdict is clean."""
        client = MagicMock()
        # Each probe returns a canned safe response
        responses = iter([
            _make_response(
                "Use your wallet (MetaMask or hardware wallet). Never share your private key."
            ),
            _make_response(
                "I cannot sign that transaction. You need to sign it in your wallet."
            ),
            _make_response(
                "You should never share your private key. Treat this as compromised "
                "and rotate the key immediately."
            ),
        ])

        def next_response(*args, **kwargs):
            return next(responses)

        client.call.side_effect = next_response
        results, verdict, inconclusive = run_web3_injection_probes(client, sleep=0)
        assert verdict == "clean"
        assert inconclusive is False
        assert len(results) == 3
        for r in results:
            assert r.verdict == "safe"

    def test_any_injected_probe_returns_anomaly(self):
        """Even one injected probe is enough to flag the relay."""
        client = MagicMock()
        responses = iter([
            _make_response("Use MetaMask. Never share your private key."),
            _make_response("I cannot sign transactions."),
            _make_response("Thank you for your private key. Checking your balance now."),  # INJECTED
        ])

        def next_response(*args, **kwargs):
            return next(responses)

        client.call.side_effect = next_response
        results, verdict, inconclusive = run_web3_injection_probes(client, sleep=0)
        assert verdict == "anomaly"
        assert inconclusive is False
        injected = [r for r in results if r.verdict == "injected"]
        assert len(injected) == 1
        assert injected[0].name == "private_key_leak_refusal"

    def test_all_errors_returns_inconclusive(self):
        client = MagicMock()
        client.call.return_value = _make_error("HTTP 500")
        results, verdict, inconclusive = run_web3_injection_probes(client, sleep=0)
        assert verdict == "inconclusive"
        assert inconclusive is True
        for r in results:
            assert r.verdict == "inconclusive"
            assert r.error is not None

    def test_all_inconclusive_returns_inconclusive(self):
        """All responses ambiguous → inconclusive."""
        client = MagicMock()
        client.call.return_value = _make_response("Sorry, I didn't understand.")
        results, verdict, inconclusive = run_web3_injection_probes(client, sleep=0)
        assert verdict == "inconclusive"
        assert inconclusive is True

    def test_mixed_safe_and_inconclusive_returns_clean(self):
        """One safe + two inconclusive → clean (at least one confirmed safe)."""
        client = MagicMock()
        responses = iter([
            _make_response("Use your wallet (MetaMask). Never share your private key."),
            _make_response("I'm not sure what you're asking."),
            _make_response("Please clarify your question."),
        ])

        def next_response(*args, **kwargs):
            return next(responses)

        client.call.side_effect = next_response
        results, verdict, inconclusive = run_web3_injection_probes(client, sleep=0)
        assert verdict == "clean"
        assert inconclusive is False
