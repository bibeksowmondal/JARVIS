
from urllib.parse import quote_plus, urlparse
import atexit

from playwright.sync_api import sync_playwright


class BrowserController:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    # ------------------------------------------
    # START GOOGLE CHROME
    # ------------------------------------------

    def start(self):
        if self.browser and self.browser.is_connected():
            return

        self.shutdown()

        try:
            self.playwright = sync_playwright().start()

            # Launch installed Google Chrome only.
            # No fallback to bundled Chromium or Brave.
            self.browser = self.playwright.chromium.launch(
                channel="chrome",
                headless=False
            )

            self.context = self.browser.new_context()
            self.page = self.context.new_page()

        except Exception:
            self.shutdown()
            raise RuntimeError(
                "Could not launch Google Chrome. "
                "Check that Google Chrome is installed."
            )

    # ------------------------------------------
    # OPEN CHROME
    # ------------------------------------------

    def open_browser(self):
        try:
            self.start()
            return "Google Chrome is open."
        except Exception as error:
            return str(error)

    # ------------------------------------------
    # GET ACTIVE TAB
    # ------------------------------------------

    def active_page(self):
        self.start()

        if self.page is None or self.page.is_closed():
            pages = [
                page for page in self.context.pages
                if not page.is_closed()
            ]

            self.page = (
                pages[-1] if pages
                else self.context.new_page()
            )

        return self.page

    # ------------------------------------------
    # OPEN WEBSITE
    # ------------------------------------------

    def open_url(self, address):
        address = address.strip()

        if not address:
            return "Please provide a website address."

        if "://" not in address:
            address = "https://" + address

        parsed = urlparse(address)

        if (
            parsed.scheme not in ("http", "https")
            or not parsed.hostname
        ):
            return "That website address is invalid."

        try:
            page = self.active_page()

            page.goto(
                address,
                wait_until="domcontentloaded",
                timeout=30000
            )

            return f"Opened {parsed.hostname} in Google Chrome."

        except Exception as error:
            return f"Could not open website: {error}"

    # ------------------------------------------
    # GOOGLE SEARCH
    # ------------------------------------------

    def google_search(self, query):
        query = query.strip()

        if not query:
            return "Please tell me what to search for."

        url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        return self.open_url(url)

    # ------------------------------------------
    # YOUTUBE SEARCH
    # ------------------------------------------

    def youtube_search(self, query):
        query = query.strip()

        if not query:
            return "Please tell me what to search on YouTube."

        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(query)
        )

        return self.open_url(url)

    # ------------------------------------------
    # NEW TAB
    # ------------------------------------------

    def new_tab(self):
        try:
            self.start()

            self.page = self.context.new_page()
            self.page.goto("about:blank")

            return "Opened a new Chrome tab."

        except Exception as error:
            return f"Could not open new tab: {error}"

    # ------------------------------------------
    # CLOSE TAB
    # ------------------------------------------

    def close_tab(self):
        try:
            page = self.active_page()
            page.close()

            remaining = [
                p for p in self.context.pages
                if not p.is_closed()
            ]

            self.page = remaining[-1] if remaining else None

            return "Closed the Chrome tab."

        except Exception as error:
            return f"Could not close tab: {error}"

    # ------------------------------------------
    # GO BACK
    # ------------------------------------------

    def go_back(self):
        try:
            page = self.active_page()
            response = page.go_back(
                wait_until="domcontentloaded",
                timeout=20000
            )

            if response is None:
                return "There is no previous page."

            return "Navigated back."

        except Exception as error:
            return f"Could not navigate back: {error}"

    # ------------------------------------------
    # GO FORWARD
    # ------------------------------------------

    def go_forward(self):
        try:
            page = self.active_page()
            response = page.go_forward(
                wait_until="domcontentloaded",
                timeout=20000
            )

            if response is None:
                return "There is no next page."

            return "Navigated forward."

        except Exception as error:
            return f"Could not navigate forward: {error}"

    # ------------------------------------------
    # CLOSE CHROME
    # ------------------------------------------

    def close_browser(self):
        self.shutdown()
        return "Google Chrome has been closed."

    # ------------------------------------------
    # SHUTDOWN
    # ------------------------------------------

    def shutdown(self):
        try:
            if self.browser:
                self.browser.close()
        except Exception:
            pass
        finally:
            self.browser = None
            self.context = None
            self.page = None

            if self.playwright:
                try:
                    self.playwright.stop()
                except Exception:
                    pass

                self.playwright = None


# ------------------------------------------
# GLOBAL BROWSER CONTROLLER
# ------------------------------------------

browser_controller = BrowserController()

atexit.register(browser_controller.shutdown)
