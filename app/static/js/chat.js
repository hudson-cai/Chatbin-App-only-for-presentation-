// Set the scroll position to the bottom when the page is loaded and whenever the content changes
$(document).ready(function () {
  $(".chat-body").animate(
    { scrollTop: $(".chat-body").prop("scrollHeight") },
    300
  );
});

$(document).ready(function () {
  $("#chat-board").animate(
    { scrollTop: $("#chat-board").prop("scrollHeight") },
    300
  );
});

function formatTime(timestamp) {
  const date = new Date(timestamp);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const seconds = String(date.getSeconds()).padStart(2, "0");

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}



// Reference for inner HTML: https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML
function appendUserMessage(message) {
  const chatBoard = document.getElementById("chat-board");
  const messageElement = document.createElement("div");
  messageElement.classList.add("message");

  const currentTime = formatTime(Date.now());

  messageElement.innerHTML = `
                              <div class="d-flex align-items-center mb-1">
                                <span class="username me-2 text-start">You:</span>
                                <span class="timestamp text-start">${currentTime}</span>
                              </div>
                              <div class="content text-start">${message}</div>
                            `;

  chatBoard.appendChild(messageElement);

  // Make an API call to save the user message to the history database
  // Refernece: https://www.w3schools.com/jsref/api_fetch.asp
  fetch("/send-message", 
        { method: "POST",
          headers: {"Content-Type": "application/json",},
          body: JSON.stringify({content: message, timestamp: formatTime(Date.now()),}), // Change 'message' to 'content'
        });
}

function appendAutoMessage(message) {
  const chatBoard = document.getElementById("chat-board");
  const messageElement = document.createElement("div");
  messageElement.classList.add("message");

  const currentTime = formatTime(Date.now());

  messageElement.innerHTML = `
                              <div class="d-flex align-items-center mb-1">
                                <span class="username Auto me-2 text-start">ChatBot🤖️:</span>
                                <span class="timestamp text-start">${currentTime}</span>
                              </div>
                              <div class="content text-start">${message}</div>
                            `;

  chatBoard.appendChild(messageElement);

  // Make an API call to save the Auto message to the history database
  fetch("/send-message", 
        { method: "POST",
          headers: {"Content-Type": "application/json",},
          body: JSON.stringify({ username: "ChatBot", content: message,timestamp: formatTime(Date.now()),}),
        });
}

function sendMessage() {
  $(".chat-body").animate(
    { scrollTop: $(".chat-body").prop("scrollHeight") },
    400
  );

  const userMessage = document.getElementById("message-input").value;
  if (userMessage) {
    appendUserMessage(userMessage);


    // key words for comforting
    const containsKeywords = ["bad", "sad", "died", "kill"];




    // Check if the user message contains any of the keywords
    // Refernece: some() https://www.w3schools.com/jsref/jsref_some.asp
    // Reference Arrow Function for one statement: https://www.w3schools.com/js/js_arrow_function.asp
    const hasKeyword = containsKeywords.some((keyword) =>
      userMessage.toLowerCase().includes(keyword)
    );



    if (hasKeyword) {
      const comfortingMessages = [
        "I'm sorry to hear that. Remember, tough times don't last, but tough people do.",
        "It's okay to feel down sometimes. Just remember that brighter days are ahead.",
        "I'm here for you. If you need someone to talk to, I'm listening.",
        "Take a deep breath. You're stronger than you think.",
        "You're not alone. Reach out to your loved ones for support.",
        "Remember that tough times don't last forever. You have the strength to overcome this.",
        "Even in the darkest moments, there is always a glimmer of hope. Hold on to that.",
        "You are not defined by your struggles. You are defined by how you rise above them.",
        "It's okay to take things one step at a time. Progress, no matter how small, is still progress.",
        "You are not alone in this journey. Reach out to others for support and guidance.",
        "Believe in yourself. You have faced challenges before, and you will overcome this one too.",
        "Take a moment to care for yourself. Self-care is an important part of healing.",
        "You are resilient and capable of handling whatever comes your way. Trust in your abilities.",
        "Be gentle with yourself. Healing takes time, and it's okay to prioritize your well-being.",
        "Remember that setbacks are not permanent. They are opportunities for growth and learning.",
        "Surround yourself with positivity and uplifting influences. They can make a world of difference.",
        "You are stronger than you realize. Keep pushing forward, and you will come out stronger on the other side.",
      ];

      // Select a random comforting message
      const randomMessage = comfortingMessages[Math.floor(Math.random() * comfortingMessages.length)];

      // Delay the Auto's response for a better user experience
      setTimeout(() => {appendAutoMessage(randomMessage);}, 100);
    }

    // Make an API call to the server with the user message
    fetch("/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json",},
      body: JSON.stringify({ message: userMessage, timestamp: formatTime(Date.now()), 
      }),
    })
      .then((response) => response.json())
      .then((data) => { appendAutoMessage(data.message);});

    // Clear the input field
    document.getElementById("message-input").value = "";
  }
}

function displayHistory() {
  fetch("/get-messages")
    .then((response) => response.json())
    .then((data) => {
      const messages = data.messages;
      const chatHistoryBody = document.getElementById("chat-history-body");
      chatHistoryBody.innerHTML = "";

      for (let i = 0; i < messages.length; i++) {
        const message = messages[i];

        const tr = document.createElement("tr");
        const tdTimestamp = document.createElement("td");
        const tdUsername = document.createElement("td");
        const tdContent = document.createElement("td");

        tdTimestamp.textContent = message.timestamp;

        // Check if the username is "ChatBot"
        if (message.username === "ChatBot") {
          // Apply different styling or formatting for "ChatBot" messages
          tdUsername.textContent = "ChatBot (Auto)";
          tdContent.classList.add("auto-reply");
        } else {
          tdUsername.textContent = message.username;
        }

        tdContent.textContent = message.content;

        tr.appendChild(tdTimestamp);
        tr.appendChild(tdUsername);
        tr.appendChild(tdContent);

        chatHistoryBody.appendChild(tr);
      }
    });
}

displayHistory();

// Function to handle the "Clean All History" button click
function cleanHistory() {
  // Make an API call to delete all history
  fetch("/clean-history", { method: "POST" })
    .then((response) => response.json())
    .then((data) => { 
                      alert(data.message); // Display success message
                      window.location.reload(); // Reload the page to fetch and display the updated chat history
                    })
    .catch((error) => { console.error("Error cleaning chat history:", error);});
}

// Event listener for the "Clean All History" button
document
  .getElementById("clean-history-btn")
  .addEventListener("click", cleanHistory);
