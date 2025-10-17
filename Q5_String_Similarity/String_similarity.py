import tkinter as tk
from difflib import SequenceMatcher

def compare_strings():
    s1 = entry1.get().strip()
    s2 = entry2.get().strip()

    if len(s1) == 0 or len(s2) == 0:
        result_text.set(" Both strings must have at least 1 character!")
        return

    matcher = SequenceMatcher(None, s1, s2)
    similarity = matcher.ratio() * 100

    # Alignment results yeah
    lines = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        part1, part2 = s1[i1:i2], s2[j1:j2]

        # Go charcter  by charcter 
        for k in range(max(len(part1), len(part2))):
            c1 = part1[k] if k < len(part1) else "-"
            c2 = part2[k] if k < len(part2) else "-"
            mark = "✅" if c1 == c2 else "❌"
            lines.append(f"{c1}   {c2}   {mark}")

    # Build  the finall report
    report = "Char1  Char2  Match\n---------------------\n"
    report += "\n".join(lines)
    report += f"\n\nSimilarity: {similarity:.2f} %"

    result_text.set(report)


# -------------- GUI stuff ----------------
root = tk.Tk()
root.title("🔍 String Similarity Matcher")
root.geometry("600x500")
root.config(bg="black")  # Changed background to black

# Title Label
title = tk.Label(root, text="String Similarity Matcher", font=("Arial", 18, "bold"), fg="red", bg="black")  # Red text
title.pack(pady=10)

# Entry fields
entry1 = tk.Entry(root, font=("Consolas", 14), justify="center", bg="black", fg="red", insertbackground="red")
entry1.pack(pady=5, fill="x", padx=20)
entry2 = tk.Entry(root, font=("Consolas", 14), justify="center", bg="black", fg="red", insertbackground="red")
entry2.pack(pady=5, fill="x", padx=20)

# Button
btn = tk.Button(root, text="Compare Strings", font=("Arial", 14), bg="red", fg="black", command=compare_strings)
btn.pack(pady=15)

# Result area (multi-line support)
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Consolas", 12), fg="red", bg="black", justify="left", anchor="w")
result_label.pack(pady=10, padx=20, fill="both")

root.mainloop()
