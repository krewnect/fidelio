with open('dashboard.js', 'r') as f:
    lines = f.readlines()

# The bindings block starts at "    // --- TEAM MANAGEMENT (RBAC) ---"
# and ends right before "renderCRMTable();" around line 859.
start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "// --- TEAM MANAGEMENT (RBAC) ---" in line:
        start_idx = i
    if start_idx != -1 and "renderCRMTable();" in line and i > start_idx and i < start_idx + 50:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    bindings = lines[start_idx:end_idx]
    # Remove from original location
    del lines[start_idx:end_idx]
    
    # Now find the correct place to insert it.
    # The end of initFidelio is where loadDataFromSupabase() is called.
    # Actually, we can just insert it right before the END of initFidelio().
    # initFidelio ends at line 1640 approximately:
    #     renderCRMTable();
    # })();
    
    # Let's find "})();"
    insert_idx = -1
    for i in range(len(lines)-1, -1, -1):
        if "})();" in lines[i]:
            insert_idx = i
            break
            
    if insert_idx != -1:
        # Insert bindings there
        lines = lines[:insert_idx] + bindings + lines[insert_idx:]
        
        with open('dashboard.js', 'w') as f:
            f.writelines(lines)
        print("Bindings moved successfully.")
    else:
        print("Could not find })();")
else:
    print(f"Could not find bindings block. start_idx: {start_idx}, end_idx: {end_idx}")
