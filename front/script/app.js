const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

const backend_IP = 'http://192.168.168.169:5000';
//const backend_IP = "http://192.168.1.199:5000";
const backend = backend_IP + '/api/v1';
//const backend = lanIP + "/api/v1";

// #region ***  DOM references                           ***********
let htmlIpButton;
let htmlMedicationIntakeTable;

let htmlLoginForm;

let htmlAddUser;
let htmlRFIDButton;

let htmlAUName;
let htmlAULastName;
let htmlAUPhoneNumber;
let htmlAUPhoneNumberResp;
let htmlRFIDField;

let htmlNITime;
let htmlNIPatientId;
let htmlNITypeId;
let htmlNIRelDocId;
let htmlNIDosage;
let htmlNIButton;

// #endregion

// #region ***  Callback-Visualisation - show___         ***********

const showError = function () {
	console.error('Error');
}; 

const showIp = function (jsonObject) {
	try {
		console.log(jsonObject);
		htmlIpButton.innerHTML = jsonObject;
	} catch (err) {
		console.error(err);
	}
};

const showMedicationIntake = function (jsonObject) {
	try {
		console.log(jsonObject);
		let tempIntake = '';
		for (let intake of jsonObject) {
			tempIntake += `
							<li>
					<div class="c-historycontainer">
						<object data="./style/svg/pill${(() => {
							switch (intake.Status) {
								case 'Taken':
									return 'green';
								case 'Scheduled':
									return 'grey';
								default:
									return 'orange';
							}
						})()}.svg" type="image/svg+xml"></object>
						<p class="u-mb-clear">${intake.Time}</p>
						<p class="u-mb-clear">${intake.FirstName + ' ' + intake.LastName}</p>
						<p class="u-mb-clear">${intake.Name}</p>
						<p class="u-mb-clear">${intake.Dosage}</p>
						<p class="u-mb-clear">${intake.Delay} min</p>
					</div>
					<hr class="u-mb-clear">
				</li>
			`;
		}
		htmlMedicationIntakeTable.innerHTML = tempIntake;
	} catch (err) {
		console.error(err);
	}
};
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

const getlogin = function () {
	const username = document.getElementsByName('username')[0].value;
	const password = document.getElementsByName('password')[0].value;
	if (username && password) {
		socketio.emit('F2B_login', { username, password });
	}
};

const createNewUser = function () {
	let name = htmlAUName.value;
	let lastName = htmlAULastName.value;
	let phoneNumber = htmlAUPhoneNumber.value;
	let phoneNumberResp = htmlAUPhoneNumberResp.value;
	let rfidField = htmlRFIDField.value;

	if (name && lastName) {
		console.log('data being send');
		socketio.emit('F2B_add_user', { name: name, lastName: lastName, phoneNumber: phoneNumber, phoneNumberResp: phoneNumberResp, rfidField: rfidField });
	} else {
		console.log("data can't be send, not enough");
	}
};

const getRfid = function () {
	socketio.emit('F2B_request_rfid');
	console.log('rfidRequested');
};

// #endregion

// #region ***  Event Listeners - listenTo___            ***********

const listenToIpButton = function () {
	if (htmlIpButton.innerHTML === 'Show IP') {
		try {
			handleData(`${backend}/ip`, showIp, showError);
		} catch (err) {
			console.error(err);
		}
		//htmlIpButton.innerHTML = "Here is the IP";
	} else {
		htmlIpButton.innerHTML = 'Show IP';
	}
};

// #endregion

// #region ***  Init / DOMContentLoaded                  ***********
const init = function () {
	console.info('DOM geladen');
	// listenToUI();
	listenToSocket();

	htmlIpButton = document.querySelector('.js-ipButton');
	if (htmlIpButton) {
		htmlIpButton.addEventListener('click', listenToIpButton);
	}

	htmlMedicationIntakeTable = document.querySelector('.js-medicationIntakeTable');
	if (htmlMedicationIntakeTable) {
		getMedicationIntake();
	}

	htmlLoginForm = document.querySelector('.js-loginform');
	if (htmlLoginForm) {
		htmlLoginForm.addEventListener('click', getlogin);
	}

	htmlRFIDButton = document.querySelector('.js-getRfid');
	htmlRFIDField = document.querySelector('.js-rfidfield');
	if (htmlRFIDButton) {
		htmlRFIDButton.addEventListener('click', getRfid);

		htmlAUName = document.querySelector('.js-nuname');
		htmlAULastName = document.querySelector('.js-nulastname');
		htmlAUPhoneNumber = document.querySelector('.js-nuphonenumber');
		htmlAUPhoneNumberResp = document.querySelector('.js-nuphonenumberresponsible');
		htmlAddUser = document.querySelector('.js-newUserBtn');
		if (htmlAddUser) {
			htmlAddUser.addEventListener('click', createNewUser);
		}

		htmlNITime = document.querySelector('.js-');
		htmlNIPatientId = document.querySelector();
		htmlNITypeId = document.querySelector();
		htmlNIRelDocId = document.querySelector();
		htmlNIDosage = document.querySelector();
		htmlNIButton = document.querySelector();
	}
};

document.addEventListener('DOMContentLoaded', init);

// #endregion

const listenToUI = function () {};

const listenToSocket = function () {
	socketio.on('connect', function () {
		console.log('verbonden met socket webserver');
	});

	socketio.on('B2F_status_dispenser', function (jsonObject) {
		if (htmlMedicationIntakeTable) {
			console.log('clientInfo');
			console.log(jsonObject);
			showMedicationIntake(jsonObject);
		}
	});

	socketio.on('B2F_rfid_id', function (id) {
		if (htmlRFIDField) {
			console.log(id);
			htmlRFIDField.value = id;
		}
	});
};
