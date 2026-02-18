let questionNumber = 1;
let history = "";
const interviewId = window.location.pathname.split("/").pop();

async function sendAnswer(answer) {

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

    if (data.completed) {
        document.getElementById("chat-box").innerHTML += 
            "<div class='ai-msg'>" + data.response + "</div>";
        alert("Interview Completed!");
        return;
    }

    document.getElementById("chat-box").innerHTML += 
        "<div class='ai-msg'>" + data.response + "</div>";

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
