import re
with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """        // Actualizar métricas del dashboard principal
        updateDashboardMetrics();"""
replacement = """        // Actualizar métricas del dashboard principal
        updateDashboardMetrics();
        if (typeof window.loadAppointments === 'function') window.loadAppointments();"""

js = js.replace(target, replacement)
with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
