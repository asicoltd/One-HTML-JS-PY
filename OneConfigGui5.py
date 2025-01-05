import subprocess; subprocess.run("pip install PyQt5 PyQtWebEngine", shell=True)
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit, QCheckBox, QSpacerItem, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QThread, pyqtSignal

class CustomWebEngineView(QWebEngineView):
    def __init__(self):
        super().__init__()

    # Override the contextMenuEvent to disable the right-click menu
    def contextMenuEvent(self, event):
        # Do nothing to disable the context menu (both custom and browser default)
        pass

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self):
        super().__init__()

    # Override the contextMenuEvent to ensure no context menu in the page
    def contextMenuEvent(self, event):
        # Do nothing to disable the context menu
        pass

class CommandThread(QThread):
    update_output = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        # Execute the command
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        # Read output line by line and emit the output to update QTextEdit
        for line in iter(process.stdout.readline, b''):
            self.update_output.emit(line.decode('utf-8'))

        for line in iter(process.stderr.readline, b''):
            self.update_output.emit(line.decode('utf-8'))

        process.stdout.close()
        process.stderr.close()
        process.wait()

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

        # Your HTML code as a string
        html_code = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scenario Settings</title>

    <style>
        .tabs {
            display: flex;
            /* Use flexbox to display tabs in a row */
            justify-content: space-evenly;
            /* Distribute tabs evenly across the width */
            background-color: #f1f1f1;
            width: 100%;
            /* Ensure the tabs container spans the full width */
            overflow-x: auto;
            /* Allow horizontal scrolling if tabs overflow */
            flex-wrap: nowrap;
            /* Prevent tabs from wrapping to the next line */
        }

        .tablinks {
            background-color: #000000;
            border: none;
            outline: none;
            padding: 14px 16px;
            font-size: 17px;
            cursor: pointer;
            text-align: center;
            /* Center text within the tab */
            transition: 0.3s;
            white-space: nowrap;
            /* Prevent text from wrapping inside each tab */
            max-width: 200px;
            /* Optional: set max-width for tabs */
            flex: 1 1 auto;
            /* Allow each tab to grow and shrink */
        }

        .tablinks:hover {
            background-color: #66ada9;
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

        /* Style input fields */
        input[type="number"],
        input[type="text"] {
            padding: 5px;
            width: 100%;
            /* Make input fields fluid */
            box-sizing: border-box;
            /* Include padding in width calculation */
            margin-bottom: 10px;
        }

        /* Style buttons */
        button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            width: 100%;
            /* Make button fill the width */
        }

        button:hover {
            background-color: #45a049;
        }

        /* Styling for <pre> tags */
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            white-space: pre-wrap;
        }

        /* Existing styles for .tabs and other elements */

        /* Button container at the bottom */
        .button-container {
            display: flex;
            gap: 10px;
            /* Adds space between buttons */
            position: fixed;
            bottom: 20px;
            /* Distance from the bottom */
            left: 50%;
            transform: translateX(-50%);
            /* Centers the button container horizontally */
            padding: 10px;
            z-index: 10;
            /* Ensures the buttons stay above other content */
        }

        button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            width: 200px;
            /* Optional: fix the button width */
        }

        .custom {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
        }

        .default {
            background-color: #f44336;
            color: white;
            border: none;
            border-radius: 5px;
        }

        .default:hover {
            background-color: #ff0000;
        }
    </style>
</head>

<body>

    <div id="tabs">
        <button class="tablinks" onclick="openTab(event, 'ScenarioSettings')">Scenario Settings</button>
        <button class="tablinks" onclick="openTab(event, 'InterfaceSettings')">Interface Settings</button>
        <button class="tablinks" onclick="openTab(event, 'GroupSettings')">Group Settings</button>
        <button class="tablinks" onclick="openTab(event, 'EventSettings')">Event Settings</button>
        <button class="tablinks" onclick="openTab(event, 'MovementSettings')">Movement Settings</button>
        <button class="tablinks" onclick="openTab(event, 'ReportSettings')">Report Settings</button>
        <button class="tablinks" onclick="openTab(event, 'RouterOptimizationSettings')">Router and Optimization</button>
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
                <option value="BusControlSystem">Bus Control System</option>
                <option value="BusMovement">BusMovement</option>
                <option value="BusTravellerMovement">Bus Traveller Movement</option>
                <option value="CarMovement">Car Movement</option>
                <option value="ClusterMovement">Cluster Movement</option>
                <option value="EveningActivityControlSystem">Evening Activity ControlSystem</option>
                <option value="EveningActivityMovement">Evening Activity Movement</option>
                <option value="EveningTrip">Evening Trip</option>
                <option value="ExtendedMovementModel">Extended Movement Model</option>
                <option value="ExternalMovement">External Movement</option>
                <option value="ExternalPathMovement">External Path Movement</option>
                <option value="GridLocation">Grid Location</option>
                <option value="HomeActivityMovement">Home Activity Movement</option>
                <option value="LinearFormation">Linear Formation</option>
                <option value="LinearMovement">Linear Movement</option>
                <option value="MapBasedMovement">Map Based Movement</option>
                <option value="MapRouteMovement">Map Route Movement</option>
                <option value="ModifiedRandomDirection">Modified Random Direction</option>
                <option value="MovementModel">Movement Model</option>
                <option value="OfficeActivityMovement">Office Activity Movement</option>
                <option value="RandomDirection">Random Direction</option>
                <option value="RandomWalk">Random Walk</option>
                <option value="RandomWaypoint">Random Waypoint</option>
                <option value="ShortestPathMapBasedMovement">Shortest Path Map Based Movement</option>
                <option value="StationaryMovement">Stationary Movement</option>
                <option value="SwitchableMovement">Switchable Movement</option>
                <option value="TransportMovement">Transport Movement</option>
                <option value="WorkingDayMovement">Working Day Movement</option>

                <!-- Add more movement models -->
            </select><br>

            <br><label for="commonRouter">Router:</label>
            <select id="commonRouter" name="router">
                <option value="ActiveRouter">Active Router</option>
                <option value="DirectDeliveryRouter">Direct Delivery Router</option>
                <option value="EpidemicOracleRouter">Epidemic Oracle Router</option>
                <option value="EpidemicRouter">Epidemic Router</option>
                <option value="FirstContactRouter">First Contact Router</option>
                <option value="LifeRouter">Life Router</option>
                <option value="maxprop">maxprop</option>
                <option value="MaxPropRouter">Max Prop Router</option>
                <option value="MaxPropRouterWithEstimation">Max Prop Router With Estimation</option>
                <option value="MessageRouter">Message Router</option>
                <option value="PassiveRouter">Passive Router</option>
                <option value="ProphetRouter">Prophet Router</option>
                <option value="ProphetRouterWithEstimation">Prophet Router With Estimation</option>
                <option value="ProphetV2Router">Prophet V2 Router</option>
                <option value="SprayAndWaitRouter">Spray And Wait Router</option>
                <option value="WaveRouter">Wave Router</option>
                <!-- Add more routers -->
            </select><br>
            <br><label for="commonInterface">Interface:</label>
            <select id="commonInterface" name="interface">
            <option value="btInterface">Select an Interface</option>
            </select>
            <label for="commonBufferSize">Buffer Size(Example: 5M):</label>
            <input type="text" id="commonBufferSize" name="bufferSize" value="5M"><br>
            
            <label for="commonRouteFile">Route File:</label>
            <input type="file" id="commonRouteFile" name="RouteFile" accept=".wkt">

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
            <select id="Movement" name="Movement">
                <option value="BusControlSystem">Bus Control System</option>
                <option value="BusMovement">BusMovement</option>
                <option value="BusTravellerMovement">Bus Traveller Movement</option>
                <option value="CarMovement">Car Movement</option>
                <option value="ClusterMovement">Cluster Movement</option>
                <option value="EveningActivityControlSystem">Evening Activity ControlSystem</option>
                <option value="EveningActivityMovement">Evening Activity Movement</option>
                <option value="EveningTrip">Evening Trip</option>
                <option value="ExtendedMovementModel">Extended Movement Model</option>
                <option value="ExternalMovement">External Movement</option>
                <option value="ExternalPathMovement">External Path Movement</option>
                <option value="GridLocation">Grid Location</option>
                <option value="HomeActivityMovement">Home Activity Movement</option>
                <option value="LinearFormation">Linear Formation</option>
                <option value="LinearMovement">Linear Movement</option>
                <option value="MapBasedMovement">Map Based Movement</option>
                <option value="MapRouteMovement">Map Route Movement</option>
                <option value="ModifiedRandomDirection">Modified Random Direction</option>
                <option value="MovementModel">Movement Model</option>
                <option value="OfficeActivityMovement">Office Activity Movement</option>
                <option value="RandomDirection">Random Direction</option>
                <option value="RandomWalk">Random Walk</option>
                <option value="RandomWaypoint">Random Waypoint</option>
                <option value="ShortestPathMapBasedMovement">Shortest Path Map Based Movement</option>
                <option value="StationaryMovement">Stationary Movement</option>
                <option value="SwitchableMovement">Switchable Movement</option>
                <option value="TransportMovement">Transport Movement</option>
                <option value="WorkingDayMovement">Working Day Movement</option>

                <!-- Add more movement models -->
            </select><br>
            <br><label for="movementRouteType">Movement Route Type:</label>
            <input type="file" id="movementRouteType" name="mapFiles" accept=".wkt">
            

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
                <option value="ActiveRouter">Active Router</option>
                <option value="DirectDeliveryRouter">Direct Delivery Router</option>
                <option value="EpidemicOracleRouter">Epidemic Oracle Router</option>
                <option value="EpidemicRouter">Epidemic Router</option>
                <option value="FirstContactRouter">First Contact Router</option>
                <option value="LifeRouter">Life Router</option>
                <option value="maxprop">maxprop</option>
                <option value="MaxPropRouter">Max Prop Router</option>
                <option value="MaxPropRouterWithEstimation">Max Prop Router With Estimation</option>
                <option value="MessageRouter">Message Router</option>
                <option value="package">package.html</option>
                <option value="PassiveRouter">Passive Router</option>
                <option value="ProphetRouter">Prophet Router</option>
                <option value="ProphetRouterWithEstimation">Prophet Router With Estimation</option>
                <option value="ProphetV2Router">Prophet V2 Router</option>
                <option value="schedule">schedule</option>
                <option value="SprayAndWaitRouter">Spray And Wait Router</option>
                <option value="util">util</option>
                <option value="WaveRouter">Wave Router</option>

                <!-- Add other routers -->
            </select><br>

            <label for="msgTtl">Message TTL:</label>
            <input type="text" id="msgTtl" name="msgTtl" value="300"><br>

            <h3>Active Times:</h3>
            <label for="activeTimeStart1">Active Time (start1,end1,start2,end2....)</label>
            <input type="text" id="activeTimeStart1"><br>

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
                    <th>Movement Route</th>
                    <th>Router</th>
                    <th>Active Times</th>
                    <th>Message TTL</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>

    </div>
    <!-- Event Tab -->
    <div id="EventSettings" class="tabcontent">
        <h3>Event Settings</h3>

        <!-- Form for Adding New Event -->
        <form id="newEventForm">
            <label for="eventClass"> <b>Event Class:</b> </label>
            <input type="text" id="eventClass" name="eventClass" value="MessageEventGenerator" readonly><br><br>

            <label for="eventIntervalMin"> <b>Creation Interval (seconds):</b> </label>
            <input type="number" id="eventIntervalMin" name="eventIntervalMin" value="25" required> to
            <input type="number" id="eventIntervalMax" name="eventIntervalMax" value="35" required><br><br>

            <label for="eventSizeMin"> <b>Message Size:</b> </label>
            <input type="number" id="eventSizeMin" name="eventSizeMin" value="500" required> (Use k for Kb, M for MB)
            <input type="number" id="eventSizeMax" name="eventSizeMax" value="1000" required> <br><br>

            <label for="eventHostsMin"> <b>Message Source/Destination Hosts:</b> </label>
            <input type="number" id="eventHostsMin" name="eventHostsMin" value="0" required> to
            <input type="number" id="eventHostsMax" name="eventHostsMax" value="126" required><br><br>

            <label for="eventPrefix"> <b>Message ID Prefix:</b> </label>
            <input type="text" id="eventPrefix" name="eventPrefix" value="M" required><br><br>

            <button type="submit">Add Event</button>
        </form>
        <br><br><br>

        <!-- Event List Table -->
        <table border="1px" id="eventList">
            <thead>
                <tr>
                    <th>Event Class</th>
                    <th>Creation Interval (s)</th>
                    <th>Message Size (kB)</th>
                    <th>Hosts</th>
                    <th>Prefix</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <!-- Default Events will be displayed here by JavaScript -->
            </tbody>
        </table>
    </div>
    <!-- Movement Model Settings -->
    <div id="MovementSettings" class="tabcontent">
        <h3>Movement Model Settings</h3>
        <form id="movementModelForm">
            <!-- RNG Seed -->
            <label for="rngSeed">RNG Seed:</label>
            <input type="number" id="rngSeed" name="rngSeed" value="1">
            <br><br>

            <!-- World Size -->
            <label for="worldSize">World Size (width, height in meters):</label>
            <input type="text" id="worldSize" name="worldSize" value="4500, 3400">
            <br><br>

            <!-- Warmup Time -->
            <label for="warmup">Warmup Time (seconds):</label>
            <input type="number" id="warmup" name="warmup" value="1000">
            <br><br>

            <!-- Map-Based Movement Settings -->
            <label for="mapFiles">Map Files:</label>
            <input type="file" id="mapFiles" name="mapFiles[]" accept=".wkt" multiple>
            <br><br>
        </form>

        <!-- Display selected map files -->
        <h4>Selected Map Files:</h4>
        <ul id="fileList"></ul>
    </div>


    <!-- Report Settings -->
    <div id="ReportSettings" class="tabcontent">
        <h3>Report Settings</h3>

        <!-- Form for Adding New Reports -->
        <form id="newReportForm">
            <label for="reportClass"><b>Report Class:</b></label>
            <select id="reportClass" name="reportClass" required>
                <option value="AdjacencyGraphvizReport">AdjacencyGraphvizReport</option>
                <option value="BufferOccupancyReport">BufferOccupancyReport</option>
                <option value="ConnectivityDtnsim2Report">ConnectivityDtnsim2Report</option>
                <option value="ConnectivityONEReport">ConnectivityONEReport</option>
                <option value="ConnectivityReportConnector">ConnectivityReportConnector</option>
                <option value="ContactsDuringAnICTReport">ContactsDuringAnICTReport</option>
                <option value="ContactsPerHourReport">ContactsPerHourReport</option>
                <option value="ContactTimesReport">ContactTimesReport</option>
                <option value="CreatedMessagesReport">CreatedMessagesReport</option>
                <option value="DeliveredMessagesReport">DeliveredMessagesReport</option>
                <option value="DistanceDelayReport">DistanceDelayReport</option>
                <option value="DTN2Reporter">DTN2Reporter</option>
                <option value="EncountersVSUniqueEncountersReport">EncountersVSUniqueEncountersReport</option>
                <option value="EnergyLevelReport">EnergyLevelReport</option>
                <option value="EventLogReport">EventLogReport</option>
                <option value="InterContactTimesReport">InterContactTimesReport</option>
                <option value="JumpSizeDistributionReport">JumpSizeDistributionReport</option>
                <option value="LocationSnapshotReport">LocationSnapshotReport</option>
                <option value="MessageAvailabilityReport">MessageAvailabilityReport</option>
                <option value="MessageCopyCountReport">MessageCopyCountReport</option>
                <option value="MessageDelayReport">MessageDelayReport</option>
                <option value="MessageDeliveryReport">MessageDeliveryReport</option>
                <option value="MessageGraphvizReport">MessageGraphvizReport</option>
                <option value="MessageLocationReport">MessageLocationReport</option>
                <option value="MessageReport">MessageReport</option>
                <option value="MessageStatsReport">MessageStatsReport</option>
                <option value="MovementListenerTestReport">MovementListenerTestReport</option>
                <option value="MovementNs2Report">MovementNs2Report</option>
                <option value="NodeDensityReport">NodeDensityReport</option>
                <option value="PingAppReporter">PingAppReporter</option>
                <option value="RadiusOfGyrationReport">RadiusOfGyrationReport</option>
                <option value="SamplingReport">SamplingReport</option>
                <option value="SnapshotReport">SnapshotReport</option>
                <option value="TotalContactTimeReport">TotalContactTimeReport</option>
                <option value="TotalEncountersReport">TotalEncountersReport</option>
                <option value="UniqueEncountersReport">UniqueEncountersReport</option>

            </select>
            <br><br>
            <label for="reportWarmup"><b>Report Warmup Time (Sec):</b></label>
            <input type="number" id="reportWarmup" name="reportWarmup" value="0">

            <label for="reportDir"><b>Report Directory:</b></label>
            <input type="text" id="reportDir" name="reportDir" placeholder="Select directory" value="reports/" readonly>
            <button type="button" id="browseDirButton">Browse</button>
            <br><br>
            <button type="button" id="addReportButton">Add Report</button>
        </form>
        <br><br>

        <!-- Table for Displaying Reports -->
        <table border="1px" id="reportList">
            <thead>
                <tr>
                    <th>Report No</th>
                    <th>Class</th>
                    <th>Remove</th>
                </tr>
            </thead>
            <tbody>
                <!-- Default Reports will be displayed here by JavaScript -->
            </tbody>
        </table>
    </div>


    <!-- Router & Optimization Settings -->
    <div id="RouterOptimizationSettings" class="tabcontent">
        <h3>Router & Optimization Settings</h3>
        <form id="RouterOptimizationForm">
            <!-- Prophet Router Settings -->
            <fieldset>
                <legend>ProphetRouter Settings</legend>
                <label for="prophetRouterTimeUnit">Seconds in Time Unit:</label>
                <input type="number" id="prophetRouterTimeUnit" name="prophetRouterTimeUnit" value="30">
            </fieldset>

            <!-- Spray and Wait Router Settings -->
            <fieldset>
                <legend>SprayAndWaitRouter Settings</legend>
                <label for="sprayAndWaitCopies">Number of Copies:</label>
                <input type="number" id="sprayAndWaitCopies" name="sprayAndWaitCopies" value="6">
                <br>

                <label for="sprayAndWaitBinaryMode">Binary Mode:</label>
                <input type="checkbox" id="sprayAndWaitBinaryMode" name="sprayAndWaitBinaryMode" checked>
            </fieldset>

            <!-- Optimization Settings -->
            <fieldset>
                <legend>Optimization Settings</legend>
                <label for="optimizationCellSizeMult">Cell Size Multiplier:</label>
                <input type="number" id="optimizationCellSizeMult" name="optimizationCellSizeMult" value="5">
                <br>

                <label for="optimizationRandomizeUpdateOrder">Randomize Update Order:</label>
                <input type="checkbox" id="optimizationRandomizeUpdateOrder" name="optimizationRandomizeUpdateOrder"
                    checked>
            </fieldset>
    </div>
    <br>
    <!-- GUI Settings -->
    <div id="GUISettings" class="tabcontent">
        <h3>GUI Settings</h3>
        <form id="guiForm">
            <label for="underlayImageFileName">Image File :</label>
            <b>Default: data/helsinki_underlay.png</b><br>
            <b>(To change the image, place it in the data folder and choose file)</b>
            <input type="file" id="underlayImageFileName" name="underlayImageFileName" accept="image/*">
            <br><br>
            <label for="underlayImageOffset">Underlay Image Offset: </label>
            <input type="text" id="underlayImageOffset" name="underlayImageOffset" value="64,20"
                placeholder="Image offset in pixels (x, y) (Default: 64, 20)">
            <br><br>
            <label for="underlayImageScale">Underlay Image Scale: </label>
            <input type="number" id="underlayImageScale" name="underlayImageScale" value="4.75"
                placeholder="Scaling factor for the image (Default: 4.75)">
            <br><br>
            <label for="underlayImageRotate">Underlay Image Rotate: </label>
            <input type="number" id="underlayImageRotate" name="underlayImageRotate" value="-0.015"
                placeholder="Image rotation (radians) ( Default: -0.015)">
            <br><br>
            <label for="eventLogPanelNrofEvents">Number of Events: </label>
            <input type="number" id="eventLogPanelNrofEvents" name="eventLogPanelNrofEvents" value="100"
                placeholder="how many events to show in the log panel (default = 100)">
            <br><br>
        </form>
    </div>
    <br><br><br><br>

    <div class="button-container">
        <button class="custom" onclick="saveAllSettings()">Save Custom Settings</button>
        <button class="default" onclick="saveDefaultSettings()">Default Settings</button>
    </div>

    <script>
        // Default values for interface settings
        const interfaceSettings = [
            { name: "btInterface", type: "SimpleBroadcastInterface", transmitSpeed: "250k", transmitRange: "10" },
            { name: "highspeedInterface", type: "SimpleBroadcastInterface", transmitSpeed: "10M", transmitRange: "1000" }
        ];
    // Get the select element
    const selectElement = document.getElementById('commonInterface');

    // Iterate over the array and create options
    interfaceSettings.forEach(interfaceSetting => {
        const option = document.createElement('option');
        option.value = interfaceSetting.name; // Set the option value
        option.textContent = interfaceSetting.name; // Set the visible text
        selectElement.appendChild(option); // Add the option to the select element
    });
        // Default values for group settings
        const groupSettings = [
            { groupID: 'p', numHosts: 50, movementModel: "ShortestPathMapBasedMovement", routeFile:"", router: "EpidemicRouter", activeTimes: "", messageTTL: "50", actions: "Edit/Delete" },
            { groupID: 'c', numHosts: 100, movementModel: "ShortestPathMapBasedMovement", routeFile:"", router: "EpidemicRouter", activeTimes: "", messageTTL: "100", actions: "Edit/Delete" },
            { groupID: 'w', numHosts: 200, movementModel: "ShortestPathMapBasedMovement", routeFile:"", router: "EpidemicRouter", activeTimes: "", messageTTL: "150", actions: "Edit/Delete" },
            { groupID: 't', numHosts: 150, movementModel: "MapRouteMovement", routeFile:"data/tram3.wkt",  router: "EpidemicRouter", activeTimes: "", messageTTL: "200", actions: "Edit/Delete" },
            { groupID: 't', numHosts: 120, movementModel: "MapRouteMovement", routeFile:"data/tram4.wkt", router: "EpidemicRouter", activeTimes: "", messageTTL: "250", actions: "Edit/Delete" },
            { groupID: 't', numHosts: 80, movementModel: "MapRouteMovement", routeFile:"data/tram10.wkt", router: "EpidemicRouter", activeTimes: "", messageTTL: "300", actions: "Edit/Delete" }
        ];
        // Array to store events
        const events = [{
            eventClass: 'MessageEventGenerator',
            interval: `${25}, ${35}`,
            size: `${500}k, ${1}M`,
            hosts: `${500000} , ${1000000}`,
            prefix: 'M'
        }];
        let table = document.getElementById('eventList').getElementsByTagName('tbody')[0];
        let newRow = table.insertRow();

        newRow.insertCell(0).textContent = `${events[0]['eventClass']}`;
        newRow.insertCell(1).textContent = `${events[0]['interval']}`;
        newRow.insertCell(2).textContent = `${events[0]['size']}`;
        newRow.insertCell(3).textContent = `${events[0]['hosts']}`;
        newRow.insertCell(4).textContent = `${events[0]['prefix']}`;
        let actionCell = newRow.insertCell(5);
        let deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = function () {
            // Find the row to delete
            let row = deleteButton.closest('tr');

            // Remove the row from the table
            row.remove();

            // Remove the event from the array
            let index = Array.from(table.rows).indexOf(row) - 1;  // Adjusting for the header row
            events.splice(index, 1);
        };
        actionCell.appendChild(deleteButton);
        document.getElementById('newEventForm').addEventListener('submit', function (event) {
            event.preventDefault();

            // Gather form values
            let eventClass = document.getElementById('eventClass').value;
            let intervalMin = document.getElementById('eventIntervalMin').value;
            let intervalMax = document.getElementById('eventIntervalMax').value;
            let sizeMin = document.getElementById('eventSizeMin').value;
            let sizeMax = document.getElementById('eventSizeMax').value;
            let hostsMin = document.getElementById('eventHostsMin').value;
            let hostsMax = document.getElementById('eventHostsMax').value;
            let prefix = document.getElementById('eventPrefix').value;

            // Create event object to store
            let newEvent = {
                eventClass: eventClass,
                interval: `${intervalMin}, ${intervalMax}`,
                size: `${sizeMin},${sizeMax}`,
                hosts: `${hostsMin}, ${hostsMax}`,
                prefix: prefix
            };

            // Add the event to the events array
            events.push(newEvent);

            // Create new row in the event table
            let table = document.getElementById('eventList').getElementsByTagName('tbody')[0];
            let newRow = table.insertRow();

            newRow.insertCell(0).textContent = eventClass;
            newRow.insertCell(1).textContent = `${intervalMin} to ${intervalMax}`;
            newRow.insertCell(2).textContent = `${sizeMin} to ${sizeMax} kB`;
            newRow.insertCell(3).textContent = `${hostsMin} to ${hostsMax}`;
            newRow.insertCell(4).textContent = prefix;

            // Add Action Buttons (like Delete) without using eventNo
            let actionCell = newRow.insertCell(5);
            let deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.onclick = function () {
                // Find the row to delete
                let row = deleteButton.closest('tr');

                // Remove the row from the table
                row.remove();

                // Remove the event from the array
                let index = Array.from(table.rows).indexOf(row) - 1;  // Adjusting for the header row
                events.splice(index, 1);
            };
            actionCell.appendChild(deleteButton);


        });


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
                cell1.innerText = group.groupID;

                const cell2 = row.insertCell(1);
                cell2.innerText = group.numHosts;

                const cell3 = row.insertCell(2);
                cell3.innerText = group.movementModel;

                const cell4 = row.insertCell(3);
                cell4.innerText = group.routeFile;

                const cell5 = row.insertCell(4);
                cell5.innerText = group.router;

                const cell6 = row.insertCell(5);
                cell6.innerText = group.activeTimes;

                const cell7 = row.insertCell(6);
                cell7.innerText = group.messageTTL;

                const cell8 = row.insertCell(7);
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
            const groupID = document.getElementById("groupID").value;
            const numHosts = parseInt(document.getElementById("numberOfHosts").value, 10);
            const movementModel = document.getElementById('Movement')?.value;
            const waitTimeMin = parseFloat(document.getElementById("waitTimeMin").value) || 0;
            const waitTimeMax = parseFloat(document.getElementById("waitTimeMax").value) || 0;
            const speedMin = parseFloat(document.getElementById("speedMin").value) || 0;
            const speedMax = parseFloat(document.getElementById("speedMax").value) || 0;
            const movementRouteType = document.getElementById("movementRouteType").value;
            const bufferSize = parseInt(document.getElementById("bufferSize").value, 10) || 0;
            const router = document.getElementById("router").value;
            const msgTtl = document.getElementById("msgTtl").value || "infinite";

            const activeTimeStart1 = document.getElementById("activeTimeStart1").value;
            
            // Construct the new group object
            const newGroup = {
                groupID: groupID,
                numHosts: numHosts,
                movementModel: movementModel || "ShortestPathMapBasedMovement",
                routeFile : movementRouteType,
                router: router,
                activeTimes: `${activeTimeStart1}`,
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
            const newNumHosts = prompt(`Edit Number of Hosts for Group ${group.groupID}`, group.numHosts);
            const newMovementModel = prompt(`Edit Movement Model for Group ${group.groupID}`, group.movementModel);
            const newRouter = prompt(`Edit Router for Group ${group.groupID}`, group.router);
            const newActiveTimes = prompt(`Edit Active Times for Group ${group.groupID}`, group.activeTimes);
            const newMessageTTL = prompt(`Edit Message TTL for Group ${group.groupID}`, group.messageTTL);

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


        // Movement function
        let fileList = ['shops.wkt', 'pedestrian_paths.wkt', 'main_roads.wkt', 'roads.wkt'];

        // Initially display predefined files
        const fileListContainer = document.getElementById('fileList');
        fileList.forEach(file => {
            const listItem = document.createElement('li');
            listItem.textContent = file; // Display the predefined file names
            fileListContainer.appendChild(listItem);
        });

        // Event listener for file selection
        document.getElementById('mapFiles').addEventListener('change', function (event) {
            const files = event.target.files; // Get the FileList object
            fileListContainer.innerHTML = '';  // Clear previous file list

            // Loop through selected files and display them
            for (let i = 0; i < files.length; i++) {
                const listItem = document.createElement('li');
                listItem.textContent = files[i].name; // Display the selected file names
                fileListContainer.appendChild(listItem);
            }
        });


        // Report making fuctions
        const reportList = document.getElementById('reportList').getElementsByTagName('tbody')[0];
        const reportClassInput = document.getElementById('reportClass');
        const reportDirInput = document.getElementById('reportDir').value;
        const reportWarmup = document.getElementById('reportWarmup').value;
        const browseDirButton = document.getElementById('browseDirButton');
        const addReportButton = document.getElementById('addReportButton');
        const reports = []; // Array to store reports

        // Function to render reports in the table
        const renderReports = () => {
            reportList.innerHTML = ''; // Clear the table body
            let count = 1;
            reports.forEach((report, index) => {
                const row = reportList.insertRow();
                row.innerHTML = `
                <td>${count}</td>
                <td>${report.class}</td>
                <td><button onclick="removeReport(${index})">Remove</button></td>
            `;
                count++;
            });
        };

        // Function to add a new report
        const addReport = () => {
            const reportClass = reportClassInput.value.trim();
            const reportDirectory = reportDirInput.value.trim();

            if (!reportClass) {
                alert('Please select a valid report class.');
                return;
            }

            if (!reportDirectory) {
                alert('Please select a valid directory.');
                return;
            }

            if (reports.some(report => report.class === reportClass)) {
                alert('This report class is already added.');
            } else {
                reports.push({ class: reportClass, directory: reportDirectory }); // Add to the reports array
                renderReports(); // Re-render the table
            }
        };

        // Function to remove a report
        const removeReport = (index) => {
            reports.splice(index, 1); // Remove the selected report
            renderReports(); // Re-render the table
        };

        // Event listener for the "Browse" button
        browseDirButton.addEventListener('click', () => {
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.webkitdirectory = true; // Allow directory selection
            fileInput.addEventListener('change', (event) => {
                const directory = event.target.files[0]?.webkitRelativePath?.split('/')[0];
                if (directory) {
                    reportDirInput.value = directory;
                }
            });
            fileInput.click();
        });

        // Event listener for the "Add Report" button
        addReportButton.addEventListener('click', addReport);

        // Example: Preload default reports
        reports.push({ class: 'ContactTimesReport', directory: 'reports/' });
        reports.push({ class: 'MessageStatsReport', directory: 'reports/' });
        renderReports();




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
            console.log("Download Settings triggered");
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
            const commonRouteFile = document.getElementById("commonRouteFile");
            const CommoNwaitTime = document.getElementById("commonWaitTime").value;
            const commonInterface = document.getElementById("commonInterface").value;
            const commonnrofInterfaces = document.getElementById("commonnrofInterfaces").value;
            const CommoNspeed = document.getElementById("commonSpeed").value;
            const CommoNmsgTtl = document.getElementById("commonTtl").value;
            const CommoNnumHosts = document.getElementById("commonNumberOfHost").value;

            content += `
Scenario.nrofHostGroups = ${document.getElementById("groupList").getElementsByTagName("tbody")[0].rows.length}
        `;
            // Collecting Common group Data
            content += `
## Common settings for all groups:
Group.movementModel = ${CommoNmovementModel}
Group.router = ${CommoNrouter}
Group.bufferSize = ${CommoNbufferSize}
Group.routeFile = ${commonRouteFile}
Group.waitTime =${CommoNwaitTime}
# All nodes have the bluetooth interface
Group.nrofInterfaces = ${commonnrofInterfaces}
Group.interface1 = ${commonInterface}
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
                const groupID = row.cells[0].innerText;
                const numHosts = row.cells[1].innerText;
                const movementModel = row.cells[2].innerText;
                const router = row.cells[3].innerText;
                const activeTimes = row.cells[4].innerText;
                const messageTTL = row.cells[5].innerText;

                content += `
Group${serial}.groupID = ${groupID}
Group${serial}.numHosts = ${numHosts}
Group${serial}.movementModel = ${movementModel}
movementRouteType
Group${serial}.router = ${router}
Group${serial}.activeTimes = ${activeTimes}
Group${serial}.messageTTL = ${messageTTL}
        `;
                serial++;
            }

            content += `
## Event settings
Events.nrof = ${events.length}`
            let count = 1;
            for (let row of events) {

                content += `
Events${count}.class = ${row['eventClass']}
Events${count}.interval =${row['interval']}
Events${count}.size =${row['size']}
Events${count}.hosts = ${row['hosts']}
Events${count}.prefix = ${row['prefix']}
    `;
                count++;
            }

            // Event

            content += `
## Movement model settings
# seed for movement models' pseudo random number generator (default = 0)
MovementModel.rngSeed = ${document.getElementById("rngSeed").value}
# World's size for Movement Models without implicit size (width, height; meters)
MovementModel.worldSize = ${document.getElementById("worldSize").value}
# How long time to move hosts in the world before real simulation
MovementModel.warmup = ${document.getElementById("warmup").value}
## Map based movement -movement model specific settings
MapBasedMovement.nrofMapFiles = ${fileList.length}
`
            // Loop through selected files and display them
            count = 1;
            for (const file of fileList) {
                content += `
MapBasedMovement.mapFile${count} = data/${file}`;
                count++;
            }

            content += `
## Report settings
Report.nrofReports = ${reports.length}
Report.warmup = ${reportWarmup}
Report.reportDir = ${reportDirInput}`;
            count = 1;
            for (let row of reports) {
                content += `
Report.report${count} = ${row['class']}`;
                count++;
            }
            //Router&Optimization Tab
            // Retrieve values from the form
            const prophetRouterTimeUnit = document.getElementById('prophetRouterTimeUnit').value;
            const sprayAndWaitCopies = document.getElementById('sprayAndWaitCopies').value;
            const sprayAndWaitBinaryMode = document.getElementById('sprayAndWaitBinaryMode').checked;
            const optimizationCellSizeMult = document.getElementById('optimizationCellSizeMult').value;
            const optimizationRandomizeUpdateOrder = document.getElementById('optimizationRandomizeUpdateOrder').checked;

            content += `
## Default settings for some routers settings
ProphetRouter.secondsInTimeUnit = ${prophetRouterTimeUnit}
SprayAndWaitRouter.nrofCopies = ${sprayAndWaitCopies}
SprayAndWaitRouter.binaryMode = ${sprayAndWaitBinaryMode}

## Optimization settings -- these affect the speed of the simulation
## see World class for details.
Optimization.cellSizeMult = ${optimizationCellSizeMult}
Optimization.randomizeUpdateOrder = ${optimizationRandomizeUpdateOrder}
        `;

            // GUI Tab

            const underlayImageOffset = document.getElementById('underlayImageOffset').value;
            const underlayImageScale = document.getElementById('underlayImageScale').value;
            const underlayImageRotate = document.getElementById('underlayImageRotate').value;
            const eventLogPanelNrofEvents = document.getElementById('eventLogPanelNrofEvents').value;
            const fileInput = document.getElementById('underlayImageFileName');
            const file = 'helsinki_underlay.png';
            if (fileInput.value) {

                file = fileInput.files[0].name;

            }

            content += `
## GUI settings

# GUI underlay image settings
GUI.UnderlayImage.fileName = ${'data/' + file}
# Image offset in pixels (x, y)
GUI.UnderlayImage.offset = ${underlayImageOffset}
# Scaling factor for the image
GUI.UnderlayImage.scale = ${underlayImageScale}
# Image rotation (radians)
GUI.UnderlayImage.rotate = ${underlayImageRotate}

# how many events to show in the log panel (default = 30)
GUI.EventLogPanel.nrofEvents = ${eventLogPanelNrofEvents}
# Regular Expression log filter (see Pattern-class from the Java API for RE-matching details)
#GUI.EventLogPanel.REfilter = .*p[1-9]<->p[1-9]$
    `;



            // Create a Blob with the content
            const blob = new Blob([content], { type: "text/plain;charset=utf-8" });

            // Create a temporary download link
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "default_settings.txt";  // Specify filename

            // Programmatically click the link to start the download
            link.click();
        }

        function saveDefaultSettings() {
            console.log("Download Settings triggered");
            let content = '';

            // Collect all tabs' data
            // Scenario Tab
            content += `
#
# Default settings for the simulation
#

## Scenario settings
Scenario.name = default_scenario
Scenario.simulateConnections = true
Scenario.updateInterval = 0.1
# 43200s == 12h
Scenario.endTime = 10000000
Scenario.endTime = 43200

## Interface-specific settings:
# type : which interface class the interface belongs to
# For different types, the sub-parameters are interface-specific
# For SimpleBroadcastInterface, the parameters are:
# transmitSpeed : transmit speed of the interface (bytes per second) 
# transmitRange : range of the interface (meters)

# "Bluetooth" interface for all nodes
btInterface.type = SimpleBroadcastInterface
# Transmit speed of 2 Mbps = 250kBps
btInterface.transmitSpeed = 250k
btInterface.transmitRange = 10

# High speed, long range, interface for group 4
highspeedInterface.type = SimpleBroadcastInterface
highspeedInterface.transmitSpeed = 10M
highspeedInterface.transmitRange = 10

# Define 6 different node groups
Scenario.nrofHostGroups = 6

## Group-specific settings:
# groupID : Group's identifier. Used as the prefix of host names
# nrofHosts: number of hosts in the group
# movementModel: movement model of the hosts (valid class name from movement package)
# waitTime: minimum and maximum wait times (seconds) after reaching destination
# speed: minimum and maximum speeds (m/s) when moving on a path
# bufferSize: size of the message buffer (bytes)
# router: router used to route messages (valid class name from routing package)
# activeTimes: Time intervals when the nodes in the group are active (start1, end1, start2, end2, ...)
# msgTtl : TTL (minutes) of the messages created by this host group, default=infinite

## Group and movement model specific settings
# pois: Points Of Interest indexes and probabilities (poiIndex1, poiProb1, poiIndex2, poiProb2, ... )
#       for ShortestPathMapBasedMovement
# okMaps : which map nodes are OK for the group (map file indexes), default=all 
#          for all MapBasedMovent models
# routeFile: route's file path - for MapRouteMovement
# routeType: route's type - for MapRouteMovement


# Common settings for all groups
Group.movementModel = ShortestPathMapBasedMovement
Group.router = EpidemicRouter
Group.bufferSize = 5M
Group.waitTime = 0, 120
# All nodes have the bluetooth interface
Group.nrofInterfaces = 1
Group.interface1 = btInterface
# Walking speeds
Group.speed = 0.5, 1.5
# Message TTL of 300 minutes (5 hours)
Group.msgTtl = 300

Group.nrofHosts = 40

# group1 (pedestrians) specific settings
Group1.groupID = p

# group2 specific settings
Group2.groupID = c
# cars can drive only on roads
Group2.okMaps = 1
# 10-50 km/h
Group2.speed = 2.7, 13.9

# another group of pedestrians
Group3.groupID = w

# The Tram groups
Group4.groupID = t
Group4.bufferSize = 50M
Group4.movementModel = MapRouteMovement
Group4.routeFile = data/tram3.wkt
Group4.routeType = 1
Group4.waitTime = 10, 30
Group4.speed = 7, 10
Group4.nrofHosts = 2
Group4.nrofInterfaces = 2
Group4.interface1 = btInterface
Group4.interface2 = highspeedInterface

Group5.groupID = t
Group5.bufferSize = 50M
Group5.movementModel = MapRouteMovement
Group5.routeFile = data/tram4.wkt
Group5.routeType = 2
Group5.waitTime = 10, 30
Group5.speed = 7, 10
Group5.nrofHosts = 2

Group6.groupID = t
Group6.bufferSize = 50M
Group6.movementModel = MapRouteMovement
Group6.routeFile = data/tram10.wkt
Group6.routeType = 2
Group6.waitTime = 10, 30
Group6.speed = 7, 10
Group6.nrofHosts = 2


## Message creation parameters 
# How many event generators
Events.nrof = 1
# Class of the first event generator
Events1.class = MessageEventGenerator
# (following settings are specific for the MessageEventGenerator class)
# Creation interval in seconds (one new message every 25 to 35 seconds)
Events1.interval = 25,35
# Message sizes (500kB - 1MB)
Events1.size = 500k,1M
# range of message source/destination addresses
Events1.hosts = 0,125
# Message ID prefix
Events1.prefix = M


## Movement model settings
# seed for movement models' pseudo random number generator (default = 0)
MovementModel.rngSeed = 1
# World's size for Movement Models without implicit size (width, height; meters)
MovementModel.worldSize = 4500, 3400
# How long time to move hosts in the world before real simulation
MovementModel.warmup = 1000

## Map based movement -movement model specific settings
MapBasedMovement.nrofMapFiles = 4

MapBasedMovement.mapFile1 = data/roads.wkt
MapBasedMovement.mapFile2 = data/main_roads.wkt
MapBasedMovement.mapFile3 = data/pedestrian_paths.wkt
MapBasedMovement.mapFile4 = data/shops.wkt

## Reports - all report names have to be valid report classes

# how many reports to load
Report.nrofReports = 2
# length of the warm up period (simulated seconds)
Report.warmup = 0
# default directory of reports (can be overridden per Report with output setting)
Report.reportDir = reports/
# Report classes to load
Report.report1 = ContactTimesReport
Report.report2 = ConnectivityONEReport

## Default settings for some routers settings
ProphetRouter.secondsInTimeUnit = 30
SprayAndWaitRouter.nrofCopies = 6
SprayAndWaitRouter.binaryMode = true

## Optimization settings -- these affect the speed of the simulation
## see World class for details.
Optimization.cellSizeMult = 5
Optimization.randomizeUpdateOrder = true


## GUI settings

# GUI underlay image settings
GUI.UnderlayImage.fileName = data/helsinki_underlay.png
# Image offset in pixels (x, y)
GUI.UnderlayImage.offset = 64, 20
# Scaling factor for the image
GUI.UnderlayImage.scale = 4.75
# Image rotation (radians)
GUI.UnderlayImage.rotate = -0.015

# how many events to show in the log panel (default = 30)
GUI.EventLogPanel.nrofEvents = 100
# Regular Expression log filter (see Pattern-class from the Java API for RE-matching details)
#GUI.EventLogPanel.REfilter = .*p[1-9]<->p[1-9]$

    `;



            // Create a Blob with the content
            const blob = new Blob([content], { type: "text/plain;charset=utf-8" });

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

        # Load the HTML content directly
        self.browser.setHtml(html_code)

        # Handle download requests
        self.setup_download_handling()

        # Set the central widget to the browser
        self.setCentralWidget(self.browser)
        # Open the window in full screen
        self.showMaximized()
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
    def setup_download_handling(self):
        # Access the profile from the page of the browser
        profile = self.browser.page().profile()

        # Connect the download signal to the handler
        profile.downloadRequested.connect(self.handle_download)

    def handle_download(self, download_item):
        # Specify the download location (same folder as Python script)
        download_path = download_item.suggestedFileName()
        
        # Set the download path and accept the download
        download_item.setPath(download_path)
        download_item.accept()
        
# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Browser()
    main_window.show()
    sys.exit(app.exec_())
