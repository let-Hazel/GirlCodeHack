const provider = getSession();
if (!provider || provider.role !== 'provider') window.location.href = 'login.html';

const providerName = document.getElementById('providerName');
if (providerName) providerName.textContent = provider?.name || 'Provider';
document.getElementById('logoutBtn')?.addEventListener('click', logout);

const serviceList = document.querySelector('.service-list');
const addServiceButton = [...document.querySelectorAll('.btn')].find(b => b.textContent.includes('Add Service'));

async function loadProviderData() {
    try {
        const [skills, requests] = await Promise.all([
            api(`/skills?provider_id=${encodeURIComponent(provider.id)}`),
            api(`/requests/provider/${provider.id}`)
        ]);
        renderServices(skills);
        renderRequests(requests);
    } catch (error) {
        console.error(error);
        alert(error.message);
    }
}

function renderServices(skills) {
    if (!serviceList) return;
    serviceList.innerHTML = '';
    if (!skills.length) {
        serviceList.innerHTML = '<div class="service-item"><div><h3>No services yet</h3><p>Click + Add Service to list your first service.</p></div></div>';
        return;
    }
    skills.forEach(skill => {
        const item = document.createElement('div');
        item.className = 'service-item';
        item.innerHTML = `
            <div class="service-icon">🛠️</div>
            <div>
                <h3>${escapeHtml(skill.skill_name)}</h3>
                <p>${escapeHtml(skill.description || '')}</p>
                <small>${escapeHtml(skill.category || 'General')} · R${skill.price_min} - R${skill.price_max}</small>
            </div>`;
        serviceList.appendChild(item);
    });
}

function renderRequests(requests) {
    let box = document.getElementById('providerRequests');
    if (!box) {
        box = document.createElement('section');
        box.id = 'providerRequests';
        document.querySelector('.dashboard-main')?.appendChild(box);
    }
    box.innerHTML = '<div class="section-title"><h2>Service Requests</h2></div>';
    if (!requests.length) {
        box.innerHTML += '<p>No service requests yet.</p>';
        return;
    }
    requests.forEach(r => {
        const item = document.createElement('div');
        item.className = 'service-item';
        item.innerHTML = `
            <div class="service-icon">📩</div>
            <div>
                <h3>${escapeHtml(r.skill_name_snapshot)}</h3>
                <p>From ${escapeHtml(r.requester_name)} ${escapeHtml(r.requester_surname)}</p>
                <p>Budget: R${r.budget ?? 'Not specified'}</p>
                <strong>Status: ${escapeHtml(r.status)}</strong>
            </div>`;
        if (r.status === 'open') addAction(item, 'Accept', r.id, 'accept');
        if (r.status === 'accepted') addAction(item, 'Complete', r.id, 'complete');
        serviceList?.parentElement?.insertAdjacentElement('afterend', box);
        box.appendChild(item);
    });
}

function addAction(parent, label, id, action) {
    const button = document.createElement('button');
    button.className = 'btn btn-primary';
    button.textContent = label;
    button.addEventListener('click', async () => {
        try {
            await api(`/requests/${id}/${action}`, { method: 'POST' });
            alert(`Request ${action}d successfully.`);
            loadProviderData();
        } catch (error) { alert(error.message); }
    });
    parent.appendChild(button);
}

async function addService() {
    const skill_name = prompt('Service/skill name:');
    if (!skill_name) return;
    const category = prompt('Category:', 'Beauty') || '';
    const price_min = prompt('Minimum price:', '100');
    const price_max = prompt('Maximum price:', '300');
    const description = prompt('Describe your service:', '') || '';
    try {
        await api('/skills', {
            method: 'POST',
            body: JSON.stringify({ provider_id: provider.id, skill_name, category, price_min: Number(price_min), price_max: Number(price_max), description })
        });
        alert('Service added successfully.');
        loadProviderData();
    } catch (error) { alert(error.message); }
}

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#039;' }[c]));
}

addServiceButton?.addEventListener('click', addService);
loadProviderData();