import json
import pytest
from pages.chat_page import ChatPage

@pytest.mark.accessibility
def test_chat_page_has_no_critical_violations(chat_page: ChatPage, axe):
    # run axe on the current page (already logged in and on chat)
    chat_page.page.locator(chat_page.CHAT_INPUT).wait_for(state="visible",timeout=10000)
    results = axe.run(chat_page.page)

    # Optional: save full axe result for debugging
    with open("reports/axe_chat_page.json", "w", encoding="utf-8") as f:
        json.dump(results.response, f, ensure_ascii=False, indent=2)

    # Fail only on serious/critical violations, allow minor ones to be triaged
    critical_impacts = {"serious", "critical"}
    violations = [
        v for v in results.response["violations"]
        if v.get("impact") in critical_impacts
    ]

    assert not violations, f"Axe found {len(violations)} serious/critical violations"
