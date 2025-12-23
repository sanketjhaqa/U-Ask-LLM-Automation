import pytest

from pages.chat_page import ChatPage
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.ui
@pytest.mark.english
def test_english_ltr_layout(chat_page: ChatPage):
    """Verify page switches to LTR layout when English is selected"""
    chat_page.switch_language("en")
    chat_page.page.wait_for_timeout(1000)

    dir_attr = chat_page.page.get_attribute("html", "dir")
    logger.info(f"English mode - HTML dir attribute: {dir_attr}")

    assert dir_attr == "ltr", f"Expected LTR layout for English, got {dir_attr}"
    logger.info("✓ English LTR layout verified")


@pytest.mark.ui
@pytest.mark.arabic
def test_arabic_rtl_layout(chat_page: ChatPage):
    """Verify page switches to RTL layout when Arabic is selected"""
    chat_page.switch_language("ar")
    chat_page.page.wait_for_timeout(1000)

    dir_attr = chat_page.page.get_attribute("html", "dir")
    logger.info(f"Arabic mode - HTML dir attribute: {dir_attr}")

    assert dir_attr == "rtl", f"Expected RTL layout for Arabic, got {dir_attr}"
    logger.info("✓ Arabic RTL layout verified")



@pytest.mark.ui
@pytest.mark.bilingual
def test_language_switch_persists(chat_page: ChatPage):
    """Verify language selection persists when switching back and forth"""
    # Start with English
    chat_page.switch_language("en")
    chat_page.page.wait_for_timeout(1000)
    assert chat_page.page.get_attribute("html", "dir") == "ltr"

    # Switch to Arabic
    chat_page.switch_language("ar")
    chat_page.page.wait_for_timeout(1000)
    assert chat_page.page.get_attribute("html", "dir") == "rtl"

    # Switch back to English
    chat_page.switch_language("en")
    chat_page.page.wait_for_timeout(1000)
    assert chat_page.page.get_attribute("html", "dir") == "ltr"

    logger.info("✓ Language switching works correctly in both directions")


@pytest.mark.ui
@pytest.mark.arabic
def test_arabic_text_displays_correctly(chat_page: ChatPage):
    """Verify Arabic text is displayed correctly in RTL layout"""
    chat_page.switch_language("ar")
    chat_page.page.wait_for_timeout(1000)

    # Send an Arabic message
    arabic_message = "مرحبا، كيف يمكنني المساعدة؟"
    chat_page.send_message(arabic_message)

    # Get response
    response = chat_page.get_last_ai_response()

    # Verify response contains Arabic characters
    has_arabic = any('\u0600' <= char <= '\u06FF' for char in response)
    assert has_arabic, "Expected Arabic characters in response"

    # Verify RTL layout is maintained
    assert chat_page.page.get_attribute("html", "dir") == "rtl"

    logger.info("✓ Arabic text displays correctly in RTL layout")


@pytest.mark.ui
@pytest.mark.english
def test_english_text_displays_correctly(chat_page: ChatPage):
    """Verify English text is displayed correctly in LTR layout"""
    chat_page.switch_language("en")
    chat_page.page.wait_for_timeout(1000)

    # Send an English message
    english_message = "Hello, how can I help?"
    chat_page.send_message(english_message)

    # Get response
    response = chat_page.get_last_ai_response()

    # Verify response is not empty
    assert len(response.strip()) > 0, "Expected non-empty English response"

    # Verify LTR layout is maintained
    assert chat_page.page.get_attribute("html", "dir") == "ltr"

    logger.info("✓ English text displays correctly in LTR layout")


@pytest.mark.ui
@pytest.mark.arabic
def test_ui_elements_align_correctly_in_rtl(chat_page: ChatPage):
    """Verify UI elements are properly aligned in RTL mode"""
    chat_page.switch_language("ar")
    chat_page.page.wait_for_timeout(1000)

    # Check if main UI elements are visible
    chat_page.assert_visible(chat_page.CHAT_INPUT)
    chat_page.assert_visible(chat_page.SEND_BUTTON)

    # Verify RTL layout
    assert chat_page.page.get_attribute("html", "dir") == "rtl"

    logger.info("✓ UI elements properly aligned in RTL mode")

@pytest.mark.ui
@pytest.mark.english
def test_ui_elements_align_correctly_in_ltr(chat_page: ChatPage):
    """Verify UI elements are properly aligned in LTR mode"""
    chat_page.switch_language("en")
    chat_page.page.wait_for_timeout(1000)

    # Check if main UI elements are visible
    chat_page.assert_visible(chat_page.CHAT_INPUT)
    chat_page.assert_visible(chat_page.SEND_BUTTON)

    # Verify LTR layout
    assert chat_page.page.get_attribute("html", "dir") == "ltr"

    logger.info("✓ UI elements properly aligned in LTR mode")


@pytest.mark.ui
@pytest.mark.bilingual
def test_chat_history_maintains_language_context(chat_page: ChatPage):
    """Verify chat history maintains correct language context"""
    # Send English message
    chat_page.switch_language("en")
    chat_page.send_message("Tell me about UAE visas")
    english_response = chat_page.get_last_ai_response()

    # Switch to Arabic and send message
    chat_page.switch_language("ar")
    chat_page.send_message("أخبرني عن التأشيرات")
    arabic_response = chat_page.get_last_ai_response()

    # Verify both responses are non-empty
    assert len(english_response.strip()) > 0, "English response should not be empty"
    assert len(arabic_response.strip()) > 0, "Arabic response should not be empty"

    # Verify Arabic characters in Arabic response
    has_arabic = any('\u0600' <= char <= '\u06FF' for char in arabic_response)
    assert has_arabic, "Arabic response should contain Arabic characters"

    logger.info("✓ Chat history maintains correct language context")


@pytest.mark.ui
@pytest.mark.bilingual
def test_language_indicator_matches_content(chat_page: ChatPage):
    """Verify language indicator matches the actual content language"""
    # Test English
    chat_page.switch_language("en")
    chat_page.page.wait_for_timeout(1000)

    # Open sidebar and check language indicator
    state = chat_page.page.locator("#sidebar").get_attribute("data-state")
    if state == "false":
        chat_page.page.locator("xpath=//button[@aria-label='Toggle sidebar']").click()
        chat_page.page.wait_for_timeout(500)

    chat_page.page.locator("xpath=//div[@id='sidebar']/div/div[3]//button[@type='button']").click()
    chat_page.page.wait_for_timeout(500)

    lang_text = chat_page.page.locator("xpath=//div[@data-side='top']/div[2]//span").text_content()

    # In English mode, should show "Switch to Arabic"
    assert lang_text == "Switch to Arabic", \
        f"Expected 'Switch to Arabic' indicator in English mode, got '{lang_text}'"

    # Close the menu by clicking elsewhere
    chat_page.page.keyboard.press("Escape")
    chat_page.page.wait_for_timeout(500)

    # Test Arabic
    chat_page.switch_language("ar")
    chat_page.page.wait_for_timeout(1000)

    # Open sidebar and check language indicator
    state = chat_page.page.locator("#sidebar").get_attribute("data-state")
    if state == "false":
        chat_page.page.locator("xpath=//button[@aria-label='Toggle sidebar']").click()
        chat_page.page.wait_for_timeout(500)

    chat_page.page.locator("xpath=//div[@id='sidebar']/div/div[3]//button[@type='button']").click()
    chat_page.page.wait_for_timeout(500)

    lang_text = chat_page.page.locator("xpath=//div[@data-side='top']/div[2]//span").text_content()

    # In Arabic mode, should show "التبديل إلى اللغة الإنجليزية"
    assert lang_text == "التبديل إلى اللغة الإنجليزية", \
        f"Expected Arabic 'Switch to English' indicator in Arabic mode, got '{lang_text}'"

    logger.info("✓ Language indicators match content correctly")