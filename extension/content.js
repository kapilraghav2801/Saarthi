console.log(
    "Saarthi content script loaded"
);


// ============================================================
// YOUTUBE PLAYBACK
// ============================================================

let youtubePlayTimer = null;


function playFirstYouTubeResult(
    query
) {

    console.log(
        "Saarthi: PLAY_YOUTUBE received."
    );

    console.log(
        "Saarthi: Requested query:",
        query
    );


    if (
        window.location.hostname !==
        "www.youtube.com"
    ) {

        console.log(
            "Saarthi: Current page is not YouTube."
        );

        return;
    }


    // --------------------------------------------------------
    // Stop any previous search timer
    // --------------------------------------------------------

    if (youtubePlayTimer) {

        clearInterval(
            youtubePlayTimer
        );

        youtubePlayTimer =
            null;
    }


    let attempts =
        0;


    const maxAttempts =
        20;


    const retryInterval =
        500;


    console.log(
        "Saarthi: Waiting for YouTube search results..."
    );


    youtubePlayTimer =
        setInterval(
            () => {

                attempts += 1;


                const links =
                    document.querySelectorAll(
                        "a#video-title"
                    );


                console.log(
                    `Saarthi: YouTube result check ${attempts}/${maxAttempts}. Found: ${links.length}`
                );


                // ------------------------------------------------
                // RESULTS FOUND
                // ------------------------------------------------

                if (
                    links.length > 0
                ) {

                    clearInterval(
                        youtubePlayTimer
                    );


                    youtubePlayTimer =
                        null;


                    const firstResult =
                        links[0];


                    console.log(
                        "Saarthi: First YouTube result found."
                    );


                    console.log(
                        "Saarthi: Video title:",
                        firstResult.textContent.trim()
                    );


                    console.log(
                        "Saarthi: Video URL:",
                        firstResult.href
                    );


                    console.log(
                        "Saarthi: Clicking first YouTube result..."
                    );


                    firstResult.click();


                    return;
                }


                // ------------------------------------------------
                // TIMEOUT
                // ------------------------------------------------

                if (
                    attempts >=
                    maxAttempts
                ) {

                    clearInterval(
                        youtubePlayTimer
                    );


                    youtubePlayTimer =
                        null;


                    console.error(
                        "Saarthi: Could not find YouTube results."
                    );


                    chrome.runtime.sendMessage({

                        type:
                            "PLAYBACK_ERROR",

                        error:
                            "Could not find a YouTube search result."
                    });
                }

            },
            retryInterval
        );
}


// ============================================================
// YOUTUBE RESULT INSPECTION
// ============================================================

function inspectYouTubeResults() {

    const links =
        document.querySelectorAll(
            "a#video-title"
        );


    console.log(
        "SAARTHI: YouTube video links found:",
        links.length
    );


    links.forEach(
        (link, index) => {

            console.log(
                `VIDEO ${index + 1}:`,
                link.textContent.trim(),
                link.href
            );
        }
    );
}


// ============================================================
// DEBUG YOUTUBE RESULTS
// ============================================================
//
// IMPORTANT:
//
// This only INSPECTS results.
//
// It does NOT click anything.
//
// Actual clicking happens only when
// background.js explicitly sends PLAY_YOUTUBE.
// ============================================================

if (
    window.location.hostname ===
    "www.youtube.com"
) {

    setTimeout(
        inspectYouTubeResults,
        3000
    );
}


// ============================================================
// SPEECH RECOGNITION
// ============================================================

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if (!SpeechRecognition) {

    console.error(
        "Saarthi: Speech Recognition is not supported on this page."
    );

} else {

    const recognition =
        new SpeechRecognition();


    recognition.lang =
        "en-IN";


    recognition.interimResults =
        false;


    recognition.continuous =
        false;


    let isListening =
        false;


    let wasDragged =
        false;


    // ========================================================
    // CREATE DOG
    // ========================================================

    let dog =
        document.getElementById(
            "saarthi-dog"
        );


    if (!dog) {

        dog =
            document.createElement(
                "div"
            );


        dog.id =
            "saarthi-dog";


        dog.textContent =
            "🐶";


        document.body.appendChild(
            dog
        );
    }


    // ========================================================
    // LOAD SAVED DOG POSITION
    // ========================================================

    chrome.storage.local.get(
        ["dogPosition"],
        (result) => {

            if (!result.dogPosition) {

                return;
            }


            const savedLeft =
                result.dogPosition.left;


            const savedTop =
                result.dogPosition.top;


            const maxLeft =
                window.innerWidth -
                dog.offsetWidth;


            const maxTop =
                window.innerHeight -
                dog.offsetHeight;


            const safeLeft =
                Math.max(
                    0,
                    Math.min(
                        savedLeft,
                        maxLeft
                    )
                );


            const safeTop =
                Math.max(
                    0,
                    Math.min(
                        savedTop,
                        maxTop
                    )
                );


            dog.style.left =
                safeLeft + "px";


            dog.style.top =
                safeTop + "px";


            dog.style.right =
                "auto";


            dog.style.bottom =
                "auto";
        }
    );


    // ========================================================
    // START LISTENING
    // ========================================================

    function startListening() {

        if (isListening) {

            console.log(
                "Saarthi is already listening."
            );

            return;
        }


        console.log(
            "Saarthi: Starting speech recognition..."
        );


        dog.textContent =
            "🎙️";


        isListening =
            true;


        try {

            recognition.start();

        } catch (error) {

            console.error(
                "Saarthi recognition start error:",
                error
            );


            isListening =
                false;


            dog.textContent =
                "🐶";


            chrome.runtime.sendMessage({

                type:
                    "VOICE_ERROR",

                error:
                    error.message
            });
        }
    }


    // ========================================================
    // SPEECH RESULT
    // ========================================================

    recognition.onresult =
        (event) => {

            console.log(
                "FULL SPEECH EVENT:",
                event
            );


            const transcript =
                event.results[0][0]
                    .transcript
                    .trim();


            console.log(
                "SAARTHI HEARD:",
                JSON.stringify(
                    transcript
                )
            );


            dog.textContent =
                "💬";


            if (!transcript) {

                console.log(
                    "Saarthi: Empty transcript ignored."
                );


                return;
            }


            chrome.runtime.sendMessage({

                type:
                    "VOICE_RESULT",

                text:
                    transcript
            });
        };


    // ========================================================
    // SPEECH ERROR
    // ========================================================

    recognition.onerror =
        (event) => {

            console.error(
                "Saarthi speech recognition error:",
                event.error
            );


            isListening =
                false;


            dog.textContent =
                "⚠️";


            chrome.runtime.sendMessage({

                type:
                    "VOICE_ERROR",

                error:
                    event.error
            });
        };


    // ========================================================
    // SPEECH ENDED
    // ========================================================

    recognition.onend =
        () => {

            console.log(
                "Saarthi: Speech recognition ended."
            );


            isListening =
                false;


            dog.textContent =
                "🐶";


            chrome.runtime.sendMessage({

                type:
                    "VOICE_ENDED"
            });
        };


    // ========================================================
    // DOG CLICK
    // ========================================================

    dog.addEventListener(
        "click",
        () => {

            if (wasDragged) {

                wasDragged =
                    false;


                return;
            }


            startListening();
        }
    );


    // ========================================================
    // MESSAGE HANDLER
    // ========================================================

    chrome.runtime.onMessage.addListener(
        (
            message,
            sender,
            sendResponse
        ) => {

            console.log(
                "Saarthi content received:",
                message
            );


            // =================================================
            // START LISTENING
            // =================================================

            if (
                message.type ===
                "START_LISTENING"
            ) {

                startListening();


                sendResponse({

                    success:
                        true
                });


                return;
            }


            // =================================================
            // PLAY YOUTUBE
            // =================================================

            if (
                message.type ===
                "PLAY_YOUTUBE"
            ) {

                playFirstYouTubeResult(
                    message.query
                );


                sendResponse({

                    success:
                        true
                });


                return;
            }
        }
    );


    // ========================================================
    // DRAGGING
    // ========================================================

    let isDragging =
        false;


    let startMouseX =
        0;


    let startMouseY =
        0;


    let startDogLeft =
        0;


    let startDogTop =
        0;


    dog.addEventListener(
        "mousedown",
        (event) => {

            isDragging =
                true;


            wasDragged =
                false;


            startMouseX =
                event.clientX;


            startMouseY =
                event.clientY;


            const rect =
                dog.getBoundingClientRect();


            startDogLeft =
                rect.left;


            startDogTop =
                rect.top;


            dog.style.cursor =
                "grabbing";


            event.preventDefault();
        }
    );


    document.addEventListener(
        "mousemove",
        (event) => {

            if (!isDragging) {

                return;
            }


            const deltaX =
                event.clientX -
                startMouseX;


            const deltaY =
                event.clientY -
                startMouseY;


            if (
                Math.abs(deltaX) > 5 ||
                Math.abs(deltaY) > 5
            ) {

                wasDragged =
                    true;
            }


            let newLeft =
                startDogLeft +
                deltaX;


            let newTop =
                startDogTop +
                deltaY;


            const maxLeft =
                window.innerWidth -
                dog.offsetWidth;


            const maxTop =
                window.innerHeight -
                dog.offsetHeight;


            newLeft =
                Math.max(
                    0,
                    Math.min(
                        newLeft,
                        maxLeft
                    )
                );


            newTop =
                Math.max(
                    0,
                    Math.min(
                        newTop,
                        maxTop
                    )
                );


            dog.style.left =
                newLeft + "px";


            dog.style.top =
                newTop + "px";


            dog.style.right =
                "auto";


            dog.style.bottom =
                "auto";
        }
    );


    document.addEventListener(
        "mouseup",
        () => {

            if (!isDragging) {

                return;
            }


            isDragging =
                false;


            dog.style.cursor =
                "grab";


            if (wasDragged) {

                const rect =
                    dog.getBoundingClientRect();


                chrome.storage.local.set({

                    dogPosition: {

                        left:
                            rect.left,

                        top:
                            rect.top
                    }
                });
            }
        }
    );
}