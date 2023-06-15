const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

const backend_IP = 'http://192.168.168.169:5000';
//const backend_IP = "http://192.168.1.199:5000";
// const backendee = backend_IP + '/api/v1';
const backend = 'http://' + lanIP + '/api/v1';

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
let htmlSelectPatient;
let htmlNITypeId;
let htmlNIRelDocId;
let htmlNIDosage;
let htmlNIButton;

let htmlHistoryAmount;

let htmlKpstepmotorbtn;
let htmlKpcloselockbtn;
let htmlKpopenlockbtn;
let htmlKpcustomfield;
let htmlKpcustombtn;
let htmlKpenablesoundbtn;
let htmlKpdisablesoundbtn;

let htmlamname;
let htmlamdescription;
let htmlambtn;

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

const ShowId = function (jsonObject) {
	try {
		console.log(jsonObject);
		let tempinner = '';
		for (let info of jsonObject) {
			tempinner += `<option value=${info.Id}>${info.Id}: ${info.Name} ${info.LastName}</option>`;
		}
		htmlSelectPatient.innerHTML += tempinner;
	} catch (err) {
		console.error(err);
	}
};
const ShowDoctId = function (jsonObject) {
	try {
		console.log(jsonObject);
		let tempinner = '';
		for (let info of jsonObject) {
			tempinner += `<option value=${info.Id}>${info.Id}: ${info.Name} ${info.LastName}</option>`;
		}
		htmlNIRelDocId.innerHTML += tempinner;
	} catch (err) {
		console.error(err);
	}
};
const ShowMedId = function (jsonObject) {
	try {
		console.log(jsonObject);
		let tempinner = '';
		for (let info of jsonObject) {
			tempinner += `<option value=${info.Id}>${info.Id}: ${info.Name}</option>`;
		}
		htmlNITypeId.innerHTML += tempinner;
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
					<div class="c-historycontainer ${(()=>{if(intake.Status == 'InProgress'){return "c-historycontainer--active"}return 'c-historycontainer--inactive'})()}">
						<object data="./style/svg/pill${(() => {
							switch (intake.Status) {
								case 'Taken':
									return 'green';
								case 'Scheduled':
									return 'grey';
								default:
									return 'orange';
							}
						})()}.svg" type="image/svg+xml" height="24" width="24"></object>
						<div>
						<p class="u-mb-clear">${intake.Time}</p>
						<p class="u-mb-clear">${intake.FirstName + ' ' + intake.LastName}</p>
						<p class="u-mb-clear">${intake.Name}</p>
						<p class="u-mb-clear">${intake.Dosage}</p>
						<p class="u-mb-clear">${intake.Delay} min</p>
						</div>
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

const getUserData = function () {
	userid = htmlSelectPatient.value;
	histamount = htmlHistoryAmount.value;
	socketio.emit('F2B_get_status_dispenser_user', { UserId: userid, HistoryLimit: histamount });
	console.log(userid);
};

const getlogin = function () {
	const username = document.getElementsByName('username')[0].value;
	const password = document.getElementsByName('password')[0].value;
	if (username && password) {
		socketio.emit('F2B_login', { username, password });
	}
};

const sendCode = function (code) {
	console.log('wee');
	socketio.emit('F2B_Keypad_Code', code);
};
const sendCustomCode = function () {
	code = htmlKpcustomfield.value;
	socketio.emit('F2B_Keypad_Code', code);
	htmlKpcustomfield.value = '';
	return false;
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
const addNewMediTime = function () {
	let time = htmlNITime.value;
	let patientId = htmlSelectPatient.value;
	let typeId = htmlNITypeId.value;
	let docId = htmlNIRelDocId.value;
	let dosage = htmlNIDosage.value;

	if (time && patientId && typeId && docId && dosage) {
		console.log('data being send');
		socketio.emit('F2B_insert_medication_intake', { Time: time, Patient: patientId, TypeId: typeId, RelatedDocterId: docId, Dosage: dosage });
	} else {
		console.log("data can't be send, not enough");
	}
};

const addNewMedication = function () {
	let name = htmlamname.value;
	let description = htmlamdescription.value;
	socketio.emit('F2B_add_medication', { Name: name, Description: description });
};

const getRfid = function () {
	socketio.emit('F2B_request_rfid');
	console.log('rfidRequested');
};

const getUsersId = function () {
	try {
		handleData(`${backend}/getuserids`, ShowId, showError);
	} catch (err) {
		console.error(err);
	}
	console.log();
};
const getDoctId = function () {
	try {
		handleData(`${backend}/getdoctids`, ShowDoctId, showError);
	} catch (err) {
		console.error(err);
	}
	console.log();
};
const getMedTypeId = function () {
	try {
		handleData(`${backend}/getmedtypeids`, ShowMedId, showError);
	} catch (err) {
		console.error(err);
	}
	console.log();
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

	htmlSelectPatient = document.querySelector('.js-select-patient');
	if (htmlSelectPatient) {
		getUsersId();
	}

	htmlambtn = document.querySelector('.js-ambtn');
	if (htmlambtn) {
		htmlamname = document.querySelector('.js-amname');
		htmlamdescription = document.querySelector('.js-amdescription');
		htmlambtn.addEventListener('click', addNewMedication);
	}

	htmlKpstepmotorbtn = document.querySelector('.js-kp-stepmotorbtn');
	if (htmlKpstepmotorbtn) {
		console.log('testcode on page');
		htmlKpstepmotorbtn.addEventListener('click', function () {
			sendCode('4561');
		});
		htmlKpcloselockbtn = document.querySelector('.js-kp-closelockbtn');
		htmlKpcloselockbtn.addEventListener('click', function () {
			sendCode('4562');
		});
		htmlKpopenlockbtn = document.querySelector('.js-kp-openlockbtn');
		htmlKpopenlockbtn.addEventListener('click', function () {
			sendCode('4563');
		});
		htmlKpenablesoundbtn = document.querySelector('.js-kp-enablesoundbtn');
		htmlKpenablesoundbtn.addEventListener('click', function () {
			sendCode('4564');
		});
		htmlKpdisablesoundbtn = document.querySelector('.js-kp-disablesoundbtn');
		htmlKpdisablesoundbtn.addEventListener('click', function () {
			sendCode('4565');
		});

		htmlKpcustomfield = document.querySelector('.js-kp-customfield');
		htmlKpcustombtn = document.querySelector('.js-kp-custombtn');
		htmlKpcustombtn.addEventListener('click', sendCustomCode);
	}

	htmlHistoryAmount = document.querySelector('.js-historyAmount');
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

		htmlNITime = document.querySelector('.js-ni-time');
		if (htmlNITime) {
			let currtime = new Date();
			let actualtime = new Date(currtime.getTime() - (currtime.getTimezoneOffset()) * 60000);
			htmlNITime.value = actualtime.toISOString().slice(0, 16);
		}
		htmlNITypeId = document.querySelector('.js-ni-typeid');
		htmlNIRelDocId = document.querySelector('.js-ni-relateddocter');
		htmlNIDosage = document.querySelector('.js-ni-dosage');
		htmlNIButton = document.querySelector('.js-ni-button');
		if (htmlNIButton) {
			htmlNIButton.addEventListener('click', addNewMediTime);
		}

		if (htmlNITypeId) {
			getMedTypeId();
		}

		if (htmlNIRelDocId) {
			getDoctId();
		}
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
		console.log(htmlSelectPatient.value);
		if (htmlSelectPatient === null || htmlHistoryAmount === null) {
			return;
		}

		if (htmlSelectPatient.value == 0) {
			if (htmlMedicationIntakeTable) {
				console.log('clientInfo');
				console.log(jsonObject);
				showMedicationIntake(jsonObject);
			}
		} else {
			userid = htmlSelectPatient.value;
			histamount = htmlHistoryAmount.value;
			socketio.emit('F2B_get_status_dispenser_user', { UserId: userid, HistoryLimit: histamount });
		}
	});
	socketio.on('B2F_status_dispenser_user', function (jsonObject) {
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
