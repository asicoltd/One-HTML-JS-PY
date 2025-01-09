import os
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView


class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Get the current directory where the Python script is located
        self.script_directory = os.path.dirname(os.path.realpath(__file__))

        # Define the paths for the HTML, JS, and CSS files
        self.html_file = os.path.join(self.script_directory, "index.html")
        self.js_file = os.path.join(self.script_directory, "script.js")
        self.css_file = os.path.join(self.script_directory, "styles.css")

        # Save the HTML, JS, and CSS files inside the Python file directory
        self.save_html_file()
        self.save_js_file()
        self.save_css_file()

        # Set up the browser to load the local HTML file
        self.browser = QWebEngineView(self)
        self.browser.setUrl(QUrl.fromLocalFile(self.html_file))  # Load the HTML file
        self.setCentralWidget(self.browser)

        self.setWindowTitle('Local HTML Browser')
        self.setGeometry(100, 100, 1200, 800)  # Set window size
        self.show()

    def save_html_file(self):
        html_content = f'''
        <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scenario Settings</title>
    <link rel="stylesheet" href="styles.css">
</head>

<body>

    <div id="tabs">
        <button class="tablinks" onclick="openTab(event, 'ScenarioSettings')">Scenario Settings</button>
        <button class="tablinks" onclick="openTab(event, 'InterfaceSettings')">Interface Settings</button>
        <button class="tablinks" onclick="openTab(event, 'GroupSettings')">Group Settings</button>
        <button class="tablinks" onclick="openTab(event, 'MovementSettings')">Movement Settings</button>
        <button class="tablinks" onclick="openTab(event, 'ReportSettings')">Report Settings</button>
        <button class="tablinks" onclick="openTab(event, 'GUISettings')">GUI Settings</button>
    </div>
    <br><br><br>
    <!-- Scenario Settings -->
    <div id="ScenarioSettings" class="tabcontent">

        <h3>Scenario Settings</h3>
        <form id="scenarioForm">
            <label for="scenarioName">Scenario Name: </label>
            <input type="text" id="scenarioName" name="scenarioName" value="Default Scenario">
            <br><br>
            <label for="simulateConnections">Simulate Connections: </label>
            <input type="checkbox" id="simulateConnections" name="simulateConnections" checked>
            <br><br>
            <label for="updateInterval">Update Interval (s): </label>
            <input type="number" id="updateInterval" name="updateInterval" value="0.1">
            <br><br>
            <label for="endTime">End Time (s): </label>
            <input type="number" id="endTime" name="endTime" value="43200" min="0" max="0000" step="1">
            <br>
            <input type="range" id="endTimeRange" name="endTimeRange" value="43200" min="0" max="604800" step="60">
            <br><br>
            <button type="button" onclick="saveAllSettings()">Save Settings</button>
        </form>

    </div>

    <!-- Interface Tab -->
    <div id="InterfaceSettings" class="tabcontent">
        <h3>Interface Settings</h3>

        <!-- Form for Adding New Interface -->
        <form id="newInterfaceForm">
            <label for="interfaceName"> <b>Interface Name:</b></label>
            <input type="text" id="interfaceName" name="interfaceName" required>
            <br>
            <label><b>Type</b></label>
            <input type="radio" id="simpleBroadcast" name="interfaceType" value="SimpleBroadcastInterface">
            <label for="simpleBroadcast">SimpleBroadcastInterface</label>

            <input type="radio" id="interferenceLimited" name="interfaceType" value="InterferenceLimitedInterface">
            <label for="interferenceLimited">InterferenceLimitedInterface</label>

            <input type="radio" id="distanceCapacity" name="interfaceType" value="DistanceCapacityInterface">
            <label for="distanceCapacity">DistanceCapacityInterface</label>
            <br>
            <input type="radio" id="connectivityOptimizer" name="interfaceType" value="ConnectivityOptimizer">
            <label for="connectivityOptimizer">ConnectivityOptimizer</label>

            <input type="radio" id="connectivityGrid" name="interfaceType" value="ConnectivityGrid">
            <label for="connectivityGrid">ConnectivityGrid</label>

            <br><br>
            <label for="transmitSpeed"><b>Transmit Speed:</b></label>
            <input type="number" id="transmitSpeed" name="transmitSpeed" required min="1">

            <label for="transmitRange"><b>Transmit Range:</b></label>
            <input type="number" id="transmitRange" name="transmitRange" required min="1">

            <button type="submit">Add Interface</button>
        </form>
        <br><br><br>
        <!-- Interface List Table -->
        <table border="1px" id="interfaceList">
            <thead>
                <tr>
                    <th>Interface Name</th>
                    <th>Type</th>
                    <th>Transmit Speed</th>
                    <th>Transmit Range</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <!-- Default Interfaces will be displayed here by JavaScript -->
            </tbody>
        </table>
    </div>


    <!-- Group Settings -->
    <div id="GroupSettings" class="tabcontent">
        <h3>Group Settings</h3>
        <!-- Group Tab Form -->
        <!-- Common Group Settings Form -->
        <form id="commonGroupSettingsForm">
            <h3>Common Group Settings</h3>
            
            <br><label for="commonMovementModel">Movement Model:</label>
            <select id="commonMovementModel" name="movement">
                <option value="ShortestPathMapBasedMovement">Shortest Path Map Based Movement</option>
                <option value="OfficeActivityMovement">Office Activity Movement</option>
                <option value="RandomDirectionMapBasedMovement">Random Direction Map Based Movement</option>
                <!-- Add more routers -->
            </select><br>
            <!-- Add more movement models -->

            <br><label for="commonRouter">Router:</label>
            <select id="commonRouter" name="router">
                <option value="MessageRouter">Message Router</option>
                <option value="MaxPropRouter">Max Prop Router</option>
                <option value="EpidemicRouter">Epidemic Router</option>
                <option value="SprayAndWaitRouter">Spray And Wait Router</option>
                <!-- Add more routers -->
            </select><br>

            <label for="commonBufferSize">Buffer Size(Example: 5M):</label>
            <input type="text" id="commonBufferSize" name="bufferSize" value="5M"><br>

            <label for="commonWaitTime">Wait Time (Example: 0, 120):</label>
            <input type="text" id="commonWaitTime" name="WaitTime" value="0, 120"><br>

            <label for="commonnrofInterfaces">Interface Number:</label>
            <input type="number" id="commonnrofInterfaces" name="nrofInterfaces" value="1"><br>
            
            <label for="commonSpeed">Speed(Example: 0.5, 1.5 (Walking Speed)):</label>
            <input type="text" id="commonSpeed" name="Speed" value="0.5, 1.5"><br>

            <label for="commonTtl">Ttl(Message TTL of 300 minutes (5 hours)):</label>
            <input type="number" id="commonTtl" name="commonTtl" value="300"><br>
            
            <label for="commonNumberOfHost">Number of Host:</label>
            <input type="number" id="commonNumberOfHost" name="commonNumberOfHost" value="40"><br>
            <br><br>
        </form>

        <form id="newGroupForm">
            <h3>Cusom Groups</h3>
            <label for="groupID">Group ID:</label>
            <input type="text" id="groupID" name="groupID" required><br>

            <label for="numberOfHosts">Number of Hosts:</label>
            <input type="number" id="numberOfHosts" name="numberOfHosts" required><br>

            <label>Movement Model:</label>
            <input type="radio" id="ShortestPathMapBasedMovement" name="movementModel"
                value="ShortestPathMapBasedMovement">
            <label for="ShortestPathMapBasedMovement">ShortestPathMapBasedMovement</label>
            <input type="radio" id="OfficeActivityMovement" name="movementModel" value="OfficeActivityMovement">
            <label for="OfficeActivityMovement">OfficeActivityMovement</label>
            <!-- Add other movement models as needed -->

            <br><label for="waitTimeMin">Wait Time Min (seconds):</label>
            <input type="number" id="waitTimeMin" name="waitTimeMin"><br>

            <label for="waitTimeMax">Wait Time Max (seconds):</label>
            <input type="number" id="waitTimeMax" name="waitTimeMax"><br>

            <label for="speedMin">Speed Min (m/s):</label>
            <input type="number" step="0.1" id="speedMin" name="speedMin"><br>

            <label for="speedMax">Speed Max (m/s):</label>
            <input type="number" step="0.1" id="speedMax" name="speedMax"><br>

            <label for="bufferSize">Buffer Size (bytes):</label>
            <input type="number" id="bufferSize" name="bufferSize"><br>

            <label for="router">Router:</label>
            <select id="router" name="router">
                <option value="MessageRouter">MessageRouter</option>
                <option value="MaxPropRouter">MaxPropRouter</option>
                <option value="EpidemicRouter">EpidemicRouter</option>
                <!-- Add other routers -->
            </select><br>

            <label for="msgTtl">Message TTL:</label>
            <input type="text" id="msgTtl" name="msgTtl" value="infinite"><br>

            <h3>Active Times:</h3>
            <label for="activeTimeStart1">Start 1:</label>
            <input type="number" id="activeTimeStart1">
            <label for="activeTimeEnd1">End 1:</label>
            <input type="number" id="activeTimeEnd1"><br>

            <!-- Repeat for active time intervals as needed -->

            <button type="submit">Add Group</button>
        </form>

        <!-- Group List Table -->
        <table id="groupList">
            <thead>
                <tr>
                    <th>Group ID</th>
                    <th>Number of Hosts</th>
                    <th>Movement Model</th>
                    <th>Router</th>
                    <th>Active Times</th>
                    <th>Message TTL</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>

    </div>

    <!-- Movement Settings -->
    <div id="MovementSettings" class="tabcontent">
        <h3>Movement Settings</h3>
        <form id="movementForm">
            <label for="movementRngSeed">Movement Model RNG Seed: </label>
            <input type="number" id="movementRngSeed" name="movementRngSeed" value="1">
            <br><br>
            <label for="movementWorldSize">World Size (width, height): </label>
            <input type="text" id="movementWorldSize" name="movementWorldSize" value="4500,3400">
            <br><br>
            <label for="movementWarmup">Warmup Time: </label>
            <input type="number" id="movementWarmup" name="movementWarmup" value="1000">
            <br><br>

            <button type="button" onclick="saveAllSettings()">Save Settings</button>
        </form>
    </div>

    <!-- Report Settings -->
    <div id="ReportSettings" class="tabcontent">
        <h3>Report Settings</h3>
        <form id="reportForm">
            <label for="reportCount">Number of Reports: </label>
            <input type="number" id="reportCount" name="reportCount" value="2">
            <br><br>
            <label for="reportDir">Report Directory: </label>
            <input type="text" id="reportDir" name="reportDir" value="reports/">
            <br><br>

            <button type="button" onclick="saveAllSettings()">Save Settings</button>
        </form>
    </div>

    <!-- GUI Settings -->
    <div id="GUISettings" class="tabcontent">
        <h3>GUI Settings</h3>
        <form id="guiForm">
            <label for="guiUnderlayImage">Underlay Image File Name: </label>
            <input type="text" id="guiUnderlayImage" name="guiUnderlayImage" value="data/helsinki_underlay.png">
            <br><br>
            <label for="guiEventLog">Event Log Panel Events: </label>
            <input type="number" id="guiEventLog" name="guiEventLog" value="100">
            <br><br>

            <button type="button" onclick="saveAllSettings()">Save Settings</button>
        </form>
    </div>
    <br>
    <button onclick="saveAllSettings()">Save All Settings</button>

    <script src="script.js"></script>

</body>

</html>
        '''
        with open(self.html_file, 'w') as f:
            f.write(html_content)

    def save_js_file(self):
        js_content = '''
        // Default values for interface settings
const interfaceSettings = [
    { name: "btInterface", type: "SimpleBroadcastInterface", transmitSpeed: "250k", transmitRange: "10" },
    { name: "highspeedInterface", type: "SimpleBroadcastInterface", transmitSpeed: "10M", transmitRange: "1000" }
];

// Default values for group settings
const groupSettings = [
    { groupId: 'p', numHosts: 50, movementModel: "ShortestPathMapBasedMovement", router: "EpidemicRouter", activeTimes: "0-100", messageTTL: "50", actions: "Edit/Delete" },
    { groupId: 'c', numHosts: 100, movementModel: "ShortestPathMapBasedMovement", router: "EpidemicRouter", activeTimes: "50-150", messageTTL: "100", actions: "Edit/Delete" },
    { groupId: 'w', numHosts: 200, movementModel: "ShortestPathMapBasedMovement", router: "EpidemicRouter", activeTimes: "100-200", messageTTL: "150", actions: "Edit/Delete" },
    { groupId: 't', numHosts: 150, movementModel: "MapRouteMovement", router: "EpidemicRouter", activeTimes: "150-250", messageTTL: "200", actions: "Edit/Delete" },
    { groupId: 't', numHosts: 120, movementModel: "MapRouteMovement", router: "EpidemicRouter", activeTimes: "200-300", messageTTL: "250", actions: "Edit/Delete" },
    { groupId: 't', numHosts: 80, movementModel: "MapRouteMovement", router: "EpidemicRouter", activeTimes: "250-350", messageTTL: "300", actions: "Edit/Delete" }
];

// Function to populate the Interface settings table dynamically
function populateInterfaceTable() {
    const tableBody = document.getElementById("interfaceList").getElementsByTagName("tbody")[0];

    // Clear any existing content
    tableBody.innerHTML = "";

    // Add rows for each interface setting
    interfaceSettings.forEach((setting, index) => {
        const row = tableBody.insertRow();

        const cell1 = row.insertCell(0);
        cell1.innerText = setting.name;

        const cell2 = row.insertCell(1);
        cell2.innerText = setting.type;

        const cell3 = row.insertCell(2);
        cell3.innerText = setting.transmitSpeed;

        const cell4 = row.insertCell(3);
        cell4.innerText = setting.transmitRange;

        const cell5 = row.insertCell(4);
        const editButton = document.createElement("button");
        editButton.innerText = "Edit";
        editButton.onclick = () => editInterfaceSetting(setting);
        cell5.appendChild(editButton);

        // Add Remove button
        const removeButton = document.createElement("button");
        removeButton.innerText = "Remove";
        removeButton.onclick = () => removeInterfaceSetting(index);
        cell5.appendChild(removeButton);
    });
}

// Function to populate the Group settings table dynamically
function populateGroupTable() {
    const tableBody = document.getElementById("groupList").getElementsByTagName("tbody")[0];

    // Clear any existing content
    tableBody.innerHTML = "";

    // Add rows for each group setting
    groupSettings.forEach((group, index) => {
        const row = tableBody.insertRow();

        const cell1 = row.insertCell(0);
        cell1.innerText = group.groupId;

        const cell2 = row.insertCell(1);
        cell2.innerText = group.numHosts;

        const cell3 = row.insertCell(2);
        cell3.innerText = group.movementModel;

        const cell4 = row.insertCell(3);
        cell4.innerText = group.router;

        const cell5 = row.insertCell(4);
        cell5.innerText = group.activeTimes;

        const cell6 = row.insertCell(5);
        cell6.innerText = group.messageTTL;

        const cell7 = row.insertCell(6);
        const editButton = document.createElement("button");
        editButton.innerText = "Edit";
        editButton.onclick = () => editGroupSetting(group);
        cell7.appendChild(editButton);

        // Add Remove button
        const removeButton = document.createElement("button");
        removeButton.innerText = "Remove";
        removeButton.onclick = () => removeGroupSetting(index);
        cell7.appendChild(removeButton);
    });
}

// Function to remove an interface setting
function removeInterfaceSetting(index) {
    // Remove the item from the array
    interfaceSettings.splice(index, 1);

    // Re-populate the table after removal
    populateInterfaceTable();
}

// Function to remove a group setting
function removeGroupSetting(index) {
    // Remove the item from the array
    groupSettings.splice(index, 1);

    // Re-populate the table after removal
    populateGroupTable();
}

// Function to edit interface settings (as an example)
function editInterfaceSetting(setting) {
    // Here you can prompt for new values or open a modal to edit settings
    const newSpeed = prompt(`Edit Transmit Speed for ${setting.name}`, setting.transmitSpeed);
    const newRange = prompt(`Edit Transmit Range for ${setting.name}`, setting.transmitRange);
    if (newSpeed && newRange) {
        setting.transmitSpeed = newSpeed;
        setting.transmitRange = newRange;
    }
    populateInterfaceTable();  // Update the table with new values
}




// Add an event listener to handle the form submission
document.getElementById("newGroupForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Extract values from the form
    const groupId = document.getElementById("groupID").value;
    const numHosts = parseInt(document.getElementById("numberOfHosts").value, 10);
    const movementModel = document.querySelector('input[name="movementModel"]:checked')?.value;
    const waitTimeMin = parseFloat(document.getElementById("waitTimeMin").value) || 0;
    const waitTimeMax = parseFloat(document.getElementById("waitTimeMax").value) || 0;
    const speedMin = parseFloat(document.getElementById("speedMin").value) || 0;
    const speedMax = parseFloat(document.getElementById("speedMax").value) || 0;
    const bufferSize = parseInt(document.getElementById("bufferSize").value, 10) || 0;
    const router = document.getElementById("router").value;
    const msgTtl = document.getElementById("msgTtl").value || "infinite";

    const activeTimeStart1 = parseInt(document.getElementById("activeTimeStart1").value, 10) || 0;
    const activeTimeEnd1 = parseInt(document.getElementById("activeTimeEnd1").value, 10) || 0;

    // Construct the new group object
    const newGroup = {
        groupId: groupId,
        numHosts: numHosts,
        movementModel: movementModel || "ShortestPathMapBasedMovement",
        router: router,
        activeTimes: `${activeTimeStart1}-${activeTimeEnd1}`,
        messageTTL: msgTtl,
        actions: "Edit/Delete", // Default action text
    };

    // Add the new group to the groupSettings array
    groupSettings.push(newGroup);

    // Repopulate the group table to include the new group
    populateGroupTable();

    // Reset the form for a new entry
    document.getElementById("newGroupForm").reset();
});

// Function to edit group settings (as an example)
function editGroupSetting(group) {
    // Here you can prompt for new values or open a modal to edit group settings
    const newNumHosts = prompt(`Edit Number of Hosts for Group ${group.groupId}`, group.numHosts);
    const newMovementModel = prompt(`Edit Movement Model for Group ${group.groupId}`, group.movementModel);
    const newRouter = prompt(`Edit Router for Group ${group.groupId}`, group.router);
    const newActiveTimes = prompt(`Edit Active Times for Group ${group.groupId}`, group.activeTimes);
    const newMessageTTL = prompt(`Edit Message TTL for Group ${group.groupId}`, group.messageTTL);

    if (newNumHosts && newMovementModel && newRouter && newActiveTimes && newMessageTTL) {
        group.numHosts = newNumHosts;
        group.movementModel = newMovementModel;
        group.router = newRouter;
        group.activeTimes = newActiveTimes;
        group.messageTTL = newMessageTTL;
    }
    populateGroupTable();  // Update the table with new values
}

// Call the functions to populate tables when the page loads
document.addEventListener("DOMContentLoaded", function () {
    populateInterfaceTable();  // Populate the Interface settings table
    populateGroupTable();      // Populate the Groups settings table
});


// Function to handle tab switching
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}
// Synchronize the number input and range slider for "End Time"
const endTimeInput = document.getElementById("endTime");
const endTimeRange = document.getElementById("endTimeRange");

endTimeInput.addEventListener("input", function () {
    endTimeRange.value = this.value;
});

endTimeRange.addEventListener("input", function () {
    endTimeInput.value = this.value;
});

// Function to generate and download the settings file based on the tab
function saveAllSettings() {
    let content = '';

    // Collect all tabs' data
    // Scenario Tab
    content += `
## Scenario settings
Scenario.name = ${document.getElementById("scenarioName").value}
Scenario.simulateConnections = ${document.getElementById("simulateConnections").checked ? "true" : "false"}
Scenario.updateInterval = ${document.getElementById("updateInterval").value}
Scenario.endTime = ${document.getElementById("endTime").value}
    `;


    // Movement Tab
    content += `
## Movement model settings
MovementModel.rngSeed = ${document.getElementById("movementRngSeed").value}
MovementModel.worldSize = ${document.getElementById("movementWorldSize").value}
MovementModel.warmup = ${document.getElementById("movementWarmup").value}
    `;

    // Now for the Interface and Group Tables
    // Collecting Interface Table Data
    content += `
## Interface List Settings:
`;
    const interfaceTableRows = document.getElementById("interfaceList").getElementsByTagName("tbody")[0].rows;
    for (let row of interfaceTableRows) {
        const interfaceName = row.cells[0].innerText;
        const interfaceType = row.cells[1].innerText;
        const transmitSpeed = row.cells[2].innerText;
        const transmitRange = row.cells[3].innerText;

        content += `
#${interfaceName}.name = ${interfaceName}
${interfaceName}.type = ${interfaceType}
${interfaceName}.transmitSpeed = ${transmitSpeed}
${interfaceName}.transmitRange = ${transmitRange}
        `;
    }
 // Extract values from the form
//  document.getElementById("commonGroupSettingsForm").addEventListener("submit", function (event) {
//     event.preventDefault(); // Prevent the default form submission

    // Extract values from the form
    const CommoNmovementModel = document.getElementById("commonMovementModel").value;
    const CommoNrouter = document.getElementById("commonRouter").value;
    const CommoNbufferSize = document.getElementById("commonBufferSize").value;
    const CommoNwaitTime = document.getElementById("commonWaitTime").value;
    const CommoNinterface = document.getElementById("commonnrofInterfaces").value;
    const CommoNspeed = document.getElementById("commonSpeed");
    const CommoNmsgTtl = document.getElementById("commonTtl").value;
    const CommoNnumHosts = document.getElementById("commonNumberOfHost").value;
    

    // Collecting Common group Data
    content += `
## Common settings for all groups:
Group.movementModel = ${CommoNmovementModel}
Group.router = ${CommoNrouter}
Group.bufferSize = ${CommoNbufferSize}
Group.waitTime =${CommoNwaitTime}
# All nodes have the bluetooth interface
Group.nrofInterfaces = ${CommoNinterface}
Group.interface = btInterface
Group.speed = ${CommoNspeed}
# Message TTL of 300 minutes (5 hours)
Group.msgTtl = ${CommoNmsgTtl}
Group.nrofHosts = ${CommoNnumHosts}
`;
// });
    // Collecting Group Table Data
    const groupTableRows = document.getElementById("groupList").getElementsByTagName("tbody")[0].rows;
    let serial = 1;
    for (let row of groupTableRows) {
        const groupId = row.cells[0].innerText;
        const numHosts = row.cells[1].innerText;
        const movementModel = row.cells[2].innerText;
        const router = row.cells[3].innerText;
        const activeTimes = row.cells[4].innerText;
        const messageTTL = row.cells[5].innerText;

        content += `
Group${serial}.groupId = ${groupId}
Group${serial}.numHosts = ${numHosts}
Group${serial}.movementModel = ${movementModel}
Group${serial}.router = ${router}
Group${serial}.activeTimes = ${activeTimes}
Group${serial}.messageTTL = ${messageTTL}
        `;
        serial++;
    }
    content += `
Scenario.nrofHostGroups = ${serial}
        `;
    // Report Tab
    content += `
## Report settings
Report.count = ${document.getElementById("reportCount").value}
Report.directory = ${document.getElementById("reportDir").value}
    `;

    // GUI Tab
    content += `
## GUI settings
GUI.underlayImageFileName = ${document.getElementById("guiUnderlayImage").value}
GUI.eventLogPanel.events = ${document.getElementById("guiEventLog").value}
    `;



    // Create a Blob with the content and download it as a .txt file
    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "default_settings.txt";
    link.click();
}

        '''
        with open(self.js_file, 'w') as f:
            f.write(js_content)

    def save_css_file(self):
        css_content = '''
        /* Styling for tab navigation */
.tabs {
    overflow: hidden;
    background-color: #f1f1f1;
}

.tablinks {
    float: left;
    background-color: #000000;
    border: none;
    outline: none;
    padding: 14px 16px;
    font-size: 17px;
    cursor: pointer;
    transition: 0.3s;
}

.tablinks:hover {
    background-color: #66ad69;
}

.tablinks.active {
    background-color: #4CAF50;
    color: white;
}

/* Tab content styling */
.tabcontent {
    display: none;
    padding: 20px;
    background-color: #f4f4f4;
    border: 1px solid #ddd;
    margin-top: 10px;
}

input[type="number"],
input[type="text"] {
    padding: 5px;
    width: 200px;
}

button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}

pre {
    background-color: #f4f4f4;
    padding: 10px;
    border-radius: 5px;
    white-space: pre-wrap;
}

        '''
        with open(self.css_file, 'w') as f:
            f.write(css_content)


def main():
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
