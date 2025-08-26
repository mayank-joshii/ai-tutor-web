// app.js

document.getElementById('tutor-form').addEventListener('submit', function (e) {
    e.preventDefault();
    
    const topic = document.getElementById('topic').value;
    const level = document.getElementById('level').value;

    fetch('http://127.0.0.1:8000/api/tutor/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer <your_token>',  // Replace with actual JWT token
        },
        body: JSON.stringify({ topic, level })
    })
    .then(response => response.json())
    .then(data => {
        // Display the explanation
        document.getElementById('explanation').textContent = data.explanation;

        // Display the quiz
        const quizContainer = document.getElementById('quiz');
        quizContainer.innerHTML = ''; // Clear any previous content
        const quizQuestions = data.quiz.split('\n');
        quizQuestions.forEach(question => {
            const questionElement = document.createElement('p');
            questionElement.textContent = question;
            quizContainer.appendChild(questionElement);
        });

        // Show retry button
        document.getElementById('retry-btn').style.display = 'inline-block';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Something went wrong!');
    });
});

// Optional: Fetch user progress (previous topics)
function fetchProgress() {
    fetch('http://127.0.0.1:8000/api/user-progress/', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer <your_token>'  // Replace with actual JWT token
        }
    })
    .then(response => response.json())
    .then(data => {
        const progressList = document.getElementById('progress-list');
        progressList.innerHTML = '';
        data.forEach(log => {
            const listItem = document.createElement('li');
            listItem.textContent = `${log.topic} - Score: ${log.quiz_score}`;
            progressList.appendChild(listItem);
        });
    })
    .catch(error => console.error('Error fetching progress:', error));
}

fetchProgress();  // Call to load progress on page load
