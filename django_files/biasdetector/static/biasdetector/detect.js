document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#detect-form').addEventListener('submit', event => {
        event.preventDefault();
        const submitButton = document.querySelector('#submit');
        submitButton.disabled = true;
        submitButton.textContent = 'Analyzing...'

        const url = document.querySelector('#articleUrl').value;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        // Django's CSRF adds this:
        // <input type="hidden" name="csrfmiddlewaretoken" value="csrf_token">

        fetch('/api/analyze/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ 'article_url': url })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.querySelector('#results').innerHTML =
                    `<p style="color: red;">${data.error}</p>`;
            } else {
                document.querySelector('#results').innerHTML = `
                    <h3>Article title:</h3>
                    <h4>${data.title}</h4><br>
                    <h3>Bias Type: ${data.bias}</h3>
                    <button id="toggle-text" class="btn btn-sm btn-info">Show article text</button>
                    <div id="article-text" style="display: none; margin-top: 10px;">
                        <h5>Article text:</h5>
                        <p>${data.text}</p><br><br><br>
                    </div>
                `;
                // <p><strong>Clickbait:</strong> ${data.clickbait_result}</p>
                // <p><strong>Bias:</strong> ${data.bias_result}</p>

                const toggleButton = document.querySelector('#toggle-text');
                const textDiv = document.querySelector('#article-text');
                const formDiv = document.querySelector('#form');
                formDiv.style.display = 'none';

                toggleButton.addEventListener('click', () => {
                    if (textDiv.style.display === 'none') {
                        textDiv.style.display = 'block';
                        toggleButton.textContent = 'Hide text';
                    } else {
                        textDiv.style.display = 'none';
                        toggleButton.textContent = 'Show text';
                    }
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result-box').innerHTML =
                `<p style="color: red;">An unexpected error occurred.</p>`;
        });
    })
})