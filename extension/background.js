console.log(
    "Saarthi background service started"
);


// ============================================================
// SIDE PANEL
// ============================================================

chrome.sidePanel.setPanelBehavior({
    openPanelOnActionClick: true
});


// ============================================================
// SEND MESSAGE TO SIDE PANEL
// ============================================================

function sendToSidePanel(message) {

    chrome.runtime.sendMessage(
        message,
        () => {

            if (chrome.runtime.lastError) {
                return;
            }

        }
    );
}


// ============================================================
// ANALYZE TEXT
// ============================================================

async function analyzeText(
    text,
    tabId
) {

    if (!text || !text.trim()) {

        console.log(
            "Saarthi: Empty text ignored."
        );

        return;
    }


    try {

        console.log(
            "Saarthi sending to backend:",
            text
        );


        const response =
            await fetch(
                "http://127.0.0.1:8000/browser/analyze",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            text: text
                        })
                }
            );


        if (!response.ok) {

            throw new Error(
                `FastAPI returned ${response.status}`
            );
        }


        const data =
            await response.json();


        console.log(
            "Response from Saarthi backend:",
            data
        );


        // ----------------------------------------------------
        // EXECUTE BROWSER COMMAND
        // ----------------------------------------------------

        if (
            data.success &&
            data.command
        ) {

            executeBrowserCommand(
                data.command
            );
        }


        // ----------------------------------------------------
        // SIDE PANEL RESULT
        // ----------------------------------------------------

        let resultText =
            "Command processed";


        if (data.action) {

            resultText =
                `${data.action.action} → ${data.action.target}`;
        }


        sendToSidePanel({

            type:
                "ANALYSIS_RESULT",

            text:
                resultText,

            data:
                data
        });


        // ----------------------------------------------------
        // SEND RESULT BACK TO ORIGINAL TAB
        // ----------------------------------------------------

        if (tabId) {

            chrome.tabs.sendMessage(
                tabId,
                {
                    type:
                        "ANALYSIS_RESULT",

                    data:
                        data
                },
                () => {

                    if (
                        chrome.runtime.lastError
                    ) {

                        console.log(
                            "Saarthi: Could not send analysis result to tab."
                        );

                        return;
                    }

                }
            );
        }


    } catch (error) {

        console.error(
            "Saarthi backend error:",
            error
        );


        sendToSidePanel({

            type:
                "VOICE_ERROR",

            error:
                error.message
        });
    }
}


// ============================================================
// OPEN YOUTUBE SEARCH AND PLAY FIRST RESULT
// ============================================================

function openYouTubeAndPlay(
    query
) {

    if (!query) {

        console.error(
            "Saarthi: Missing YouTube query."
        );

        return;
    }


    const encodedQuery =
        encodeURIComponent(
            query
        );


    const url =
        "https://www.youtube.com/results?search_query=" +
        encodedQuery;


    console.log(
        "Saarthi: Opening YouTube search:",
        url
    );


    chrome.tabs.create(
        {
            url: url
        },
        (tab) => {

            if (
                chrome.runtime.lastError
            ) {

                console.error(
                    "Saarthi: Failed to create YouTube tab:",
                    chrome.runtime.lastError.message
                );

                return;
            }


            if (!tab || !tab.id) {

                console.error(
                    "Saarthi: YouTube tab ID missing."
                );

                return;
            }


            const tabId =
                tab.id;


            console.log(
                "Saarthi: YouTube tab created:",
                tabId
            );


            // ------------------------------------------------
            // WAIT FOR THIS SPECIFIC TAB TO FINISH LOADING
            // ------------------------------------------------

            const handleTabUpdate =
                (
                    updatedTabId,
                    changeInfo
                ) => {

                    // Ignore updates from other tabs
                    if (
                        updatedTabId !==
                        tabId
                    ) {

                        return;
                    }


                    // We only care about the
                    // fully loaded state.
                    if (
                        changeInfo.status !==
                        "complete"
                    ) {

                        return;
                    }


                    console.log(
                        "Saarthi: YouTube tab finished loading:",
                        tabId
                    );


                    // We only need this listener once.
                    chrome.tabs.onUpdated.removeListener(
                        handleTabUpdate
                    );


                    // ------------------------------------------------
                    // TELL CONTENT SCRIPT TO PLAY
                    // ------------------------------------------------

                    chrome.tabs.sendMessage(
                        tabId,
                        {
                            type:
                                "PLAY_YOUTUBE",

                            query:
                                query
                        },
                        (response) => {

                            if (
                                chrome.runtime.lastError
                            ) {

                                console.error(
                                    "Saarthi: Could not send PLAY_YOUTUBE to YouTube:",
                                    chrome.runtime.lastError.message
                                );

                                return;
                            }


                            console.log(
                                "Saarthi: PLAY_YOUTUBE sent to content script:",
                                response
                            );
                        }
                    );
                };


            chrome.tabs.onUpdated.addListener(
                handleTabUpdate
            );
        }
    );
}


// ============================================================
// EXECUTE BROWSER COMMAND
// ============================================================

function executeBrowserCommand(
    command
) {

    if (!command) {
        return;
    }


    console.log(
        "Executing browser command:",
        command
    );


    // ========================================================
    // OPEN URL
    // ========================================================

    if (
        command.type ===
        "OPEN_URL"
    ) {

        if (!command.url) {
            return;
        }


        chrome.tabs.create({
            url: command.url
        });


        return;
    }


    // ========================================================
    // PLAY YOUTUBE
    // ========================================================

    if (
        command.type ===
        "PLAY_YOUTUBE"
    ) {

        if (!command.query) {

            console.error(
                "Saarthi: PLAY_YOUTUBE command has no query."
            );

            return;
        }


        openYouTubeAndPlay(
            command.query
        );


        return;
    }


    // ========================================================
    // NEW TAB
    // ========================================================

    if (
        command.type ===
        "NEW_TAB"
    ) {

        chrome.tabs.create({});

        return;
    }


    // ========================================================
    // GO BACK
    // ========================================================

    if (
        command.type ===
        "GO_BACK"
    ) {

        chrome.tabs.query(
            {
                active: true,
                currentWindow: true
            },
            (tabs) => {

                if (
                    tabs.length === 0
                ) {

                    return;
                }


                const currentTab =
                    tabs[0];


                chrome.tabs.goBack(
                    currentTab.id
                );
            }
        );


        return;
    }


    // ========================================================
    // CLOSE TAB
    // ========================================================

    if (
        command.type ===
        "CLOSE_TAB"
    ) {

        chrome.tabs.query(
            {
                active: true,
                currentWindow: true
            },
            (tabs) => {

                if (
                    tabs.length === 0
                ) {

                    return;
                }


                const currentTab =
                    tabs[0];


                chrome.tabs.remove(
                    currentTab.id
                );
            }
        );


        return;
    }
}


// ============================================================
// START LISTENING ON TAB
// ============================================================

function startListeningOnTab(
    tab
) {

    if (!tab || !tab.id) {

        sendToSidePanel({

            type:
                "VOICE_ERROR",

            error:
                "No active browser tab found."
        });

        return;
    }


    if (
        !tab.url ||
        tab.url.startsWith("chrome://") ||
        tab.url.startsWith("chrome-extension://") ||
        tab.url.startsWith("edge://") ||
        tab.url.startsWith("about:")
    ) {

        sendToSidePanel({

            type:
                "VOICE_ERROR",

            error:
                "Voice is unavailable on this Chrome page. Open a normal website."
        });

        return;
    }


    chrome.tabs.sendMessage(
        tab.id,
        {
            type:
                "START_LISTENING"
        },
        (response) => {

            if (
                chrome.runtime.lastError
            ) {

                console.error(
                    "Saarthi could not reach content script:",
                    chrome.runtime.lastError.message
                );


                sendToSidePanel({

                    type:
                        "VOICE_ERROR",

                    error:
                        "Saarthi could not connect to this webpage. Please refresh the webpage once and try again."
                });


                return;
            }


            console.log(
                "Content script response:",
                response
            );
        }
    );
}


// ============================================================
// BACKGROUND MESSAGE HANDLER
// ============================================================

chrome.runtime.onMessage.addListener(
    (
        message,
        sender,
        sendResponse
    ) => {

        console.log(
            "Background received:",
            message
        );


        // ====================================================
        // START LISTENING
        // ====================================================

        if (
            message.type ===
            "START_LISTENING"
        ) {

            chrome.tabs.query(
                {
                    active: true,
                    currentWindow: true
                },
                (tabs) => {

                    if (
                        tabs.length === 0
                    ) {

                        sendToSidePanel({

                            type:
                                "VOICE_ERROR",

                            error:
                                "No active tab found."
                        });

                        return;
                    }


                    const activeTab =
                        tabs[0];


                    console.log(
                        "Saarthi active tab:",
                        activeTab.url
                    );


                    startListeningOnTab(
                        activeTab
                    );
                }
            );


            sendResponse({
                success: true
            });


            return;
        }


        // ====================================================
        // VOICE RESULT
        // ====================================================

        if (
            message.type ===
            "VOICE_RESULT"
        ) {

            const text =
                message.text;


            console.log(
                "Saarthi voice transcript:",
                JSON.stringify(text)
            );


            if (
                !text ||
                !text.trim()
            ) {

                console.log(
                    "Saarthi: Ignoring empty transcript."
                );

                return;
            }


            sendToSidePanel({

                type:
                    "VOICE_TRANSCRIPT",

                text:
                    text
            });


            analyzeText(
                text,
                sender.tab
                    ? sender.tab.id
                    : null
            );


            return;
        }


        // ====================================================
        // VOICE ERROR
        // ====================================================

        if (
            message.type ===
            "VOICE_ERROR"
        ) {

            sendToSidePanel({

                type:
                    "VOICE_ERROR",

                error:
                    message.error
            });


            return;
        }


        // ====================================================
        // VOICE ENDED
        // ====================================================

        if (
            message.type ===
            "VOICE_ENDED"
        ) {

            sendToSidePanel({

                type:
                    "VOICE_ENDED"
            });


            return;
        }


        // ====================================================
        // TYPED COMMAND
        // ====================================================

        if (
            message.type ===
            "ANALYZE_TEXT"
        ) {

            analyzeText(
                message.text,
                sender.tab
                    ? sender.tab.id
                    : null
            );


            sendResponse({
                success: true
            });


            return;
        }
    }
);