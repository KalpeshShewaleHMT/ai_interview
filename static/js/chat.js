let questionNumber = 1;
let history = "";
const interviewId = window.location.pathname.split("/").pop();

async function sendAnswer(answer) {
    history += "\nUser: " + answer;

    const response = await fetch("/api/interview", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            interview_id: interviewId,
            history: history,
            question_number: questionNumber
        })
    });

    const data = await response.json();
    document.getElementById("chat-box").innerHTML += 
        "<div class='ai-msg'>" + data.response + "</div>";

    history += "\nAI: " + data.response;
    questionNumber++;
}

function startListening() {
    const recognition = new webkitSpeechRecognition();
    recognition.start();

    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;
        document.getElementById("chat-box").innerHTML += 
            "<div class='user-msg'>" + text + "</div>";
        sendAnswer(text);
    }
}
