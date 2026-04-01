// Function to display results
function showResult(message) {
    document.getElementById('results').innerHTML = `<p>${message}</p>`;
}
// Check string length
document.getElementById('checkLength').addEventListener('click', function () {
    const inputString = document.getElementById('inputString').value;
    showResult(`The length of the string is: ${inputString.length}`);
});
// Extract "JavaScript"
document.getElementById('extractJS').addEventListener('click', function () {
    const inputString = document.getElementById('inputString').value;
    if (inputString.includes('JavaScript')) {
        const startIndex = inputString.indexOf('JavaScript');
        const extracted = inputString.substring(startIndex, startIndex + 10);
        showResult(`Extracted: "${extracted}"`);
    } else {
        showResult('The string does not contain "JavaScript"');
    }
});
// Replace word
document.getElementById('replaceWord').addEventListener('click', function () {
    const inputString = document.getElementById('inputString').value;
    // Replace ANY word typed by user (better than replacing only "old")
    const wordToReplace = prompt("Enter the word you want to replace:");
    const newWord = prompt("Enter the new word:");
    if (wordToReplace && newWord) {
        const replaced = inputString.replace(wordToReplace, newWord);
        showResult(`Original: "${inputString}"<br>Replaced: "${replaced}"`);
    } else {
        showResult("Replacement canceled or invalid input.");
    }
});
// Check if string is palindrome
document.getElementById('checkPalindrome').addEventListener('click', function () {
    const inputString = document.getElementById('inputString').value;
    const result = isPalindrome(inputString);
    showResult(`"${inputString}" is ${result ? 'a palindrome' : 'not a palindrome'}`);
});
// Function to check if a string is a palindrome
function isPalindrome(str) {
    // Remove non-alphanumeric characters and convert to lowercase
    const cleanStr = str.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
    // Compare with reversed string
    const reversedStr = cleanStr.split('').reverse().join('');
    return cleanStr === reversedStr;
}