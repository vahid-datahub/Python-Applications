/* =========================================================
   AI RESEARCH ASSISTANT
   Main Frontend Logic
   ========================================================= */


/* ---------------------------------------------------------
   Telegram Web App
   --------------------------------------------------------- */

const tg = window.Telegram?.WebApp;


/* ---------------------------------------------------------
   Initialize Telegram
   --------------------------------------------------------- */

if (tg) {

    tg.ready();

    tg.expand();

    if (tg.setHeaderColor) {
        tg.setHeaderColor("#f5f7fb");
    }

    if (tg.setBackgroundColor) {
        tg.setBackgroundColor("#f5f7fb");
    }
}


/* ---------------------------------------------------------
   DOM Elements
   --------------------------------------------------------- */

const activeDocument =
    document.getElementById("activeDocument");

const documentStatus =
    document.getElementById("documentStatus");

const statusDot =
    document.querySelector(".status-dot");

const loadingOverlay =
    document.getElementById("loadingOverlay");

const toast =
    document.getElementById("toast");

const toastMessage =
    document.getElementById("toastMessage");

const themeButton =
    document.getElementById("themeButton");


/* ---------------------------------------------------------
   Application State
   --------------------------------------------------------- */

const appState = {

    activeDocument: null,

    theme: "light",

    initialized: false

};


/* ---------------------------------------------------------
   Initialize Application
   --------------------------------------------------------- */

function initializeApp() {

    loadTheme();

    updateDocumentUI();

    registerButtonEvents();

    appState.initialized = true;

}


/* ---------------------------------------------------------
   Register Buttons
   --------------------------------------------------------- */

function registerButtonEvents() {


    /* Upload */

    document
        .getElementById("uploadButton")
        .addEventListener("click", () => {

            handleAction("upload");

        });


    /* Question */

    document
        .getElementById("questionButton")
        .addEventListener("click", () => {

            handleAction("question");

        });


    /* Summary */

    document
        .getElementById("summaryButton")
        .addEventListener("click", () => {

            handleAction("summary");

        });


    /* Key Information */

    document
        .getElementById("keyInfoButton")
        .addEventListener("click", () => {

            handleAction("key-information");

        });


    /* Documents */

    document
        .getElementById("documentsButton")
        .addEventListener("click", () => {

            handleAction("documents");

        });


    /* Home */

    document
        .getElementById("homeButton")
        .addEventListener("click", () => {

            setActiveNavigation("home");

            showToast("Home");

        });


    /* Bottom Documents */

    document
        .getElementById("navDocumentsButton")
        .addEventListener("click", () => {

            setActiveNavigation("documents");

            handleAction("documents");

        });


    /* Bottom Question */

    document
        .getElementById("navQuestionButton")
        .addEventListener("click", () => {

            setActiveNavigation("question");

            handleAction("question");

        });


    /* Theme */

    themeButton.addEventListener(
        "click",
        toggleTheme
    );

}


/* ---------------------------------------------------------
   Main Action Handler
   --------------------------------------------------------- */

function handleAction(action) {

    switch (action) {


        case "upload":

            handleUpload();

            break;


        case "question":

            handleQuestion();

            break;


        case "summary":

            handleSummary();

            break;


        case "key-information":

            handleKeyInformation();

            break;


        case "documents":

            handleDocuments();

            break;


        default:

            console.log(
                "Unknown action:",
                action
            );

    }

}


/* ---------------------------------------------------------
   Upload
   --------------------------------------------------------- */

function handleUpload() {

    showToast(
        "Upload Document"
    );


    /*
        Later:

        This action will communicate
        with the existing Telegram Bot.

        We will NOT rewrite the
        document processing system.
    */


    sendActionToBot("upload");

}


/* ---------------------------------------------------------
   Question
   --------------------------------------------------------- */

function handleQuestion() {

    if (!appState.activeDocument) {

        showToast(
            "Please select a document first"
        );

        return;

    }


    showToast(
        "Ask Research Question"
    );


    sendActionToBot("question");

}


/* ---------------------------------------------------------
   Summary
   --------------------------------------------------------- */

function handleSummary() {

    if (!appState.activeDocument) {

        showToast(
            "Please select a document first"
        );

        return;

    }


    showLoading();

    sendActionToBot("summary");

}


/* ---------------------------------------------------------
   Key Information
   --------------------------------------------------------- */

function handleKeyInformation() {

    if (!appState.activeDocument) {

        showToast(
            "Please select a document first"
        );

        return;

    }


    showLoading();

    sendActionToBot(
        "key-information"
    );

}


/* ---------------------------------------------------------
   Documents
   --------------------------------------------------------- */

function handleDocuments() {

    showToast(
        "My Documents"
    );


    sendActionToBot(
        "documents"
    );

}


/* ---------------------------------------------------------
   Send Action to Telegram Bot
   --------------------------------------------------------- */

function sendActionToBot(action) {

    console.log(
        "Action:",
        action
    );


    /*
        IMPORTANT

        This is intentionally not connected
        to the backend yet.

        Later we will connect this function
        to the existing Python Bot/API.

        Example future structure:

            Telegram Web App
                    ↓
                app.js
                    ↓
              FastAPI endpoint
                    ↓
              Existing services

        No RAG / database / Qdrant logic
        will be duplicated here.
    */


    if (
        tg &&
        tg.sendData
    ) {

        /*
            We will enable this when
            the Web App is connected
            to the Bot.

            Do NOT uncomment yet.

            tg.sendData(
                JSON.stringify({
                    action: action
                })
            );
        */

    }

}


/* ---------------------------------------------------------
   Document UI
   --------------------------------------------------------- */

function updateDocumentUI() {

    if (!appState.activeDocument) {

        activeDocument.textContent =
            "No document selected";

        documentStatus.textContent =
            "Ready for a document";

        statusDot.classList.remove(
            "active"
        );

        return;
    }


    activeDocument.textContent =
        appState.activeDocument;

    documentStatus.textContent =
        "Active document";

    statusDot.classList.add(
        "active"
    );

}


/* ---------------------------------------------------------
   Set Active Document
   --------------------------------------------------------- */

function setActiveDocument(
    documentName
) {

    appState.activeDocument =
        documentName;

    updateDocumentUI();

}


/* ---------------------------------------------------------
   Navigation
   --------------------------------------------------------- */

function setActiveNavigation(
    navigation
) {

    const navItems =
        document.querySelectorAll(
            ".nav-item"
        );


    navItems.forEach(
        item => {

            item.classList.remove(
                "active"
            );

        }
    );


    if (
        navigation === "home"
    ) {

        document
            .getElementById("homeButton")
            .classList.add("active");

    }


    if (
        navigation === "documents"
    ) {

        document
            .getElementById("navDocumentsButton")
            .classList.add("active");

    }


    if (
        navigation === "question"
    ) {

        document
            .getElementById("navQuestionButton")
            .classList.add("active");

    }

}


/* ---------------------------------------------------------
   Loading
   --------------------------------------------------------- */

function showLoading() {

    loadingOverlay.classList.remove(
        "hidden"
    );

}


function hideLoading() {

    loadingOverlay.classList.add(
        "hidden"
    );

}


/* ---------------------------------------------------------
   Toast
   --------------------------------------------------------- */

let toastTimeout = null;


function showToast(message) {

    toastMessage.textContent =
        message;

    toast.classList.add(
        "show"
    );


    clearTimeout(
        toastTimeout
    );


    toastTimeout = setTimeout(
        () => {

            toast.classList.remove(
                "show"
            );

        },
        2200
    );

}


/* ---------------------------------------------------------
   Theme
   --------------------------------------------------------- */

function toggleTheme() {

    const isDark =
        document.body.classList.toggle(
            "dark-theme"
        );


    appState.theme =
        isDark
            ? "dark"
            : "light";


    themeButton.textContent =
        isDark
            ? "🌙"
            : "☀️";


    localStorage.setItem(
        "researchAssistantTheme",
        appState.theme
    );


    updateTelegramTheme(
        appState.theme
    );

}


/* ---------------------------------------------------------
   Load Theme
   --------------------------------------------------------- */

function loadTheme() {

    const savedTheme =
        localStorage.getItem(
            "researchAssistantTheme"
        );


    if (
        savedTheme === "dark"
    ) {

        document.body.classList.add(
            "dark-theme"
        );

        appState.theme = "dark";

        themeButton.textContent =
            "🌙";

        updateTelegramTheme(
            "dark"
        );

    }

}


/* ---------------------------------------------------------
   Telegram Theme
   --------------------------------------------------------- */

function updateTelegramTheme(
    theme
) {

    if (!tg) {
        return;
    }


    if (
        theme === "dark"
    ) {

        if (tg.setHeaderColor) {

            tg.setHeaderColor(
                "#10121a"
            );

        }


        if (tg.setBackgroundColor) {

            tg.setBackgroundColor(
                "#10121a"
            );

        }

    } else {

        if (tg.setHeaderColor) {

            tg.setHeaderColor(
                "#f5f7fb"
            );

        }


        if (tg.setBackgroundColor) {

            tg.setBackgroundColor(
                "#f5f7fb"
            );

        }

    }

}


/* ---------------------------------------------------------
   Telegram Back Button
   --------------------------------------------------------- */

if (
    tg &&
    tg.BackButton
) {

    tg.BackButton.onClick(
        () => {

            showToast(
                "Back"
            );

        }
    );

}


/* ---------------------------------------------------------
   Start Application
   --------------------------------------------------------- */

document.addEventListener(
    "DOMContentLoaded",
    initializeApp
);