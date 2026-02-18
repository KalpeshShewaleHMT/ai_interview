let questionNumber = 1;
let isProcessing = false;

// Auto first question
window.onload = function() {
    fetchQuestion("");
};

function updateProgress() {
    const percent = ((questionNumber - 1) / TOTAL_QUESTIONS) * 100;
    document.getElementById("progress-bar").style.width = percent + "%";
    document.getElementById("progress-text").innerText =
        "Question " + questionNumber + " of " + TOTAL_QUESTIONS;
}

function scrollToBottom() {
    const chatBox = document.getElementById("chat-box");
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showLoading() {
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML +=
        "<div class='ai-msg loading' id='loading'>AI is typing...</div>";
    scrollToBottom();
}

function removeLoading() {
    const loading = document.getElementById("loading");
    if (loading) loading.remove();
}

async function fetchQuestion(answer) {

    if (isProcessing) return;
    isProcessing = true;

    if (answer) {
        document.getElementById("chat-box").innerHTML +=
            "<div class='user-msg'>" + answer + "</div>";
        scrollToBottom();
    }

    showLoading();

    const response = await fetch("/api/interview", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            interview_id: interviewId,
            question_number: questionNumber,
            answer: answer
        })
    });

    const data = await response.json();

    removeLoading();

    document.getElementById("chat-box").innerHTML +=
        "<div class='ai-msg'>" + data.response + "</div>";

    scrollToBottom();

    if (data.completed) {
        document.getElementById("progress-bar").style.width = "100%";
        document.getElementById("progress-text").innerText = "Interview Completed";
        isProcessing = false;
        return;
    }

    questionNumber++;
    updateProgress();
    isProcessing = false;
}

// Manual typing
function sendTypedAnswer() {
    const input = document.getElementById("answer-input");
    const text = input.value.trim();

    if (!text) return;

    input.value = "";
    fetchQuestion(text);
}

// Speech input
function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;
        fetchQuestion(text);
    };
}
