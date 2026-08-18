import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        const filtered = processedCustomers.filter(c => {
            const matchesSearch = c.name.toLowerCase().includes(searchTerm) || 
                                  (c.phone && c.phone.includes(searchTerm)) || """

replacement = """        const filtered = processedCustomers.filter(c => {
            const matchesSearch = (c.full_name || c.name || '').toLowerCase().includes(searchTerm) || 
                                  (c.phone && c.phone.includes(searchTerm)) || """

text = text.replace(target, replacement)

target2 = """            crmTableBody.innerHTML += `
                <tr class="crm-table-row" data-id="${c.id}" style="cursor:pointer;" onclick="openCRMDetail('${c.id}')">
                    <td style="display:flex; align-items:center; gap:12px;">
                        <img src="https://ui-avatars.com/api/?name=${encodeURIComponent(c.name)}&background=random" style="width:36px; height:36px; border-radius:50%;">
                        <div>
                            <div style="font-weight:600; color:var(--text-main);">${c.name}</div>"""

replacement2 = """            crmTableBody.innerHTML += `
                <tr class="crm-table-row" data-id="${c.id}" style="cursor:pointer;" onclick="openCRMDetail('${c.id}')">
                    <td style="display:flex; align-items:center; gap:12px;">
                        <img src="https://ui-avatars.com/api/?name=${encodeURIComponent(c.full_name || c.name || 'U')}&background=random" style="width:36px; height:36px; border-radius:50%;">
                        <div>
                            <div style="font-weight:600; color:var(--text-main);">${c.full_name || c.name}</div>"""

text = text.replace(target2, replacement2)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(text)
