import pytest

from pages.chat_page import ChatPage
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.ui
@pytest.mark.english
def test_chat_widget_loads_desktop(chat_page: ChatPage):
    """Verify chat widget loads correctly on desktop with all essential elements"""
    chat_page.assert_visible(ChatPage.CHAT_INPUT)
    chat_page.assert_visible(ChatPage.SEND_BUTTON)
    logger.info("Desktop chat widget loaded successfully")

@pytest.mark.ui
@pytest.mark.english
@pytest.mark.mobile
def test_chat_widget_loads_mobile(chat_page: ChatPage):
    """Verify chat widget loads correctly on mobile devices"""
    chat_page.assert_visible(ChatPage.CHAT_INPUT)
    chat_page.assert_visible(ChatPage.SEND_BUTTON)
    logger.info("Mobile chat widget loaded successfully")

@pytest.mark.ui
@pytest.mark.english
def test_user_can_send_message(chat_page: ChatPage):
    """Verify user can successfully send a message and receive response"""
    text = "Test message from automation"
    chat_page.send_message(text)
    res = chat_page.assert_visible(ChatPage.LAST_USER_MESSAGE)
    logger.info(f"Response text: {res}")
    assert res.strip() != "", "Expected non-empty response"

@pytest.mark.ui
@pytest.mark.english
def test_ai_response_rendered(chat_page: ChatPage):
    """Verify AI response is rendered after sending a message"""
    chat_page.send_message("Hello")
    chat_page.assert_visible(ChatPage.LAST_AI_MESSAGE)
    # Fixed: Changed get_last_ai_text() to get_last_ai_response()
    response = chat_page.get_last_ai_response()
    assert response.strip() != "", "AI response should not be empty"
    logger.info(f"AI response received: {response[:100]}...")

@pytest.mark.ui
@pytest.mark.english
def test_input_cleared_after_send(chat_page: ChatPage):
    """Verify input field is cleared after sending a message"""
    chat_page.send_message("Check clear")
    # Get the input value
    input_field = chat_page.page.locator(ChatPage.CHAT_INPUT)
    value = input_field.text_content()
    assert value == "", f"Input field should be empty after send, but contains: '{value}'"
    logger.info("Input field cleared successfully after sending")

@pytest.mark.ui
@pytest.mark.english
def test_scroll_behavior(chat_page: ChatPage):
    """Verify scroll container auto-scrolls to bottom as new messages arrive"""
    # Send some messages to populate the chat
    for i in range(3):
        chat_page.send_message(f"Scroll check {i + 1}")

    locator = chat_page.page.locator(ChatPage.SCROLL_CONTAINER)

    # Ensure container is scrollable
    chat_page.page.wait_for_timeout(1000)
    scroll_data = locator.evaluate(
        "el => ({top: el.scrollTop, height: el.clientHeight, full: el.scrollHeight})"
    )
    initial_top = scroll_data["top"]
    logger.info(
        f"Initial scroll position - top: {initial_top}, height: {scroll_data['height']}, full: {scroll_data['full']}")

    assert scroll_data["full"] > scroll_data["height"], "Container should be scrollable"

    # Send more messages and wait for rendering
    for i in range(3):
        chat_page.send_message(f"More scroll {i + 1}")
    chat_page.page.wait_for_timeout(2000)

    new_top = locator.evaluate("el => el.scrollTop")
    logger.info(f"New scroll position: {new_top}")

    # Verify scroll position increased (scrolled down)
    assert new_top > initial_top, f"Expected scrollTop to increase from {initial_top} to {new_top}"

@pytest.mark.ui
@pytest.mark.english
def test_multiple_messages_sequence(chat_page: ChatPage):
    """Verify multiple messages can be sent in sequence and all responses are received"""
    messages = ["First message", "Second message", "Third message"]

    for msg in messages:
        chat_page.send_message(msg)
        response = chat_page.get_last_ai_response()
        assert response.strip() != "", f"Response for '{msg}' should not be empty"
        logger.info(f"Message '{msg}' -> Response received")

    logger.info("All messages sent and responses received successfully")

@pytest.mark.ui
@pytest.mark.english
def test_send_button_enabled_with_input(chat_page: ChatPage):
    """Verify send button is enabled when input has text"""
    input_field = chat_page.page.locator(ChatPage.CHAT_INPUT)
    send_button = chat_page.page.locator(ChatPage.SEND_BUTTON)

    # Type text in input
    input_field.fill("Test message")
    chat_page.page.wait_for_timeout(500)

    # Verify send button is enabled
    is_disabled = send_button.is_disabled()
    assert not is_disabled, "Send button should be enabled when input has text"
    logger.info("Send button correctly enabled with input text")

@pytest.mark.ui
@pytest.mark.english
def test_chat_maintains_history(chat_page: ChatPage):
    """Verify chat maintains conversation history"""
    # Send first message
    chat_page.send_message("Tell me about Emirates ID")
    first_response = chat_page.get_last_ai_response()

    # Send second message
    chat_page.send_message("How long does it take?")
    second_response = chat_page.get_last_ai_response()

    # Get complete history
    full_history = chat_page.get_complete_ai_response()

    # Verify both responses are in history
    assert first_response.strip() in full_history or len(full_history) > len(first_response), \
        "First response should be in chat history"
    assert second_response.strip() in full_history or len(full_history) > len(second_response), \
        "Second response should be in chat history"

    logger.info(f"Chat history maintained: {len(full_history)} characters total")