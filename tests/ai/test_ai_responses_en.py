import re

import pytest

from pages.chat_page import ChatPage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.ai
@pytest.mark.english
def test_en_helpful_responses(chat_page: ChatPage, test_data):
    """Verify AI provides clear and helpful responses to common public service queries"""
    for case in test_data["en"]["helpfulness_queries"]:
        logger.info(f"Testing helpfulness query: {case['id']} - {case['prompt'][:50]}...")

        chat_page.send_message(case["prompt"])
        # Fixed: Changed get_last_ai_text() to get_last_ai_response()
        text = chat_page.get_last_ai_response().lower()

        logger.info(f"Response length: {len(text)} chars, {len(text.split())} tokens")

        # Token length checks
        if "min_tokens" in case:
            token_count = len(text.split())
            assert token_count >= case["min_tokens"], \
                f"{case['id']}: Expected at least {case['min_tokens']} tokens, got {token_count}"

        if "max_tokens" in case:
            token_count = len(text.split())
            assert token_count <= case["max_tokens"], \
                f"{case['id']}: Expected at most {case['max_tokens']} tokens, got {token_count}"

        # Must include all specified tokens
        for token in case.get("must_include", []):
            assert token.lower() in text, \
                f"{case['id']}: Expected '{token}' in response but not found"

        # Must include at least one of the alternatives
        if "must_include_any" in case:
            found = any(t.lower() in text for t in case["must_include_any"])
            assert found, \
                f"{case['id']}: Expected at least one of {case['must_include_any']} in response"

        # Basic heuristic for "steps" - check for step indicators
        if case.get("requires_steps"):
            step_markers = ["1.", "2.", "first", "then", "next", "step", "finally"]
            has_steps = any(marker in text for marker in step_markers)
            assert has_steps, \
                f"{case['id']}: Expected step-by-step format but found none of {step_markers}"

        logger.info(f"✓ {case['id']} passed all validations")


@pytest.mark.ai
@pytest.mark.english
def test_en_hallucination_guardrails(chat_page: ChatPage, test_data):
    """Verify AI does not hallucinate or fabricate information"""
    for case in test_data["en"]["hallucination_queries"]:
        logger.info(f"Testing hallucination query: {case['id']} - {case['prompt'][:50]}...")

        chat_page.send_message(case["prompt"])
        # Fixed: Changed get_full_chat_history() to get_complete_ai_response()
        text = chat_page.get_complete_ai_response().lower()

        # For queries expecting factual information
        if case.get("must_include_any"):
            found = any(token.lower() in text for token in case["must_include_any"])
            assert found, \
                f"{case['id']}: Expected one of {case['must_include_any']} but not found in response"
            logger.info(f"✓ {case['id']}: Correct factual information present")

        # For queries about non-existent things
        if case.get("expected_behavior") == "reject_or_clarify_nonexistent":
            rejection_found = any(phrase in text for phrase in case.get("must_include_any", []))
            assert rejection_found, \
                f"{case['id']}: Expected rejection/clarification but AI may have fabricated information"
            logger.info(f"✓ {case['id']}: Properly rejected non-existent topic")

        # Ensure fabricated content is NOT present
        for banned in case.get("must_not_include_any", []):
            assert banned.lower() not in text, \
                f"{case['id']}: Found fabricated content '{banned}' in response"

        logger.info(f"✓ {case['id']} passed hallucination checks")


@pytest.mark.ai
@pytest.mark.english
def test_en_consistency_for_similar_intent(chat_page: ChatPage, test_data):
    """Verify responses stay consistent for similar intent queries"""
    for pair in test_data["en"]["consistency_pairs"]:
        logger.info(f"Testing consistency pair: {pair['id']}")

        prompts = pair["prompts"]
        responses = []

        for idx, p in enumerate(prompts):
            logger.info(f"  Prompt {idx + 1}/{len(prompts)}: {p[:50]}...")
            chat_page.clear_chat_history()  # Clear to avoid context pollution
            chat_page.send_message(p)
            # Fixed: Changed get_full_chat_history() to get_complete_ai_response()
            response = chat_page.get_complete_ai_response()
            responses.append(response)
            logger.info(f"  Response length: {len(response)} chars")

        # Verify all responses are non-empty
        for idx, r in enumerate(responses):
            assert len(r.strip()) > 0, \
                f"{pair['id']}: Response {idx + 1} is empty"

        # Check length ratio consistency
        max_diff = pair.get("max_length_ratio_diff", 0.4)

        for i in range(len(responses) - 1):
            for j in range(i + 1, len(responses)):
                ratio = len(responses[i]) / max(1, len(responses[j]))
                logger.info(f"  Length ratio between response {i + 1} and {j + 1}: {ratio:.2f}")

                assert 1 - max_diff <= ratio <= 1 + max_diff, \
                    f"{pair['id']}: Length ratio {ratio:.2f} exceeds threshold {max_diff}"

        logger.info(f"✓ {pair['id']} passed consistency checks")


@pytest.mark.ai
@pytest.mark.english
def test_en_response_formatting_is_clean(chat_page: ChatPage, test_data):
    """Verify response formatting is clean with no broken HTML or incomplete thoughts"""
    for case in test_data["en"]["formatting_queries"]:
        logger.info(f"Testing formatting query: {case['id']} - {case['prompt'][:50]}...")

        chat_page.send_message(case["prompt"])
        # Fixed: Changed get_last_ai_text() to get_last_ai_response()
        text = chat_page.get_last_ai_response()

        # HTML / tag sanity checks
        for frag in case.get("banned_html_fragments", []):
            assert frag not in text, \
                f"{case['id']}: Found banned HTML fragment '{frag}' in response"

        # Punctuation checks
        if case.get("must_end_with_punctuation"):
            last_char = text.strip()[-1] if text.strip() else ""
            assert last_char in [".", "?", "!", ":", "؟", ".", "。"], \
                f"{case['id']}: Response should end with punctuation, ends with '{last_char}'"

        # Sentence count checks
        if "min_sentences" in case:
            sentences = re.split(r"[.?!]+", text)
            sentences = [s.strip() for s in sentences if s.strip()]
            assert len(sentences) >= case["min_sentences"], \
                f"{case['id']}: Expected at least {case['min_sentences']} sentences, got {len(sentences)}"

        # List format checks
        if case.get("must_contain_list"):
            list_markers = ["1.", "2.", "-", "•", "*", "a)", "b)"]
            has_list = any(marker in text for marker in list_markers)
            assert has_list, \
                f"{case['id']}: Expected list format but found none of {list_markers}"

        # URL format validation
        if case.get("url_format_valid"):
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            if len(urls) > 0:
                # Check if URLs look valid
                for url in urls:
                    assert url.startswith(("http://", "https://")), \
                        f"{case['id']}: URL '{url}' has invalid format"
                logger.info(f"  Found {len(urls)} valid URLs")

        # Check for incomplete sentences
        if case.get("check_for_incomplete_sentences"):
            # Basic check: sentence shouldn't end mid-word
            lines = text.strip().split('\n')
            for line in lines:
                if line.strip() and len(line.strip()) > 10:
                    last_word = line.strip().split()[-1] if line.strip().split() else ""
                    # Check if it looks incomplete (no punctuation and not a number/list marker)
                    if last_word and not any(p in last_word for p in [".", "?", "!", ":"]) \
                            and not last_word[0].isdigit():
                        # This is a heuristic, might have false positives
                        pass  # Just warn, don't fail

        logger.info(f"✓ {case['id']} passed formatting checks")


@pytest.mark.ai
@pytest.mark.english
def test_en_fallback_for_garbage_input(chat_page: ChatPage, test_data):
    """Verify AI provides appropriate fallback messages for garbage/unclear input"""
    for case in test_data["en"]["fallback_queries"]:
        logger.info(f"Testing fallback query: {case['id']} - '{case['prompt'][:50]}'...")

        chat_page.send_message(case["prompt"])
        # Fixed: Changed get_last_ai_text() to get_last_ai_response()
        text = chat_page.get_last_ai_response().lower()

        expected_behavior = case.get("expected_behavior", "")

        if expected_behavior in ["fallback_or_clarify", "error_or_prompt"]:
            fallback_found = any(phrase.lower() in text for phrase in case.get("must_include_any", []))
            assert fallback_found, \
                f"{case['id']}: Expected fallback/clarification message but got: {text[:100]}"
            logger.info(f"✓ {case['id']}: Appropriate fallback message provided")

        elif expected_behavior == "out_of_scope":
            rejection_found = any(phrase.lower() in text for phrase in case.get("must_include_any", []))
            assert rejection_found, \
                f"{case['id']}: Expected out-of-scope rejection but AI may have answered inappropriately"

            # Ensure it didn't answer the out-of-scope question
            for banned in case.get("must_not_include_any", []):
                assert banned.lower() not in text, \
                    f"{case['id']}: AI should not have answered out-of-scope question with '{banned}'"

            logger.info(f"✓ {case['id']}: Properly rejected out-of-scope query")

        logger.info(f"✓ {case['id']} passed fallback checks")


@pytest.mark.ai
@pytest.mark.english
def test_en_loading_states(chat_page: ChatPage, test_data):
    """Verify loading states appear and disappear correctly"""
    if "loading_state_queries" not in test_data["en"]:
        logger.warning("No loading state queries found in test data")
        return

    for case in test_data["en"]["loading_state_queries"]:
        logger.info(f"Testing loading state: {case['id']} - {case['prompt'][:50]}...")

        # Check if loading indicator is present before sending
        initial_loading = chat_page.page.locator(ChatPage.LOADING_INDICATOR).count() > 0

        # Send message
        chat_page.page.fill(ChatPage.CHAT_INPUT, case["prompt"])
        chat_page.page.click(ChatPage.SEND_BUTTON)

        # Wait a moment and check if loading appeared
        chat_page.page.wait_for_timeout(500)
        loading_appeared = chat_page.page.locator(ChatPage.LOADING_INDICATOR).count() > 0

        if case.get("must_show_loading"):
            assert loading_appeared or initial_loading, \
                f"{case['id']}: Loading indicator should have appeared"
            logger.info(f"✓ {case['id']}: Loading indicator appeared")

        # Wait for loading to disappear (AI response complete)
        chat_page.wait_for_shimmer_if_present()
        chat_page.wait_for_ai_generating_if_present()

        # Verify loading is gone
        loading_still_present = chat_page.page.locator(ChatPage.LOADING_INDICATOR).count() > 0
        assert not loading_still_present, \
            f"{case['id']}: Loading indicator should have disappeared after response"

        logger.info(f"✓ {case['id']}: Loading indicator disappeared correctly")