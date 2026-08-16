const currentUser = getSession();
if (!currentUser || currentUser.role !== 'user') window.location.href = 'login.html';

const userName = document.getElementById('userName');
if (userName) userName.textContent = currentUser?.name || 'User';

const providerGrid = document.querySelector('#providerGrid');
const searchInput = document.getElementById('serviceSearch');
const searchBtn = document.getElementById('searchBtn');

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, c => ({
        '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#039;'
    }[c]));
}

async function loadProviders(search = '') {
    if (!providerGrid) return;
    try {
        const endpoint = search ? `/providers?skill=${encodeURIComponent(search)}` : '/providers';
        const providers = await api(endpoint);
        displayProviders(providers);
    } catch (error) {
        providerGrid.innerHTML = `<p>${escapeHtml(error.message)}</p>`;
    }
}

function displayProviders(providers) {
    if (!providerGrid) return;
    providerGrid.innerHTML = '';
    if (!providers.length) {
        providerGrid.innerHTML = '<div class="no-providers"><h3>No providers found</h3><p>Try another search.</p></div>';
        return;
    }

    providers.forEach(provider => {
        const initials = `${provider.name?.[0] || ''}${provider.surname?.[0] || ''}`;
        const card = document.createElement('div');
        card.className = 'provider-card';
        card.innerHTML = `
            <div class="provider-avatar">${escapeHtml(initials)}</div>
            <h3>${escapeHtml(provider.name)} ${escapeHtml(provider.surname)}</h3>
            <p class="skill">${escapeHtml(provider.skill_name)}</p>
            <p class="location">📍 ${escapeHtml(provider.location || 'Location not provided')}</p>
            <p>⭐ ${Number(provider.avg_rating || 0).toFixed(1)}</p>
            <p>R${provider.price_min} - R${provider.price_max}</p>
            <p>${escapeHtml(provider.description || '')}</p>
            <button class="btn btn-primary request-service">Request Service</button>
            <button class="whatsapp-btn contact-provider">💬 WhatsApp Provider</button>
        `;
        card.querySelector('.request-service').addEventListener('click', () => requestService(provider));
        card.querySelector('.contact-provider').addEventListener('click', () => contactProvider(provider.phone));
        providerGrid.appendChild(card);
    });
}

async function requestService(provider) {
    const budget = prompt(`Budget for ${provider.skill_name} (R${provider.price_min} - R${provider.price_max}):`, provider.price_max);
    if (budget === null) return;
    try {
        await api('/requests', {
            method: 'POST',
            body: JSON.stringify({ skill_id: provider.skill_id, requester_id: currentUser.id, budget: Number(budget) })
        });
        alert('Service request sent to the provider.');
    } catch (error) { alert(error.message); }
}

function contactProvider(phone) {
    if (!phone) return alert('This provider has not added a phone number.');
    const clean = String(phone).replace(/\D/g, '');
    const message = encodeURIComponent('Hi, I found your service on SkillLink and would like to enquire about your services.');
    window.open(`https://wa.me/${clean}?text=${message}`, '_blank');
}

searchBtn?.addEventListener('click', () => loadProviders(searchInput?.value.trim() || ''));
searchInput?.addEventListener('keydown', e => { if (e.key === 'Enter') loadProviders(searchInput.value.trim()); });
document.getElementById('logoutBtn')?.addEventListener('click', logout);

loadProviders();