// --- PASSLOYALTY SUPER ADMIN MASTER SCRIPT (4 MAIN TABS) --- //

document.addEventListener('DOMContentLoaded', () => {

    // --- TAB NAVIGATION FOR SUPER ADMIN ---
    const adminNavTabs = document.querySelectorAll('[data-admin-tab]');
    const adminTabContents = document.querySelectorAll('.tab-content');

    adminNavTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            adminNavTabs.forEach(t => t.classList.remove('active'));
            adminTabContents.forEach(c => c.classList.remove('active'));

            tab.classList.add('active');
            const targetTabId = tab.getAttribute('data-admin-tab');
            document.getElementById(targetTabId).classList.add('active');
        });
    });

    // --- MASTER CUSTOMER DATABASE CONSOLIDATION ---
    const masterDatabase = [
        { id: "LOYAL-8842", name: "Roberto Ordóñez", restaurant: "Don Pedro Gourmet", phone: "+52 55 1234 5678", email: "roberto@ejemplo.com", birthday: "18 de Noviembre", walletType: "Apple Wallet", tier: "Oro VIP", balance: 145.00, regDate: "2026-01-15" },
        { id: "LOYAL-9912", name: "Ana Sofía Gómez", restaurant: "Don Pedro Gourmet", phone: "+52 55 9876 5432", email: "ana.gomez@gmail.com", birthday: "05 de Agosto", walletType: "Apple Wallet", tier: "Oro VIP", balance: 320.50, regDate: "2026-01-18" },
        { id: "LOYAL-1044", name: "Carlos Mendoza", restaurant: "Don Pedro Gourmet", phone: "+52 55 5555 1212", email: "carlos.m@hotmail.com", birthday: "22 de Febrero", walletType: "Google Wallet", tier: "Bronce VIP", balance: 45.00, regDate: "2026-02-01" },
        { id: "LOYAL-2390", name: "Mariana Torres", restaurant: "Don Pedro Gourmet", phone: "+52 55 4444 8888", email: "mtorres@empresa.com", birthday: "14 de Septiembre", walletType: "Apple Wallet", tier: "Plata VIP", balance: 190.00, regDate: "2026-02-05" },
        { id: "TACO-001", name: "David López", restaurant: "Tacos El Pastor", phone: "+52 55 1111 2222", email: "david@tacos.com", birthday: "12 de Diciembre", walletType: "Google Wallet", tier: "Oro VIP", balance: 210.00, regDate: "2026-02-10" },
        { id: "TACO-002", name: "Lucía Ramírez", restaurant: "Tacos El Pastor", phone: "+52 55 2222 3333", email: "lucia@gmail.com", birthday: "28 de Junio", walletType: "Apple Wallet", tier: "Bronce VIP", balance: 36.00, regDate: "2026-02-14" },
        { id: "PIZZA-501", name: "Gabriel Silva", restaurant: "Pizzería Bella Italia", phone: "+52 55 8888 7777", email: "gabriel@pizza.com", birthday: "04 de Mayo", walletType: "Apple Wallet", tier: "Plata VIP", balance: 95.00, regDate: "2026-03-01" }
    ];

    const tbody = document.getElementById('master-crm-table-body');
    const searchInput = document.getElementById('admin-search-input');

    function renderMasterTable() {
        if (!tbody) return;
        const query = searchInput ? searchInput.value.toLowerCase() : '';
        const filtered = masterDatabase.filter(c => 
            c.name.toLowerCase().includes(query) ||
            c.restaurant.toLowerCase().includes(query) ||
            c.phone.includes(query) ||
            c.email.toLowerCase().includes(query) ||
            c.birthday.toLowerCase().includes(query) ||
            c.id.toLowerCase().includes(query)
        );

        tbody.innerHTML = '';

        filtered.forEach(c => {
            const tr = document.createElement('tr');
            const tierClass = c.tier.includes('Oro') ? 'oro' : c.tier.includes('Plata') ? 'plata' : 'bronce';

            tr.innerHTML = `
                <td><code>${c.id}</code></td>
                <td><strong>${c.name}</strong></td>
                <td><span class="tier-pill" style="background:rgba(99, 102, 241, 0.15); color:var(--indigo);">${c.restaurant}</span></td>
                <td>${c.phone}</td>
                <td>${c.email}</td>
                <td><strong style="color:var(--cyan);"><i class="fa-solid fa-cake-candles"></i> ${c.birthday}</strong></td>
                <td><i class="fa-brands ${c.walletType.includes('Apple') ? 'fa-apple' : 'fa-google'}"></i> ${c.walletType}</td>
                <td><span class="tier-pill ${tierClass}">${c.tier}</span></td>
                <td><strong class="text-emerald">$${c.balance.toFixed(2)} MXN</strong></td>
                <td>${c.regDate}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', renderMasterTable);
    }

    const btnExportMaster = document.getElementById('btn-export-master-db');
    if (btnExportMaster) {
        btnExportMaster.addEventListener('click', () => {
            alert("Exportando Base de Datos Maestra Consolidada en formato CSV...");
        });
    }

    const btnSaveAi = document.getElementById('btn-save-ai-config');
    if (btnSaveAi) {
        btnSaveAi.addEventListener('click', () => {
            alert("Configuración de DeepSeek API y prompts del sistema guardados correctamente.");
        });
    }

    const btnOnboardNew = document.getElementById('btn-onboard-new-restaurant');
    if (btnOnboardNew) {
        btnOnboardNew.addEventListener('click', () => {
            alert("Abriendo formulario para dar de alta un nuevo restaurante en la plataforma...");
        });
    }

    renderMasterTable();
});
