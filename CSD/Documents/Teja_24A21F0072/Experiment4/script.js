// Function to log events to the output div
function logEvent(message) {
    const output = document.getElementById('output');
    output.innerHTML = `<p>${message}</p>` + output.innerHTML;
}
// Click event listener
document.getElementById('clickMe').addEventListener('click', function() {
    logEvent('Button clicked!');
    console.log('Button clicked!');
});
// Mouse over event listener for image
document.getElementById('imageElement').addEventListener('mouseover', function() {
    this.style.borderColor = 'red';
    logEvent('Mouse over image - border color changed to red');
});
// Mouse out event listener to reset border
document.getElementById('imageElement').addEventListener('mouseout', function() {
    this.style.borderColor = 'black';
    logEvent('Mouse out image - border color reset to black');
});
// Key press event listener
document.addEventListener('keydown', function(event) {
    const keyPressed = document.getElementById('keyPressed');
    keyPressed.textContent = event.key;
    logEvent(`Key pressed: ${event.key}`);
});