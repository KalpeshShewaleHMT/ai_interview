let questionNumber = 1;
let isProcessing = false;

// Auto first question
window.onload = function() {
    fetchQuestion("");
};

async function fetchQuestion(answer) {

    if (isProcessing) return;
    isProcessing = true;

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

    if (answer) {
        document.getElementById("chat-box").innerHTML +=
            "<div class='user-msg'>" + answer + "</div>";
    }

    document.getElementById("chat-box").innerHTML +=
        "<div class='ai-msg'>" + data.response + "</div>";

    if (data.completed) {
        alert("Interview Completed!");
        isProcessing = false;
        return;
    }

    questionNumber++;
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

// Speech to text
function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;
        fetchQuestion(text);
    };
}
