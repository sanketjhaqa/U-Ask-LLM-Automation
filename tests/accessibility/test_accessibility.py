import pytest
from playwright.sync_api import expect
from pages.chat_page import ChatPage


@pytest.mark.accessibility
@pytest.mark.english
def test_chat_input_has_label(chat_page: ChatPage):
    """Test that chat input has accessible label"""
    chat_page.page.locator(chat_page.CHAT_INPUT).wait_for(state="attached", timeout=10000)
    label = chat_page.page.get_by_label("Ask anything", exact=False)
    assert label.is_visible(), "Chat input label 'Ask anything' not visible"


@pytest.mark.accessibility
@pytest.mark.english
def test_keyboard_navigation(chat_page: ChatPage):
    """Test that user can navigate and interact using keyboard only"""
    page = chat_page.page
    page.locator(chat_page.CHAT_INPUT).wait_for(state="attached", timeout=10000)

    # Focus input and type
    page.focus(ChatPage.CHAT_INPUT)
    page.keyboard.type("keyboard navigation test")

    # Submit with Enter
    page.keyboard.press("Enter")

    # Wait for response
    chat_page.wait_for_shimmer_if_present()
    chat_page.wait_for_ai_generating_if_present()

    # Verify message was actually sent and response received
    response = chat_page.get_last_ai_response()
    assert len(response) > 0, "No AI response received after keyboard submission"
    assert chat_page.page.locator(ChatPage.LAST_USER_MESSAGE).is_visible(), \
        "User message not visible after keyboard submission"


@pytest.mark.accessibility
@pytest.mark.english
def test_aria_roles_present(chat_page: ChatPage):
    """Test that critical UI elements have proper ARIA roles"""
    page = chat_page.page
    page.locator(chat_page.CHAT_INPUT).wait_for(state="attached", timeout=10000)

    # Chat region
    region = page.get_by_role("region", name="Chat", exact=False)
    assert region.is_visible(), "Chat region role not visible"

    # Text input
    textbox = page.get_by_role("textbox")
    assert textbox.count() > 0, "No textbox role found for chat input"

    # Send button
    send_btn = page.get_by_role("button", name="Send", exact=False)
    assert send_btn.is_visible(), "Send button role not visible"


@pytest.mark.accessibility
@pytest.mark.english
def test_focus_order_left_nav_to_input(chat_page: ChatPage):
    """Test that keyboard focus follows logical order through navigation"""
    page = chat_page.page

    # Start at top-left "New Chat" button
    new_chat = page.get_by_role("button", name="New Chat", exact=False)
    new_chat.focus()
    expect(new_chat).to_be_focused()

    # Tab through Search, Gov Knowledge, Agents, then main chat input
    page.keyboard.press("Tab")  # Search
    search = page.get_by_role("button", name="Search", exact=False)
    expect(search).to_be_focused()

    page.keyboard.press("Tab")  # Gov Knowledge
    gov_knowledge = page.get_by_role("button", name="Gov Knowledge", exact=False)
    expect(gov_knowledge).to_be_focused()

    page.keyboard.press("Tab")  # Agents
    agents = page.get_by_role("button", name="Agents", exact=False)
    expect(agents).to_be_focused()

    page.keyboard.press("Tab")  # Chat input
    chat_input = page.get_by_role("textbox", name="Ask anything", exact=False)
    expect(chat_input).to_be_focused()


@pytest.mark.accessibility
@pytest.mark.english
def test_buttons_have_accessible_names(chat_page: ChatPage):
    """Test that all interactive buttons have accessible names for screen readers"""
    page = chat_page.page

    # Navigation buttons - FIXED: Added assertions
    assert page.get_by_role("button", name="New Chat", exact=False).is_visible(), \
        "New Chat button not visible or missing accessible name"

    assert page.get_by_role("button", name="Search", exact=False).is_visible(), \
        "Search button not visible or missing accessible name"

    assert page.get_by_role("button", name="Gov Knowledge", exact=False).is_visible(), \
        "Gov Knowledge button not visible or missing accessible name"

    assert page.get_by_role("button", name="Agents", exact=False).is_visible(), \
        "Agents button not visible or missing accessible name"

    # Send button in the main composer
    send_button = page.get_by_role("button", name="Send", exact=False)
    assert send_button.is_visible(), \
        "Send button not visible or missing accessible name"


@pytest.mark.accessibility
@pytest.mark.english
def test_chat_messages_region_has_live_attributes(chat_page: ChatPage):
    """Test that chat messages region has proper ARIA live attributes for screen reader announcements"""
    page = chat_page.page

    # Send message to populate chat
    chat_page.send_message("visa")

    # Check messages container
    messages_region = page.locator(ChatPage.SCROLL_CONTAINER)

    # Check aria-live attribute
    aria_live = messages_region.get_attribute("aria-live")
    assert aria_live is not None, \
        "Messages region missing aria-live attribute for screen readers"

    # FIXED: Validate aria-live has correct value
    assert aria_live in ["polite", "assertive", "off"], \
        f"Invalid aria-live value: '{aria_live}'. Expected: 'polite', 'assertive', or 'off'"

    # For chat, "polite" is recommended (doesn't interrupt screen reader)
    # Uncomment if you want to enforce "polite" specifically
    # assert aria_live == "polite", \
    #     f"Chat messages should use aria-live='polite' for better UX, found '{aria_live}'"