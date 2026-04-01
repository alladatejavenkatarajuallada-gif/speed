// Create student object
const student = {
    name: "SIVA SHANKAR",
    grade: 84,
    subjects: ["DATA STRUCTURE", "OPERATING SYSTEM", "COMPUTER ORGANIZATION", "DBMS"],
    displayInfo: function() {
        return `Name: ${this.name}, Grade: ${this.grade}, Subjects: ${this.subjects.join(", ")}`;
    }
};
// Function to display output
function showOutput(message) {
    document.getElementById('output').innerHTML = message;
}
// Display student info
document.getElementById('displayInfo').addEventListener('click', function() {
    showOutput(`<h3>Student Information:</h3><p>${student.displayInfo()}</p>`);
});
// Add passed property
document.getElementById('addProperty').addEventListener('click', function() {
    // Add passed property based on grade
    student.passed = student.grade >= 60;
    let message = `<h3>Added 'passed' property:</h3>`;
    message += `<p>${student.name} has ${student.passed ? 'passed' : 'failed'} with a grade of ${student.grade}.</p>`;
    showOutput(message);
});
// Display all keys and values
document.getElementById('displayKeys').addEventListener('click', function() {
    let message = `<h3>All Keys and Values:</h3><ul>`;
    // Loop through all keys and values
    for (let key in student) {
        // Check if the property is not a function
        if (typeof student[key] !== 'function') {
            message += `<li><strong>${key}:</strong> ${Array.isArray(student[key]) ? student[key].join(", ") : student[key]}</li>`;
        } else {
            message += `<li><strong>${key}:</strong> [Function]</li>`;
        }
    }
    message += `</ul>`;
    showOutput(message);
});