import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class ModernTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Modern To-Do Manager")
        self.root.geometry("800x700")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(True, True)
        
        # Modern color scheme
        self.colors = {
            'primary': '#16213e',
            'secondary': '#0f3460',
            'accent': '#e94560',
            'success': '#00d084',
            'warning': '#ff9f43',
            'danger': '#ee5a52',
            'light': '#f8f9fa',
            'dark': '#1a1a2e',
            'text': '#ffffff',
            'text_muted': '#a8a8a8',
            'card': '#2a2a4a',
            'border': '#3a3a5a'
        }
        
        # File to store tasks
        self.data_file = "tasks.json"
        self.tasks = self.load_tasks()
        
        # Configure ttk styles
        self.setup_styles()
        self.setup_ui()
        self.refresh_task_list()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure combobox style
        style.configure('Modern.TCombobox',
                       fieldbackground=self.colors['card'],
                       background=self.colors['secondary'],
                       foreground=self.colors['text'],
                       borderwidth=0,
                       relief='flat')
        
        style.map('Modern.TCombobox',
                  fieldbackground=[('readonly', self.colors['card'])],
                  foreground=[('readonly', self.colors['text'])])
    
    def setup_ui(self):
        # Create main container with gradient effect
        main_container = tk.Frame(self.root, bg=self.colors['dark'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        self.create_header(main_container)
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors['dark'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Input section
        self.create_input_section(content_frame)
        
        # Filter and stats section
        self.create_filter_section(content_frame)
        
        # Task list section
        self.create_task_list_section(content_frame)
        
        # Footer stats
        self.create_footer(content_frame)
    
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(expand=True)
        
        # Title with modern typography
        title_label = tk.Label(header_content, 
                              text="✨ Modern To-Do Manager", 
                              font=('Segoe UI', 28, 'bold'), 
                              bg=self.colors['primary'], 
                              fg=self.colors['text'])
        title_label.pack(pady=(20, 5))
        
        subtitle_label = tk.Label(header_content,
                                 text="Organize your life with style",
                                 font=('Segoe UI', 12),
                                 bg=self.colors['primary'],
                                 fg=self.colors['text_muted'])
        subtitle_label.pack()
    
    def create_input_section(self, parent):
        # Card-like container for input
        input_card = tk.Frame(parent, bg=self.colors['card'], relief='flat', bd=0)
        input_card.pack(fill=tk.X, pady=(0, 25))
        
        # Add subtle border effect
        border_frame = tk.Frame(input_card, bg=self.colors['border'], height=2)
        border_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        input_content = tk.Frame(input_card, bg=self.colors['card'])
        input_content.pack(fill=tk.X, padx=25, pady=25)
        
        # Section title
        tk.Label(input_content, text="➕ Add New Task", 
                font=('Segoe UI', 16, 'bold'), 
                bg=self.colors['card'], 
                fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 15))
        
        # Input row
        input_row = tk.Frame(input_content, bg=self.colors['card'])
        input_row.pack(fill=tk.X, pady=(0, 15))
        
        # Task entry with modern styling
        entry_frame = tk.Frame(input_row, bg=self.colors['secondary'], relief='flat')
        entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        self.task_entry = tk.Entry(entry_frame, 
                                  font=('Segoe UI', 12), 
                                  bg=self.colors['secondary'],
                                  fg=self.colors['text'],
                                  insertbackground=self.colors['text'],
                                  relief='flat',
                                  bd=10)
        self.task_entry.pack(fill=tk.BOTH, padx=15, pady=12)
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        # Priority and button row
        controls_row = tk.Frame(input_content, bg=self.colors['card'])
        controls_row.pack(fill=tk.X)
        
        # Priority selection
        priority_frame = tk.Frame(controls_row, bg=self.colors['card'])
        priority_frame.pack(side=tk.LEFT)
        
        tk.Label(priority_frame, text="Priority:", 
                font=('Segoe UI', 10, 'bold'), 
                bg=self.colors['card'], 
                fg=self.colors['text_muted']).pack(anchor=tk.W)
        
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(priority_frame, 
                                    textvariable=self.priority_var,
                                    values=["🔴 High", "🟡 Medium", "🟢 Low"], 
                                    state="readonly", 
                                    style='Modern.TCombobox',
                                    width=12,
                                    font=('Segoe UI', 10))
        priority_combo.pack(pady=(5, 0))
        
        # Add button with modern styling
        add_btn = tk.Button(controls_row, 
                           text="➕ Add Task", 
                           command=self.add_task,
                           bg=self.colors['accent'], 
                           fg=self.colors['text'], 
                           font=('Segoe UI', 11, 'bold'),
                           relief='flat', 
                           bd=0,
                           padx=30, 
                           pady=12,
                           cursor='hand2')
        add_btn.pack(side=tk.RIGHT)
        
        # Hover effects
        add_btn.bind('<Enter>', lambda e: add_btn.config(bg='#d63851'))
        add_btn.bind('<Leave>', lambda e: add_btn.config(bg=self.colors['accent']))
    
    def create_filter_section(self, parent):
        filter_card = tk.Frame(parent, bg=self.colors['card'])
        filter_card.pack(fill=tk.X, pady=(0, 20))
        
        filter_content = tk.Frame(filter_card, bg=self.colors['card'])
        filter_content.pack(fill=tk.X, padx=25, pady=15)
        
        # Filter controls in a row
        filter_row = tk.Frame(filter_content, bg=self.colors['card'])
        filter_row.pack(fill=tk.X)
        
        tk.Label(filter_row, text="🔍 Filter Tasks:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=self.colors['card'], 
                fg=self.colors['text']).pack(side=tk.LEFT)
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_row, 
                                  textvariable=self.filter_var,
                                  values=["All", "📋 Pending", "✅ Completed", "🔴 High Priority", "🟡 Medium Priority", "🟢 Low Priority"],
                                  state="readonly", 
                                  style='Modern.TCombobox',
                                  width=18,
                                  font=('Segoe UI', 10))
        filter_combo.pack(side=tk.LEFT, padx=(15, 0))
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_task_list())
        
        # Quick stats
        self.quick_stats = tk.Label(filter_row, text="", 
                                   font=('Segoe UI', 10), 
                                   bg=self.colors['card'], 
                                   fg=self.colors['text_muted'])
        self.quick_stats.pack(side=tk.RIGHT)
    
    def create_task_list_section(self, parent):
        # Task list container
        list_container = tk.Frame(parent, bg=self.colors['card'])
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # List header
        list_header = tk.Frame(list_container, bg=self.colors['secondary'], height=50)
        list_header.pack(fill=tk.X)
        list_header.pack_propagate(False)
        
        tk.Label(list_header, text="📝 Your Tasks", 
                font=('Segoe UI', 14, 'bold'), 
                bg=self.colors['secondary'], 
                fg=self.colors['text']).pack(side=tk.LEFT, padx=25, pady=15)
        
        # Scrollable area
        scroll_frame = tk.Frame(list_container, bg=self.colors['card'])
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Canvas and scrollbar
        self.canvas = tk.Canvas(scroll_frame, 
                               bg=self.colors['card'], 
                               highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['card'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_footer(self, parent):
        footer = tk.Frame(parent, bg=self.colors['primary'], height=60)
        footer.pack(fill=tk.X, pady=(20, 0))
        footer.pack_propagate(False)
        
        self.stats_label = tk.Label(footer, text="", 
                                   font=('Segoe UI', 12, 'bold'), 
                                   bg=self.colors['primary'], 
                                   fg=self.colors['text'])
        self.stats_label.pack(expand=True)
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("⚠️ Warning", "Please enter a task!")
            return
        
        # Clean priority value
        priority_raw = self.priority_var.get()
        priority = priority_raw.split(' ')[1] if ' ' in priority_raw else priority_raw
        
        task = {
            'id': max([t.get('id', 0) for t in self.tasks], default=0) + 1,
            'text': task_text,
            'priority': priority,
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.task_entry.delete(0, tk.END)
        self.refresh_task_list()
        
        # Success animation effect
        original_bg = self.task_entry.master.cget('bg')
        self.task_entry.master.config(bg=self.colors['success'])
        self.root.after(200, lambda: self.task_entry.master.config(bg=original_bg))
    
    def create_task_widget(self, task):
        # Modern task card
        task_card = tk.Frame(self.scrollable_frame, bg='#353560', relief='flat', bd=0)
        task_card.pack(fill=tk.X, padx=20, pady=8)
        
        # Hover effect
        def on_enter(e):
            task_card.config(bg='#404070')
        def on_leave(e):
            task_card.config(bg='#353560')
        
        task_card.bind('<Enter>', on_enter)
        task_card.bind('<Leave>', on_leave)
        
        # Task content
        content_frame = tk.Frame(task_card, bg='#353560')
        content_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Top row: checkbox, text, priority
        top_row = tk.Frame(content_frame, bg='#353560')
        top_row.pack(fill=tk.X, pady=(0, 10))
        
        # Custom checkbox
        checkbox_frame = tk.Frame(top_row, bg='#353560')
        checkbox_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        checkbox_color = self.colors['success'] if task['completed'] else self.colors['border']
        checkbox_text = "✓" if task['completed'] else "○"
        
        checkbox_btn = tk.Button(checkbox_frame, 
                               text=checkbox_text, 
                               font=('Segoe UI', 16, 'bold'),
                               bg=checkbox_color, 
                               fg=self.colors['text'],
                               relief='flat',
                               bd=0,
                               width=2, 
                               height=1,
                               cursor='hand2',
                               command=lambda: self.toggle_task(task['id']))
        checkbox_btn.pack()
        
        # Task text
        text_frame = tk.Frame(top_row, bg='#353560')
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        text_color = self.colors['text_muted'] if task['completed'] else self.colors['text']
        font_style = ('Segoe UI', 12, 'overstrike') if task['completed'] else ('Segoe UI', 12)
        
        task_label = tk.Label(text_frame, 
                            text=task['text'], 
                            font=font_style,
                            bg='#353560', 
                            fg=text_color, 
                            anchor='w',
                            wraplength=400)
        task_label.pack(anchor='w')
        
        # Priority badge
        priority_colors = {
            'High': self.colors['danger'],
            'Medium': self.colors['warning'],
            'Low': self.colors['success']
        }
        
        priority_frame = tk.Frame(top_row, bg='#353560')
        priority_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        priority_badge = tk.Label(priority_frame, 
                                text=f"● {task['priority']}", 
                                font=('Segoe UI', 10, 'bold'),
                                bg='#353560',
                                fg=priority_colors.get(task['priority'], self.colors['text_muted']))
        priority_badge.pack()
        
        # Bottom row: timestamp and actions
        bottom_row = tk.Frame(content_frame, bg='#353560')
        bottom_row.pack(fill=tk.X, pady=(5, 0))
        
        # Timestamp
        time_label = tk.Label(bottom_row, 
                            text=f"Created: {task['created_at']}", 
                            font=('Segoe UI', 9),
                            bg='#353560', 
                            fg=self.colors['text_muted'])
        time_label.pack(side=tk.LEFT)
        
        # Action buttons
        actions_frame = tk.Frame(bottom_row, bg='#353560')
        actions_frame.pack(side=tk.RIGHT)
        
        # Modern buttons
        edit_btn = tk.Button(actions_frame, 
                           text="✏️ Edit", 
                           command=lambda: self.edit_task(task['id']),
                           bg=self.colors['secondary'], 
                           fg=self.colors['text'],
                           font=('Segoe UI', 9),
                           relief='flat', 
                           bd=0,
                           padx=12, 
                           pady=4,
                           cursor='hand2')
        edit_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_btn = tk.Button(actions_frame, 
                             text="🗑️ Delete", 
                             command=lambda: self.delete_task(task['id']),
                             bg=self.colors['danger'], 
                             fg=self.colors['text'],
                             font=('Segoe UI', 9),
                             relief='flat', 
                             bd=0,
                             padx=12, 
                             pady=4,
                             cursor='hand2')
        delete_btn.pack(side=tk.LEFT)
        
        # Button hover effects
        def edit_hover_in(e): edit_btn.config(bg='#0a2c50')
        def edit_hover_out(e): edit_btn.config(bg=self.colors['secondary'])
        def delete_hover_in(e): delete_btn.config(bg='#c23e37')
        def delete_hover_out(e): delete_btn.config(bg=self.colors['danger'])
        
        edit_btn.bind('<Enter>', edit_hover_in)
        edit_btn.bind('<Leave>', edit_hover_out)
        delete_btn.bind('<Enter>', delete_hover_in)
        delete_btn.bind('<Leave>', delete_hover_out)
    
    def toggle_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                if task['completed']:
                    task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                else:
                    task.pop('completed_at', None)
                break
        
        self.save_tasks()
        self.refresh_task_list()
    
    def delete_task(self, task_id):
        if messagebox.askyesno("🗑️ Confirm Delete", "Are you sure you want to delete this task?"):
            self.tasks = [task for task in self.tasks if task['id'] != task_id]
            self.save_tasks()
            self.refresh_task_list()
    
    def edit_task(self, task_id):
        task = next((t for t in self.tasks if t['id'] == task_id), None)
        if not task:
            return
        
        # Modern edit dialog
        edit_window = tk.Toplevel(self.root)
        edit_window.title("✏️ Edit Task")
        edit_window.geometry("500x300")
        edit_window.configure(bg=self.colors['dark'])
        edit_window.grab_set()
        edit_window.resizable(False, False)
        
        # Center the window
        edit_window.transient(self.root)
        
        # Dialog content
        content = tk.Frame(edit_window, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(content, text="✏️ Edit Task", 
                font=('Segoe UI', 16, 'bold'), 
                bg=self.colors['card'], 
                fg=self.colors['text']).pack(pady=(0, 20))
        
        # Entry field
        tk.Label(content, text="Task Description:", 
                font=('Segoe UI', 10, 'bold'), 
                bg=self.colors['card'], 
                fg=self.colors['text_muted']).pack(anchor='w', pady=(0, 5))
        
        entry_frame = tk.Frame(content, bg=self.colors['secondary'])
        entry_frame.pack(fill=tk.X, pady=(0, 20))
        
        entry = tk.Entry(entry_frame, 
                        font=('Segoe UI', 12), 
                        bg=self.colors['secondary'],
                        fg=self.colors['text'],
                        insertbackground=self.colors['text'],
                        relief='flat', 
                        bd=0)
        entry.pack(fill=tk.X, padx=15, pady=12)
        entry.insert(0, task['text'])
        entry.focus()
        
        # Priority selection
        tk.Label(content, text="Priority:", 
                font=('Segoe UI', 10, 'bold'), 
                bg=self.colors['card'], 
                fg=self.colors['text_muted']).pack(anchor='w', pady=(0, 5))
        
        priority_var = tk.StringVar(value=f"{'🔴' if task['priority'] == 'High' else '🟡' if task['priority'] == 'Medium' else '🟢'} {task['priority']}")
        priority_combo = ttk.Combobox(content, 
                                    textvariable=priority_var,
                                    values=["🔴 High", "🟡 Medium", "🟢 Low"], 
                                    state="readonly",
                                    style='Modern.TCombobox',
                                    font=('Segoe UI', 10))
        priority_combo.pack(anchor='w', pady=(0, 30))
        
        # Buttons
        btn_frame = tk.Frame(content, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X)
        
        def save_edit():
            new_text = entry.get().strip()
            if new_text:
                task['text'] = new_text
                priority_raw = priority_var.get()
                task['priority'] = priority_raw.split(' ')[1] if ' ' in priority_raw else priority_raw
                self.save_tasks()
                self.refresh_task_list()
                edit_window.destroy()
            else:
                messagebox.showwarning("⚠️ Warning", "Task cannot be empty!")
        
        save_btn = tk.Button(btn_frame, 
                           text="💾 Save Changes", 
                           command=save_edit,
                           bg=self.colors['success'], 
                           fg=self.colors['text'],
                           font=('Segoe UI', 11, 'bold'),
                           relief='flat', 
                           bd=0,
                           padx=20, 
                           pady=10,
                           cursor='hand2')
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(btn_frame, 
                             text="❌ Cancel", 
                             command=edit_window.destroy,
                             bg=self.colors['danger'], 
                             fg=self.colors['text'],
                             font=('Segoe UI', 11, 'bold'),
                             relief='flat', 
                             bd=0,
                             padx=20, 
                             pady=10,
                             cursor='hand2')
        cancel_btn.pack(side=tk.LEFT)
        
        # Enter key binding
        entry.bind('<Return>', lambda e: save_edit())
    
    def get_filtered_tasks(self):
        filter_value = self.filter_var.get()
        
        if filter_value == "All":
            return self.tasks
        elif "Pending" in filter_value:
            return [task for task in self.tasks if not task['completed']]
        elif "Completed" in filter_value:
            return [task for task in self.tasks if task['completed']]
        elif "High Priority" in filter_value:
            return [task for task in self.tasks if task['priority'] == 'High']
        elif "Medium Priority" in filter_value:
            return [task for task in self.tasks if task['priority'] == 'Medium']
        elif "Low Priority" in filter_value:
            return [task for task in self.tasks if task['priority'] == 'Low']
        
        return self.tasks
    
    def refresh_task_list(self):
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        filtered_tasks = self.get_filtered_tasks()
        
        if not filtered_tasks:
            # Empty state
            empty_frame = tk.Frame(self.scrollable_frame, bg=self.colors['card'])
            empty_frame.pack(expand=True, fill=tk.BOTH, pady=100)
            
            tk.Label(empty_frame, 
                    text="📭", 
                    font=('Segoe UI', 48), 
                    bg=self.colors['card'], 
                    fg=self.colors['text_muted']).pack()
            
            tk.Label(empty_frame, 
                    text="No tasks found", 
                    font=('Segoe UI', 16, 'bold'), 
                    bg=self.colors['card'], 
                    fg=self.colors['text_muted']).pack(pady=(10, 5))
            
            tk.Label(empty_frame, 
                    text="Add a new task to get started!", 
                    font=('Segoe UI', 12), 
                    bg=self.colors['card'], 
                    fg=self.colors['text_muted']).pack()
        else:
            # Sort tasks
            priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
            filtered_tasks.sort(key=lambda x: (x['completed'], priority_order.get(x['priority'], 3)))
            
            for task in filtered_tasks:
                self.create_task_widget(task)
        
        self.update_stats()
    
    def update_stats(self):
        total = len(self.tasks)
        completed = len([task for task in self.tasks if task['completed']])
        pending = total - completed
        
        if total == 0:
            progress_text = "🚀 Ready to be productive!"
        else:
            percentage = int((completed / total) * 100)
            progress_text = f"📊 Progress: {completed}/{total} tasks completed ({percentage}%)"
        
        self.stats_label.config(text=progress_text)
        
        # Update quick stats
        quick_text = f"Total: {total} • Completed: {completed} • Pending: {pending}"
        self.quick_stats.config(text=quick_text)
    
    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_tasks(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            messagebox.showerror("💥 Error", f"Could not save tasks: {str(e)}")

def main():
    root = tk.Tk()
    app = ModernTodoApp(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()