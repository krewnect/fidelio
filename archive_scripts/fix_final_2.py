with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add exactly 4 closing divs before </section> of tab-builder
html = html.replace("""        </div>
        
    </div>
</div>
</section>

            <!-- CRM TAB -->""",
"""        </div>
        
    </div>
</div>
</div></div></div></div>
</section>

            <!-- CRM TAB -->""")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Added 4 missing divs.")
