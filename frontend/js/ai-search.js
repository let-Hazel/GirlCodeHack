const aiRequest = document.getElementById('aiRequest');
const aiSearchBtn = document.getElementById('aiSearchBtn');
const aiResult = document.getElementById('aiResult');
const providerGridForAI = document.querySelector('#providerGrid');

const keywords = {
    Beauty: ['hair','hairdresser','braids','braiding','makeup','nails','beauty'],
    Repairs: ['repair','fix','plumber','plumbing','electrician','pipe','leak'],
    Technology: ['computer','laptop','phone','wifi','internet','printer','software','tech'],
    Education: ['tutor','tutoring','teacher','maths','mathematics','lesson','school','study'],
    Creative: ['design','designer','logo','poster','flyer','photography','video']
};

function detectCategory(text) {
    let best = 'General Services';
    let score = 0;
    for (const [category, words] of Object.entries(keywords)) {
        const hits = words.filter(word => text.includes(word)).length;
        if (hits > score) { score = hits; best = category; }
    }
    return best;
}

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#039;' }[c]));
}

async function runAISearch() {
    const text = aiRequest?.value.trim().toLowerCase();
    if (!text) return;
    if (aiResult) aiResult.innerHTML = '<div class="ai-loading">✨ Matching your request with live SkillLink services...</div>';
    try {
        const providers = await api(`/providers?skill=${encodeURIComponent(text)}`);
        if (aiResult) aiResult.innerHTML = `
            <div class="ai-result-card">
                <div class="ai-result-header"><span>✨ SKILLINK AI</span><span class="ai-match">AI MATCH</span></div>
                <h3>${escapeHtml(detectCategory(text))}</h3>
                <p>Matched your description against services registered in SkillLink.</p>
                <div class="ai-request"><strong>Your request:</strong><p>“${escapeHtml(text)}”</p></div>
                <strong>${providers.length} provider(s) found</strong>
            </div>`;
        if (providerGridForAI) {
            providerGridForAI.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    } catch (error) {
        if (aiResult) aiResult.innerHTML = `<div class="ai-error">${escapeHtml(error.message)}</div>`;
    }
}

aiSearchBtn?.addEventListener('click', runAISearch);
aiRequest?.addEventListener('keydown', e => { if (e.ctrlKey && e.key === 'Enter') runAISearch(); });