import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from GoogleNews import GoogleNews 
import threading
from datetime import datetime
import webbrowser
import sv_ttk 

class NewsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("News Explorer")
        self.root.geometry("1300x850")
        
        # Theme toggle menu
        self.menu_bar = tk.Menu(root)
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="Toggle Dark/Light Mode", command=self.toggle_theme)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.root.config(menu=self.menu_bar)
        
        # Configuration
        self.indian_states = [
            'Andhra Pradesh','Bihar','Gujarat','Jammu and Kashmir'
            ,'Karnataka','Maharashtra','Punjab','Rajasthan','Uttar Pradesh'
        ]
        
        self.Continents = [
            'Africa','Antarctica','Asia','Australia','Europe','North America','South America'
        ]
        
        self.india_current_affairs = [
            ('Politics', 'India Politics'),
            ('Economy', 'India Economy'),
            ('Defense', 'India Defense'),
            ('Technology', 'India Technology'),
            ('Health', 'India Health'),
            ('Education', 'India Education'),
            ('Environment', 'India Environment')
        ]
        
        self.global_current_affairs = [
            ('World Politics', 'World Politics'),
            ('Global Economy', 'Global Economy'),
            ('Climate', 'Climate Change'),
            ('Technology', 'Technology'),
            ('Health', 'Global Health'),
            ('Science', 'Science'),
            ('Business', 'Global Business')
        ]
        
        self.tech_subcategories = [
            'Artificial Intelligence',
            'Gadgets',
            'Cybersecurity',
            'Startups',
            'Gaming Technology',
            'Computer Hardware',
            'AR/VR Technology'
        ]
        
        self.renewable_subcategories = [
            'Solar/Wind Projects',
            'EV Infrastructure',
            'Green Policies'
        ]
        
        self.current_articles = []
        sv_ttk.set_theme("light")
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Indian States
        states_frame = ttk.Frame(notebook)
        notebook.add(states_frame, text='Indian States')
        ttk.Label(states_frame, text="Select Indian State:").pack(pady=5)
        state_btn_frame = ttk.Frame(states_frame)
        state_btn_frame.pack()
        cols = 3
        for idx, state in enumerate(self.indian_states):
            btn = ttk.Button(state_btn_frame, text=state,
                           command=lambda s=state: self.fetch_news(f"{s} India"))
            btn.grid(row=idx//cols, column=idx%cols, padx=5, pady=5)

        # Tab 2: Continents News
        continents_frame = ttk.Frame(notebook)
        notebook.add(continents_frame, text='Continents')
        ttk.Label(continents_frame, text="Select Country:").pack(pady=5)
        global_btn_frame = ttk.Frame(continents_frame)
        global_btn_frame.pack()
        for idx, country in enumerate(self.Continents): 
            btn = ttk.Button(global_btn_frame, text=country,
                           command=lambda c=country: self.fetch_news(c))
            btn.grid(row=idx//4, column=idx%4, padx=5, pady=5)

        # Tab 3: India Current Affairs
        india_affairs_frame = ttk.Frame(notebook)
        notebook.add(india_affairs_frame, text='India Current Affairs')
        today = datetime.now().strftime("%d %B %Y")
        ttk.Label(india_affairs_frame, text="Today's Headlines in India:", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        ttk.Label(india_affairs_frame, text=f"🗓️ {today}", font=('Arial', 10)).pack()
        btn_frame = ttk.Frame(india_affairs_frame)
        btn_frame.pack(pady=15)
        for idx, (display_name, search_query) in enumerate(self.india_current_affairs):
            btn = ttk.Button(btn_frame, text=display_name, width=18,
                            command=lambda q=search_query: self.fetch_news(f"{q} today"))
            btn.grid(row=idx//4, column=idx%4, padx=5, pady=5)

        # Tab 4: Global Current Affairs
        global_affairs_frame = ttk.Frame(notebook)
        notebook.add(global_affairs_frame, text='Global Current Affairs')
        ttk.Label(global_affairs_frame, text="Today's International Headlines:", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        ttk.Label(global_affairs_frame, text=f"🗓️ {today}", font=('Arial', 10)).pack()
        btn_frame = ttk.Frame(global_affairs_frame)
        btn_frame.pack(pady=15)
        for idx, (display_name, search_query) in enumerate(self.global_current_affairs):
            btn = ttk.Button(btn_frame, text=display_name, width=18,
                            command=lambda q=search_query: self.fetch_news(f"{q} today"))
            btn.grid(row=idx//4, column=idx%4, padx=5, pady=5)

        # Tab 5: Technology News
        tech_frame = ttk.Frame(notebook)
        notebook.add(tech_frame, text='Technology News')
        ttk.Label(tech_frame, text="Technology Subcategories:", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        top_btn_frame = ttk.Frame(tech_frame)
        top_btn_frame.pack()
        bottom_btn_frame = ttk.Frame(tech_frame)
        bottom_btn_frame.pack()
        for idx, subcat in enumerate(self.tech_subcategories[:4]):
            btn = ttk.Button(top_btn_frame, text=subcat, width=20,
                           command=lambda s=subcat: self.fetch_news(s))
            btn.grid(row=0, column=idx, padx=5, pady=5)
        for idx, subcat in enumerate(self.tech_subcategories[4:]):
            btn = ttk.Button(bottom_btn_frame, text=subcat, width=20,
                           command=lambda s=subcat: self.fetch_news(s))
            btn.grid(row=0, column=idx, padx=5, pady=5)

        # Tab 6: Renewable Energy
        renewable_frame = ttk.Frame(notebook)
        notebook.add(renewable_frame, text='Renewable Energy')
        ttk.Label(renewable_frame, text="Clean Energy Focus Areas:", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        btn_frame = ttk.Frame(renewable_frame)
        btn_frame.pack(pady=15)
        for idx, subcat in enumerate(self.renewable_subcategories):
            btn = ttk.Button(btn_frame, text=subcat, width=25,
                           command=lambda s=subcat: self.fetch_news(f"{s} Renewable Energy"))
            btn.grid(row=0, column=idx, padx=10, pady=5)

        # Tab 7: Local News (Coming Soon)
        local_frame = ttk.Frame(notebook)
        notebook.add(local_frame, text='Local News')
        ttk.Label(local_frame, text="Coming Soon!", 
                 font=('Arial', 16, 'bold'), foreground='gray').pack(pady=50)
        ttk.Label(local_frame, text="Local news feature under development", 
                 font=('Arial', 12)).pack()

        # Search Frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, fill=tk.X)
        self.search_entry = ttk.Entry(search_frame, width=40, font=('Arial', 12))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="🔍 Search", 
                  command=self.perform_search).pack(side=tk.LEFT)

        # News display area
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD,
                                                 font=('Arial', 12), padx=15, pady=15,
                                                 bg='white', fg='black')
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Status bar
        self.status = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def toggle_theme(self):
        current_theme = sv_ttk.get_theme()
        new_theme = "dark" if current_theme == "light" else "light"
        sv_ttk.set_theme(new_theme)
        self.text_area.config(
            bg='#1e1e1e' if new_theme == 'dark' else 'white',
            fg='white' if new_theme == 'dark' else 'black'
        )
        self.text_area.tag_config("hyperlink", 
                                foreground='#569CD6' if new_theme == 'dark' else 'blue',
                                underline=True)

    def perform_search(self):
        query = self.search_entry.get()
        if query:
            self.fetch_news(query)
        else:
            messagebox.showwarning("Input Error", "Please enter a search term")

    def fetch_news(self, query):
        self.status.config(text=f"Searching: {query}...")
        self.text_area.delete(1.0, tk.END)
        threading.Thread(target=self._fetch_news_thread, args=(query,), daemon=True).start()

    def _fetch_news_thread(self, query):
        try:
            if 'India' in query:
                news = GoogleNews(period='1d', lang='en', region='IN')
            else:
                news = GoogleNews(period='1d', lang='en')
                
            news.search(query)
            results = news.result()
            
            self.current_articles = []
            for item in results:
                self.current_articles.append({
                    'title': item['title'],
                    'source': item['media'],
                    'date': item['date'],
                    'desc': item['desc'],
                    'link': item['link']
                })

            self.root.after(0, self._display_news)
            self.status.config(text=f"Found {len(self.current_articles)} articles")
            
        except Exception as e:
            self.root.after(0, lambda e=e: messagebox.showerror("Error", str(e)))
            self.status.config(text="Error fetching news")

    def _display_news(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        
        for idx, article in enumerate(self.current_articles, 1):
            emoji = "🇮🇳" if 'India' in article['title'] else "🌍"
            for tech_cat in self.tech_subcategories:
                if tech_cat.lower() in article['title'].lower():
                    if tech_cat == 'Gaming Technology':
                        emoji = '🎮'
                    elif tech_cat == 'Computer Hardware':
                        emoji = '💻'
                    elif tech_cat == 'AR/VR Technology':
                        emoji = '👓'
                    break
            
            self.text_area.insert(tk.END, 
                f"{emoji} {article['title']}\n"
                f"📰 {article['source']} | 📅 {article['date']}\n"
                f"📝 {article['desc']}\n"
                f"{'-'*100}\n\n")
            
            start = f"{idx*4 - 3}.0"
            end = f"{idx*4}.0"
            self.text_area.tag_add(f"article_{idx}", start, end)
            self.text_area.tag_config(f"article_{idx}", foreground='blue', underline=True)
            self.text_area.tag_bind(f"article_{idx}", "<Button-1>", 
                                  lambda e, link=article['link']: webbrowser.open(link))
        
        self.text_area.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = NewsApp(root)
    root.mainloop()

