import json
import yaml
import platform
from pathlib import Path
from playwright.sync_api import sync_playwright
from utils.logger import get_logger
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from axe_playwright_python.sync_playwright import Axe

import os
import pytest
from langchain_openai import ChatOpenAI
from ragas.llms.base import LangchainLLMWrapper
from langchain_huggingface import HuggingFaceEmbeddings
from ragas.embeddings.base import LangchainEmbeddingsWrapper
import allure
from allure_commons.types import AttachmentType

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def config():
    with open("config/config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def test_data():
    base_dir = Path(__file__).resolve().parent
    data_file = base_dir / "data" / "test_data.json"
    print("Loading test data from:", data_file)
    assert data_file.exists(), f"{data_file} does not exist"
    with data_file.open(encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="function")
def playwright_instance():
    p = sync_playwright().start()
    yield p
    p.stop()


@pytest.fixture(scope="function")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser, playwright_instance, request, config):
    # Check if the test has @pytest.mark.mobile
    is_mobile = request.node.get_closest_marker("mobile") is not None

    # Get video recording settings from config
    enable_video = config.get("enable_video_recording", False)
    video_dir = config.get("video_dir", "videos/")

    # Prepare base context options
    base_options = {}
    if enable_video:
        base_options["record_video_dir"] = video_dir

    if is_mobile:
        device = playwright_instance.devices["iPhone 12 Pro"]
        context = browser.new_context(**device, **base_options)
    else:
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            is_mobile=False,
            has_touch=False,
            **base_options
        )

    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context, config):
    page = context.new_page()
    page.set_default_timeout(config["timeout_ms"])
    page.goto(config["base_url"])
    return page


@pytest.fixture(scope="function")
def chat_page(page, config):
    login_page = LoginPage(page)
    login_page.login(config["username"], config["password"])
    chat_page = ChatPage(page)
    return chat_page


@pytest.fixture(scope="session")
def axe():
    # Single Axe instance reused across tests
    return Axe()


@pytest.fixture(scope="session")
def llm_wrapper(config):
    """
    Fixture to provide LLM wrapper for RAGAS metrics.

    Uses:
    - PerplexityCompatibleChatOpenAI for LLM (forces n=1)
    - HuggingFace embeddings for ResponseRelevancy metric
    """

    # Custom ChatOpenAI that forces n=1 for Perplexity compatibility
    class PerplexityCompatibleChatOpenAI(ChatOpenAI):
        """
        Custom ChatOpenAI that forces n=1 for all API requests.
        This is required because Perplexity's sonar-pro model doesn't support n>1.
        """

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            """Override sync generation to force n=1."""
            kwargs['n'] = 1
            return super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)

        async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs):
            """Override async generation to force n=1."""
            kwargs['n'] = 1
            return await super()._agenerate(messages, stop=stop, run_manager=run_manager, **kwargs)

    llm = PerplexityCompatibleChatOpenAI(
        model="sonar-pro",
        temperature=0.3,
        api_key=config["PERPLEXITY_API_KEY"],
        base_url="https://api.perplexity.ai"
    )
    logger.info("Initializing HuggingFace embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    embeddings_wrapper = LangchainEmbeddingsWrapper(embeddings)
    logger.info("✓ HuggingFace embeddings initialized")

    llm_wrapper = LangchainLLMWrapper(langchain_llm=llm)
    llm_wrapper.embeddings = embeddings_wrapper

    return llm_wrapper


# ============================================================================
# PYTEST HOOKS
# ============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to attach screenshots to both pytest-html and Allure reports on test failure.

    This hook handles:
    1. pytest-html: Saves screenshot to reports/screenshots/ and adds link to HTML report
    2. Allure: Attaches screenshot directly to the report
    """
    outcome = yield
    report = outcome.get_result()

    # Only process test execution phase (not setup/teardown)
    if report.when != "call":
        return

    # Handle test failures - attach screenshots
    if report.failed:
        # Get the page object from fixtures
        page = item.funcargs.get("page")
        chat_page = item.funcargs.get("chat_page")
        page_obj = chat_page.page if chat_page and hasattr(chat_page, "page") else page

        if page_obj:
            try:
                # Take screenshot once
                screenshot = page_obj.screenshot(full_page=True)

                # === PYTEST-HTML INTEGRATION ===
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html:
                    # Save screenshot to reports/screenshots/
                    reports_dir = Path("reports")
                    screenshots_dir = reports_dir / "screenshots"
                    screenshots_dir.mkdir(parents=True, exist_ok=True)

                    file_name = report.nodeid.replace("::", "_").replace("/", "_") + ".png"
                    path = screenshots_dir / file_name

                    # Save the screenshot
                    with open(path, 'wb') as f:
                        f.write(screenshot)

                    # Add link to pytest-html report (relative path)
                    rel_path = Path("screenshots") / file_name
                    extra = getattr(report, "extra", [])
                    extra.append(pytest_html.extras.url(str(rel_path), name="Open screenshot"))
                    report.extra = extra

                # === ALLURE INTEGRATION ===
                # Attach screenshot to Allure report
                allure.attach(
                    screenshot,
                    name=f"failure_{item.name}",
                    attachment_type=AttachmentType.PNG
                )

                logger.info(f"✓ Screenshot captured for failed test: {item.name}")

            except Exception as e:
                logger.warning(f"Could not capture screenshot: {e}")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Add environment info to Allure report.
    """
    # Create environment.properties file for Allure
    allure_results_dir = config.getoption('--alluredir', default=None)

    if allure_results_dir:
        os.makedirs(allure_results_dir, exist_ok=True)

        env_file = os.path.join(allure_results_dir, 'environment.properties')
        with open(env_file, 'w') as f:
            f.write(f"Browser=Chromium\n")
            f.write(f"Environment=Sandbox\n")
            f.write(f"Base_URL=https://govgpt.sandbox.dge.gov.ae/\n")
            f.write(f"Python_Version={platform.python_version()}\n")
            f.write(f"Pytest_Version={pytest.__version__}\n")