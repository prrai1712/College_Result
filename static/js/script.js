async function fetchResult() {
    const scholarno = document.getElementById('scholarno').value.trim();
    const semester = parseInt(document.getElementById('semester').value);
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';

    if (!scholarno) {
        resultDiv.innerHTML = '<p class="error">Please enter a scholar number.</p>';
        return;
    }

    try {
        const response = await fetch('/fetch-student-result', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ scholarno, semester })
        });

        if (!response.ok) {
            const errorData = await response.json();
            resultDiv.innerHTML = `<p class="error">Error: ${errorData.message || 'Unknown error'}</p>`;
            return;
        }

        const data = await response.json();
        let html = '<h3>Result Details:</h3><ul>';
        for (const key in data) {
            html += `<li><strong>${key}:</strong> ${data[key]}</li>`;
        }
        html += '</ul>';
        resultDiv.innerHTML = html;

    } catch (err) {
        resultDiv.innerHTML = `<p class="error">Error: ${err.message}</p>`;
    }
}
