// Define threshold for preparation time
const THRESHOLD = 3000.0; // Example threshold (seconds)

// Function to fetch and update data
async function fetchData() {
    try {
        const response = await fetch('/api/sensor-data');
        const data = await response.json();

        // Update part count
        document.getElementById('part-count').textContent = data.partCount;

        // Format preparation time to 3 decimal places
        const formattedTime = data.preparationTime.toFixed(3);
        document.getElementById('preparation-time').textContent = formattedTime;

        // Update progress
        document.getElementById('progress').textContent = `${data.progress}%`;

        // Check if partCount has reached 10 before displaying the message
        const statusMessage = document.getElementById('status-message');
        const message = document.getElementById('message');
        
        if (data.partCount === 10) { // Only show the message when partCount is 10
            if (data.preparationTime <= THRESHOLD) {
                message.innerHTML = "😊 Preparation within time limit!";
                statusMessage.classList.remove("sad");
                statusMessage.classList.add("happy");
            } else {
                message.innerHTML = "😞 Exceeded time limit!";
                statusMessage.classList.remove("happy");
                statusMessage.classList.add("sad");
            }
            statusMessage.style.display = "block"; // Show the message
        } else {
            statusMessage.style.display = "none"; // Hide the message if partCount is not 10
        }

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Fetch data every 2 seconds
setInterval(fetchData, 2000);
