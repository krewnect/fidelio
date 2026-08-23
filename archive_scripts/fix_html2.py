with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Put back the 5 divs
html = html.replace("""        <!-- Canvas Controls -->""",
        """                                </div>
                            </div>
                        </div>
                    </div>
                </div>
        <!-- Canvas Controls -->""")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Restored 5 divs.")
