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
```
git clone https://github.com/akeranen/the-one.git
cd the-one
git clone https://github.com/asicoltd/One-HTML-JS-PY.git
cd One-HTML-JS-PY
pip install -r requirements.txt
move OneConfigGui5.py ../
move index.html ../
cd ..
Python OneConfigGui5.py
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

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAlEAAAEtCAYAAAAodDX5AAAQdUlEQVR4Xu3dz4p0SV7H4bqnBucCnIULBxzcCuLCm+hNb1x6K03vxFsQkVEvYLBd6qYRBRcjr+Q7HIj5noiTmb8TJ6q68nngQ9WJ8ycrw5fMHyPDvH0BAOBpb7kAAMB9higAgAJDFABAwW6Ient700XZ4zXZ5zXZ5+uzx2uyz2v6jHbvKt+05mWP12Sf12Sfr88er8k+r+kz2r2rfNOalz1ek31ek32+Pnu8Jvu8ps9o967yTWte9nhN9nlN9vn67PGa7POaPqPdu8o3rXnZ4zXZ5zXZ5+uzx2uyz2v6jHbvKt+05mWP12Sf12Sfr88er8k+r+kz2r2rfNOalz1ek31ek32+Pnu8Jvu8ps9o967yTT/bjGdUa1/7Pf+OUbP2+EwzX3/ms2Z25T5f9dx7vdfrHnXlPp/t6O8anRutv2cz9jjvz+NVta/7Xn/DqE2un23mez66f3RutP5efUa7d5Vvekb57GeOU3tNvs6o7dqe3mvm8/NctVnPybZnts/v/d7Ka9rnjI5Ha7neurc2esaZ8nVWtL1e+9r5N7Ty/l7tta3RNb3r2t9nd+WzH6l9/Vae247z/lxvPbLWe8bs8rXO1j7v6Nm969rj9rq8Z1trzx3VXp9yPe9pz+dzn2nGM3qNnpnrjxxvRtf01lvPrLW/z+wz2r2rfNOVRs/J9d5xu9Y7zuvb49HaaL23dmWbXJ9R+9x8jd65o2t6x0fn8rhXXnPv+EybXL+69jV7f0Me57n2fF6bx1mez+dd0dWv0dqO2/W8Lu8dPW90TR731u4dz26T62fKZ7bHR+eyXM/jXqNreuvbWu/c7Da5frb2mc8+P6/P423t6DXyONd697fHs/uMdu8q3/SZnn1e/g2947w+n/FMz97/7PXZJtdn1D43X6N37uia3vHRem8ty2vy+N76M21yfXb5Gu1x72/I46Py2jzO8nweX9Em11eUr/vscW8tj3treXxv/WybXH+29jn5zPb3R45H63l8tu15jz730et6bXL9bGeemffeO+6t5XGubXrnrugz2r2rfNPPduYZ+Tf0jtuf2TPXHp0b3ZvHz7bJ9RkdPbc9t/2eP/P86PjoXB4/cm5bz59n2uT6jJ55bl6bx8907948v8nrZrbiNbLR6+V6Hh+d245zfbTWO3/vumqbXD/T6HnPruf5R6979J7RNffWK21y/WztM7ffH/2ZjdZ7546e1a7l+U3eM6vPaPeu8k1rXvZ4TR91n1f+TSte66Pu82fKHq/JPv++q/fgM9q9q3zTr9hVe3HVc3+uXbUXH3WfV/xNK9/7ytf6SK183ytf6+fSFXtyxTN/Tq16/5/R7l3lm9a87PGa7POa7PP12eM12ec1fUa7d5VvWvOyx2uyz2uyz9dnj9dkn9f0Ge3eVb5pzcser8k+r8k+X589XpN9XtNntHtX+aY1L3u8Jvu8Jvt8ffZ4TfZ5TZ/R7l3lm9a87PGa7POa7PP12eM12ec1fUa7d5VvWvOyx2uyz2uyz9dnj9dkn9f0Ge3eVb5pzcser8k+r8k+X589XpN9XtNntHtX+aY1L3u8Jvu8JoBXt/skzA9Kzcser8k+rwng1e0+CfODUvOyx2uyz2sCeHW7T8L8oNS87PGa7POaAF7d7pMwPyg1L3u8Jvu8JoBXt/skzA9Kzcser8k+rwng1e0+CfODUvOyx2uyz2sCeHW7T8L8oBz1zLVXt/0tH+lv6vXsHs+u99q9tXvnRusfpU2un6l93uxnbz363EevuzqAV7f7JMwPykfq3ZfP7P2+Hec9o2va30drvetbvdfJ+9vzj14/Oj66dnW91861PO6ttx5Z6z3jyvJ1Z5TP247b12p/790zuu9eeU+rvWZ0nOdmBfDqdp+E+UE5Kq89Os7f89q85pHj0frR8fb76Gevo3NH1+XxttZbX1XvtUdr7Xpek8e9tXvHV7bJ9TPl8/I18vxoPY+z0fnea42uzeuuCuDV7T4J84OyV++6XGuPe/L+3j2jc0frR8fb76Ofed3ouFdek8fbWm99Vb3X7q1lrdE9uZbHo7Ur2uT6mfJ5PXl+dF8+u1d7/6Z3Lu87ekaePxvAq9t9EuYH5ajt2tE9o/XRuXxe75rReu+eR67Ln70euaZX7/pNrr9Hj7yvPHd0T2+td/7edTPa5PqZ2uc98+y8No/vnTta65175PysAF7d7pMwPyg1L3u8Jvv8+67eA4BXt/skzA9KzevV9vi93u97ve5HadX7B3h1u0/C/KDUvOzxmuzzmgBe3e6TMD8oNS97vCb7vCaAV7f7JMwPSs3LHq/JPq8J4NXtPgnzg1Lzssdrss9rAnh1u0/C/KDUvOzxmuzzmgBe3e6TMD8oNS97vCb7vCaAV7f7JMwPSs3LHq/JPq8J4NX5JAQAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoOOFf/vNfv/zpD3+mC/rVD7/+8rvf/OOX//7jP9IV/fIX+c8ZeJIhCk74i7/7y92Xv+b1P3/+J/svf00LOMcQBSfkl77mll/6mhtwjiEKTsgvfc0tv/Q1N+AcQxSckF/6mlt+6WtuwDmGKDghv/TvVb0vm/Wco555jUeve7b80p9RK8+11+Tao917dl6baysDzjFEwQn5pf9oZ+5tm/Wcj1p+6X+0bnLt7LmVAecYouCE/NK/1+iedj2vOTrX6941987fu663nmv3jh8tv/RndzM6zt/z2rzmaC3Xt9/z2k2u5bNmBZxjiIIT8kv/0bZ781nbz965PH/U0XVH545q9c49cjy6f1R+6c/uZvu5OTo/ur9X3tte257Le3LtaP1swDmGKDghv/QfLe/djnN9tHbm3Gj90Xr359q940fLL/2ruxn93h73rsnyXD4v17bjXLsy4BxDFJyQX/r3yvtaee12PteOntO7b/s9r7lX7/r2ePv96LrW6Nqj8kt/Rq1cv3dtXtOeu7eW5ze96/JcHs8KOMcQBSfkl77+sLP7lF/6r9Im12cHnGOIghPyS19zyy99zQ04xxAFJ+SXvuaWX/qaG3COIQpO8D9AfG3+B4ivDTjHEAUn/OY//nn3xa85/eqHX3/53T/9w+6LX5P65S/ynzPwJEMUnPTjf/37l7/6+7/eDQGqd9vPzf/922/3A4BO9b9/+zfNv2CgyhAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABYYoAIACQxQAQIEhCgCgwBAFAFBgiAIAKDBEAQAUGKIAAAoMUQAABW8//fTTF0mSJD2XIUqSJKmQIUqSJKmQIeqDBsD7aT+Pv//++y8//vijmvI7K8+/Qrf3bYj6oAHwftrPY0PUvvzOyvOv0O19d//bed98881ug7Q2AN5P+3lsiNqX31l5/hW6ve93GaLe3t52a4/Uu6+3NquZz+49q7e2dfPdd9/94f9hFnm11wVI7efxmSHq9jm//dx+P9Ozz3j2+tE9+ffnd1Ze/2hH+5PHj/TsPaPre+v5N379Hs9/ODePDlG3h+Xao+e283lde3x07ug5vd9HP/M5R2u9+9ufeX2+xuhZvW5uQ8VosNjWj665OTo/esbo+pT39dZ753tGzwJ4D+3n8SND1O3zPL988/etXBs9Kxtd36v3etv6s8/qXZ/fWXl91nut9pn3/t5cu7fens9r29fKc0fl9V+/x/Mfzk0OUbebcsOO1h85Nzrfnstr8rhd653rXTcqz4/+xny99mfv+rzv3trWzdFQcXSudTSctOuj34+Mnt2u98632uvuXQuwSvt53A5Rt8/t/HJt19vz7dpW3tdrdN2jz2hfL6/PvynvHZXX53dWPj/rreff2bum1+jadr13vnftI9flPdvx1+/x/Idzk0PU1wubF2zX8vfede16Xtv7OXrO0TPy96Pj0T3t+d617XWj+3Ktd0/+ns+/dbMNFjlcPDOgjO7PZ7TXtGt5b2t0b1uu946PzgG8h/bzuPefRG2f44982bZr96575Nre+fa63u/3rslr87XymvzOynvz78vf85mje/Lvynt61+bP3r35e6/2b+o98+t3eG6EPkYAvJ/287g3RL16+Z2V51+h2/s2RH3Qvv32W0nSO9V+Hhui9uV3Vp5/hW7v2xAlSZJUyBAlSZJUyBAlSZJU6C3//8CSJEm631v+V/gkSZJ0nCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSpkCFKkiSp0G2I+n8UceTBCUOYlAAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,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>

[image3]: <data:image/png;base64,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>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnAAAAAcCAIAAABu2BX8AAACq0lEQVR4Xu3a223jQAyFYfXk7vSyFbkod+AOHMgETk7IGflGZB3j/x6EEclRol1gDmJ4OQMAgJctuYDHret6AYA+Ol6Ox+PpE9kJes69v0YvQqA2IFAB9NLxQqC+P73IFqiHw2H2f4l7EKgAeul4IVDfn17kRqAuV7p91D3bNXBz8h0Mf8kI1H9X+jf09Z2e2FI98ZAXf20A7XS8RKDGWZoPclO7vuXm9vvdfJR367Bu7QTdArVOJhrQVXxAt86Lw4GhNJke7rd6kRuBOrT8DBW/TWtRMfFuLFSpu4at2breyvAhKs52neddBapfUzINg8rH6pYo1spOcdi9/PzdvBKLWh8+BMCv0fHy6F+oyyhEfZ0qqS51i4q1Hq24qrszdhoFqg+kn1KfGQN1ptbVUnfYSmvdpqL4o/QiWzzsB+pSIiRV/DatRUXvxlXdWqlmLe2txaoO64fOfvp+1z/yVSDdk0k+9sSWWhx2L6OAnG1RURUAv0/HiwJ1mZzsz4nTLBa5d6UBvxUb/B6Iq7o7Y6fXAjW69fmqp5YqtbVDW3Ljyh+lF9niYT9QQ2zWOhWHrTpQi8O6PyfVa2t2rUXnz6yTs0d53flHvimQVKl8Pt163ak7q4vqvo6Fr+tw3KoI4L/Q8ZL+Qo2DyCuqp7VP1l1pxhfpmtTW7CH7LTtBvwPVhzUZUkUzUUyLWKfbtIi1qKXbnUpq6UW2bDgU3y/6oZYSiq/gS0kAeul4efQj37/CTtDP+lISXrQCQCsdLwTq+9OLEKgAADQgUAEAaECgAgDQgEAFAKDBFqjrusb3gAEAwEP0JTICFQCA5xGoAAA0IFABAGhAoAIA0IBABQCgAYEKAEADAhUAgAYEKgAADQhUAAAaEKgAADQgUAEAaECgAgDQgEAFAKCBAvULXJZFdFeajVQAAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,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>
