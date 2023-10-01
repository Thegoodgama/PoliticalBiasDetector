import tkinter as tk
from tkinter import ttk, filedialog
import openai
import webbrowser

openai.api_key = "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"
liberalFile = 'liberal.txt'
consFile = 'conservative.txt'
neutFile = 'Neutral.txt'

def open_link(link):
    webbrowser.open(link)

def analyze_file():
    file_path = filedialog.askopenfilename()

    if file_path:
        liberal = 0
        conservative = 0
        neutral = 0

        messages = [
            {"role": "system", "content": "I will prompt you with a potentially biased sentence about a modern political issue, tell me if there is a liberal, conservative, or neutral stance in one word along with phrases. Separate all this with commas"},
        ]

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    messages.append(
                        {"role": "user", "content": line}
                    )
                    chat = openai.ChatCompletion.create(
                        model="gpt-4", messages=messages
                    )
                    reply = (chat.choices[0].message.content).lower()
                    reply = reply.split(", ")
                    if "liberal" in reply:
                        liberal += 1
                        with open (liberalFile, 'w') as lFile:
                            for word in range(1,len(reply)):
                                lFile.write(reply[word] + "\n")

                    elif "conservative" in reply:
                        conservative += 1
                        with open (consFile, 'w') as cFile:
                            for word in range(1,len(reply)):
                                cFile.write(reply[word]+ "\n")
                    elif "neutral" in reply:
                        neutral += 1
                        with open (neutFile, 'w') as nFile:
                            for word in range(1,len(reply)):
                                nFile.write(reply[word]+ "\n")

            percent = ((liberal + conservative) / (conservative + liberal + neutral)) * 100
            result_label.config(
                text=f"Analysis Results:\n"
                     f"Liberal Bias: {liberal} phrases\n"
                     f"Conservative Bias: {conservative} phrases\n"
                     f"No Bias: {neutral} phrases\n"
                     f"Bias Percentage: {percent:.2f}%",
                fg="white",
                bg="#222",
                padx=20,
                pady=10,
                font=("Helvetica", 12)
            )

            liberal_link.config(state=tk.NORMAL, command=lambda: open_link(liberalFile))
            conservative_link.config(state=tk.NORMAL, command=lambda: open_link(consFile))
            neutral_link.config(state=tk.NORMAL, command=lambda: open_link(neutFile))

        except FileNotFoundError:
            result_label.config(text=f"The file was not found.", fg="red")
        except Exception as e:
            result_label.config(text=f"An error occurred: {str(e)}", fg="red")

app = tk.Tk()
app.title("Bias Analyzer")
app.configure(bg="#222")

title_label = tk.Label(app, text="Political Bias Analyzer", font=("Helvetica", 16), fg="white", bg="#222")
title_label.pack(pady=10)

analyze_button = tk.Button(app, text="Analyze File", command=analyze_file, padx=10, pady=5, font=("Helvetica", 12))
analyze_button.pack(pady=20)

result_label = tk.Label(app, text="", font=("Helvetica", 12), fg="white", bg="#222")
result_label.pack()

liberal_link = ttk.Button(app, text="Download Liberal Phrases", state=tk.DISABLED)
liberal_link.pack()
conservative_link = ttk.Button(app, text="Download Conservative Phrases", state=tk.DISABLED)
conservative_link.pack()
neutral_link = ttk.Button(app, text="Download Neutral Phrases", state=tk.DISABLED)
neutral_link.pack()

app.mainloop()
