const lanIP = `${window.location.hostname}:5000`;
// const socketio = io(lanIP);

const backend_IP = "http://192.168.1.199:5000";
const backend = backend_IP + "/api/v1";
//const backend = lanIP + "/api/v1";

// #region ***  DOM references                           ***********
let htmlIpButton;
let htmlMedicationIntakeTable;

// #endregion

// #region ***  Callback-Visualisation - show___         ***********

const showError = function () {
	console.error("Error");
};


const showIp = function(jsonObject){
	try{
		console.log(jsonObject)
		htmlIpButton.innerHTML = jsonObject
	} catch(err){
		console.error(err);
	}
}

const showMedicationIntake = function(jsonObject){
	try {
		console.log(jsonObject);
		let tempIntake = "";
		for (let intake of jsonObject) {
			tempIntake += 
			`
			<li>
	<div class="c-historycontainer">
		<object data="./style/svg/pill${(() => {
			switch (intake.Status) {
				case "Taken":
					return "green";
				case "Scheduled":
					return "grey";
				default:
					return "orange";
			}
		})()}.svg" type="image/svg+xml"></object>
		<p class="u-mb-clear">${intake.Time}</p>
		<p class="u-mb-clear">${intake.FirstName + " " +intake.LastName}</p>
		<p class="u-mb-clear">${intake.Name}</p>
		<p class="u-mb-clear">${}</p>
		<p class="u-mb-clear">1min</p>
	</div>
	<hr class="u-mb-clear">
</li>
			`
		}
		htmlMedicationIntakeTable.innerHTML = tempIntake;
	} catch (err) {
		console.error(err);
	}
}
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
const getMedicationIntake = function () {
	try {
		handleData(`${backend}/getrecentdata`, showMedicationIntake, showError);
	} catch (err) {
		console.error(err);
	}
};


// #endregion

// #region ***  Event Listeners - listenTo___            ***********
const addEventListeners = function () {
	htmlIpButton.addEventListener("click", listenToIpButton)
};

const listenToIpButton = function () {
	if (htmlIpButton.innerHTML === "Show IP") {
		try{
		handleData(`${backend}/ip`, showIp, showError)
		}catch(err){
			console.error(err);
		}
		//htmlIpButton.innerHTML = "Here is the IP";
	} else {
		htmlIpButton.innerHTML = "Show IP";
	}
};

// #endregion

// #region ***  Init / DOMContentLoaded                  ***********
const init = function () {
	console.info("DOM geladen");
	// listenToUI();
	// listenToSocket();

	htmlIpButton = document.querySelector(".js-ipButton");
	if(htmlIpButton){
		addEventListeners();
	}

	htmlMedicationIntakeTable =document.querySelector(".js-medicationIntakeTable")
	if(htmlMedicationIntakeTable){
		getMedicationIntake()
	}
};

document.addEventListener("DOMContentLoaded", init);

// #endregion

// const listenToUI = function () {};

// const listenToSocket = function () {
// 	socketio.on("connect", function () {
// 		console.log("verbonden met socket webserver");
// 	});
// };
