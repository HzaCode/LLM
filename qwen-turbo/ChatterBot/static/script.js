document.getElementById("askForm").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent the default form submission behavior

    // Get the value of the question input
    const question = document.getElementById("question").value.trim();
    if (!question) {
        alert('Please enter a valid question.');
        return;
    }

    // Send a POST request to the '/ask' route
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: question })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        return response.json();  // Parse the response as JSON
    })
    .then(data => {
        // Display the response text
        document.getElementById("responseText").textContent = data.response.text || 'No response received from the server.';
        document.getElementById("responseContainer").style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Something went wrong! Please try again later.');
    });
});
