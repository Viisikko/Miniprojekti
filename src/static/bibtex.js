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
        const response = await fetch('/export_bibtex');
        if (!response.ok) throw new Error('Network response was not ok');
        const bibtexText = await response.text();
        
        await navigator.clipboard.writeText(bibtexText);

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