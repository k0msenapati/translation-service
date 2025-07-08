function translateText() {
    const text = document.getElementById('textInput').value;
    const languagesInput = document.getElementById('languagesInput').value;

    if (!text || !languagesInput) {
        alert('Please enter both text and languages');
        return;
    }

    const languages = languagesInput.split(',').map(lang => lang.trim());

    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('result').classList.add('hidden');

    fetch('/api/translate', {
        method: 'POST',
        body: JSON.stringify({
            text: text,
            languages: languages
        }),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            const taskId = data.task_id;


            document.getElementById('translationIdInput').value = taskId;


            alert(`Translation submitted! Task ID: ${taskId}\n\nYou can now use the "Check Status" and "Check Content" buttons below to monitor your translation.`);


            pollTranslationStatus(taskId);
        })
        .catch(error => {
            document.getElementById('loading').classList.add('hidden');
            alert('Error: ' + error.message);
        });
}

function pollTranslationStatus(taskId) {
    fetch(`/api/status/${taskId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'completed') {
                document.getElementById('loading').classList.add('hidden');
                displayTranslations(data.translations);
                document.getElementById('result').classList.remove('hidden');
            } else {
                setTimeout(() => pollTranslationStatus(taskId), 1000);
            }
        })
        .catch(error => {
            document.getElementById('loading').classList.add('hidden');
            alert('Error checking status: ' + error.message);
        });
}

function displayTranslations(translations) {
    let html = '';
    for (const [lang, translation] of Object.entries(translations)) {
        html += `<div class="mb-2"><strong>${lang}:</strong> ${translation}</div>`;
    }
    document.getElementById('translatedText').innerHTML = html;
}

function checkTranslationStatus() {
    const id = document.getElementById('translationIdInput').value;
    if (!id) {
        alert('Please enter a translation ID');
        return;
    }

    document.getElementById('checkResult').textContent = 'Checking status...';

    fetch(`/api/status/${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Translation not found');
            }
            return response.json();
        })
        .then(data => {
            let resultText = `Status: ${data.status}`;
            if (data.translations) {
                resultText += '\nTranslations: ' + JSON.stringify(data.translations, null, 2);
            }
            document.getElementById('checkResult').textContent = resultText;
        })
        .catch(error => {
            document.getElementById('checkResult').textContent = `Error: ${error.message}`;
        });
}

function checkTranslationContent() {
    const id = document.getElementById('translationIdInput').value;
    if (!id) {
        alert('Please enter a translation ID');
        return;
    }

    document.getElementById('checkResult').textContent = 'Checking content...';

    fetch(`/api/content/${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Translation not found');
            }
            return response.json();
        })
        .then(data => {
            let resultText = `ID: ${data.id}\nText: ${data.text}\nLanguages: ${data.languages.join(', ')}\nStatus: ${data.status}`;
            if (data.translations && Object.keys(data.translations).length > 0) {
                resultText += '\nTranslations:\n';
                for (const [lang, translation] of Object.entries(data.translations)) {
                    resultText += `  ${lang}: ${translation}\n`;
                }
            }
            document.getElementById('checkResult').textContent = resultText;
        })
        .catch(error => {
            document.getElementById('checkResult').textContent = `Error: ${error.message}`;
        });
}
