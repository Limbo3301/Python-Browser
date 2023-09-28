import sys
import requests
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.browser = QWebEngineView()
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        self.browser.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)

        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        self.search_bar = QLineEdit()
        self.search_bar.returnPressed.connect(self.search)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.urlbar)
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.progressBar = QProgressBar()
        self.progressBar.setMaximumWidth(120)
        navtb.addWidget(self.progressBar)

        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        js_btn = QAction("JavaScript", self)
        js_btn.setStatusTip("Enable/Disable JavaScript")
        js_btn.setCheckable(True)
        js_btn.setChecked(True)
        js_btn.toggled.connect(self.toggle_js)
        navtb.addAction(js_btn)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.browser.load(QUrl("http://www.google.com"))
        self.showMaximized()
        self.setWindowTitle("Python Browser")

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(title)

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

    def update_urlbar(self, q):
        if q.toString() == "about:blank":
            return

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def search(self):
        search_query = self.search_bar.text()
        q = QUrl(f"http://www.google.com/search?q={search_query}")
        self.browser.setUrl(q)

    def toggle_js(self, enabled):
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, enabled)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    sys.exit(app.exec_())