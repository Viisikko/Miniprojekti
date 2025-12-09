function openBibtexModal() {
    document.getElementById('bibtexModal').style.display = 'flex';
}

function closeBibtexModal() {
    document.getElementById('bibtexModal').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('bibtexModal');
    if (event.target == modal) {
        closeBibtexModal();
    }
}

async function copyBibtexToClipboard() {
    const copyBtn = document.getElementById('copyBtn');
    const originalText = copyBtn.innerText;

    try {
        const urlParams = new URLSearchParams(window.location.search);
        const searchQuery = urlParams.get('q');
        const exportUrl = searchQuery ? `/export_bibtex?q=${encodeURIComponent(searchQuery)}` : '/export_bibtex';
        const response = await fetch(exportUrl);
        if (!response.ok) throw new Error('Network response was not ok');
        const bibtexText = await response.text();

        if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
            await navigator.clipboard.writeText(bibtexText);
        } else {
            const textarea = document.createElement('textarea');
            textarea.value = bibtexText;
            textarea.style.position = 'fixed';
            textarea.style.left = '-9999px';
            document.body.appendChild(textarea);
            textarea.select();
            try {
                const successful = document.execCommand('copy');
                if (!successful) throw new Error('Fallback: copy command was unsuccessful');
            } finally {
                document.body.removeChild(textarea);
            }
        }

        copyBtn.classList.add('success');

        copyBtn.innerText = "Copied!";

        setTimeout(() => {
            closeBibtexModal();

            copyBtn.classList.remove('success');
            copyBtn.innerText = originalText; 
        }, 1500);


    } catch (err) {
        console.error('Failed to copy: ', err);
        copyBtn.innerText = "Error!";
        setTimeout(() => { copyBtn.innerText = originalText; }, 2000);
    }
}