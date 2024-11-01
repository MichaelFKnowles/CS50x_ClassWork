const hashkey = uuidv4();
// ##### for quote opeartions
function fetchStocks() {
    const symbol = document.getElementsByName("symbol")[0].value;
    fetch('/quote', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                symbol: symbol
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.error) {} else {
                createTable(data);
            }
            displayError(data.error);
            displayMessage(data.message);

        })
};

// ##### UUID 4 key gen - Reference: https://stackoverflow.com/questions/105034/how-do-i-create-a-guid-uuid/2117523#2117523 user Broofa
function uuidv4() {
    return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
        (+c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> +c / 4).toString(16)
    );
}

// ##### for buy operations

function buyConfirmation(symbol, shares) {
    let result = confirm("Are you sure you want to BUY this stock?")
    if (result === true) {
        requestBuy(symbol, shares)
    } else {
        displayError('Purchase cancelled');
        displayMessage('');
    }
}

function requestBuy(symbol, shares) {

    console.log("**** UUIDv4 Key: " + hashkey)
    fetch('/buy', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                symbol: symbol,
                shares: shares,
                hashkey: hashkey
            })
        })
        .then(response => {
            console.log('************ response: ', response)
            return response.json()
        })
        .then(data => {
            console.log('*********** Data: ', data);
            if (data.error) {
                console.log('************ Failed Data: ', data)
            } else {
                if (document.getElementById("symbol")) {
                    fetchStocks()
                } else {
                    showWallet();
                }
                console.log('******** Passed Data: ', data)
            }
            displayError(data.error);
            displayMessage(data.message);
        })
};
// #### for global error handling
function displayError(error) {
    document.getElementById("error-message").innerText = error || ``;
};

function displayMessage(message) {
    document.getElementById("message").innerText = message || ``;
};

// #### for SELL operations
function sellConfirmation(symbol, shares) {
    let result = confirm("Are you sure you want to SELL this stock?")
    if (result === true) {
        requestSell(symbol, shares)
    } else {
        displayError('Sale cancelled');
        displayMessage('');
    }
}
async function requestSell(symbol, shares) {
    console.log('******** Request Sell Called')
    try {
        const response = await fetch('/sell', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                symbol: symbol,
                shares: shares,
                hashkey: hashkey
            })
        });

        const data = await response.json();
        console.log('*** Request Sell Data: ', data);

        if (data.error) {} else {
            showWallet();
        }
        displayError(data.error);
        displayMessage(data.message);
    } catch (error) {
        console.error('*** Error:', error);
    }
};

// Functions accessed by both Sell and Buy functions:

function Listener() {
    const throttleHandleCheck = throttle(handleCheck, 2500);
    console.log("*** Setting cooldown for throttle function")

    let sellElements = document.getElementsByName("sell");
    let buyElements = document.getElementsByName("buy");
    let sharesElements = document.getElementsByName("shares");
    let symbolElements = document.querySelectorAll('.symbol');

    if (sellElements) {
        sellElements.forEach(element => {
            element.removeEventListener("click", throttleHandleCheck);
            element.addEventListener("click", throttleHandleCheck);
        })
    }
    if (buyElements) {
        buyElements.forEach(element => {
            element.removeEventListener("click", throttleHandleCheck);
            element.addEventListener("click", throttleHandleCheck);
        })
    }
    sharesElements.forEach(element => {
        element.removeEventListener("keydown", throttleHandleCheck);
        element.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                throttleHandleCheck(event)
            }
        });
    })

};

function throttle(func, cooldown) {
    console.log("*** throttle function called");
    let inThrottle = false;
    return function(...args) {
        console.log("***inThrottle:", inThrottle);
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            console.log("*** throttle function REFRESHED COOLDOWN");
            setTimeout(() => {
                inThrottle = false;
                console.log("*** throttle function COOLDOWN ENDED");
            }, cooldown);
        }
    }
};

function handleCheck(event) {

    if (event.type === "keydown" && event.key === "Enter") {
        console.log("**** handleCheck Enter Pressed")
        if (event.target.classList.contains('sell-shares-quantity')) {
            console.log("**** handleCheck Enter Pressed - sell shares")
            activateEvent('sell-shares-quantity')
        }
        if (event.target.classList.contains('buy-shares-quantity')) {
            console.log("**** handleCheck Enter Pressed - buy shares")
            activateEvent('buy-shares-quantity')
        }
    }

    if (event.type === "click") {
        if (event.target.classList.contains('sell-button')) {
            activateEvent('sell-button')
        }
        if (event.target.classList.contains('buy-button')) {
            activateEvent('buy-button')
        }
    }

    function activateEvent(eventClass) {
        if (event.target.classList.contains(eventClass)) {
            let row = event.target.closest('tr');
            let symbol = row.querySelector('.symbol').childNodes[0].textContent.trim();
            let sharesSell;
            try {
                sharesSell = row.querySelector('.sell-shares-quantity').value;
            } catch (error) {
                console.log("**** activateEvent shareSell error: " + error)
            }
            let sharesBuy
            try {
                sharesBuy = row.querySelector('.buy-shares-quantity').value;
            } catch (error) {
                console.log("**** activateEvent shareBuy error: " + error)
            }
            console.log("*** REQUEST SELL FROM BUTTON symbol: " + symbol + " shares: " + sharesSell);
            if (eventClass == "sell-button" || eventClass == "sell-shares-quantity") {
                console.log("**** activateEvent: Sell button")
                console.log("**** symbol: " + symbol + " shares: " + sharesSell)
                sellConfirmation(symbol, sharesSell);
            }
            if (eventClass == "buy-button" || eventClass == "buy-shares-quantity") {
                console.log("**** activateEvent: Buy button")
                console.log("**** symbol: " + symbol + " shares: " + sharesBuy)
                buyConfirmation(symbol, sharesBuy);
            }
        }
    }
};

function showWallet() {
    console.log("in fetch")
    fetch('/wallet')
        .then(response => {
            console.log('Response: ', response);
            return response.json();
        })
        .then(data => {
            console.log('Data: ', data);
            if (data.error) {
                displayError(data.error);
            } else {
                createTable(data);
            }
        })
        .catch(error => console.error('Error:', error));
}


// #### Transaction history
function showHistory() {
    console.log("********in fetch")
    fetch('/showHistory')
        .then(response => {
            console.log('Response: ', response);
            return response.json();
        })
        .then(data => {
            console.log('Data: ', data);
            if (data.error) {} else {
                createTable(data);
            }
            displayError(data.error);
            displayMessage(data.message);
        })
        .catch(error => console.error('Error:', error));
}
