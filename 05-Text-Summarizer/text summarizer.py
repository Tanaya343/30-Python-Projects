import tkinter as tk #for GUI
from tkinter import messagebox, scrolledtext #For GUI
from nltk.tokenize import sent_tokenize, word_tokenize #breaks text into words and sentences
from collections import defaultdict #Helps build a frequency table without needing to check if a key exists first



def summarize_text():
    text = input_text.get("1.0", tk.END).strip() #pulls text from the input box
    #.get("1.0", tk.END) grabs everything from line 1, character 0 to the end

    if not text:
        messagebox.showwarning("Warning", "Please enter some text.")
        return
    #checks if text is empty, shows a warning and stop the function

    sentences = sent_tokenize(text) #breaks the paragraph into a list of sentences
    words = word_tokenize(text.lower()) #then tokenize the entire text into lowercase words

    # Create frequency table (ignore punctuation/common stopwords)
    freq_table = defaultdict(int)
    for word in words:
        if word.isalpha():
            freq_table[word] += 1 #for every alphabetical word (ignoring punctuation), adds to frequency count

    # Score each sentence based on word frequencies
    sentence_scores = {}
    for sentence in sentences: #for each sentence in sentences
        sentence_words = word_tokenize(sentence.lower()) 
        sentence_score = 0 #initialized sentence score zero
        for word in sentence_words: #for everyy word in sentence
            if word in freq_table: #each sentence is given a score based on the total frequency of its words
                sentence_score += freq_table[word] 
        sentence_scores[sentence] = sentence_score

    # Select top 30% of sentences based on score
    top_n = max(1, int(len(sentences) * 0.3)) #range is from 1 to number of sentences *0.3
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:top_n]
    summary = " ".join(summary_sentences) #Calculates how many sentences to keep, atleast 1
    #picks the top scoring sentences and joins them as summary

    # Word count & reading time
    original_words = len(word_tokenize(text))
    summary_words = len(word_tokenize(summary))
    original_eta = round(original_words / 200, 2)
    summary_eta = round(summary_words / 200, 2)
    #assumes avrg spped of 200 words per minute and calculates Estimated reading time
    
    # Display summary
    #enables editing, clears old summary, inserts the new one, then disables editing again
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, summary)
    output_text.config(state='disabled')

    #displayes how long the original and summarized texts might take to read
    stats_label.config(
        text=f"Original: {original_words} words | {original_eta} min\n"
             f"Summary: {summary_words} words | {summary_eta} min"
    )

# GUI Setup
#creates basic GUI Window with a light grey background
root = tk.Tk()
root.title("Text Summarizer")
root.geometry("750x600")
root.config(bg="#f2f2f2")

# Input Text Area where users paste the pparagraph
tk.Label(root, text="Enter your text below:", font=("Arial", 14), bg="#f2f2f2").pack(pady=10)
input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10, font=("Arial", 12))
input_text.pack(padx=10)


# Summarize Button runs the summarize_text() function
tk.Button(root, text="Summarize", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
          command=summarize_text).pack(pady=10)

# Output Summary Area
tk.Label(root, text="Summary:", font=("Arial", 14), bg="#f2f2f2").pack(pady=5)
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=8, font=("Arial", 12), state='disabled')
output_text.pack(padx=10)

# Stats Label
stats_label = tk.Label(root, text="", font=("Arial", 12), bg="#f2f2f2", fg="gray")
stats_label.pack(pady=5)
#runs the app
root.mainloop()
