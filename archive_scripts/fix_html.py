with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the missing div in tab-caja
html = html.replace("""                            <tbody id="caja-transactions-tbody">
                                <!-- Llenado por JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>""",
            """                            <tbody id="caja-transactions-tbody">
                                <!-- Llenado por JS -->
                            </tbody>
                        </table>
                        </div>
                    </div>
                </div>
            </section>""")

# Fix the extra divs in tab-builder
# We know the extra divs are just before <!-- Canvas Controls -->
html = html.replace("""                                </div>
                            </div>
                        </div>
                    </div>
                </div>
           
        
        <!-- Canvas Controls -->""",
        """        <!-- Canvas Controls -->""")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Fixed HTML div structure.")
