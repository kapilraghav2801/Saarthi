const commandInput =
    document.getElementById(
        "commandInput"
    );

const sendButton =
    document.getElementById(
        "sendButton"
    );

const micButton =
    document.getElementById("micButton");


const status =
    document.getElementById("status");


const transcript =
    document.getElementById("transcript");

function sendTypedCommand() {

    const text =
        commandInput.value.trim();


    if (!text) {

        return;
    }


    console.log(
        "Typed command:",
        text
    );


    listening = true;


    status.textContent =
        "Understanding...";


    transcript.textContent =
        `"${text}"`;


    chrome.runtime.sendMessage(

        {
            type: "ANALYZE_TEXT",

            text: text
        },

        (response) => {

            if (
                chrome.runtime.lastError
            ) {

                console.error(

                    "Typed command error:",

                    chrome.runtime.lastError.message

                );


                listening = false;


                status.textContent =
                    "Error";


                transcript.textContent =
                    "Could not send command.";

                return;
            }


            console.log(
                "Typed command response:",
                response
            );
        }
    );


    commandInput.value = "";
}

sendButton.addEventListener(
    "click",
    sendTypedCommand
);

commandInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter"
        ) {

            sendTypedCommand();
        }
    }
);


let listening = false;


// --------------------------------------------------
// MIC BUTTON
// --------------------------------------------------

micButton.addEventListener(
    "click",
    () => {

        if (listening) {
            return;
        }


        listening = true;

        micButton.classList.add(
            "listening"
        );


        status.textContent =
            "Listening...";


        transcript.textContent =
            "I'm listening";


        chrome.runtime.sendMessage({

            type: "START_LISTENING"

        });
    }
);


// --------------------------------------------------
// RECEIVE UPDATES FROM BACKGROUND
// --------------------------------------------------

chrome.runtime.onMessage.addListener(
    (message) => {


        // ------------------------------------------
        // TRANSCRIPT
        // ------------------------------------------

        if (
            message.type ===
            "VOICE_TRANSCRIPT"
        ) {

            transcript.textContent =
                message.text;

            status.textContent =
                "Understanding...";

            return;
        }


        // ------------------------------------------
        // BACKEND RESPONSE
        // ------------------------------------------

        if (
            message.type ===
            "ANALYSIS_RESULT"
        ) {

            listening = false;

            micButton.classList.remove(
                "listening"
            );


            status.textContent =
                "Done";


            if (
                message.text
            ) {

                transcript.textContent =
                    message.text;
            }

            return;
        }


        // ------------------------------------------
        // VOICE ERROR
        // ------------------------------------------

        if (
            message.type ===
            "VOICE_ERROR"
        ) {

            listening = false;

            micButton.classList.remove(
                "listening"
            );


            status.textContent =
                "Voice error";


            transcript.textContent =
                message.error;

            return;
        }


        // ------------------------------------------
        // LISTENING ENDED
        // ------------------------------------------

        if (
            message.type ===
            "VOICE_ENDED"
        ) {

            status.textContent =
                "Processing...";

            return;
        }
    }
);