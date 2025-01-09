import sys
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
import html  # This will be used for escaping HTML characters

class WebHandler(QObject):
    @pyqtSlot()
    def send_text_file_content(self):
        # Reading content of the text file (abc.txt)
        try:
            with open('default_settings.txt', 'r') as file:
                content = file.read()
            # Send the file content to JavaScript (escape HTML to prevent issues in JS)
            self.text_content.emit(content)
        except Exception as e:
            self.text_content.emit(f"Error: {e}")

    # Signal to send content to JavaScript
    text_content = pyqtSignal(str)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 and HTML Communication")
        self.setGeometry(100, 100, 800, 600)

        # Initialize the WebEngine view
        self.browser = QWebEngineView(self)

        # HTML code stored in a Python variable
        html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PyQt5 and HTML Communication</title>
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <script>
                // Declare the backend object here
                var backend;

                // Function to update the content in HTML with data from Python
                function updateFileContent(content) {
                    document.getElementById('fileContent').textContent = content;
                }

                // Function to initialize the WebChannel and connect to the Python backend
                function initWebChannel() {
                    new QWebChannel(qt.webChannelTransport, function(channel) {
                        // Assign the Python backend to the global variable
                        backend = channel.objects.backend;
                        
                        // Once initialized, we can now safely call the Python function
                        backend.send_text_file_content();
                    });
                }

                // Ensure the WebChannel is initialized before trying to access the backend
                window.onload = function() {
                    initWebChannel();
                }
            </script>
        </head>
        <body>
            <h1>Text File Content</h1>
            <div id="fileContent" style="white-space: pre-wrap; border: 1px solid #ccc; padding: 10px; margin-top: 20px;">
                <!-- File content will be displayed here -->
            </div>
        </body>
        </html>
        """

        # Load HTML code directly into the browser
        self.browser.setHtml(html_code)

        # Create a WebChannel and set the JavaScript interface
        self.channel = QWebChannel(self)
        self.web_handler = WebHandler()
        self.channel.registerObject("backend", self.web_handler)
        self.browser.page().setWebChannel(self.channel)

        # Connect the signal to handle content update
        self.web_handler.text_content.connect(self.display_text_content)

        # Show the browser window
        self.browser.show()

    def display_text_content(self, content):
        # Escape the content to safely pass it to JavaScript
        escaped_content = html.escape(content)
        # This method updates the HTML content with the text received from Python
        self.browser.page().runJavaScript(f"updateFileContent('{escaped_content}')")

# Main execution
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
