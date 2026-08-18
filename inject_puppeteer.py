import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Add the require
app_js = app_js.replace("const express = require('express');", "const express = require('express');\nconst { generateStampsStrip } = require('./render_stamps.js');")

# We want to replace the backgroundColor logic to make it white.
target_bg = """                backgroundColor: campaign.color_primary || "#090d16",
                foregroundColor: "#ffffff",
                labelColor: campaign.color_accent || "#8b5cf6","""
replacement_bg = """                backgroundColor: "rgb(255, 255, 255)",
                foregroundColor: "rgb(17, 24, 39)",
                labelColor: "rgb(107, 114, 128)","""

app_js = app_js.replace(target_bg, replacement_bg)

target_add = """        // Intentar agregar iconos o logos customizados"""
replacement_add = """        // Generar strip.png usando Puppeteer si es tipo stamps
        if (campaign.type === 'stamps') {
            try {
                const totalStamps = campaign.rules_config?.stamps_total || 5;
                const earnedStamps = stamps;
                const cPrimary = campaign.color_primary || '#8b5cf6';
                const stripBuffer = await generateStampsStrip(totalStamps, earnedStamps, cPrimary);
                pass.addBuffer('strip.png', stripBuffer);
                pass.addBuffer('strip@2x.png', stripBuffer);
            } catch (e) {
                console.error("Puppeteer strip generation failed", e);
            }
        }
        
        // Intentar agregar iconos o logos customizados"""

app_js = app_js.replace(target_add, replacement_add)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
