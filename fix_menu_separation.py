import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add logic to hide/show tabs based on industry
menu_logic = """
            // Strict Profile Separation Logic
            const industry = (merchantData.industry || '').toLowerCase();
            const isProfessional = industry === 'servicios profesionales' || industry === 'salud y bienestar' || industry === 'belleza y spa';
            
            // Elements
            const navStripe = document.getElementById('nav-stripe');
            const navAppointments = document.getElementById('nav-appointments');
            const navCrm = document.querySelector('[data-tab="tab-crm"]');
            const navStaff = document.querySelector('[data-tab="tab-staff"]');
            const navBank = document.querySelector('[data-tab="tab-bank"]');
            const navLoyalty = document.querySelector('[data-tab="tab-loyalty"]');
            const navAi = document.querySelector('[data-tab="tab-ai"]');

            if (isProfessional) {
                // Professionals see Stripe, Appointments, CRM. Hide Staff, Loyalty, Bank.
                if (navStripe) navStripe.style.display = 'block';
                if (navAppointments) navAppointments.style.display = 'block';
                
                if (navStaff) navStaff.style.display = 'none';
                if (navLoyalty) navLoyalty.style.display = 'none';
                if (navBank) navBank.style.display = 'none';
                if (navAi) navAi.style.display = 'none';
            } else {
                // Restaurants/Retail see Loyalty, Staff, Bank. Hide Stripe, Appointments.
                if (navStripe) navStripe.style.display = 'none';
                if (navAppointments) navAppointments.style.display = 'none';
                
                if (navStaff) navStaff.style.display = 'block';
                if (navLoyalty) navLoyalty.style.display = 'block';
                if (navBank) navBank.style.display = 'block';
                if (navAi) navAi.style.display = 'block';
            }
"""

js = js.replace('document.getElementById("merchant-name-display").textContent = merchantData.business_name;', 'document.getElementById("merchant-name-display").textContent = merchantData.business_name;\n' + menu_logic)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Menu separation applied successfully.")
