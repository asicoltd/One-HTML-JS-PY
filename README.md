### **Overview of the GUI Tool: OneConfigGui**

#### **Main Interface:**

The **OneConfigGui** interface is designed to provide an intuitive and user-friendly way to configure parameters for the **ONE Simulator**. The GUI allows users to easily input, adjust, and generate the default\_settings.txt configuration file.

1. **Input Fields for Parameters:**  
   * These fields allow the user to input or select various parameters related to the simulation scenario.  
   * Example: Scenario name, simulation interval, transmit speed, range, and the number of hosts.  
2. **Checkboxes:**  
   * **Compile Checkbox:** Users can decide to compile the simulator code before running it.  
   * **Event Generation Options:** Users can check if event generation is needed for the simulation.  
3. **Buttons:**  
   * **Run Simulation Button:** To start the simulation with the configured settings.  
   * **Save Settings Button:** To save the generated default\_settings.txt file after configuration.  
   * **Load Settings Button:** Load an existing settings file into the interface for easy modification.  
4. **Text Area (Output Panel):**  
   * A real-time output display of simulation events and logs generated during the simulation process.

**Screenshot:**  
![image_2025-01-09_174025801](https://github.com/user-attachments/assets/04cce410-8089-4172-8004-64beede49168)

Fig 1: Full GUI

![image_2025-01-05_040401038](https://github.com/user-attachments/assets/f5c1aa87-d9a3-4306-912e-6b4d5832e5fc)

Fig 2: Main Menu

![image_2025-01-09_174039674](https://github.com/user-attachments/assets/649d16b9-a127-4ae4-b0f8-c5bd333c93af)

Fig 3: Buttons to set default\_settings.txt to customized or ONE provided one

![image_2025-01-09_174107606](https://github.com/user-attachments/assets/cf72cc53-7979-49c8-803f-58bad4734230)

Fig 4: Check-box, fill box, and buttons for running compile.bat, one.bat with GUI/ without GUI

![image_2025-01-09_174117421](https://github.com/user-attachments/assets/93e9d246-7573-4d50-a9d6-c800e21e80dc)

Fig 5: Command Prompt to show the direct output of the script

#### **How to Install and Run**
Open cmd/powershell and copy paste these:
```
git clone https://github.com/akeranen/the-one.git
cd the-one
git clone https://github.com/asicoltd/One-HTML-JS-PY.git
cd One-HTML-JS-PY
pip install -r requirements.txt
move OneConfigGui5.py ../
move index.html ../
cd ..
rmdir /s /q .git
rmdir /s /q One-HTML-JS-PY
python OneConfigGui5.py

```

**IMPORTANT NOTE:**

If running OneConfigGui**.**py is difficult, run the **index.html** file with a browser. However, it will generate the default\_settings.txt in the Download file, which needs to be manually replaced with the main txt file. Also, it needs to run ‘one.bat’ manually with a command prompt or PowerShell. However, running HTML is much faster than running a Python script.

Now this is the part for details for the code in the **OneConfigGui:**

It has 3 layers in it. 

In the core, there is a webpage with HTML, CSS, and JS. This part controls the editing by giving inputs and downloading the default\_settings.txt. 

    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    
    
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Scenario Settings</title>
    ………………………………………………………………………………………………………………………………
              ( All codes inside )
    ……………………………………………………………………………………………………………………………
                // Create a temporary download link
                const link = document.createElement("a");
                link.href = URL.createObjectURL(blob);
                link.download = "default_settings.txt";  // Specify filename
                // Programmatically click the link to start the download
                link.click();
            }
        </script>
    </body>
    </html>
            """

Then we have a browser() class to create a Python webview to show the HTML in a window.

    class Browser(QMainWindow):
        def __init__(self):
            super().__init__()
            # Set up the main window
            self.setWindowTitle("ONE Configuration GUI")
            self.setGeometry(100, 100, 850, 700)
            # Create the main layout
            self.layout = QVBoxLayout()
            # Create a web engine view
            self.browser = CustomWebEngineView()
            # Set the custom page to the browser
            self.browser.setPage(CustomWebEnginePage())

These are the codes to run the command prompt inside the GUI and show the buttons:

        button_layout = QHBoxLayout()


        # Add a checkbox for "compile.bat"
        self.compile_checkbox = QCheckBox("Run compile.bat before executing one.bat", self)


        # Add the input box for the number
        self.number_input = QLineEdit(self)
        self.number_input.setPlaceholderText("Enter number for multiple batch")


        self.run_without_gui_button = QPushButton("Run ONE Simulator without GUI")
        self.run_without_gui_button.clicked.connect(self.run_without_gui)


        self.run_with_gui_button = QPushButton("Run ONE Simulator with GUI")
        self.run_with_gui_button.clicked.connect(self.run_with_gui)


        # Add the widgets to the horizontal layout
        button_layout.addWidget(self.compile_checkbox)
        button_layout.addWidget(self.number_input)
        button_layout.addWidget(self.run_without_gui_button)
        button_layout.addWidget(self.run_with_gui_button)


        # Create a QTextEdit to show the command output
        self.cmd_output = QTextEdit(self)
        self.cmd_output.setReadOnly(True)
        self.cmd_output.setStyleSheet("background-color: black; color: white; font-family: Consolas, monospace; font-size: 10pt;")


        # Add the widgets to the vertical layout
        self.layout.addWidget(self.browser)
        self.layout.addLayout(button_layout)  # Add the horizontal layout of buttons
        self.layout.addWidget(self.cmd_output)


        # Create a QWidget for the central layout and set it as the main widget
        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)


        # Maximize the window
        self.showMaximized()


        # Make the command output take 50% of the available space
        self.cmd_output.setMinimumHeight(self.height() // 3)  # Set the minimum height to 50% of the window height
        self.cmd_output.setMaximumHeight(self.height() // 3)  # Set the maximum height to 50% of the window height


    def run_with_gui(self):
        # Base command to run with GUI
        command = "one.bat"


        # Check if compile.bat should be run
        if self.compile_checkbox.isChecked():
            command = "compile.bat && " + command


        # Create a CommandThread to run the command and update the QTextEdit
        self.command_thread = CommandThread(command)
        self.command_thread.update_output.connect(self.update_cmd_output)
        self.command_thread.start()


    def run_without_gui(self):
        # Get the number from the input box
        number = self.number_input.text().strip()


        # Construct the command based on the input
        if number:
            command = f"one.bat -b {number}"
        else:
            command = "one.bat -b"


        # Check if compile.bat should be run
        if self.compile_checkbox.isChecked():
            command = "compile.bat && " + command


        # Create a CommandThread to run the command and update the QTextEdit
        self.command_thread = CommandThread(command)
        self.command_thread.update_output.connect(self.update_cmd_output)
        self.command_thread.start()


    def update_cmd_output(self, text):
        # Update the QTextEdit with the command output
        self.cmd_output.append(text)

