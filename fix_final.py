with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# The exact problematic block at the end of tab-builder:
old_block = """                        <div style="margin-top:auto; padding-top:16px;">
                            <button id="btn-save-design-push" class="fidelio-btn-primary"><i class="fa-solid fa-cloud-arrow-up"></i> Guardar y Publicar Diseño</button>
                        </div>
            </div>"""

new_block = """                        <div style="margin-top:auto; padding-top:16px;">
                            <button id="btn-save-design-push" class="fidelio-btn-primary"><i class="fa-solid fa-cloud-arrow-up"></i> Guardar y Publicar Diseño</button>
                        </div>"""

html = html.replace(old_block, new_block)

# And remove the 5 divs I restored previously
old_block2 = """                                </div>
                            </div>
                        </div>
                    </div>
                </div>
        <!-- Canvas Controls -->"""

new_block2 = """        <!-- Canvas Controls -->"""

html = html.replace(old_block2, new_block2)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Applied strict HTML fix.")
