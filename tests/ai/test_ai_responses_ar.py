import re

import pytest

from pages.chat_page import ChatPage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.ai
@pytest.mark.arabic
def test_ar_helpful_responses(chat_page: ChatPage, test_data):
    """Verify AI provides clear and helpful responses in Arabic"""
    chat_page.switch_language("ar")
    chat_page.page.wait_for_timeout(1000)

    for case in test_data["ar"]["helpfulness_queries"]:
        logger.info(f"Testing Arabic helpfulness query: {case['id']} - {case['prompt'][:50]}...")

        chat_page.clear_chat_history()
        chat_page.send_message(case["prompt"])
        # Fixed: Changed get_full_chat_history() to get_complete_ai_response()
        text = chat_page.get_complete_ai_response()

        logger.info(f"Response length: {len(text)} chars")

        # Token length checks
        if "min_tokens" in case:
            token_count = len(text.split())
            assert token_count >= case["min_tokens"], \
                f"{case['id']}: Expected at least {case['min_tokens']} tokens, got {token_count}"

        # Must include all specified Arabic tokens
        for token in case.get("must_include", []):
            assert token in text, \
                f"{case['id']}: Expected '{token}' in Arabic response but not found"

        # Must include at least one of the alternatives
        if "must_include_any" in case:
            found = any(t in text for t in case["must_include_any"])
            assert found, \
                f"{case['id']}: Expected at least one of {case['must_include_any']} in response"

        # Check for step-by-step format
        if case.get("requires_steps"):
            step_markers = ["1.", "2.", "أولاً", "ثانياً", "أولا", "ثانيا", "الخطوة"]
            has_steps = any(marker in text for marker in step_markers)
            assert has_steps, \
                f"{case['id']}: Expected step-by-step format in Arabic"

        logger.info(f"✓ {case['id']} passed all validations")


@pytest.mark.ai
@pytest.mark.arabic
def test_ar_hallucination_guardrails(chat_page: ChatPage, test_data):
    """Verify AI does not hallucinate or fabricate information in Arabic"""
    chat_page.switch_language("ar")
    chat_page.page.wait_for_timeout(1000)

    for case in test_data["ar"]["hallucination_queries"]:
        logger.info(f"Testing Arabic hallucination query: {case['id']} - {case['prompt'][:50]}...")

        chat_page.clear_chat_history()
        chat_page.send_message(case["prompt"])
        text = chat_page.get_complete_ai_response()

        # For queries expecting factual information
        if case.get("must_include_any"):
            found = any(token in text for token in case["must_include_any"])
            assert found, \
                f"{case['id']}: Expected one of {case['must_include_any']} but not found"
            logger.info(f"✓ {case['id']}: Correct factual information in Arabic")

        # For queries about non-existent things
        if case.get("expected_behavior") == "reject_or_clarify_nonexistent":
            rejection_found = any(phrase in text for phrase in case.get("must_include_any", []))
            assert rejection_found, \
                f"{case['id']}: Expected rejection in Arabic but AI may have fabricated"
            logger.info(f"✓ {case['id']}: Properly rejected non-existent topic in Arabic")

        # Ensure fabricated content is NOT present
        for banned in case.get("must_not_include_any", []):
            assert banned not in text, \
                f"{case['id']}: Found fabricated Arabic content '{banned}' in response"

        logger.info(f"✓ {case['id']} passed hallucination checks")


@pytest.mark.ai
@pytest.mark.arabic
def test_ar_consistency_same_language(chat_page: ChatPage, test_data):
    """Verify responses stay consistent for similar intent queries in Arabic"""
    chat_page.switch_language("ar")
    chat_page.page.wait_for_timeout(1000)

    # Find Arabic-only consistency tests
    for pair in test_data["ar"]["consistency_pairs"]:
        # Skip cross-language tests
        if pair.get("cross_language"):
            continue

        if "prompts" not in pair:
            continue

        logger.info(f"Testing Arabic consistency pair: {pair['id']}")

        prompts = pair["prompts"]
        responses = []

        for idx, p in enumerate(prompts):
            logger.info(f"  Arabic prompt {idx + 1}/{len(prompts)}: {p[:50]}...")
            chat_page.clear_chat_history()
            chat_page.send_message(p)
            response = chat_page.get_complete_ai_response()
            responses.append(response)
            logger.info(f"  Response length: {len(response)} chars")

        # Verify all responses are non-empty
        for idx, r in enumerate(responses):
            assert len(r.strip()) > 0, \
                f"{pair['id']}: Arabic response {idx + 1} is empty"

        # Check length ratio consistency
        max_diff = pair.get("max_length_ratio_diff", 0.4)

        for i in range(len(responses) - 1):
            for j in range(i + 1, len(responses)):
                ratio = len(responses[i]) / max(1, len(responses[j]))
                logger.info(f"  Length ratio: {ratio:.2f}")

                assert 1 - max_diff <= ratio <= 1 + max_diff, \
                    f"{pair['id']}: Length ratio {ratio:.2f} exceeds threshold"

        logger.info(f"✓ {pair['id']} passed consistency checks")


@pytest.mark.ai
@pytest.mark.arabic
def test_en_ar_intent_consistency(chat_page: ChatPage, test_data):
    """Verify responses stay consistent for similar intent in English vs Arabic (cross-language)"""

    # Find cross-language consistency tests
    for pair in test_data["ar"]["consistency_pairs"]:
        if not pair.get("cross_language"):
            continue

        if "en_prompt" not in pair or "ar_prompt" not in pair:
            continue

        logger.info(f"Testing cross-language consistency: {pair['id']}")

        # Test English
        logger.info(f"  Testing English: {pair['en_prompt'][:50]}...")
        chat_page.switch_language("en")
        chat_page.page.wait_for_timeout(1000)
        chat_page.clear_chat_history()
        chat_page.send_message(pair["en_prompt"])
        # Fixed: Changed get_last_ai_text() to get_last_ai_response()
        en_text = chat_page.get_last_ai_response()
        logger.info(f"  English response: {len(en_text)} chars")

        # Test Arabic
        logger.info(f"  Testing Arabic: {pair['ar_prompt'][:50]}...")
        chat_page.switch_language("ar")
        chat_page.page.wait_for_timeout(1000)
        chat_page.clear_chat_history()
        chat_page.send_message(pair["ar_prompt"])
        # Fixed: Changed get_last_ai_text() to get_last_ai_response()
        ar_text = chat_page.get_last_ai_response()
        logger.info(f"  Arabic response: {len(ar_text)} chars")

        # Verify both responses are non-empty
        assert len(en_text.strip()) > 0, f"{pair['id']}: English response is empty"
        assert len(ar_text.strip()) > 0, f"{pair['id']}: Arabic response is empty"

        # Check length ratio consistency
        ratio = len(en_text) / max(1, len(ar_text))
        max_diff = pair.get("max_length_ratio_diff", 0.4)

        logger.info(f"  Cross-language length ratio: {ratio:.2f}")
        assert 1 - max_diff <= ratio <= 1 + max_diff, \
            f"{pair['id']}: Cross-language ratio {ratio:.2f} exceeds threshold {max_diff}"

        logger.info(f"✓ {pair['id']} passed cross-language consistency checks")


@pytest.mark.ai
@pytest.mark.arabic
def test_ar_response_formatting_is_clean(chat_page: ChatPage, test_data):
    """Verify Arabic response formatting is clean with no broken HTML"""
    chat_page.switch_language("ar")
    chat_page.page.wait_for_timeout(1000)

    for case in test_data["ar"]["formatting_queries"]:
        logger.info(f"Testing Arabic formatting: {case['id']} - {case['prompt'][:50]}...")

        chat_page.clear_chat_history()
        chat_page.send_message(case["prompt"])
        text = chat_page.get_last_ai_response()

        # HTML / tag sanity checks
        for frag in case.get("banned_html_fragments", []):
            assert frag not in text, \
                f"{case['id']}: Found banned HTML fragment '{frag}' in Arabic response"

        # Arabic punctuation checks
        if case.get("must_end_with_punctuation"):
            last_char = text.strip()[-1] if text.strip() else ""
            assert last_char in [".", "?", "!", ":", "؟", ".", "。", "،"], \
                f"{case['id']}: Arabic response should end with punctuation, ends with '{last_char}'"

        # Sentence count checks
        if "min_sentences" in case:
            # Split by Arabic and English punctuation
            sentences = re.split(r"[.?!؟]+", text)
            sentences = [s.strip() for s in sentences if s.strip()]
            assert len(sentences) >= case["min_sentences"], \
                f"{case['id']}: Expected at least {case['min_sentences']} sentences, got {len(sentences)}"

        # List format checks
        if case.get("must_contain_list"):
            list_markers = ["1.", "2.", "-", "•", "*", "أ)", "ب)", "١.", "٢."]
            has_list = any(marker in text for marker in list_markers)
            assert has_list, \
                f"{case['id']}: Expected list format in Arabic response"

        # URL format validation
        if case.get("url_format_valid"):
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            if len(urls) > 0:
                for url in urls:
                    assert url.startswith(("http://", "https://")), \
                        f"{case['id']}: URL '{url}' has invalid format"
                logger.info(f"  Found {len(urls)} valid URLs in Arabic response")

        # Must contain certain content
        if case.get("must_contain_any"):
            found = any(content in text for content in case["must_contain_any"])
            assert found, \
                f"{case['id']}: Expected one of {case['must_contain_any']} in Arabic response"

        logger.info(f"✓ {case['id']} passed Arabic formatting checks")


@pytest.mark.ai
@pytest.mark.arabic
def test_ar_fallback_for_garbage_input(chat_page: ChatPage, test_data):
    """Verify AI provides appropriate fallback messages in Arabic for garbage input"""
    chat_page.switch_language("ar")
    chat_page.page.wait_for_timeout(1000)

    for case in test_data["ar"]["fallback_queries"]:
        logger.info(f"Testing Arabic fallback: {case['id']} - '{case['prompt'][:50]}'...")

        chat_page.clear_chat_history()
        chat_page.send_message(case["prompt"])
        text = chat_page.get_last_ai_response()

        expected_behavior = case.get("expected_behavior", "")

        if expected_behavior in ["fallback_or_clarify", "error_or_prompt"]:
            fallback_found = any(phrase in text for phrase in case.get("must_include_any", []))
            assert fallback_found, \
                f"{case['id']}: Expected Arabic fallback message but got: {text[:100]}"
            logger.info(f"✓ {case['id']}: Appropriate Arabic fallback provided")

        elif expected_behavior == "out_of_scope":
            rejection_found = any(phrase in text for phrase in case.get("must_include_any", []))
            assert rejection_found, \
                f"{case['id']}: Expected Arabic out-of-scope rejection"

            # Ensure it didn't answer the out-of-scope question
            for banned in case.get("must_not_include_any", []):
                assert banned not in text, \
                    f"{case['id']}: AI should not have answered in Arabic with '{banned}'"

            logger.info(f"✓ {case['id']}: Properly rejected out-of-scope query in Arabic")

        logger.info(f"✓ {case['id']} passed Arabic fallback checks")


@pytest.mark.ai
@pytest.mark.arabic
def test_ar_loading_states(chat_page: ChatPage, test_data):
    """Verify loading states work correctly with Arabic language"""
    chat_page.switch_language("ar")
    chat_page.page.wait_for_timeout(1000)

    if "loading_state_queries" not in test_data["ar"]:
        logger.warning("No Arabic loading state queries found in test data")
        return

    for case in test_data["ar"]["loading_state_queries"]:
        logger.info(f"Testing Arabic loading state: {case['id']}")

        chat_page.clear_chat_history()

        # Check initial state
        initial_loading = chat_page.page.locator(ChatPage.LOADING_INDICATOR).count() > 0

        # Send message
        chat_page.page.fill(ChatPage.CHAT_INPUT, case["prompt"])
        chat_page.page.click(ChatPage.SEND_BUTTON)

        # Wait and check if loading appeared
        chat_page.page.wait_for_timeout(500)
        loading_appeared = chat_page.page.locator(ChatPage.LOADING_INDICATOR).count() > 0

        if case.get("must_show_loading"):
            assert loading_appeared or initial_loading, \
                f"{case['id']}: Loading indicator should appear for Arabic"
            logger.info(f"✓ {case['id']}: Arabic loading indicator appeared")

        # Wait for completion
        chat_page.wait_for_shimmer_if_present()
        chat_page.wait_for_ai_generating_if_present()

        # Verify loading disappeared
        loading_still_present = chat_page.page.locator(ChatPage.LOADING_INDICATOR).count() > 0
        assert not loading_still_present, \
            f"{case['id']}: Loading should disappear after Arabic response"

        logger.info(f"✓ {case['id']}: Arabic loading indicator disappeared correctly")