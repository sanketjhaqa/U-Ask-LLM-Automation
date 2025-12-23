from markdown_it.rules_block import reference

from pages.base_page import BasePage, logger


class ChatPage(BasePage):
    # Locators
    CHAT_INPUT = "#chat-input"
    SEND_BUTTON = "#send-message-button"
    LAST_USER_MESSAGE = "xpath=//div[@id='response-content-container']"
    LAST_AI_MESSAGE = "xpath=//div[@id='response-content-container']"
    LOADING_INDICATOR = "xpath=//div[@id='response-content-container']//span[starts-with(@class,'shimmer-text')]"
    LANGUAGE_TOGGLE_EN = "LANG_EN_DOM"
    LANGUAGE_TOGGLE_AR = "LANG_AR_DOM"
    SCROLL_CONTAINER = "#messages-container"
    FALLBACK_MESSAGE = "FALLBACK_MESSAGE_DOM"
    SHIMMER = "xpath=//div[@id='response-content-container']//span[starts-with(@class,'shimmer-text')]"
    AI_GENERATING_BTN = "xpath=//button[@class='transition rounded-full']"
    ENGLISH_OPTION = "xpath=//span[text()='التبديل إلى اللغة الإنجليزية']/../following-sibling::div"
    ARABIC_OPTION = "xpath=//span[text()='Switch to Arabic']/../following-sibling::div"
    ALL_MESSAGES = "xpath=//div[@id='response-content-container']"
    NEW_CHAT_BTN = "#sidebar-new-chat-button"
    SOURCE_BTN = "xpath=//span[text()='Sources']"
    CITATION ="xpath=//*[contains(text(),'Citations')]"
    SOURCE_DETAILS = "xpath=//*[text()='Citations']/../../following-sibling::div//a"
    CITATION_CLOSE_BTN = "xpath=//*[text()='Citations']/parent::div/following-sibling::button"

    def send_message(self, text: str):
        """Send a message and wait for AI response"""
        self.page.locator(self.CHAT_INPUT).type(text=text,delay=30)
        self.page.click(self.SEND_BUTTON)
        self.wait_for_shimmer_if_present()
        self.wait_for_ai_generating_if_present()

    def get_last_ai_response(self) -> str:
        """Get the last AI response text"""
        self.wait_for_shimmer_if_present()
        self.wait_for_ai_generating_if_present()
        return self.page.locator(self.LAST_AI_MESSAGE).last.inner_text()

    def get_last_ai_text(self) -> str:
        """Alias for get_last_ai_response for backward compatibility"""
        return self.get_last_ai_response()

    def get_complete_ai_response(self) -> str:
        """Get ALL AI responses concatenated from entire chat history"""
        self.wait_for_shimmer_if_present()
        self.wait_for_ai_generating_if_present()

        # Get ALL response containers
        all_responses = self.page.locator(self.ALL_MESSAGES)
        ai_texts = []

        for i in range(all_responses.count()):
            text = all_responses.nth(i).inner_text()
            if text.strip():  # Skip empty
                ai_texts.append(text)

        return "\n\n".join(ai_texts)

    def get_full_chat_history(self) -> str:
        """Alias for get_complete_ai_response for backward compatibility"""
        return self.get_complete_ai_response()

    def wait_for_shimmer_if_present(self, timeout_ms: int = 60000):
        """Wait for shimmer/loading animation to disappear if present"""
        shimmer = self.page.locator(self.SHIMMER).first
        # count() returns immediately; if 0, skip waiting
        if shimmer.count() > 0:
            # wait until shimmer is gone (hidden or removed)
            try:
                self.page.wait_for_selector(
                    self.SHIMMER,
                    state="hidden",
                    timeout=timeout_ms
                )
            except Exception as e:
                logger.warning(f"Shimmer did not disappear within timeout: {str(e)}")

    def wait_for_ai_generating_if_present(self):
        """Wait for AI generating button to appear and then disappear"""
        btn = self.page.locator(self.AI_GENERATING_BTN)
        # If it never appears, don't fail the test
        try:
            # Fixed: Reduced timeout from 60s to 5s for checking if element appears
            btn.wait_for(state="visible", timeout=5000)
        except Exception:
            # Element didn't become visible; nothing to wait for
            return

        # If it did appear, then wait for it to go away (AI finished responding)
        try:
            btn.wait_for(state="hidden", timeout=120000)
        except Exception as e:
            logger.warning(f"AI generating button did not hide within timeout: {str(e)}")

    def switch_language(self, language: str):
        """Switch language to English or Arabic"""
        logger.info(f"Switching to {language}")

        # Open sidebar if closed
        state = self.page.locator("#sidebar").get_attribute("data-state")
        if state == "false":
            self.page.locator("xpath=//button[@aria-label='Toggle sidebar']").click()
            self.page.wait_for_timeout(500)

        # Click on user name/profile
        self.page.locator("xpath=//div[@id='sidebar']/div/div[3]//button[@type='button']").click()
        self.page.wait_for_timeout(500)

        # Get current language text
        lang_text = self.page.locator("xpath=//div[@data-side='top']/div[2]//span").text_content()

        if language.lower() == "en":
            try:
                if lang_text == "Switch to Arabic":
                    logger.info("Already on English language")
                else:
                    self.page.locator(self.ENGLISH_OPTION).click()
                    logger.info("English option clicked")
                    self.page.wait_for_timeout(1000)
            except Exception as e:
                # Fixed: Changed self.logger to logger
                logger.warning(f"Could not switch to English: {str(e)}")

        elif language.lower() == "ar":
            try:
                if lang_text == "التبديل إلى اللغة الإنجليزية":
                    logger.info("Already on Arabic language")
                else:
                    self.page.locator(self.ARABIC_OPTION).click()
                    logger.info("Arabic option clicked")
                    self.page.wait_for_timeout(1000)
            except Exception as e:
                # Fixed: Changed self.logger to logger
                logger.warning(f"Could not switch to Arabic: {str(e)}")

        self.page.wait_for_timeout(1000)
        logger.info(f"Language switched to {language}")
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

    def clear_chat_history(self):
        """Clear chat to start fresh for each test"""
        # Look for "New chat" button
        state = self.page.locator("#sidebar").get_attribute("data-state")
        if state == "false":
            self.page.locator("xpath=//button[@aria-label='Toggle sidebar']").click()
            self.page.wait_for_timeout(500)

        clear_btn = self.page.locator(self.NEW_CHAT_BTN)
        if clear_btn.is_visible():
            clear_btn.click()
            self.page.wait_for_timeout(1000)
            logger.info("Chat history cleared")

    # def get_retrieved_context(self):
    #     """Get references/sources from the AI response"""
    #     references = []
    #     self.wait_for_ai_generating_if_present()
    #     self.page.wait_for_timeout(6000)
    #
    #     source_btn = self.page.locator(self.SOURCE_BTN)
    #     logger.info("------------Going to collect retrieved context, Source button found")
    #     try:
    #         logger.info("-------------Waiting for source button to appear")
    #         source_btn.wait_for(state="visible", timeout=60000)
    #         logger.info("--------------Source button is visible")
    #     except Exception as e:
    #         logger.error("-----------No Source attached with answer")
    #         return references
    #
    #     source_btn.scroll_into_view_if_needed()
    #     bbox = source_btn.bounding_box()
    #     if bbox:
    #         x = bbox['x']+bbox['width']/2
    #         y = bbox['y']+bbox['height']/2
    #         self.page.mouse.click(x, y)
    #     else:
    #         source_btn.click(force=True)
    #     logger.info("------------Clicked on source button")
    #     self.page.wait_for_timeout(5000)
    #     sources_detail = self.page.locator(self.SOURCE_DETAILS).first
    #     try:
    #         sources_detail.wait_for(state="visible", timeout=60000)
    #     except Exception:
    #         logger.warning("Source details not visible")
    #         return references
    #
    #     # Wait for all sources to load
    #     count = 0
    #     max_iterations = 10
    #     iteration = 0
    #     while iteration < max_iterations:
    #         current_count = self.page.locator(self.SOURCE_DETAILS).count()
    #         if current_count > count:
    #             count = current_count
    #             logger.info(f"Sources loaded: {count}")
    #             self.page.wait_for_timeout(1000)
    #         else:
    #             break
    #         iteration += 1
    #
    #     # Extract all sources
    #     length = self.page.locator(self.SOURCE_DETAILS).count()
    #     for i in range(length):
    #         try:
    #             item = self.page.locator(self.SOURCE_DETAILS).nth(i)
    #             title = item.get_attribute("title")
    #             url = item.get_attribute("href")
    #             references.append(f"Title: {title} | URL: {url}")
    #             logger.info(f"Source {i + 1}: Title: {title} | URL: {url}")
    #         except Exception as e:
    #             logger.warning(f"Could not extract source {i + 1}: {str(e)}")
    #
    #     return references

    def get_retrieved_context(self):
        """
        Extract citations by clicking exactly on "Sources" text position.
        Uses bounding_box() to get coordinates and clicks at center.
        """
        references = []
        self.wait_for_ai_generating_if_present()
        self.page.wait_for_timeout(2000)

        logger.info("=== Extracting citations with position click ===")

        try:
            # Step 1: Find the "Sources" text span
            sources_text = self.page.locator(self.SOURCE_BTN)

            if sources_text.count() == 0:
                logger.error("Sources text not found!")
                return references

            logger.info("✓ Found Sources text")

            # Step 2: Get bounding box and click at center
            bounding_box = sources_text.first.bounding_box()

            if bounding_box:
                # Calculate center position
                center_x = bounding_box['x'] + bounding_box['width'] / 2
                center_y = bounding_box['y'] + bounding_box['height'] / 2

                logger.info(f"✓ Clicking at position: x={center_x:.1f}, y={center_y:.1f}")

                # Click at exact center of text
                self.page.mouse.click(center_x, center_y)
            else:
                # Fallback to force click
                logger.warning("Could not get bounding box, using force click")
                sources_text.first.click(force=True)

            self.page.wait_for_timeout(1500)

            # Step 3: Wait for Citations panel
            logger.info("Waiting for Citations panel...")
            self.page.locator(self.CITATION).first.wait_for(
                state="visible",
                timeout=10000
            )
            logger.info("✓ Citations panel opened")
            self.page.wait_for_timeout(5000)
            # Step 4: Extract citations
            citation_links = self.page.locator(self.SOURCE_DETAILS)

            count = citation_links.count()
            logger.info(f"✓ Found {count} citations")
            for retry in range(count):
                references = self.get_citation_data(count)
                if len(references) == count:
                    break
                else:
                    references = []
                    self.page.wait_for_timeout(2000)
            # Step 5: Close panel
            close_btn = self.page.locator(self.CITATION_CLOSE_BTN)
            if close_btn.count() > 0:
                close_btn.first.click()
                logger.info("✓ Panel closed")

        except Exception as e:
            logger.error(f"Citation extraction failed: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

        logger.info(f"=== Extraction complete: {len(references)} citations ===")
        return references

    def get_citation_data(self,count):
        references = []
        citation_links = self.page.locator(self.SOURCE_DETAILS)
        for i in range(count):
            href = citation_links.nth(i).get_attribute("href")
            title = citation_links.nth(i).get_attribute("title")
            if not title:
                title = citation_links.nth(i).inner_text()

            if href:
                references.append(f"Title: {title} | URL: {href}")
                logger.info(f"  - Title: {title} | URL: {href}")
        return references

    def verify_loading_indicator_appeared(self) -> bool:
        """Verify that loading indicator appeared during AI response generation"""
        # This method should be called right after sending a message
        # to check if loading indicator was present at any point
        try:
            shimmer = self.page.locator(self.SHIMMER).first
            if shimmer.count() > 0:
                return True

            ai_btn = self.page.locator(self.AI_GENERATING_BTN)
            if ai_btn.count() > 0:
                return True

            return False
        except Exception as e:
            logger.warning(f"Could not verify loading indicator: {str(e)}")
            return False

    def is_rtl_layout(self) -> bool:
        """Check if the page is in RTL (Right-to-Left) layout"""
        html_dir = self.page.get_attribute("html", "dir")
        return html_dir == "rtl"

    def is_ltr_layout(self) -> bool:
        """Check if the page is in LTR (Left-to-Right) layout"""
        html_dir = self.page.get_attribute("html", "dir")
        return html_dir == "ltr"