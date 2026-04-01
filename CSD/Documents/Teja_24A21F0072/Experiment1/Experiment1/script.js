// Part A: Hello World and Sum Calculation
console.log("Hello, World!");

document.getElementById('sumBtn').addEventListener('click', function() {
    const num1 = 10;
    const num2 = 20;
    const sum = num1 + num2;
    alert(`The sum of ${num1} and ${num2} is ${sum}`);
});

// Part B: Array Operations
const cities = ["tanuku", "palakollu", "bhimavaram", "narasapuram", "vijayawada"];

// Function to display array operations
function displayArrayOperations() {
    let output = document.getElementById('arrayOutput');
    
    // Log total number of cities
    output.innerHTML += `<p>Total number of cities: ${cities.length}</p>`;
    
    // Add a new city at the end
    cities.push("sitharamapuram");
    output.innerHTML += `<p>After adding Berlin: ${cities.join(", ")}</p>`;
    
    // Remove the first city
    const removedCity = cities.shift();
    output.innerHTML += `<p>Removed city: ${removedCity}</p>`;
    output.innerHTML += `<p>Cities after removal: ${cities.join(", ")}</p>`;
    
    // Find and log the index of a specific city
    const cityToFind = "tanuku";
    const cityIndex = cities.indexOf(cityToFind);
    output.innerHTML += `<p>Index of ${cityToFind}: ${cityIndex}</p>`;
}

// Call the function when the page loads
window.onload = displayArrayOperations;