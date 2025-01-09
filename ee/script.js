
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

        